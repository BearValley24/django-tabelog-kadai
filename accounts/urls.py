from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    #path('mypage/',views.mypagefunc,  name='mypage'),
    path('mypage/',views.Mypage.as_view(),  name='mypage'),
    #path('update/<int:pk>', views.Mypage.as_view(), name='update'),
    path('follow/<int:pk>', views.followShop, name='follow'),
    path('kanrisha/', views.CountMember.as_view(), name='kanrisha'),
    path('member_delete/<int:pk>', views.memberDelete.as_view(), name='MemberDelete'),
    path('member_update/<int:pk>',views.memberUpdate.as_view(), name='MemberUpdate'),
    path('kiyaku/', views.kiyaku.as_view(), name='kiyaku'),
    path('password_change/', views.passwordChange.as_view(), name='password_change'),
    path('password_change_done/', views.passwordChangeDone.as_view(), name='password_change_done'),
    path('signup_and_login',views.SignupAndLoginView.as_view(), name='signup_and_login'),
]
