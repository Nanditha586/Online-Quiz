from django.urls import path
from . import views

urlpatterns = [

    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('register/',views.register_choice,name='register'),
    path('register/student/',views.student_register,name='student_register'),
    path('register/staff/',views.staff_register,name='staff_register'),
    path('profile/', views.student_profile, name='student_profile'),

]