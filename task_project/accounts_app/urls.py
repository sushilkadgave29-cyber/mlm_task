from django.urls import path
from .views import register, downline_view, dashboard, user_login, user_logout

app_name = 'mlm'  

urlpatterns = [
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('downline/', downline_view, name='downline'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]


