from django.core import exceptions
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model as User
from .models import HouseInfo, User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required
def home(request):
    context = {
        'page': 'home',
    }
    if request.user.is_staff:
        # print ("This is a staff")
        return render(request, "user/dashboard.html", context)
    else:
        # print (user.user_role)
        # print ("This is a user")
        return render(request, "cve_user/user_dash.html")
        # return redirect("cvapp:userDash")
    # return render(request, "user/dashboard.html", context)

# @login_required
# def staffHome(request):
#     return render(request, "cv_staff/staff_home.html")

# def userDash(request):
#     context = {
#         'page': 'dash',
#     }
#     return render(request, "cve_user/user_dash.html", context)

def userProp(request):
    context = {
        'page': 'prop',
    }
    return render(request, "cve_user/user_properties.html", context)

def payDetails(request):
    context = {
        'page': 'payD',
    }
    return render(request, "cve_user/payment_details.html", context)

def forgotPass(request):
    return render(request, "auth/auth-forgot.html")

def login(request):
    if request.user.is_authenticated:
        return redirect("cvapp:home")
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # user = User().objects.filter(email=email).filter(password=password)
        # print(f'after query is :{user}')
        # print(f'email: {email}, password: {password}')
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            return redirect("cvapp:home")
        else:
            messages.success(request, "Incorrect credentials. Please check them and try again")
    return render(request, "auth/auth-login.html")

def resetPass(request):
    return render(request, "auth/auth-reset-pass.html")

@login_required
def addOwner(request):
    user1 = request.user
    # print (User.objects.get(id=user1.user_role))
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user1.id)
            first_name = request.POST.get('firstname')
            last_name = request.POST.get('lastname')
            email = request.POST.get('email')
            phonenumber = request.POST.get('phoneNumber')
            pass1 = request.POST.get('password')
            img = request.POST.get('image')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists.')
            elif User.objects.filter(phone_number=phonenumber).exists():
                messages.info(request, 'Phone number already exists.')
            else:
                user = User(email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.phone_number = phonenumber
                user.default_pwd = True
                # user.is_active = True
                user.user_role = "H"
                user.profile_photo = img
                user.set_password(pass1)
                # print(user)
                user.save()
                context = {
                    'passa':pass1,
                    'page':'addowner'
                }
                # messages.success(request, "User successfully added")
                return render(request, "user/add-home-owner.html", context)
        except ObjectDoesNotExist:
            messages.error(request, 'Unauthorised access')
    context = {'page':'addowner'}
    return render(request, "user/add-home-owner.html", context)

@login_required
def addProp(request):
    user1 = request.user
    # print(user1.id)
    # print (User.objects.get(id=user1.user_role))
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user1.id)
            house_id = request.POST.get('houseID')
            location = request.POST.get('location')
            cost = request.POST.get('cost')
            description = request.POST.get('description')
            img = request.POST.get('image')
            if HouseInfo.objects.filter(street_info=location).exists():
                messages.info(request, 'House ID has been used')
            elif int(cost) < 1000000:
                messages.info(request, 'Cost too low')
            else:
                house = HouseInfo(street_info=location, cost=cost, desription=description, images=[img])
                house.created_by = user
                house.save()
                context = {
                    'passa': house_id,
                    'page':'addprop'
                }
                return render(request, "user/add-property.html", context)
        except BaseException:
            messages.error(request, 'Unauthorised access')
    
    context = {'page':'addprop'}
    return render(request, "user/add-property.html", context)

def propView(request, id):
    # print (request.GET.get(id))
    propName = request.GET.get(id)
    context = {
        'page': 'propView',
        'prop' : propName
    }
    return render(request, "user/property-view.html", context)

# list all property
@login_required
def allProp(request):
    properties = HouseInfo.objects.all()
    context = {
        'page': 'allprop',
        'properties': properties,
    }

    return render(request, "user/all-property.html", context)

# list all owners
@login_required
def allOwner(request):
    owners = User.objects.filter(user_role="H")
    context = {
        'page': 'allowner',
        'owners': owners,
    }
    return render(request, "user/all-owners.html", context)

# @login_required
# def addOwner(request):
#     return render(request, "user/add-home-owner.html")

def logout(request):
    auth.logout(request)
    return redirect("cvapp:login")



# USER VIEW
@login_required
def userDash(request):
    return render(request, "cve_user/user_dash.html")

