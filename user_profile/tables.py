import django_tables as tables
from devtracker.user_profile.models import Profile

class ProfileTable(tables.ModelTable):
  class Meta:
    model = Profile