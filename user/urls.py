from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.allUsers , name = 'AllUsers'),
    path('signup/', views.signUp , name = 'SignUp'),
    path('login/', views.loginUser , name = 'LoginUser'),
    path('logout/', views.logoutUser , name = 'LogoutUser'),
    path('detail/<int:id>', views.userDetail , name = 'UserDetail'),
    path('detail/edit/<int:id>/<str:field>', views.editUserDetail , name = 'EditUserDetail'),
    path('delete/<int:id>', views.deleteUser , name = 'DeleteUser'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profiles/', views.ProfileApi.as_view()),
]
