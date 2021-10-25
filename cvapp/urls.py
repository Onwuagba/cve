from django.urls import path
from .views import home, login, forgotPass, allProp, allOwner, addProp, addOwner, logout

app_name = 'cvapp'

urlpatterns = [
    path("", home, name='home'),
    path("login/", login, name='login'),
    path("logout/", logout, name='logout'),
    path("forgot_password/", forgotPass, name='fPass'),
    path("property/", allProp, name='aProp'),
    path("add-property/", addProp, name='addProp'),
    path("add-client/", addOwner, name='addOwner'),
    path("home-owners/", allOwner, name='aOwner'),
]