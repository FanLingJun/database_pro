from django.urls import path
from system import views
urlpatterns = [
    path('', views.login),
    # path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('student_index/', views.student_index),
    path('teacher_index/', views.teacher_index),
    path('admin_index/', views.admin_index),

    # 学生端的跳转页面
    path('check_my_score/', views.check_my_score),
    path('check_my_table/', views.check_my_table),
    path('select_course/', views.select_course),
    path('delete_course/', views.delete_course),
    path('student_daily_post/', views.student_daily_post),
    # 教师端的跳转页面
    path('teacher_course/', views.teacher_course),
    path('teacher_edit_score/', views.teacher_edit_score),
    path('teacher_mod_score/', views.teacher_mod_score),
    path('teacher_daily_post/', views.teacher_daily_post),
    # 管理员端的跳转页面
    path('admin_edit_student/', views.admin_edit_student),
    path('admin_edit_teacher/', views.admin_edit_teacher),
    path('admin_mod_student/', views.admin_mod_student),
    path('admin_mod_teacher/', views.admin_mod_teacher),
    path('admin_edit_course/', views.admin_edit_course),
    path('admin_mod_course/', views.admin_mod_course),
    path('admin_daily_post/', views.admin_daily_post),
]

# handler404 = views.page_not_found
