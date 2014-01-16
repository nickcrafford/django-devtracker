from devtracker.time_tracking.models import *
from django.forms                    import ModelForm
from django                          import forms
from django.forms                    import extras

def make_custom_datefield(f):
    formfield = f.formfield()
    if isinstance(f, models.DateField):
        formfield.widget.format = '%m/%d/%Y'
        formfield.widget.attrs.update({'class':'datePicker'})
    return formfield

def make_form_read_only(form):
    for field_key in form.fields:
        field = form.fields[field_key]
        field.widget.attrs['readonly'] = True
        field.widget.attrs['disabled'] = True

class BusinessForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super (BusinessForm,self ).__init__(*args,**kwargs)

    class Meta:
        model   = Business
        exclude = ['user']

class ClientForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super (ClientForm,self ).__init__(*args,**kwargs)
        self.fields['business'].queryset = Business.objects.filter(user=self.request.user)
    class Meta:
        model = Client
        exclude = ['user']

class ProjectForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super (ProjectForm,self ).__init__(*args,**kwargs)
        self.fields['client'].queryset = Client.objects.filter(user=self.request.user)
    class Meta:
        model   = Project
        exclude = ['user']

class RateForm(ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super (RateForm,self ).__init__(*args,**kwargs)

    class Meta:
        model   = Rate
        exclude = ['user']

class InvoiceForm(ModelForm):
    formfield_callback = make_custom_datefield
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super (InvoiceForm,self ).__init__(*args,**kwargs)
        self.fields['client'].queryset = Client.objects.filter(user=self.request.user)

    class Meta:
        model  = Invoice
        fields = ('client', 'name', 'sent_date', 'paid_date')

class TimeEntryForm(ModelForm):
    formfield_callback = make_custom_datefield
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super (TimeEntryForm,self ).__init__(*args,**kwargs)
        self.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        self.fields['rate'].queryset    = Rate.objects.filter(user=self.request.user)
        self.fields['invoice'].queryset = Invoice.objects.filter(user=self.request.user)

    class Meta:
        model   = TimeEntry
        exclude = ['user']

class FixedEntryForm(ModelForm):
    formfield_callback = make_custom_datefield
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        super (FixedEntryForm,self ).__init__(*args,**kwargs)
        self.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        self.fields['invoice'].queryset = Invoice.objects.filter(user=self.request.user)

    class Meta:
        model   = FixedEntry
        exclude = ['user']