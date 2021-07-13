from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from mailing_campaign import views

urlpatterns = [
    path('mailing_campaign/', views.mailing_lists),
    path('start_campaign/', views.start_campaign),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)