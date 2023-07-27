from django.contrib import admin
from django.urls import path

from . import views as users_views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'api/v1.0/users', users_views.UserViewSet)


urlpatterns = router.urls