from django.urls import path

from aqua_airdrop_checker.airdrop.api import AccountCheckView

urlpatterns = [
    path('account-check/', AccountCheckView.as_view()),
]
