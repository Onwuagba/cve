from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model as User
from .models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

# Create your views here.

@login_required
def home(request):
    return render(request, "user/dashboard.html")

@login_required
def staffHome(request):
    return render(request, "cv_staff/staff_home.html")

@login_required
def userDash(request):
    return render(request, "cve_user/user_dash.html")

def userProp(request):
    return render(request, "cve_user/user_properties.html")

def payDetails(request):
    context = {
        'active': "active",
    }
    return render(request, "cve_user/payment_details.html", context)

def forgotPass(request):
    return render(request, "auth/auth-forgot.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # user = User().objects.filter(email=email).filter(password=password)
        # print(f'after query is :{user}')
        # print(f'email: {email}, password: {password}')
        user = auth.authenticate(email=email, password=password)
        if user:
            auth.login(request, user)
            # return redirect("cvapp:home")
            if user.user_role == 'S':
                # print ("This is a staff")
                return redirect("cvapp:home")
            else:
                # print (user.user_role)
                # print ("This is a user")
                return redirect("cvapp:userDash")
        else:
            messages.success(request, "Incorrect credentials. Please check them and try again")
    return render(request, "auth/auth-login.html")

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
                user.is_active = True
                user.user_role = "H"
                user.profile_photo = img
                user.set_password(pass1)
                # print(user)
                user.save()
                context = {
                    'passa':pass1,
                }
                # messages.success(request, "User successfully added")
                return render(request, "user/add-home-owner.html", context)
        except ObjectDoesNotExist:
            messages.error(request, 'Unauthorised access')
    return render(request, "user/add-home-owner.html")

@login_required
def addProp(request):
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
                user.profile_photo = img
                user.set_password(pass1)
                # print(user)
                user.save()
                context = {
                    'passa':pass1,
                }
                # messages.success(request, "User successfully added")
                return render(request, "user/add-property.html", context)
        except ObjectDoesNotExist:
            messages.error(request, 'Unauthorised access')
    return render(request, "user/add-property.html")

# list all property
@login_required
def allProp(request):
    return render(request, "user/all-property.html")

# list all owners
@login_required
def allOwner(request):
    return render(request, "user/all-owners.html")

# @login_required
# def addProp(request):
#     return render(request, "user/add-property.html")

# @login_required
# def addOwner(request):
#     return render(request, "user/add-home-owner.html")

def logout(request):
    auth.logout(request)
    return redirect("cvapp:login")