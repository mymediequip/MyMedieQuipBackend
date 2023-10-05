from django.contrib import admin
from django.urls import path

from . import views as users_views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', users_views.ProductViewSet),
router.register(r'category', users_views.CategoryViewSet),
router.register(r'equipment', users_views.EquipmentViewSet),
router.register(r'speciality', users_views.SpecialityViewSet)
router.register(r'order', users_views.OrderViewSet)


urlpatterns = router.urls