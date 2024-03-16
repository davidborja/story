"""
URL configuration for storyChallenge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSet
from account.views import AccountViewSet
from accountType.views import AccountTypeViewSet
from transaction.views import TransactionViewSet
from template.views import TemplateViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"accounts", AccountViewSet)
router.register(r"transaction", TransactionViewSet)
router.register(r"account_types", AccountTypeViewSet)
router.register(r"template", TemplateViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
