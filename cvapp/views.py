import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model as User
from .models import HouseInfo, ProjectUpdate, User, UserHouse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
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

@login_required
def userProp(request):
    context = {
        'page': 'Properties',
    }
    return render(request, "cve_user/user_properties.html", context)

@login_required
def userDoc(request):
    context = {
        'page': 'Documents',
    }
    return render(request, "cve_user/user_documents.html", context)

@login_required
def payDetails(request):
    context = {
        'page': 'Payment History',
    }
    return render(request, "cve_user/payment_details.html", context)

@login_required
def newPayment(request):
    context = {
        'page': 'New Payment',
    }
    return render(request, "cve_user/new_payment.html", context)

@login_required
def addFeature(request):
    context = {
        'page': 'Add Feature',
    }
    return render(request, "user/add-feature.html", context)

@login_required
def allFeature(request):
    context = {
        'page': 'Feature',
    }
    return render(request, "user/all-features.html", context)

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
    # print (user1)
    # if user1.user_role == 'S': #use permissions instead
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
                user.added_by = user1.first_name
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
    # else:
    #     messages.error(request, 'Unauthorised access')
    #     return redirect("cvapp:logout")

def addStaff(request):
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
                'page':'Add Staff'
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
                user.user_role = "S"
                # user.profile_photo = img
                user.set_password(pass1)
                # print(user)
                user.save()
                success_note = {
                    'passa':pass1,
                    'page':'Add Staff'
                }
                return render(request, "user/add-staff.html", success_note)
        except ObjectDoesNotExist:
            messages.error(request, 'Unauthorised access')
    context = {'page':'Add Staff'}
    return render(request, "user/add-staff.html", context)

@login_required
def addProp(request):
    user1 = request.user
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user1.id)
            # house_id = request.POST.get('houseID')
            title = request.POST.get('title')
            quantity = request.POST.get('quantity')
            progress = request.POST.get('progress')
            cost = request.POST.get('cost')
            description = request.POST.get('description')
            img = request.POST.get('image')
            context = {
                'title':title,
                'quantity':quantity,
                'progress':progress,
                'cost':cost,
                # 'img':img,
                'page':'Add Property'
            }
            if HouseInfo.objects.filter(title=title).exists():
                messages.info(request, 'Property title already exists')
                return render(request, "user/add-property.html", context)
            else:
                house = HouseInfo(title=title, progress=progress, quantity=quantity, cost=cost, desription=description, images=img)
                house.created_by = user
                house.save()
                context = {
                    'success': 'House successfully created',
                    'page':'Add Property'
                }
                return render(request, "user/add-property.html", context)
        except ObjectDoesNotExist:
            messages.error(request, 'Unauthorised access')
            return redirect("cvapp:logout")
    context = {'page':'Add Property'}
    return render(request, "user/add-property.html", context)

# list all property
@login_required
def allProp(request):
    properties = HouseInfo.objects.all()

    paginator = Paginator(properties, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page': 'All Properties',
        'properties': page_obj,
    }

    return render(request, "user/all-property.html", context)

@login_required
def allStaff(request):
    staff = User.objects.filter(user_role="S")
    context = {
        'page': 'All Staff',
        'owners': staff,
    }
    return render(request, "user/all-staff.html", context)

# list all owners
@login_required
def allOwner(request):
    owners = User.objects.filter(user_role="H")
    paginator = Paginator(owners, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page': 'All Owners',
        'owners': page_obj,
    }
    return render(request, "user/all-owners.html", context)

def logout(request):
    auth.logout(request)
    return redirect("cvapp:login")

def assignProp(request):
    user1 = request.user
    users = User.objects.all()
    properties = HouseInfo.objects.all()
    context = {
        'page': "Assign Property",
        'users': users,
        'properties': properties
    }
    if request.method == "POST":
        try:
            user = User.objects.get(id=user1.id)
            client = request.POST.get("client")
            house = request.POST.get("house")

            ownership = UserHouse()
            ownership.user_id = User.objects.filter(email=client)[0]
            ownership.home_id = HouseInfo.objects.filter(title=house)[0]
            ownership.created_by = user
            ownership.save()
            context = {
                    'success': 'House successfully created',
                    'page':'Assign Property',
                    'users': users,
                    'properties': properties
                }
            render(request, "user/assign-property.html", context)

        except Exception as e:
            print(e)
            messages.error(request, 'Unauthorised access')
    return render(request, "user/assign-property.html", context)

##################
#Project Update
################

@login_required
def addPUpdate(request):
    user1 = request.user
    if request.method == 'POST':
        try:
            user = User.objects.get(id=user1.id)
            description = request.POST.get('description')
            img = request.FILES['feature_image']
            date = request.POST.get('date')
            print(request.POST)
            # ProjectUpdate.objects
            update = ProjectUpdate.objects.create(desription=description, update_images=img, update_date=date,added_by = user)
            update.save()
            # context = {
            #     'success': 'Project update successfully added',
            #     'page':'Add Update'
            # }
            messages.error(request, 'Project update successfully added')
            return redirect("cvapp:addPUpdate")
            # return render(request, "user/add-project-update.html", context)
        except ObjectDoesNotExist:
            messages.error(request, 'Unauthorised access')
            return redirect("cvapp:logout")
    context = {'page':'Add Update'}
    return render(request, "user/add-project-update.html", context)

@login_required
def allPUpdate(request):
    # context = {
    #     'page': 'Project Update',
    # }
    # return render(request, "user/all-project-update.html", context)

    p_updates = ProjectUpdate.objects.all()
    paginator = Paginator(p_updates, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page': 'All Project Update',
        'p_updates': page_obj,
    }
    return render(request, "user/all-project-update.html", context)