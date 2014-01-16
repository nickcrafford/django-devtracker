from django.db                  import models
from django.db                  import connection
from django.contrib.auth.models import User
from decimal import Decimal
import decimal
import locale

locale.setlocale(locale.LC_ALL, 'en_CA.UTF-8')

def get_time_entry_total(entries):
    total = Decimal("0.00")
    for entry in list(entries):
        total += entry.rate.moneys_per_hour * entry.num_hours
    return locale.currency(total)


def get_invoice_total(invoices):
    total = Decimal("0.00")
    for invoice in list(invoices):
        total += invoice.raw_amount()
    return locale.currency(total)

class Business(models.Model):
  user        = models.ForeignKey(User)
  name        = models.CharField(max_length=100, unique=True)
  address     = models.CharField(max_length=100)
  city        = models.CharField(max_length=25)
  state       = models.CharField(max_length=4)
  postal      = models.CharField(max_length=15)
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)

  child_path  = "/businesses"

  class Meta:
      verbose_name = "Business"
      verbose_name_plural = "Businesses"

  def __str__(self):
      return self.name

  def is_readonly(self):
      return False

class Client(models.Model):
  user        = models.ForeignKey(User)
  business    = models.ForeignKey(Business)
  email       = models.EmailField()
  name        = models.CharField(max_length=100, unique=True)
  address     = models.CharField(max_length=100)
  city        = models.CharField(max_length=25)
  state       = models.CharField(max_length=4)
  postal      = models.CharField(max_length=15)
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)

  child_path  = "/clients"

  class Meta:
      ordering = ['business','name']
      verbose_name = "Client"
      verbose_name_plural = "Clients"

  def __str__(self):
      return self.name

  def is_readonly(self):
      return False

class Project(models.Model):
  user        = models.ForeignKey(User)
  client      = models.ForeignKey(Client)
  name        = models.CharField(max_length=100, unique=True)
  budget      = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
  description = models.TextField()
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)

  child_path  = "/projects"

  class Meta:
      ordering = ['client','name']
      verbose_name = "Project"
      verbose_name_plural = "Projects"

  def __str__(self):
      return self.name

  def budget_amount(self):
      if self.budget:
          return locale.currency(self.budget)
      return "N/A"

  def running_cost(self):
      """ Sum up all the time and fixed entry costs """
      cost   = decimal.Decimal(0)
      cursor = connection.cursor()
      cursor.execute("""
        select sum(x.moneys) moneys
        from (
          select r.moneys_per_hour * e.num_hours moneys, e.project_id
          from
          time_tracking_timeentry e,
          time_tracking_rate      r
          where r.id = e.rate_id
          union all
          select moneys, e.project_id
          from
          time_tracking_fixedentry e
        ) x
        where x.project_id = %d
        group by x.project_id
      """ % (self.id))

      row = cursor.fetchone()

      try:
          cost = decimal.Decimal(row[0])
      except:
          pass

      if cost <= decimal.Decimal(0):
          return "N/A"

      return locale.currency(cost)

  def is_readonly(self):
      return False

class Rate(models.Model):
  user            = models.ForeignKey(User)
  name            = models.CharField(max_length=100, unique=True)
  description     = models.TextField()
  moneys_per_hour = models.DecimalField(decimal_places=2, max_digits=15)
  create_date     = models.DateTimeField(auto_now_add=True)
  update_date     = models.DateTimeField(auto_now=True)

  child_path      = "/rates"

  class Meta:
      verbose_name = "Rate"
      verbose_name_plural = "Rates"

  def dollars_per_hour(self):
      return locale.currency(self.moneys_per_hour)

  def __str__(self):
      return str(locale.currency(self.moneys_per_hour)) + "/hr - " + self.name

  def is_readonly(self):
      return False

class Invoice(models.Model):
  user        = models.ForeignKey(User)
  client      = models.ForeignKey(Client)
  name        = models.CharField(max_length=150)
  sent_date   = models.DateTimeField(null=True, blank=True)
  paid_date   = models.DateTimeField(null=True, blank=True)
  create_date = models.DateTimeField()
  update_date = models.DateTimeField(auto_now=True)

  child_path  = "/invoices"

  class Meta:
      ordering = ['-sent_date']
      verbose_name = "Invoice"
      verbose_name_plural = "Invoices"

  def __str__(self):
      return self.status() + " - " + self.name

  def get_export_filename(self):
      return self.name + ".pdf"

  def date_sent(self):
      if self.sent_date:
          return self.sent_date.strftime("%B %d, %Y")
      else:
          return "N/A"

  def date_paid(self):
      if self.paid_date:
          return self.paid_date.strftime("%B %d, %Y")
      else:
          return "N/A"

  def date_created(self):
      if self.create_date:
          return self.create_date.strftime("%B %d, %Y")
      else:
          return "N/A"

  def raw_amount(self):
      amount = decimal.Decimal(0)  
      cursor = connection.cursor()
      cursor.execute("""
        select sum(x.moneys)
        from (
          select r.moneys_per_hour * e.num_hours moneys, e.invoice_id
          from
          time_tracking_timeentry e,
          time_tracking_rate      r
          where r.id = e.rate_id
          union all
          select moneys, e.invoice_id
          from
          time_tracking_fixedentry e
        ) x
        where x.invoice_id = %d
        group by x.invoice_id    
      """ % (self.id))

      row = cursor.fetchone()

      try:
          amount = decimal.Decimal(row[0])
      except:
          pass

      return amount

  def amount(self):
      return locale.currency(self.raw_amount())

  def first_entry_date(self):
      cursor = connection.cursor()
      cursor.execute("""
        select min(date) from (
          SELECT date FROM devtracker.time_tracking_timeentry
          where invoice_id = %d
          union all
          SELECT date FROM devtracker.time_tracking_fixedentry
          where invoice_id = %d
        ) x """ % (self.id, self.id))

      row = cursor.fetchone()

      try:
          return row[0].strftime("%B %d, %Y")
      except:
          return "N/A"

  def last_entry_date(self):
      cursor = connection.cursor()
      cursor.execute("""
        select max(date) from (
          SELECT date FROM devtracker.time_tracking_timeentry
          where invoice_id = %d
          union all
          SELECT date FROM devtracker.time_tracking_fixedentry
          where invoice_id = %d
        ) x """ % (self.id,self.id))

      row = cursor.fetchone()

      try:
          return row[0].strftime("%B %d, %Y")
      except:
          return "N/A"

  def status(self):
      if not self.sent_date:
          return "UNSENT"
      elif not self.paid_date:
          return "UNPAID"
      elif self.sent_date and self.paid_date:
          return "PAID"

  def is_readonly(self):
      return False

class TimeEntry(models.Model):
  user        = models.ForeignKey(User)
  project     = models.ForeignKey(Project)
  rate        = models.ForeignKey(Rate)
  invoice     = models.ForeignKey(Invoice, blank=True, null=True)
  num_hours   = models.DecimalField(decimal_places=2, max_digits=15)
  date        = models.DateTimeField()
  is_billable = models.BooleanField()
  description = models.TextField()
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)

  child_path  = "/time-entries"

  def __str__(self):
      return self.date.strftime("%B %d, %Y") + " " + str(self.project)

  class Meta:
      ordering = ['-date']
      verbose_name = "Time Entry"
      verbose_name_plural = "Time Entries"

  def is_readonly(self):
      try:
          return self.invoice.sent_date != None
      except:
          return False

  def work_date(self):
      return self.date.strftime("%B %d, %Y")

  def cost(self):
      if self.is_billable:
          return locale.currency(self.rate.moneys_per_hour * self.num_hours)
      else:
          return '$0.00'

  def hours(self):
      return self.num_hours

  def invoiced(self):
      if self.invoice and self.invoice.id > 0:
          return "Yes"
      return "No"

  def hourly_rate(self):
      return str(self.rate.dollars_per_hour()) + "/hr"

  def client(self):
      return self.project.client

class FixedEntry(models.Model):
  user        = models.ForeignKey(User)
  project     = models.ForeignKey(Project)
  invoice     = models.ForeignKey(Invoice, blank=True, null=True)
  moneys      = models.DecimalField(decimal_places=2, max_digits=15)
  date        = models.DateTimeField()
  is_billable = models.BooleanField()
  description = models.TextField()
  create_date = models.DateTimeField(auto_now_add=True)
  update_date = models.DateTimeField(auto_now=True)

  child_path  = "/fixed-entries"

  def __str__(self):
      return self.date.strftime("%B %d, %Y") + " " + str(self.project)

  class Meta:
      ordering = ['-date']
      verbose_name = "Fixed Entry"
      verbose_name_plural = "Fixed Entries"

  def is_readonly(self):
      try:
          return self.invoice.sent_date != None
      except:
          return False

  def work_date(self):
      return self.date.strftime("%B %d, %Y")

  def cost(self):
      if self.is_billable:
          return locale.currency(self.moneys)
      else:
          return '$0.00'

  def invoiced(self):
      if self.invoice and self.invoice.id > 0:
        return "Yes"
      return "No"
