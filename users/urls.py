from django.urls import path, include
from .views import (UserView,
                    GetUser,
                    CreateUser,
                    LoginView,
                    WhoIsLoggedIn,
                    LogOutView)

urlpatterns = [
    path('all-users/', UserView.as_view()),
    path('get-user/', GetUser.as_view()),
    path('create-user/', CreateUser.as_view()),
    path('login/', LoginView.as_view()),
    path('logged-in/', WhoIsLoggedIn.as_view()),
    path('logout/', LogOutView.as_view())
]
