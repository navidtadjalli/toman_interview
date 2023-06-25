from django.db import models

from django.utils.translation import gettext_lazy as _


class Wallet(models.Model):
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=24,
        db_index=True,
        null=False,
        blank=False
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
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        return f"Transaction for {self.wallet} wallet at {self.created_at}"
