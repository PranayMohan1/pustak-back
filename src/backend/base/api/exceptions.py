from django.utils.encoding import force_text
from rest_framework.exceptions import ValidationError


class PlutonicValidationError(ValidationError):
    def __init__(self, detail):
        if isinstance(detail, dict) or isinstance(detail, list):
            self.detail = force_text(detail)
        else:
            self.detail = force_text(detail)
