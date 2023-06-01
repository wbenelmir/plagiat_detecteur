from django.db import models
from django.utils.translation import gettext_lazy as _

class status(models.TextChoices):
    archive = 'archive', _('archive')
    not_archive = 'not_archive', _('not_archive')