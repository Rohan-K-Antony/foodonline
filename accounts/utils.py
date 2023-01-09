def role_check(user):
    redirectlink = ''
    if user.role == 2:
        redirectlink ='custDashboard'
    elif user.role == 1:
        redirectlink = 'venDashboard'
    elif user.role is None and user.is_superadmin is True:
        redirectlink = '/admin'
    return redirectlink