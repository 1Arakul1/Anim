#users\validators.py
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _('Пароль должен содержать хотя бы одну букву.'),
                code='password_no_letters'
            )

    def get_help_text(self):
        return _(
            "Ваш пароль должен содержать хотя бы одну букву."
        )