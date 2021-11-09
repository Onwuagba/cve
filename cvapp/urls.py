from django.urls import path
from .views import home, login, forgotPass, allProp, allOwner, addProp, addOwner, logout, userProp, payDetails, resetPass, userDash, propView

app_name = 'cvapp'

urlpatterns = [
    #auth URL
    path("login/", login, name='login'),
    path("logout/", logout, name='logout'),
    path("forgot_password/", forgotPass, name='fPass'),
    path("reset_password/", resetPass, name='rePass'),

    #staff URLs
    path("", home, name='home'),
    path("property/", allProp, name='aProp'),
    path("add-property/", addProp, name='addProp'),
    path("add-client/", addOwner, name='addOwner'),
    path("home-owners/", allOwner, name='aOwner'),
    path("property-view/<str:id>", propView, name='propView'),

    # user URLS
    path("dashboard/", userDash, name='userDash'),
    path("properties/", userProp, name='userProp'),
    path("payments/", payDetails, name='payDetails'),
]