from django.urls import path
from account.views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePassword

urlpatterns=[
    path("register/", UserRegistrationView.as_view(), name = "registration api" ),
    path("login/", UserLoginView.as_view(), name="login api"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("changepassword/", UserChangePassword.as_view(), name = "changepassword")
]