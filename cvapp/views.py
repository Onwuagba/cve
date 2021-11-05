import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model as User
from .models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password

# Create your views here.

@login_required
def home(request):
    context = {
        'page': 'Dashboard',
    }
    if request.user.user_role == 'S':
        return render(request, "user/dashboard.html", context)
    else:
        return render(request, "cve_user/user_dash.html", context)

def userProp(request):
    context = {
        'page': 'Properties',
    }
    return render(request, "cve_user/user_properties.html", context)

def userDoc(request):
    context = {
        'page': 'Documents',
    }
    return render(request, "cve_user/user_documents.html", context)

def payDetails(request):
    context = {
        'page': 'Payment History',
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
            context = {
                'email':email,
            }
            messages.error(request, "Incorrect credentials. Please check them and try again")
            return render(request, "auth/auth-login.html", context)
    return render(request, "auth/auth-login.html")

def resetPass(request, token):
    auth_token = get_object_or_404(User, regToken=token)
    if request.user.is_authenticated:
        if auth_token.id == request.user.id:
            if request.method == "POST":
                p1 = request.POST.get("pass1")
                p2 = request.POST.get("pass2")
                if p1 == p2:
                    if check_password(p1, auth_token.password):
                    # if p1 == auth_token.password:
                        messages.error(request, "Password same as old. Please use a new password.")
                    else:
                        auth_token.set_password(p1)
                        auth_token.default_pwd = False
                        auth_token.regToken = uuid.uuid4()
                        auth_token.save()
                        messages.success(request, "Password reset successfully")
                        return redirect("cvapp:logout")
                else:
                    messages.error(request, "Passwords do not match.")
                    return render(request, "auth/auth-reset-pass.html")
        else:
            return redirect("cvapp:login")
    else:
        if request.method == "POST":
            p1 = request.POST.get("pass1")
            p2 = request.POST.get("pass2")
            if p1 == p2:
                if check_password(p1, auth_token.password):
                    messages.error(request, "Password same as old. Please use a new password.")
                else:
                    auth_token.set_password(p1)
                    auth_token.default_pwd = False
                    auth_token.regToken = uuid.uuid4()
                    auth_token.save()
                    messages.success(request, "Password reset successfully")
                    return redirect("cvapp:logout")
            else:
                messages.error(request, "Passwords do not match.")
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
            phone_number = request.POST.get('phoneNumber')
            pass1 = request.POST.get('password')
            # img = request.POST.get('image')
            context = {
                'passa':pass1,
                'first_name':first_name,
                'last_name':last_name,
                'email':email,
                'phone_number':phone_number,
                # 'img':img,
                'page':'Add Owner'
            }
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return render(request, "user/add-home-owner.html", context)
            elif User.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Phone number already exists.')
                return render(request, "user/add-home-owner.html", context)
            else:
                user = User(email=email)
                user.first_name = first_name
                user.last_name = last_name
                user.phone_number = phone_number
                user.default_pwd = True
                user.user_role = "H"
                # user.profile_photo = img
                user.set_password(pass1)
                # print(user)
                user.save()
                success_note = {
                    'passa':pass1,
                    'page':'Add Owner'
                }
                return render(request, "user/add-home-owner.html", success_note)
        except ObjectDoesNotExist:
            messages.error(request, 'Unauthorised access')
    context = {'page':'Add Owner'}
    return render(request, "user/add-home-owner.html", context)

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
                    'page':'Add Property'
                }
                # messages.success(request, "User successfully added")
                return render(request, "user/add-property.html", context)
        except ObjectDoesNotExist:
            messages.error(request, 'Unauthorised access')
    
    context = {'page':'Add Property'}
    return render(request, "user/add-property.html", context)

# list all property
@login_required
def allProp(request):
    context = {
        'page': 'Properties',
    }
    return render(request, "user/all-property.html", context)

# list all owners
@login_required
def allOwner(request):
    context = {
        'page': 'Home Owners',
    }
    return render(request, "user/all-owners.html", context)

# @login_required
# def addProp(request):
#     return render(request, "user/add-property.html")

# @login_required
# def addOwner(request):
#     return render(request, "user/add-home-owner.html")

def logout(request):
    auth.logout(request)
    return redirect("cvapp:login")
