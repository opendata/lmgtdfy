from django.conf import settings

from crispy_forms.layout import Submit
from yboss import YBoss


class CleanSubmitButton(Submit):
    field_classes = 'btn btn-default'


def get_yboss():
    return YBoss(
        settings.CONSUMER_KEY,
        settings.CONSUMER_SECRET
    )
