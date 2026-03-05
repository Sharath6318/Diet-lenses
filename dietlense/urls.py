"""
URL configuration for dietlense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from diet_app.views import RegisterView, UserprofileCreateView, UserProfileDetailView, UserRetriveUpdateView, UserRetriveView, FoodLogCreateListView, FoodLogUpdateRetriveDestroyview, SummaryView, GetDietPlan

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view()),
    path('retriveuser/<int:pk>/',UserRetriveView.as_view()),
    path('token/', ObtainAuthToken.as_view()),
    path('profile/', UserprofileCreateView.as_view()),
    path('profiledetail/', UserProfileDetailView.as_view()),
    path('profileretrive/<int:pk>/', UserRetriveUpdateView.as_view()),
    path('foodlog/', FoodLogCreateListView.as_view()),
    path('foodlog/<int:pk>/', FoodLogUpdateRetriveDestroyview.as_view()),
    path('summary/', SummaryView.as_view()),
    path('diet-plan/', GetDietPlan.as_view()),
]
