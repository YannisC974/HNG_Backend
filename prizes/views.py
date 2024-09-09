from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from django.utils.translation import gettext as _
from django.db.models import Value, Sum, Case, When, Q, FloatField
from django.db.models.functions import Coalesce
from surveys.models import Survey

class DailyPrizeListView(generics.ListAPIView):
    queryset = DailyPrize.objects.all().order_by('-id')
    serializer_class = DailyPrizeSerializer
    permission_classes = (IsAuthenticated,)

# class MedalView(generics.ListAPIView):
#     serializer_class = MedalSerializer
#     permission_classes = (IsAuthenticated,)
#     def get_queryset(self):
#         total_completed = Survey.objects.filter(user=self.request.user).aggregate(
#             total = Coalesce(Sum("number_of_completed"), Value(0))
#         )["total"]
#         queryset = Medal.objects.annotate(total_completed_number=Value(total_completed)).annotate(
#             progression_rate = Case(
#                 When(Q(name=Value("Bronze")) & Q(total_completed_number__lte=37), then=total_completed/37*100),
#                 When(Q(name=Value("Silver")) & Q(total_completed_number__lte=37), then=Value(0)),
#                 When(Q(name=Value("Gold")) & Q(total_completed_number__lte=47), then=Value(0)),
#                 When(Q(name=Value("Silver")) & Q(total_completed_number__lte=47), then=total_completed/47*100),
#                 When(Q(name=Value("Gold")) & Q(total_completed_number__lte=63), then=total_completed/63*100),
#                 default=Value(100),
#                 output_field=FloatField()
#             )
#         )
#         return queryset
    
class DailyPrizesListView(generics.ListAPIView):
    serializer_class = DailyPrizeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        day = self.request.query_params.get('day', None)
        
        if day is None:
            return DailyPrize.objects.none()
        
        try:
            day_number = int(day)
            if day_number < 1:
                return DailyPrize.objects.none()
            
            return DailyPrize.objects.filter(day=f"{day_number}")
        except ValueError:
            return DailyPrize.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"detail": "No prizes found for the specified day."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class UserMedalListView(generics.ListAPIView):
    serializer_class = UserMedalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserMedal.objects.filter(user=self.request.user)

class UserBadgeListView(generics.ListAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)

class UserTrophyListView(generics.ListAPIView):
    serializer_class = UserTrophySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserTrophy.objects.filter(user=self.request.user)
