from django.db import models
from django.utils.translation import gettext_lazy as _
from common.uid_base_model import UUIDBase
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from mmq_apps.users.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'mmq_category'


class Speciality(UUIDBase):
    name = models.CharField(max_length=200,null=True,blank=True,unique=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_speciality'


class Equipment(UUIDBase):
    name = models.CharField(max_length=200,null=True,blank=True, unique=True)
    category = ArrayField(models.PositiveIntegerField(),default=list)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_equipment'


class Product(UUIDBase):
    user = models.ForeignKey(User,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True)
    speciality = models.ForeignKey(Speciality,to_field="uid", verbose_name=_("Speciality"),on_delete=models.DO_NOTHING,null=True,blank=True)
    equipment = models.ForeignKey(Equipment,to_field="uid", verbose_name=_("Equipment"),on_delete=models.DO_NOTHING,null=True,blank=True)
    # name = models.CharField(max_length=200,null=True,blank=True)
    # price = models.DecimalField(max_digits=40,decimal_places=4,default=0)
    POST_TYPE = (
        (1, "USED"),
        (2, "NEW"),
        (3, "SPARE & ACCESSORIES"),
        (4, "SERVICES")
    )
    post_type = models.CharField(
        _("Condition"), choices=POST_TYPE, max_length=50, blank=True)
    category = models.ForeignKey(Category, verbose_name=_("Category"),on_delete=models.DO_NOTHING,null=True,blank=True)
    speciality_name = models.CharField(max_length=200,null=True,blank=True)
    equip_name = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(verbose_name="description",null=True,blank=True)
    asking_price = models.DecimalField(max_digits=40,decimal_places=4,default=0)
    EQUIP_CONDITION = (
        (1, "Good"),
        (2, "Excellent"),
        (3, "As Good as New")
    )
    equip_condition = models.CharField(
        _("Condition"), choices=EQUIP_CONDITION, max_length=50, blank=True)
    NEGOTIABLE = (
        (1, "Negotiable"),
        (2, "Slightly Negotiable"),
        (3, "Non-Negotiable")
    )
    negotiable_type = models.CharField(
        _("negotiable Type"), choices=NEGOTIABLE, max_length=50, blank=True)
    year = models.PositiveIntegerField(verbose_name=_("Manufacturing/ Purchase Year"),default=0)
    brand = models.CharField(max_length=200,null=True,blank=True)
    model = models.CharField(max_length=200,null=True,blank=True)
    warranty = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Yes; 0 for No"), default=0)
    existing_amc = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Yes; 0 for No"), default=0)
    other_details = models.TextField(verbose_name="other_details",null=True,blank=True)
    shipping_form = models.CharField(max_length=200,null=True,blank=True)
    posted = models.DateField(_("DOB"), null=True)
    visit = models.CharField(max_length=200,null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_product'



# class ProductDetails(UUIDBase):
#     user = models.ForeignKey(User,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True)
#     POST_TYPE = (
#         (1, "USED"),
#         (2, "NEW"),
#         (3, "SPARE & ACCESSORIES"),
#         (4, "SERVICES")
#     )
#     post_type = models.CharField(
#         _("Condition"), choices=POST_TYPE, max_length=50, blank=True)
#     category = models.ForeignKey(Category, verbose_name=_("Category"),on_delete=models.DO_NOTHING,null=True,blank=True)
#     product = models.OneToOneField(Product,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True,unique=True)
#     equip_name = models.CharField(max_length=200,null=True,blank=True)
#     description = models.TextField(verbose_name="description",null=True,blank=True)
#     asking_price = models.DecimalField(max_digits=40,decimal_places=4,default=0)
#     EQUIP_CONDITION = (
#         (1, "Good"),
#         (2, "Excellent"),
#         (3, "As Good as New")
#     )
#     equip_condition = models.CharField(
#         _("Condition"), choices=EQUIP_CONDITION, max_length=50, blank=True)
#     NEGOTIABLE = (
#         (1, "Negotiable"),
#         (2, "Slightly Negotiable"),
#         (3, "Non-Negotiable")
#     )
#     negotiable_type = models.CharField(
#         _("negotiable Type"), choices=NEGOTIABLE, max_length=50, blank=True)
#     brand = models.CharField(max_length=200,null=True,blank=True)
#     model = models.CharField(max_length=200,null=True,blank=True)
#     condition = models.CharField(max_length=200,null=True,blank=True)
#     warrenty = models.CharField(max_length=200,null=True,blank=True)
#     shipping_form = models.CharField(max_length=200,null=True,blank=True)
#     posted = models.DateField(_("DOB"), null=True)
#     visit = models.CharField(max_length=200,null=True,blank=True)
#     status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
#     is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

#     class Meta:
#         db_table = 'mmq_product_details'


class ProductImage(UUIDBase):
    product = models.ForeignKey(Product,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    # image = models.ImageField(upload_to = "upload/profile_image/",null=True,blank=True)
    p_image = models.CharField(max_length=250,null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_product_image'


class ProductVideo(UUIDBase):
    product = models.ForeignKey(Product,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    link = models.CharField(max_length=200,null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_product_video'