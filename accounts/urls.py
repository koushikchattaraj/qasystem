from django.urls import path
from . import views


app_name= 'accounts'

urlpatterns = [

    #  path('/')

    path('api/login/', views.UserLoginView.as_view(), name="sign_in_api"),
    path('api/user/', views.UserView.as_view(), name="user_api"),
    path('sign_in/', views.LoginView.as_view(), name="sign_in"),
    path('api/sign_up/', views.UserCreateView.as_view(), name="sign_up_api"),
    path('sign_up/', views.CreateView.as_view(), name="sign_up"),
    path('', views.IndexView.as_view(), name="home"),
    path('account/', views.AccountView.as_view(), name="account"),
    path('drive/', views.DriveView.as_view(), name="drive"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('trash/', views.TrashView.as_view(), name="trash"),
    path('starred/', views.StarredView.as_view(), name="starred"),
    path('recent/', views.RecentView.as_view(), name="recent"),
    path('account_verification/<user>/<token>', views.AccountVerification.as_view(), name="AccountVerification"),
]