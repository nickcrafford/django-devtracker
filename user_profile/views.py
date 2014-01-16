from devtracker.user_profile.forms  import *
from devtracker.user_profile.tables import *
from devtracker.user_profile.models import *

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
import django.contrib.auth as auth

from django.template import RequestContext

def new_profile(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        form = ProfileForm(request.POST)
        if form.is_valid() and userForm.is_valid():
            username = userForm.cleaned_data['username']
            password = userForm.cleaned_data['password']
            user = User.objects.create_user(username,
                                            userForm.cleaned_data['email'],
                                            password)
            
            # Requires Email Confirmation to enable
            user.is_active = False
            user.save()
            
            profile                 = Profile()
            profile.user            = user
            profile.billing_name    = form.cleaned_data['billing_name']
            profile.billing_address = form.cleaned_data['billing_address']
            profile.billing_city    = form.cleaned_data['billing_city']
            profile.billing_state   = form.cleaned_data['billing_state']
            profile.billing_postal  = form.cleaned_data['billing_postal']
            profile.save()

            authUser = auth.authenticate(username=username,password=password)
            auth.login(request, authUser)
            
            return HttpResponseRedirect('/dashboard/')
    else:
        userForm = UserForm()
        form = ProfileForm()
        
    return render_to_response('new_profile.html', {'profileForm': form,
                                                   'userForm': userForm})

def profile(request):
    message = ""

    try:
        profile = Profile.objects.get(user__id=request.user.id)
    except:
        profile = Profile()
        profile.user = request.user

    if request.method == 'POST':
        request.user.email = request.POST["email_address"]
        request.user.save()

        form = ProfileForm(request.POST)

        if form.is_valid():
            profile.billing_name    = form.cleaned_data['billing_name']
            profile.billing_address = form.cleaned_data['billing_address']
            profile.billing_city    = form.cleaned_data['billing_city']
            profile.billing_state   = form.cleaned_data['billing_state']
            profile.billing_postal  = form.cleaned_data['billing_postal']

            profile.weekly_revenue_goal  = form.cleaned_data['weekly_revenue_goal']
            profile.monthly_revenue_goal = form.cleaned_data['monthly_revenue_goal']
            profile.yearly_revenue_goal  = form.cleaned_data['yearly_revenue_goal']
            profile.tax_bracket          = form.cleaned_data['tax_bracket']

            profile.save()
            message = "Changes Saved"
    else:
        form = ProfileForm(initial={"billing_name" : profile.billing_name,
                                    "billing_address" : profile.billing_address,
                                    "billing_city" : profile.billing_city,
                                    "billing_state" : profile.billing_state,
                                    "billing_postal" : profile.billing_postal,
                                    "weekly_revenue_goal" : profile.weekly_revenue_goal,
                                    "monthly_revenue_goal" : profile.monthly_revenue_goal,
                                    "yearly_revenue_goal" : profile.yearly_revenue_goal,
                                    "tax_bracket"         : profile.tax_bracket})
    return render_to_response('profile.html', {'profileForm' : form,
                                               'message'     : message},
                              context_instance=RequestContext(request))