from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from mailing_campaign import views

urlpatterns = [
    path("mailing_campaign/", views.mailing_lists),
    path("start_campaign/", views.start_campaign),
]

urlpatterns = format_suffix_patterns(urlpatterns)
