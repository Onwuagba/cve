from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils import timezone
from django.core.validators import RegexValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField
import uuid

# Create your models here.

class MyManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        
        if not email:
            raise ValueError("Email is required")

        user = self.model(
            email = self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=150, null=False, blank=False, verbose_name='first name')
    last_name = models.CharField(max_length=150, null=False, blank=False, verbose_name='last name')
    password = models.CharField(max_length=128, null=False, blank=False, verbose_name='password')
    phone_regex = RegexValidator(regex=r'^(\+\d{1,3}[- ]?)?\d{10}$', message="Phone number not validated.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True) 
    default_pwd = models.BooleanField(default=True) #checks that the newly created user does not have the first password set
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False)
    regToken = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='token') ##for new registrations
    # profile_photo = models.ImageField(upload_to='img/profilePhoto/', verbose_name="profile photo", blank=True, null=True, unique=True)
    USER_ROLE = [
        ('S', 'Staff'), 
        ('H', 'Home Owner'),
    ]
    user_role = models.CharField(max_length=2, choices=USER_ROLE, default='H')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyManager()

    def __str__(self):
        return f'{self.first_name}'

class HouseInfo(models.Model):
    house_id = models.AutoField(primary_key=True, verbose_name='House ID')
    street_info = models.CharField(max_length=80, unique=True)
    cost = models.DecimalField(max_digits=15, decimal_places=2)
    desription = models.TextField(null=False, blank=False)
    images = ArrayField(models.ImageField(upload_to='img/housePhotos/', unique=True), blank=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    readonly_fields = [
        'date_updated', 'date_created'
    ]

    def __str__(self):
        return f"{self.house_id}"

#pivot table for users and house
class UserHouse(models.Model):
    user_id = models.ForeignKey(User, related_name='home_owner', on_delete=models.CASCADE)
    home_id = models.ForeignKey(HouseInfo, related_name='house_info', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='staff_approver', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    readonly_fields = [
        'date_updated', 'date_created'
    ]

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'home_id'], name='unique_homeOwner')
        ]

class Payment(models.Model):
    pay_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='payment id')
    user_id = models.ForeignKey(User, related_name='homePay_owner', on_delete=models.CASCADE)
    home_id = models.ForeignKey(HouseInfo, related_name='housePay_info', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    payment_proof = models.ImageField(upload_to='img/paymentProof/', verbose_name="proof of payment", unique=True)
    #status of payment. A staff has to manually change the status
    STATUS = [
        ('D', 'Declined'), 
        ('P', 'Pending'), 
        ('A', 'Approved'),
    ]
    payment_status = models.CharField(max_length=2, choices=STATUS, default='P')
    approved_by = models.ForeignKey(User, related_name='approver', on_delete=models.CASCADE)
    date_paid = models.DateField()
    date_updated = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    readonly_fields = [
        'date_updated'
    ]

    def __str__(self):
        return f"{self.pay_id}"