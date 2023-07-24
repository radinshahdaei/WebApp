from django.urls import path, include
from .views import (UserView,
                    GetUser,
                    CreateUser,
                    CheckPassword)

urlpatterns = [
    path('all-users/', UserView.as_view()),
    path('get-user/', GetUser.as_view()),
    path('create-user/', CreateUser.as_view()),
    path('check-password/', CheckPassword.as_view())
]
