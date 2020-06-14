from django.urls import path
from system import views
urlpatterns = [
    path('', views.login),
    # path('index/', views.index),
    path('login/', views.login),
    path('student_index/', views.student_index),
    path('teacher_index/', views.teacher_index),
    path('admin_index/', views.admin_index),

    # 学生端的跳转页面
    path('check_my_score/', views.check_my_score),
    path('check_my_table/', views.check_my_table),
    path('select_course/', views.select_course),
    path('delete_course/', views.delete_course),
    # 教师端的跳转页面
    path('check_my_course/', views.check_my_course),
    path('edit_score/', views.edit_score),
    path('submit_score/', views.submit_score),
    # 管理员端的跳转页面
    path('edit_student/', views.edit_student),
    path('submit_student/', views.submit_student),
    path('edit_course/', views.edit_course),
    path('submit_course/', views.submit_course),

]
