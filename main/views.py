from django.shortcuts import render_to_response
from django.http      import HttpResponseForbidden
from django.http      import HttpResponseBadRequest
from django.http      import HttpResponseRedirect

from django.template import RequestContext

from devtracker.user_profile.forms   import *
from devtracker.user_profile.tables  import *
from devtracker.time_tracking.models import *
from devtracker.main.models          import *

from django.contrib.auth.decorators import login_required

import django.contrib.auth as auth

def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home/")

    return HttpResponseRedirect("/login/")

def login(request):
    if request.method not in ('POST','GET'):
        return HttpResponseForbidden("")

    errorMsg = ""
    if request.method == 'POST':

        if not "username" in request.POST and not "password" in request.POST:
            return HttpResponseBadRequest("")

        username = request.POST["username"]
        password = request.POST["password"]
        user     = auth.authenticate(username=username,password=password)

        if user is not None:
            if user.is_active:
                # User is authenticated and active. Log them in..
                auth.login(request, user)
                # Redirect user to the dashboard
                try:
                    nextPage = request.GET["next"]
                except:
                    nextPage = "/time-entries/"

                return HttpResponseRedirect(nextPage)
            else:
                errorMsg = "Your account is not active"
        else:
            errorMsg = "Your credentials are incorrect"

    return render_to_response('login.html', {"errorMsg": errorMsg})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login/")

@login_required
def home(request):
    dash        = Dashboard()
    profile     = Profile.objects.get(user__id=request.user.id)
    tax_exposure = float(dash.getTotalPaid(request.user.id)) * (float(profile.tax_bracket)/100.0)

    return render_to_response('dashboard.html',
                              {"total_invoiced" : dash.getTotalInvoiced(request.user.id),
                               "total_paid"     : dash.getTotalPaid(request.user.id),
                               "tax_exposure"   : tax_exposure},
                              context_instance=RequestContext(request))
