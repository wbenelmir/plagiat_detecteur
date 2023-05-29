from django.db import models
from django.utils.translation import gettext_lazy as _

class domain(models.TextChoices):
    nule       =    '', _('Please select')
    domain01   =    'Agriculture', _('Agriculture')
    domain02   =    'Engineering', _('Engineering')
    domain03   =    'Health Professions', _('Health Professions')
    domain04   =    'Math and Computer Science', _('Math and Computer Science')
    domain05   =    'Physical and Life Sciences', _('Physical and Life Sciences')
    domain06   =    'Social Sciences', _('Social Sciences')
    domain07   =    'Humanities', _('Humanities')
    domain08   =    'Business and Management', _('Business and Management')
    domain09   =    'Education', _('Education')
    domain10   =    'Fine and Applied Arts', _('Fine and Applied Arts')
    domain11   =    'Legal Studies and Law Enforcement', _('Legal Studies and Law Enforcement')
    domain12   =    'Communications and Journalism', _('Communications and Journalism')

