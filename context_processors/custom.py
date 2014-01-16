from django.conf import settings
import re

def logged_in(request):
    request.session.set_expiry(3600)
    return {"is_logged_in" : request.user.is_authenticated(),
            "username"     : request.user.username}

def menu_selected(request):
    pathSearch = re.search('/(.*)/', request.path,re.IGNORECASE)

    if pathSearch:
        menu_selected = pathSearch.group(1)
    else:
        menu_selected = ""

    return {"menu_selected" : menu_selected}