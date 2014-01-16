import django_tables as tables
from devtracker.time_tracking.models import *

class BusinessTable(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    class Meta:
        model = Business
        exclude = ['user','create_date', 'update_date']

class ClientTable(tables.ModelTable):
    id = tables.Column(sortable=False, visible=False)
    class Meta:
        model = Client
        exclude = ['user','create_date', 'update_date', 'email']

class ProjectTable(tables.ModelTable):
    id            = tables.Column(sortable=False, visible=False)
    budget_amount = tables.Column(default="$0.00")
    running_cost  = tables.Column(default="$0.00")
    class Meta:
        model = Project
        exclude = ['user','create_date', 'update_date', 'description','budget']

class RateTable(tables.ModelTable):
    id               = tables.Column(sortable=False, visible=False)
    dollars_per_hour = tables.Column(default="$0.00")
    class Meta:
        model   = Rate
        exclude = ['user','create_date', 'update_date',
                   'description', 'moneys_per_hour']

class InvoiceTable(tables.ModelTable):
    id           = tables.Column(sortable=False, visible=False)
    amount       = tables.Column(default="")
    date_created = tables.Column(default="")
    date_sent    = tables.Column(default="")
    date_paid    = tables.Column(default="")
    class Meta:
        model = Invoice
        exclude = ['user','create_date', 'update_date', 'description',
                   'sent_date', 'is_sent', 'is_paid', 'paid_date']

class TimeEntryTable(tables.ModelTable):
    id          = tables.Column(sortable=False, visible=False)
    client      = tables.Column(default="")
    hours       = tables.Column(default="")
    hourly_rate = tables.Column(default="")
    cost        = tables.Column(default="$0.00")
    work_date   = tables.Column(default="")
    invoiced    = tables.Column(default="")

    class Meta:
        model = TimeEntry
        exclude = ['user','create_date', 'update_date', 'description',
                   'invoice', 'rate', 'date', 'is_billable', 'num_hours']

class FixedEntryTable(tables.ModelTable):
    id        = tables.Column(sortable=False, visible=False)
    cost      = tables.Column(default="$0.00")
    work_date = tables.Column(default="")
    invoiced  = tables.Column(default="")

    class Meta:
        model   = FixedEntry
        exclude = ['user','create_date', 'update_date', 'description',
                   'invoice', 'date', 'is_billable', 'moneys']