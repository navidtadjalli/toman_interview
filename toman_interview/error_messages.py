from django.utils.translation import gettext_lazy as _


def get_error_dict(msg: str) -> dict:
    return {
        "detail": msg
    }


INSUFFICIENT_BALANCE_ERROR_MESSAGE = get_error_dict(_("Insufficient balance."))
