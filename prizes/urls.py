from django.urls import path
from .views import *
app_name = "prizes"
urlpatterns = [
    path("daily-prize-list/", DailyPrizeListView.as_view(), name="daily-prize-list"),
    path("get-medal-list/", UserMedalListView.as_view(), name="medal-list"),
    path("get-badge-list/", UserBadgeListView.as_view(), name="badge-list"),
    path("get-trophy-list/", UserTrophyListView.as_view(), name="badge-list"),
    path("daily-prize-by-day/", DailyPrizesListView.as_view(), name="daily-prize-list-by-day"),
]
