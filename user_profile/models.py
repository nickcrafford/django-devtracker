from django.db                  import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user                 = models.ForeignKey(User, unique=True)
  billing_name         = models.CharField(max_length=50)
  billing_address      = models.CharField(max_length=50)
  billing_city         = models.CharField(max_length=50)
  billing_state        = models.CharField(max_length=50)
  billing_postal       = models.CharField(max_length=50)
  weekly_revenue_goal  = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
  monthly_revenue_goal = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
  yearly_revenue_goal  = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
  tax_bracket          = models.IntegerField(max_length=2)