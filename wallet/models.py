from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.db.models.functions import Coalesce
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from django.db.transaction import Atomic, get_connection


class LockedAtomicTransaction(Atomic):
    """
    Does a atomic transaction, but also locks the entire table for any transactions, for the duration of this
    transaction. Although this is the only way to avoid concurrency issues in certain situations, it should be used with
    caution, since it has impacts on performance, for obvious reasons...
    """

    def __init__(self, model, using=None, savepoint=None):
        if using is None:
            using = DEFAULT_DB_ALIAS
        super().__init__(using, savepoint, durable=False)
        self.model = model

    def __enter__(self):
        super(LockedAtomicTransaction, self).__enter__()

        # Make sure not to lock, when sqlite is used, or you'll run into problems while running tests!!!
        if settings.DATABASES[self.using]['ENGINE'] != 'django.db.backends.sqlite3':
            cursor = None
            try:
                cursor = get_connection(self.using).cursor()
                cursor.execute(
                    'LOCK TABLE {db_table_name}'.format(db_table_name=self.model._meta.db_table)
                )
            finally:
                if cursor and not cursor.closed:
                    cursor.close()


class Wallet(models.Model):
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=24,
        db_index=True,
        unique=True,
        null=False,
        blank=False
    )

    @property
    def balance(self) -> Decimal:
        return Wallet.objects.aggregate(
            balance=Coalesce(models.Sum("transactions__amount",
                                        filter=models.Q(transactions__available_at__lte=timezone.now())),
                             Decimal("0.0"))
        )["balance"]

    def deposit(self,
                amount: Decimal,
                lock_time: int):
        self.transactions.create(
            amount=amount,
            available_at=timezone.now() + timedelta(seconds=lock_time)
        )

    def withdraw(self,
                 amount: Decimal):
        self.transactions.create(
            amount=amount * -1,
            available_at=timezone.now()
        )

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    def __str__(self):
        return self.username


class Transaction(models.Model):
    wallet = models.ForeignKey(
        verbose_name=_("Wallet"),
        to="wallet.Wallet",
        db_index=True,
        null=False,
        blank=False,
        on_delete=models.DO_NOTHING,
        related_name="transactions",
        editable=False
    )
    amount = models.DecimalField(
        verbose_name=_("Amount"),
        max_digits=14,
        decimal_places=2,
        editable=False
    )
    available_at = models.DateTimeField(
        verbose_name=_('Available at'),
        null=False,
        blank=False,
        default=timezone.now
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")
        ordering = ["created_at"]

    def __str__(self):
        return f"Transaction for {self.wallet} wallet at {self.created_at}"
