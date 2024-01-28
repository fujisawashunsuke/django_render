from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/<int:pk>/', views.UserProfileView.as_view(),name='user_profile'),
         #具体的なusernameが入る(accounts-views.pyでとってきた名前)
         #クラスに変えたときはas_viewをつける
    path('registration',views.registration_user,name='user_registration'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('profile_change/<int:pk>/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('profile_follow/<int:pk>/',views.users_follow,name='profile_follow'),
]