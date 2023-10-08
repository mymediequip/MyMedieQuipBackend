from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.uid_base_model import UUIDBase
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
import json
# Create your models here.

class CustomUserManager(BaseUserManager):

    def _create_user(self, email,mobile, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        # now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        if not mobile:
            raise ValueError('The given mobile must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # mobile = self.normalize_email(email)
        # TODO: Fix Magic Numbers
        # By default user_type will be admin
        user.user_type = UserType.objects.get(user_type='Admin')
        user.status = 1
        # ----------- Hashing password is done in model --------#
        user.password = password
        user.mobile = mobile
        user.save(using=self._db)
        profile = Profile()
        profile.user_id = user.id
        profile.save(using=self._db)
        return user

#    def create_user(self, email, password=None,**extra_fields):
#        return self._create_user(email, password,**extra_fields)

    def create_superuser(self, email, mobile, password=None, **extra_fields):
        return self._create_user(email, mobile, password, **extra_fields)





class UserType(models.Model):
    user_type = models.CharField(_('User Type'), max_length=50)
    
    class Meta:
        db_table = 'mmq_usertype'
        app_label = 'users'
        


class User(UUIDBase, AbstractBaseUser):
    # first_name = models.CharField(verbose_name=_("First Name"), max_length=115, null=True, blank=True)
    # last_name = models.CharField(verbose_name=_("Last Name"), max_length=100, null=True, blank=True)
    mobile = models.CharField(verbose_name=_("Mobile Number"), max_length=15, null=False, blank=False,unique=True)
    DEVICE_CHOICE = (
        (1, "Website"),
        (2, "IOS"),
        (3, "Android")
    )
    device_type = models.CharField(
        _("Device Type"), choices=DEVICE_CHOICE, max_length=50, blank=True)
    is_verified = models.BooleanField(_("is verified "), default=False)
    email_verification_code = models.CharField(verbose_name=_("Email Verification"), max_length=45, null=True)
    username = models.CharField(verbose_name=_("Username"), max_length=50, null=True, blank=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=100, null=True, blank=True, unique=True)
    password = models.CharField(verbose_name=_("Password"), max_length=200, null=True, blank=True)
    user_type = models.ForeignKey(UserType, null=True,on_delete=models.SET_NULL)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Deleted; 0 for Not Deleted"), default=0)
    deleted_date = models.DateField(null=True,blank=True)
    activation_key = models.CharField(max_length=40, blank=True)
    reset_password_key = models.CharField(max_length=40, null=True)
    is_email_verified = models.BooleanField(_("is verified "), default=False)
    is_mobile_verified = models.BooleanField(_("is verified "), default=False)
    objects = CustomUserManager()
    update_password = True
    update_email = False
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email']
    # USERNAME_FIELD = 'mobile'
    last_login = models.DateTimeField(null=True,blank=True)
    # REQUIRED_FIELDS = ['email']

    usertypes = ArrayField(models.IntegerField(),default=list)

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def user_email(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return '{"id":"%s","email":"%s","user_type":"%s","status":"%s", "uid":"%s", "username":"%s"}' % (
            self.id, self.email, self.user_type, self.status, self.uid, self.username)


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return True

    @property
    def _disable_signals(self):
        return self.status

    # Overriding
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        # check if the row with this hash already exists.
        # try:
        #     if self.password and self.update_password and self.user_type.user_type != 'Admin':
        #         self.set_password(self.password)
        # except:
        if self.password and self.update_password:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)

    @property
    def is_superuser(self):
        if self.user_type_id==1:
            return True
        else:
            return False


    class Meta:
        db_table = 'mmq_user'


class Profile(UUIDBase):
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    first_name = models.CharField(_("First Name"), max_length=100, null=True, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=100, null=True, blank=True)
    gstin = models.CharField(_("GSTIN"), max_length=100, null=True, blank=True) 
    pan_no = models.CharField(_("Pan No"), max_length=100, null=True, blank=True) 
    describe = models.TextField(_("Describe"), null=True, blank=True) 
    profile_image = models.CharField(_("GSTIN"), max_length=250, null=True, blank=True) 
    dob = models.DateField(_("DOB"), null=True)
    gender = models.CharField(_("Gender"), null=True, max_length=10,blank=True)
    location = models.CharField(_("location"), max_length=200, null=True,blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=50, null=True,blank=True)
    user = models.OneToOneField(User, null=True, related_name="user_profile", on_delete=models.CASCADE, unique=True)
    image = models.ImageField(upload_to = "upload/profile_image/",null=True,blank=True)
    latitude = models.CharField(verbose_name=_("Latitude"), max_length=20, blank=True, null=True)
    longitude = models.CharField(verbose_name=_("Longitude"), max_length=20, blank=True, null=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)

    class Meta:
        db_table = 'mmq_profile'



class Address(UUIDBase):
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    mobile = models.CharField(_("mobile"), max_length=14, null=True, blank=True)
    alternate_mobile = models.CharField(_("alternate_mobile"), max_length=14, null=True, blank=True)
    location = models.CharField(_("location"), max_length=250, null=True,blank=True)
    address = models.TextField(_("address"),null=True,blank=True)
    state = models.CharField(_("state"), max_length=100, null=True,blank=True)
    city = models.CharField(_("city"), max_length=100, null=True,blank=True)
    zip_code = models.CharField(_("Zip Code"), max_length=50, null=True,blank=True)
    landmark = models.CharField(_("city"), max_length=250, null=True,blank=True)
    user = models.ForeignKey(User, to_field="uid", null=True, related_name="user_address", on_delete=models.CASCADE)
    latitude = models.CharField(verbose_name=_("Latitude"), max_length=20, blank=True, null=True)
    longitude = models.CharField(verbose_name=_("Longitude"), max_length=20, blank=True, null=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    # meta_data = models.JsonField(verbose_name=_("Meta data"), max_length=20, blank=True, null=True)
    is_default = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Yes; 0 for No"), default=0)

    class Meta:
        db_table = 'mmq_address'


class Otp(models.Model):
    mobile = models.CharField(max_length=13,null=True,blank=True,unique=True)
    email = models.EmailField(max_length=255,null=True,blank=True,unique=True)
    otp_generated_time = models.DateTimeField(null=True,blank=True, auto_now=False)
    counter = models.IntegerField(default=0, blank=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'mmq_otp'



class Banner(UUIDBase):
    title = models.CharField(max_length=200,null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to = "upload/banner/",null=True,blank=True)
    banner_image = models.CharField(_("Image"), max_length=250, null=True, blank=True) 
    description = models.TextField(verbose_name="description",null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_banner'


class Expertise(UUIDBase):
    name = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to = "upload/expertise/",null=True,blank=True)
    expertise_image = models.CharField(_("Image"), max_length=250, null=True, blank=True) 
    description = models.TextField(verbose_name="description",null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_expertise'


class OurClient(UUIDBase):
    name = models.CharField(max_length=200,null=True,blank=True)
    image = models.ImageField(upload_to = "upload/expertise/",null=True,blank=True)
    client_image = models.CharField(_("Image"), max_length=250, null=True, blank=True) 
    description = models.TextField(verbose_name="description",null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_our_client'



class PaymentOption(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)

    class Meta:
        db_table = 'mmq_payment_option'