from django.urls import path
<<<<<<< HEAD
from .views import home, login, forgotPass, allProp, allOwner, addProp, addOwner, logout, userProp, payDetails, resetPass, userDash, propView
=======
from .views import home, login, forgotPass, allProp, allOwner, addProp, addOwner, logout, userProp, payDetails, resetPass, userDoc, newPayment, allFeature, addFeature, allPUpdate, addPUpdate
>>>>>>> b64feed19b106cec5bd7199ba3c6ae47015591cc

app_name = 'cvapp'

urlpatterns = [
    #auth URL
    path("login/", login, name='login'),
    path("logout/", logout, name='logout'),
    path("forgot_password/", forgotPass, name='fPass'),
    path("reset_password/<str:token>/", resetPass, name='rePass'),
    # path("reset_password/", resetPass, name='rePass'),

    #staff URLs
    path("", home, name='home'),
    path("property/", allProp, name='aProp'),
    path("add-property/", addProp, name='addProp'),
    path("add-client/", addOwner, name='addOwner'),
    path("home-owners/", allOwner, name='aOwner'),
<<<<<<< HEAD
    path("property-view/<str:id>", propView, name='propView'),
=======
    path("add-feature/", addFeature, name='addFeature'),
    path("features/", allFeature, name='allFeature'),
    path("project-update/", allPUpdate, name='allPUpdate'),
    path("add-update/", addPUpdate, name='addPUpdate'),
>>>>>>> b64feed19b106cec5bd7199ba3c6ae47015591cc

    # user URLS
    path("dashboard/", userDash, name='userDash'),
    path("properties/", userProp, name='userProp'),
    path("new-payment/", newPayment, name='newPayment'),
    path("payment/", payDetails, name='payDetails'),
    path("document/", userDoc, name='userDoc'),
]