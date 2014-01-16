from django.conf.urls.defaults    import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'devtracker.views.home', name='home'),
    # url(r'^devtracker/', include('devtracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    (r'^login[/]?$',       'devtracker.main.views.login'),
    (r'^logout[/]?$',      'devtracker.main.views.logout'),
    (r'^home[/]?$',        'devtracker.main.views.home'),
    (r'^businesses[/]?$',  'devtracker.time_tracking.views.listBusinesses'),
    (r'^businesses/(\d+)[/]?$',  'devtracker.time_tracking.views.business'),
    (r'^businesses/new[/]?$',  'devtracker.time_tracking.views.business'),
    (r'^businesses/delete/(\d+)[/]?$',  'devtracker.time_tracking.views.delBusiness'),
    (r'^clients[/]?$',     'devtracker.time_tracking.views.listClients'),
    (r'^clients/(\d+)[/]?$',     'devtracker.time_tracking.views.client'),
    (r'^clients/new[/]?$',     'devtracker.time_tracking.views.client'),
    (r'^clients/delete/(\d+)[/]?$',     'devtracker.time_tracking.views.delClient'),
    (r'^projects[/]?$',    'devtracker.time_tracking.views.listProjects'),
    (r'^projects/(\d+)[/]?$',    'devtracker.time_tracking.views.project'),
    (r'^projects/new[/]?$',    'devtracker.time_tracking.views.project'),
    (r'^projects/delete/(\d+)[/]?$',    'devtracker.time_tracking.views.delProject'),
    (r'^rates[/]?$',       'devtracker.time_tracking.views.listRates'),
    (r'^rates/(\d+)[/]?$',       'devtracker.time_tracking.views.rate'),
    (r'^rates/new[/]?$',       'devtracker.time_tracking.views.rate'),
    (r'^rates/delete/(\d+)[/]?$',       'devtracker.time_tracking.views.delRate'),
    (r'^time-entries[/]?$',       'devtracker.time_tracking.views.listRecentTimeEntries'),
    (r'^time-entries/all[/]?$',       'devtracker.time_tracking.views.listTimeEntries'),
    (r'^time-entries/(\d+)[/]?$',       'devtracker.time_tracking.views.timeEntry'),
    (r'^time-entries/new[/]?$',       'devtracker.time_tracking.views.timeEntry'),
    (r'^time-entries/delete/(\d+)[/]?$',       'devtracker.time_tracking.views.delTimeEntry'),
    (r'^fixed-entries[/]?$',                'devtracker.time_tracking.views.listRecentFixedEntries'),
    (r'^fixed-entries/all[/]?$',                'devtracker.time_tracking.views.listFixedEntries'),
    (r'^fixed-entries/(\d+)[/]?$',       'devtracker.time_tracking.views.fixedEntry'),
    (r'^fixed-entries/new[/]?$',       'devtracker.time_tracking.views.fixedEntry'),
    (r'^fixed-entries/delete/(\d+)[/]?$',       'devtracker.time_tracking.views.delFixedEntry'),
    (r'^invoices[/]?$',       'devtracker.time_tracking.views.listRecentInvoices'),
    (r'^invoices/all[/]?$',       'devtracker.time_tracking.views.listInvoices'),
    (r'^invoices/(\d+)[/]?$',       'devtracker.time_tracking.views.invoice'),
    (r'^invoices/new[/]?$',       'devtracker.time_tracking.views.invoice'),
    (r'^invoices/delete/(\d+)[/]?$',       'devtracker.time_tracking.views.delInvoice'),
    (r'^invoices/export/(\d+)/(.+)[/]?$',       'devtracker.export.views.exportInvoice'),

    (r'^profile[/]?$',     'devtracker.user_profile.views.profile'),
    (r'^profile/new[/]?$', 'devtracker.user_profile.views.new_profile'),
    (r'^[/]?$', 'devtracker.main.views.index'),
)
