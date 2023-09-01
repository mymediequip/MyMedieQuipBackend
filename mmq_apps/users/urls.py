from django.contrib import admin
from django.urls import path

from . import views as users_views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', users_views.UserViewSet),
router.register(r'banner', users_views.BannerViewSet),
router.register(r'master', users_views.MasterViewSet)


urlpatterns = router.urls