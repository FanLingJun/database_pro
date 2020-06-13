from django.urls import path
from system import views
urlpatterns = [
    path('', views.login),
    # path('index/', views.index),
    path('login/', views.login),
    path('student_index/', views.student_index),
    path('teacher_index/', views.teacher_index),
    path('admin_index/', views.admin_index),
    path('student_coursetable/', views.student_coursetable),
    path('student_choose/', views.student_choose),
    path('student_drop/', views.student_drop),




]
