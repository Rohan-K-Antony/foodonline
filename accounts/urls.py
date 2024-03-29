from django.urls import path
from . import views
urlpatterns = [
    
    path('registerUser/',views.registerUser, name=  'registerUser'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('myAccount/',views.myAccount,name='myAccount'),
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('venDashboard/',views.vendDashboard,name='venDashboard'),
    path('activate/<uid64>/<token>/',views.activate , name='activate'),
    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uid64>/<token>',views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/',views.reset_password, name='reset_password'),
]