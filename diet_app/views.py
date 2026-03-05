from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum

from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from diet_app.serializers import UserSerializer, UserProfileSerializer, FoodLogSerializer
from diet_app.utility_fun import daily_calorie_consumaption
from diet_app.models import UserProfile, User, FoodLog
from diet_app.permissions import IsOwner, HasUserProfile
from diet_app.get_diet_plan import generate_kerala_diet_plan


class RegisterView(CreateAPIView):

    serializer_class = UserSerializer
    

class UserRetriveView(RetrieveAPIView):


    serializer_class = UserSerializer

    queryset = User.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner]



class UserprofileCreateView(CreateAPIView): 

    serializer_class = UserProfileSerializer

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):

        validated_data = serializer.validated_data

        cal = daily_calorie_consumaption(height = validated_data.get('height'),
                                        weight = validated_data.get('weight'),
                                        age = validated_data.get("age"),
                                        gender=validated_data.get('gender'),
                                        activity_leval=float(validated_data.get('activity_level', 1.2)) 
                                        )
        
        serializer.save(owner = self.request.user, bmr = cal)


class UserProfileDetailView(ListAPIView):
    
    serializer_class = UserProfileSerializer

    queryset = UserProfile.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

class UserRetriveUpdateView(UpdateAPIView, RetrieveAPIView):

    serializer_class = UserProfileSerializer

    queryset = UserProfile.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [HasUserProfile,IsOwner]

class FoodLogCreateListView(CreateAPIView, ListAPIView):

    serializer_class = FoodLogSerializer

    queryset = FoodLog.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [HasUserProfile, permissions.IsAuthenticated]

    def perform_create(self, serializer):

        return serializer.save(owner = self.request.user)
    
    def get_queryset(self):

        return FoodLog.objects.filter(owner = self.request.user)
    

class FoodLogUpdateRetriveDestroyview(RetrieveAPIView, UpdateAPIView, DestroyAPIView):

    serializer_class = FoodLogSerializer

    queryset = FoodLog.objects.all()

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [IsOwner]

class SummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated, HasUserProfile]

    def get(self, request, *args, **kwargs):

        cur_date = timezone.now().date()

        qs = FoodLog.objects.filter(owner = request.user, created_at__date = cur_date)

        total_consumed= qs.values("calories").aggregate(total=Sum("calories"))

        meal_type_summary = qs.values("meal_type").annotate(total = Sum('calories'))

        print(meal_type_summary)

        context  = {
            'Daily_target' : request.user.profile.bmr,
            "total_consumed":total_consumed.get("total",0),
            "balance":request.user.profile.bmr - total_consumed.get("total",0)
        }

        return Response(data=context)


class GetDietPlan(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated, HasUserProfile]


    def post(self, request, *args, **kwargs):

        goal = request.data.get("goal")

        age = request.user.profile.age

        weight = request.user.profile.weight

        gender = request.user.profile.gender

        target_weight = request.data.get('target_weight')

        duration = request.data.get("duration")

        print(goal, age, weight, gender, target_weight, duration)

        result = generate_kerala_diet_plan(goal=goal,
                                           age=age,
                                           weight=weight,
                                           gender=gender,
                                           target_weight=weight,
                                           duration=duration,
                                           )

        return Response(data=result)


