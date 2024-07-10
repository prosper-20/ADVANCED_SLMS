from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_size(value):
    filesize = value.size
    if filesize > 5242880:  # 5 MB (in bytes)
        raise ValidationError(_('The maximum file size that can be uploaded is 5MB'))
