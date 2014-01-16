from django                          import http
from django.shortcuts                import render_to_response
from django.template.loader          import get_template
from django.template                 import Context
from devtracker.time_tracking.models import *
from devtracker.user_profile.models  import *

import xhtml2pdf.pisa as pisa
import cStringIO      as StringIO

import cgi

def exportInvoice(request, invoiceId, filename):
    invoice      = Invoice.objects.get(id=invoiceId)
    timeEntries  = TimeEntry.objects.filter(invoice__id=invoiceId)
    fixedEntries = FixedEntry.objects.filter(invoice__id=invoiceId)
    profile      = Profile.objects.get(user__id=request.user.id)

    return render_to_pdf("exports/invoice.html", {"time_entries"  : timeEntries,
                                                  "fixed_entries" : fixedEntries,
                                                  "invoice"       : invoice,
                                                  "profile"       : profile})

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context  = Context(context_dict)
    html     = template.render(context)
    result   = StringIO.StringIO()
    pdf      = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)

    if not pdf.err:
        return http.HttpResponse(result.getvalue(), mimetype='application/pdf')

    return http.HttpResponse('<b>Error:</b><pre>%s</pre>' % cgi.escape(html))