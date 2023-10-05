from django.db import models
from django.utils.translation import gettext_lazy as _
from common.uid_base_model import UUIDBase
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from mmq_apps.users.models import User,PaymentOption
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
    category = ArrayField(models.CharField(max_length=200,null=True,blank=True),default=list)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_equipment'


class Product(UUIDBase):
    user = models.ForeignKey(User,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True)
    speciality = models.ForeignKey(Speciality,to_field="uid", verbose_name=_("Speciality"),on_delete=models.DO_NOTHING,null=True,blank=True)
    # equipment = models.ForeignKey(Equipment,to_field="uid", verbose_name=_("Equipment"),on_delete=models.DO_NOTHING,null=True,blank=True)
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
    # category = models.ForeignKey(Category, verbose_name=_("Category"),on_delete=models.DO_NOTHING,null=True,blank=True)
    # category_list = models.ManyToManyField(Category)
    category_list = models.CharField(max_length=200,null=True, blank=True)
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
    address = models.TextField(null=True,blank=True)
    latitude = models.CharField(max_length=200,null=True,blank=True)
    longitude = models.CharField(max_length=200,null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)
    PRODUCT_STATUS = (
        (1, "OPEN"),
        (2, "LOCK")
    )
    product_status = models.CharField(
        _("product_status"), choices=PRODUCT_STATUS, max_length=50, blank=True,default=1)

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
    # title = models.CharField(max_length=200,null=True,blank=True)
    # image = models.ImageField(upload_to = "upload/profile_image/",null=True,blank=True)
    p_image = models.CharField(max_length=250,null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_product_image'


class ProductVideo(UUIDBase):
    product = models.ForeignKey(Product,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True)
    # title = models.CharField(max_length=200,null=True,blank=True)
    # link = models.CharField(max_length=200,null=True,blank=True)
    video = models.CharField(max_length=250,null=True,blank=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    is_deleted = models.PositiveSmallIntegerField(verbose_name=_("Deleted: 1 for Active; 0 for Not Deleted"), default=0)

    class Meta:
        db_table = 'mmq_product_video'



class ScheduleMeeting(UUIDBase):
    buyer= models.ForeignKey(User,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True,related_name="buyer")
    seller = models.ForeignKey(User,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True,related_name="seller")
    product = models.ForeignKey(Product,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True,related_name="meeting_product")
    title=models.CharField(max_length=200,null=True,blank=True)
    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    duration=models.DurationField()
    remind_me=models.TimeField(blank=True,null=True)
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    
    class Meta:
        db_table='mmq_schedule_meeting'




class Order(UUIDBase):
    buyer= models.ForeignKey(User,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True,related_name="order_buyer")
    seller = models.ForeignKey(User,to_field="uid", verbose_name=_("User"),on_delete=models.DO_NOTHING,null=True,blank=True,related_name="orderseller")
    product = models.ForeignKey(Product,to_field="uid", verbose_name=_("Product"),on_delete=models.DO_NOTHING,null=True,blank=True,related_name="order_product")
    asking_price = models.DecimalField(max_digits=40,decimal_places=4,default=0)
    sub_total = models.DecimalField(max_digits=40,decimal_places=4,default=0)
    total = models.DecimalField(max_digits=40,decimal_places=4,default=0)
    payment_type = models.ForeignKey(PaymentOption,verbose_name=_("Payment Type"),on_delete=models.DO_NOTHING,null=True,blank=True)
    PAYMENT_STATUS = (
        (1, "Pending"),
        (2, "Partial"),
        (3, "Completed")
    )
    payment_status = models.CharField(_("payment status"), choices=PAYMENT_STATUS, max_length=50, blank=True,default=1)

    ORDER_STATUS = (
        (1, "Pending"),
        (2, "InProcess"),
        (3, "Completed"),
        (4, "Canceled")
    )
    order_status = models.CharField(_("payment status"), choices=ORDER_STATUS, max_length=50, blank=True,default=1)    
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    inspection_status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for True; 0 for False"), default=0)
    
    class Meta:
        db_table='mmq_order'



class Payment(UUIDBase):
    order= models.ForeignKey(Order,to_field="uid", verbose_name=_("Order"),on_delete=models.DO_NOTHING,null=True,blank=True,related_name="payment_order")
    sub_total = models.DecimalField(max_digits=40,decimal_places=4,default=0)
    total = models.DecimalField(max_digits=40,decimal_places=4,default=0)
    payment_type = models.ForeignKey(PaymentOption,verbose_name=_("Payment Type"),on_delete=models.DO_NOTHING,null=True,blank=True)
    PAYMENT_STATUS = (
        (1, "Pending"),
        (2, "Partial"),
        (3, "Completed")
    )
    payment_status = models.CharField(_("payment status"), choices=PAYMENT_STATUS, max_length=50, blank=True)
    ORDER_TYPE = (
        (1, "Order"),
        (2, "Inspection")
    )
    order_type = models.CharField(_("Order Type"), choices=ORDER_TYPE, max_length=50, blank=True,default=1)
   
    status = models.PositiveSmallIntegerField(verbose_name=_("Status: 1 for Active; 0 for InActive"), default=1)
    
    class Meta:
        db_table='mmq_payment'