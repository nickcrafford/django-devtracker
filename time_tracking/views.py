from devtracker.time_tracking.forms  import *
from devtracker.time_tracking.tables import *
from devtracker.time_tracking.models import *
from django.shortcuts                import render_to_response
from django.http                     import HttpResponseRedirect
from django.http                     import HttpResponseNotFound
from django.http                     import Http404
from django.template                 import RequestContext
from django.contrib.auth.decorators  import login_required

import re
import datetime

@login_required
def listBusinesses(request, pageNumber=None):
    return crudTable(request, BusinessTable, Business)

@login_required
def listClients(request, pageNumber=None):
    return crudTable(request, ClientTable, Client)

@login_required
def listProjects(request, pageNumber=None):
    return crudTable(request, ProjectTable, Project)

@login_required
def listRates(request, pageNumber=None):
    return crudTable(request, RateTable, Rate)


@login_required
def listRecentTimeEntries(request, pageNumber=None):
    return listTimeEntries(request, None, 20)

@login_required
def listTimeEntries(request, pageNumber=None, maxTimeEntries=None):
    tables      = []
    viewAllMode = False

    uninvoiced_data  = TimeEntry.objects.filter(is_billable=True,invoice__isnull=True,user=request.user)
    invoiced_data    = TimeEntry.objects.filter(is_billable=True,invoice__isnull=False,user=request.user)
    unbillable_data  = TimeEntry.objects.filter(is_billable=False,user=request.user)

    if maxTimeEntries:
        uninvoiced_data = uninvoiced_data[:maxTimeEntries]
        invoiced_data   = invoiced_data[:maxTimeEntries]
        unbillable_data = unbillable_data[:maxTimeEntries]

        uninvoicedTitle = "Last %d Un-invoiced Time Entries" % maxTimeEntries
        invoicedTitle   = "Last %d Invoiced Time Entries"    % maxTimeEntries
        unBillableTitle = "Last %d Un-billable Time Entries" % maxTimeEntries
    else:
        uninvoicedTitle = "All Un-invoiced Time Entries"
        invoicedTitle   = "All Invoiced Time Entries"
        unBillableTitle = "All Un-billable Time Entries"
        viewAllMode     = True

    tables.append({"title" : uninvoicedTitle,
                   "data"  : TimeEntryTable(data=uninvoiced_data),
                   "total" : get_time_entry_total(uninvoiced_data)})
    tables.append({"title" : invoicedTitle,
                   "data"  : TimeEntryTable(data=invoiced_data)})
    tables.append({"title" : unBillableTitle,
                   "data"  : TimeEntryTable(data=unbillable_data)})

    return crudTable(request, TimeEntryTable, TimeEntry, tables, viewAllMode, True)

@login_required
def listRecentFixedEntries(request, pageNumber=None):
    return listFixedEntries(request, None, 20)

@login_required
def listFixedEntries(request, pageNumber=None, maxFixedEntries=None):
    tables      = []
    viewAllMode = False

    uninvoiced_data  = FixedEntry.objects.filter(is_billable=True,invoice__isnull=True,user=request.user)
    invoiced_data    = FixedEntry.objects.filter(is_billable=True,invoice__isnull=False,user=request.user)
    unbillable_data  = FixedEntry.objects.filter(is_billable=False,user=request.user)

    if maxFixedEntries:
        uninvoiced_data = uninvoiced_data[:maxFixedEntries]
        invoiced_data   = invoiced_data[:maxFixedEntries]
        unbillable_data = unbillable_data[:maxFixedEntries]

        uninvoicedTitle = "Last %d Un-invoiced Fixed Entries" % maxFixedEntries
        invoicedTitle   = "Last %d Invoiced Fixed Entries"    % maxFixedEntries
        unBillableTitle = "Last %d Un-billable Fixed Entries" % maxFixedEntries
    else:
        uninvoicedTitle = "All Un-invoiced Fixed Entries"
        invoicedTitle   = "All Invoiced Fixed Entries"
        unBillableTitle = "All Un-billable Fixed Entries"
        viewAllMode     = True

    tables.append({"title" : uninvoicedTitle,
                   "data"  : FixedEntryTable(data=uninvoiced_data)})
    tables.append({"title" : invoicedTitle,
                   "data"  : FixedEntryTable(data=invoiced_data)})
    tables.append({"title" : unBillableTitle,
                   "data"  : FixedEntryTable(data=unbillable_data)})

    return crudTable(request, FixedEntryTable, FixedEntry, tables, viewAllMode, True)

@login_required
def listRecentInvoices(request, pageNumber=None):
    return listInvoices(request, None, 20)

@login_required
def listInvoices(request, pageNumber=None, maxInvoices=None):
    # Tables of invoices to be rendered on the invoices page
    tables      = []
    viewAllMode = False

    unsent_data = Invoice.objects.filter(sent_date__isnull=True, user=request.user)
    paid_data   = Invoice.objects.filter(sent_date__isnull=False, paid_date__isnull=False, user=request.user)
    unpaid_data = Invoice.objects.filter(paid_date__isnull=True,sent_date__isnull=False,user=request.user)

    if maxInvoices:
        unsent_data = unsent_data[:maxInvoices]
        paid_data   = paid_data[:maxInvoices]
        unpaid_data = unpaid_data[:maxInvoices]
        unsentTitle = "Last %d Unsent Invoices" % maxInvoices
        unpaidTitle = "Last %d Unpaid Invoices" % maxInvoices
        paidTitle   = "Last %d Paid Invoices"   % maxInvoices
    else:
        unsentTitle = "All Unsent Invoices"
        unpaidTitle = "All Unpaid Invoices"
        paidTitle   = "All Paid Invoices"
        viewAllMode = True

    tables.append({"title" : unsentTitle,
                   "total" : get_invoice_total(unsent_data),
                   "data"  : InvoiceTable(data=unsent_data)})

    tables.append({"title" : unpaidTitle,
                   "total" : get_invoice_total(unpaid_data),
                   "data"  : InvoiceTable(data=unpaid_data)})

    tables.append({"title" : paidTitle,
                   "total" : get_invoice_total(paid_data),
                   "data"  : InvoiceTable(data=paid_data)})



    return crudTable(request, InvoiceTable, Invoice, tables, viewAllMode, True)

@login_required
def invoice(request, invoiceId=None):

    # Upsert an invoice
    def saveFun(request, invoiceForm, invoice=None):
        if not invoice:
            invoice             = Invoice()
            invoice.create_date = datetime.date.today()

        if invoice.is_readonly():
            return

        invoice.user        = request.user
        invoice.client      = invoiceForm.cleaned_data['client']
        invoice.paid_date   = invoiceForm.cleaned_data['paid_date']
        invoice.sent_date   = invoiceForm.cleaned_data['sent_date']
        invoice.name        = invoiceForm.cleaned_data['name']
        invoice.save()

    # Look up child data tables
    childTables = []
    if invoiceId:
        timeEntryData = TimeEntry.objects.filter(invoice__id=invoiceId,user=request.user)
        if timeEntryData.count() > 0:
            childTables.append({"title"      : TimeEntry._meta.verbose_name_plural,
                                "child_path" : TimeEntry.child_path,
                                "table"      : TimeEntryTable(data=timeEntryData)})

        fixedEntryData = FixedEntry.objects.filter(invoice__id=invoiceId,user=request.user)
        if fixedEntryData.count() > 0:
            childTables.append({"title"      : FixedEntry._meta.verbose_name_plural,
                                "child_path" : FixedEntry.child_path,
                                "table"      : FixedEntryTable(data=fixedEntryData)})

    # Extra form data
    readOnlyFields      = [{"name" : "Status",      "value" : "status"},
                           {"name" : "Create date", "value" : "date_created"},
                           {"name" : "Amount",      "value" : "amount"}]
    initialValues       = {}
    includeExportButton = True

    return crudForm(request, InvoiceForm, initialValues, saveFun, Invoice,
                    invoiceId, childTables, readOnlyFields, includeExportButton)

@login_required
def fixedEntry(request, fixedEntryId=None):
    def saveFun(request, fixedEntryForm, fixedEntry=None):
        if not fixedEntry:
            fixedEntry = FixedEntry()

        if fixedEntry.is_readonly():
            return

        fixedEntry.user        = request.user
        fixedEntry.project     = fixedEntryForm.cleaned_data['project']
        fixedEntry.date        = fixedEntryForm.cleaned_data['date']
        fixedEntry.moneys      = fixedEntryForm.cleaned_data['moneys']
        fixedEntry.invoice     = fixedEntryForm.cleaned_data['invoice']
        fixedEntry.is_billable = fixedEntryForm.cleaned_data['is_billable']
        fixedEntry.description = fixedEntryForm.cleaned_data['description']
        fixedEntry.save()

    childTables = []
    if fixedEntryId:
        try:
            fixedEntry  = FixedEntry.objects.get(id=fixedEntryId)
        except:
            return HttpResponseNotFound('<h1>Fixed entry not found</h1>')

        if fixedEntry.invoice:
            invoiceData = Invoice.objects.filter(id=fixedEntry.invoice.id,user=request.user)

            if invoiceData.count() > 0:
                childTables.append({"title"      : Invoice._meta.verbose_name_plural,
                                    "child_path" : Invoice.child_path,
                                    "table"      : InvoiceTable(data=invoiceData)})

        projectData = Project.objects.filter(id=fixedEntry.project.id,user=request.user)

        if projectData.count() > 0:
            childTables.append({"title"      : Project._meta.verbose_name_plural,
                                "child_path" : Project.child_path,
                                "table"      : ProjectTable(data=projectData)})

    readOnlyFields      = []
    initialValues       = {"date": datetime.date.today(),
                           "is_billable" : True }
    includeExportButton = False

    return crudForm(request, FixedEntryForm, initialValues, saveFun, FixedEntry,
                    fixedEntryId, childTables, readOnlyFields, includeExportButton)

@login_required
def timeEntry(request, timeEntryId=None):
    def saveFun(request, timeEntryForm, timeEntry=None):
        if not timeEntry:
            timeEntry = TimeEntry()

        if timeEntry.is_readonly():
            return

        timeEntry.user        = request.user
        timeEntry.project     = timeEntryForm.cleaned_data['project']
        timeEntry.rate        = timeEntryForm.cleaned_data['rate']
        timeEntry.num_hours   = timeEntryForm.cleaned_data['num_hours']
        timeEntry.invoice     = timeEntryForm.cleaned_data['invoice']
        timeEntry.date        = timeEntryForm.cleaned_data['date']
        timeEntry.is_billable = timeEntryForm.cleaned_data['is_billable']
        timeEntry.description = timeEntryForm.cleaned_data['description']
        timeEntry.save()

    childTables = []
    if timeEntryId:
        try:
            timeEntry  = TimeEntry.objects.get(id=timeEntryId)
        except:
            return HttpResponseNotFound('<h1>Time entry not found</h1>')
        
        if timeEntry.invoice:
            invoiceData = Invoice.objects.filter(id=timeEntry.invoice.id,user=request.user)

            if invoiceData.count() > 0:
                childTables.append({"title"      : Invoice._meta.verbose_name_plural,
                                    "child_path" : Invoice.child_path,
                                    "table"      : InvoiceTable(data=invoiceData)})

        projectData = Project.objects.filter(id=timeEntry.project.id,user=request.user)

        if projectData.count() > 0:
            childTables.append({"title"      : Project._meta.verbose_name_plural,
                                "child_path" : Project.child_path,
                                "table"      : ProjectTable(data=projectData)})

    readOnlyFields      = []
    initialValues       = {"date"        : datetime.date.today(),
                           "is_billable" : True }
    includeExportButton = False

    return crudForm(request, TimeEntryForm, initialValues, saveFun, TimeEntry,
                    timeEntryId, childTables, readOnlyFields, includeExportButton)

@login_required
def business(request, businessId=None):
    def saveFun(request, businessForm, business=None):
        if not business:
            business = Business()

        if business.is_readonly():
            return

        business.user    = request.user
        business.address = businessForm.cleaned_data['address']
        business.name    = businessForm.cleaned_data['name']
        business.city    = businessForm.cleaned_data['city']
        business.state   = businessForm.cleaned_data['state']
        business.postal  = businessForm.cleaned_data['postal']
        business.save()

    # Look up child data tables
    childTables = []
    if businessId:
        clientData = Client.objects.filter(business__id=businessId)
        if clientData.count() > 0:
            childTables.append({"title"      : Client._meta.verbose_name_plural,
                                "child_path" : Client.child_path,
                                "table"      : BusinessTable(data=clientData)})

    readOnlyFields      = []
    initialValues       = {}
    includeExportButton = False

    return crudForm(request, BusinessForm, initialValues, saveFun, Business,
                    businessId, childTables, readOnlyFields, includeExportButton)

@login_required
def client(request, clientId=None):
    def saveFun(request, clientForm, client=None):
        if not client:
            client = Client()

        if client.is_readonly():
            return

        client.user     = request.user
        client.business = clientForm.cleaned_data['business']
        client.address  = clientForm.cleaned_data['address']
        client.city     = clientForm.cleaned_data['city']
        client.state    = clientForm.cleaned_data['state']
        client.postal   = clientForm.cleaned_data['postal']
        client.name     = clientForm.cleaned_data['name']
        client.save()

    # Look up child data tables
    childTables = []
    if clientId:
        projectData = Project.objects.filter(client__id=clientId,user=request.user)
        if projectData.count() > 0:
            childTables.append({"title"      : Project._meta.verbose_name_plural,
                                "child_path" : Project.child_path,
                                "table"      : ProjectTable(data=projectData)})

    readOnlyFields      = []
    initialValues       = {}
    includeExportButton = False

    return crudForm(request, ClientForm, initialValues, saveFun, Client,
                    clientId, childTables, readOnlyFields, includeExportButton)

@login_required
def project(request, projectId=None):
    def saveFun(request, projectForm, project=None):
        if not project:
            project = Project()

        if project.is_readonly():
            return

        project.user        = request.user
        project.client      = projectForm.cleaned_data['client']
        project.name        = projectForm.cleaned_data['name']
        project.budget      = projectForm.cleaned_data['budget']
        project.description = projectForm.cleaned_data['description']
        project.save()

    # Look up child data tables
    childTables = []
    if projectId:
        timeEntryData = TimeEntry.objects.filter(project__id=projectId,user=request.user)

        if timeEntryData.count() > 0:
            childTables.append({"title"      : TimeEntry._meta.verbose_name_plural,
                                "child_path" : TimeEntry.child_path,
                                "table"      : TimeEntryTable(data=timeEntryData)})

        fixedEntryData = FixedEntry.objects.filter(project__id=projectId,user=request.user)
        if fixedEntryData.count() > 0:
            childTables.append({"title"      : FixedEntry._meta.verbose_name_plural,
                                "child_path" : FixedEntry.child_path,
                                "table"      : FixedEntryTable(data=fixedEntryData)})

    readOnlyFields      = [{"name"  : "Running Cost",
                            "value" : "running_cost"}]
    initialValues       = {}
    includeExportButton = False

    return crudForm(request, ProjectForm, initialValues, saveFun, Project,
                    projectId, childTables, readOnlyFields, includeExportButton)

@login_required
def rate(request, rateId=None):
    def saveFun(request, rateForm, rate=None):
        if not rate:
            rate = Rate()

        if rate.is_readonly():
            return

        rate.user            = request.user
        rate.description     = rateForm.cleaned_data['description']
        rate.name            = rateForm.cleaned_data['name']
        rate.moneys_per_hour = rateForm.cleaned_data['moneys_per_hour']
        rate.save()

    childTables         = []
    readOnlyFields      = []
    initialValues       = {}
    includeExportButton = False

    return crudForm(request, RateForm, initialValues, saveFun, Rate,
                    rateId, childTables, readOnlyFields, initialValues)

@login_required
def delInvoice(request, invoiceId):
    return delObject(request, Invoice, invoiceId)

@login_required
def delTimeEntry(request, timeEntryId):
    return delObject(request, TimeEntry, timeEntryId)

@login_required
def delFixedEntry(request, fixedEntryId):
    return delObject(request, FixedEntry, fixedEntryId)

@login_required
def delBusiness(request, businessId):
    return delObject(request, Business, businessId)

@login_required
def delClient(request, clientId):
    return delObject(request, Client, clientId)

@login_required
def delProject(request, projectId):
    return delObject(request, Project, projectId)

@login_required
def delRate(request, rateId):
    return delObject(request, Rate, rateId)

def crudTable(request, tableClass, objClass, tables=None, viewAllMode=False, hasViewAll=False):
    """ Render a table for the passed table class. If tables
    are passed render them instead. """
    if not tables:
        tables = [{"data"  : tableClass(data=objClass.objects.filter(user=request.user)),
                   "title" : objClass._meta.verbose_name_plural}]

    return render_to_response('table.html',
                              {"tables"              : tables,
                               "view_all_mode"       : viewAllMode,
                               "base_path"           : objClass.child_path,
                               "verbose_name"        : objClass._meta.verbose_name,
                               "verbose_name_plural" : objClass._meta.verbose_name_plural,
                               "has_view_all"        : hasViewAll},
                              context_instance=RequestContext(request))

def crudForm(request, formClass, initialValues, saveFun, objClass, objId,
             childTables=[], readOnlyFields=[], includeExportButton=False):
    """ Render a form for the passed form class, populate the form with the
    passed initialValues. If a POST request is sent then run the saveFun to
    either save a new instance in the DB or update an existing one (if
    the object id is present). """
    basePath = objClass.child_path

    # If the object id has been passed i.e. "Edit"
    if objId:
        # Attempt to load an object instance via the passed id
        try:
            obj  = objClass.objects.get(id=objId)

        # If loading fails forward to a 404 page
        except:
            raise Http404

        # Save an existing instance of the object being worked on
        if request.method == 'POST':
            form = formClass(request.POST, instance=obj, request=request)
            if form.is_valid():
                saveFun(request, form, obj)
                message = "Changes Saved"
            else:
                message = ""

        # Display the editing form for the object being worked on
        else:
            form    = formClass(instance=obj, request=request)
            message = ""

    # Save a new instance of the object type being worked on
    else:
        obj = None

        if request.method == 'POST':
            form = formClass(request.POST, request=request)
            if form.is_valid():
                saveFun(request, form, obj)
                form    = formClass(request=request)
                message ="Creation Successful"
            else:
                message = ""
        else:
            form    = formClass(initial=initialValues, request=request)
            message = ""

    # Retrieve value for title attribute
    if obj:
        title = str(obj)
    else:
        title = "New " + objClass._meta.verbose_name

    # Process read only fields
    for field in readOnlyFields:
        if obj:
            method         =  getattr(obj, field["value"])
            field["value"] = method()
        else:
            field["value"] = "N/A"


    # Figure out what the export filename should be
    exportFilename = ""
    if includeExportButton:
        try:
            exportFilename = obj.get_export_filename()
        except:
            pass

    # Make the form read only if required
    readOnly = False
    try:
        readOnly = obj.is_readonly()
        if readOnly:
            make_form_read_only(form)
    except:
        pass

    # Only include an export button if the object instance already exists
    # and we have asked for it
    includeExportButton = includeExportButton and objId > 0

    return render_to_response('detail.html',
                              {"title"                 : title.title(),
                               "form"                  : form,
                               "id"                    : objId,
                               "action"                : request.path,
                               "base_path"             : basePath,
                               "message"               : message,
                               "child_tables"          : childTables,
                               "read_only_fields"      : readOnlyFields,
                               "include_export_button" : includeExportButton,
                               "export_filename"       : exportFilename,
                               "readonly"              : readOnly},
                              context_instance=RequestContext(request))

def delObject(request, objClass, id):
    """ Delete an object instance from the DB and
    redirect the user to the passed page. """
    if request.method == 'POST':
        obj = objClass.objects.get(id=id,user=request.user)
        obj.delete()
    return HttpResponseRedirect(objClass.child_path + "/")

def getBasePath(path):
    """ Determine the base path i.e. /base/ of /base/123/ew/df
    of the passed full path. """
    pathSearch = re.search('/(.*)/', path,re.IGNORECASE)

    if pathSearch:
        basePath = pathSearch.group(1)
    else:
        basePath = ""

    return basePath
