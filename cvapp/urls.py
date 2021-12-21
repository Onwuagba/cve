from django.urls import path
from .views import home, login, forgotPass, allProp, allOwner, addProp, addOwner, logout, userProp, payDetails, resetPass, userDoc, newPayment, allFeature, addFeature, allPUpdate, addPUpdate, addStaff, allStaff, assignProp, propInfo

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
    path("all-property/", allProp, name='aProp'),
    path("add-property/", addProp, name='addProp'),
    path("add-client/", addOwner, name='addOwner'),
    path("add-staff/", addStaff, name='addStaff'),
    path("home-owners/", allOwner, name='aOwner'),
    path("assign-property/", assignProp, name='assignProp'),
    path("all-staff/", allStaff, name='aStaff'),
    path("add-feature/", addFeature, name='addFeature'),
    path("features/", allFeature, name='allFeature'),
    path("project-update/", allPUpdate, name='allPUpdate'),
    path("add-update/", addPUpdate, name='addPUpdate'),
    path("property-info/<int:id>/", propInfo, name='propInfo'),

    # user URLS
    path("properties/", userProp, name='userProp'),
    path("new-payment/", newPayment, name='newPayment'),
    path("payment/", payDetails, name='payDetails'),
    path("document/", userDoc, name='userDoc'),
]