from django.shortcuts import redirect


def detectUser(user):
    redirectURL = ''
    if user.role == 1:
        redirectURL = 'vendorDashboard'
    elif user.role == 2:
        redirectURL = 'custDashboard'
    elif user.role == None and user.is_superadmin:
        redirectURL = '/admin'
    return redirectURL
