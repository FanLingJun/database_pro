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
    path('teacher_course/', views.teacher_course),
    path('teacher_edit_score/', views.teacher_edit_score),
    path('submit_score/', views.teacher_submit_score),
    # 管理员端的跳转页面
    path('admin_edit_user/', views.admin_edit_user),
    path('admin_submit_user/', views.admin_submit_user),
    path('admin_edit_course/', views.admin_edit_course),
    path('admin_submit_course/', views.admin_submit_course),
]
