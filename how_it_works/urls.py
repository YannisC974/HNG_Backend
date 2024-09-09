from django.urls import path
from .views import HowItWorksView, FAQView
app_name = "how_it_works"

urlpatterns = [
    path("get-how-it-works/", HowItWorksView.as_view(), name="how-it-works"),
    path("get-faq/", FAQView.as_view(), name="faq"),
]
