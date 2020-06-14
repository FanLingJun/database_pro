from django.shortcuts import render, redirect
from django.contrib import messages
from system import models # 引入对象模型
from django.db import connection

# 在这个视图文件中，定义方法
# 编写函数逻辑判断，应对响应
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        number = request.POST.get('number')
        pswd = request.POST.get('pswd')
        if number and pswd:
            # 先与数据库字段进行比对,逐个比对
            # filter就是select语句，匹配查找
            student = models.student.objects.filter(xh=number).filter(pwd=pswd)
            teacher = models.teacher.objects.filter(gh=number).filter(pwd=pswd)
            admin = models.admin.objects.filter(gh=number).filter(pwd=pswd)
            if student: # 在学生表里找到了登录者的信息
                request.session['number'] = number
                request.session['islogin'] = True
                return redirect('/student_index/')
            elif teacher:
                request.session['number'] = number
                request.session['islogin'] = True
                return redirect('/teacher_index/')
            elif admin:
                request.session['number'] = number
                request.session['islogin'] = True
                return redirect('/admin_index/')
            else:
                # 密码错误
                messages.success(request, "Error!")
                return render(request, 'login.html')
        # 账号或密码不存在
        else:
            messages.success(request, "Error!")
            return render(request, 'login.html')


def student_index(request):
    number = request.session.get('number')
    print(number,type(number))
    cursor = connection.cursor()
    # 查询操作
    cursor.execute("select xh,xm,xb,jg,sjhm,mc from system_student,system_department "
                   "where system_student.yxh_id = system_department.yxh and system_student.xh = %s",[number])
    student_info = cursor.fetchall()  # 读取所有
    print(student_info,type(student_info))
    # student_info = [('0101', '陈迪茂', '男', '副教授', '计算机学院')]
    student_info = student_info[0]
    print(student_info)
    return render(request, 'student_index.html', context={'xh': student_info[0],'xm':student_info[1],
                                                          'xb':student_info[2],'jg':student_info[3],
                                                          'sjhm':student_info[4],'mc':student_info[5]})


def teacher_index(request):
    number = request.session.get('number')
    print(number,type(number))
    cursor = connection.cursor()
    # 查询操作
    cursor.execute("select gh,xm,xb,xl,mc from system_teacher,system_department "
                   "where system_teacher.yxh_id = system_department.yxh and system_teacher.gh = %s",[number])
    teacher_info = cursor.fetchall()  # 读取所有
    print(teacher_info,type(teacher_info))
    # teacher_info = [('0101', '陈迪茂', '男', '副教授', '计算机学院')]
    teacher_info = teacher_info[0]
    print(teacher_info)
    return render(request, 'teacher_index.html', context={'gh': teacher_info[0],'xm':teacher_info[1],
                                                          'xb':teacher_info[2],'xl':teacher_info[3],
                                                          'mc':teacher_info[4]})

def admin_index(request):
  number = request.session.get('number')
  admin = models.admin.objects.filter(gh=number)
  return render(request, 'admin_index.html', context={'gh': number, 'xm': admin[0].xm, 'xb': admin[0].xb
                                                        })

def check_my_score(request):
  number = request.session.get('number')
  cursor = connection.cursor()
  cursor.execute("select kh,km,xf,zpcj from system_course,system_e_table where system_e_table.kh_id = system_course.kh and xh_id = %s and zpcj is not null", [number])
  all_scores = cursor.fetchall()  # 读取所有
  # print(all_scores, type(all_scores))
  all_s = []
  for item in all_scores:
    scores = dict() # 注意这里一定要放在循环之内！！！！！！！！！！！！
    scores['kh'] = item[0]
    scores['km'] = item[1]
    scores['xf'] = item[2]
    scores['zpcj'] = item[3]
    if int(item[3]) > 89:
      scores['gpa'] = 4.0
    elif int(item[3]) > 84:
      scores['gpa'] = 3.7
    elif int(item[3]) > 79:
      scores['gpa'] = 3.0
    elif int(item[3]) > 69:
      scores['gpa'] = 2.0
    elif int(item[3]) > 59:
      scores['gpa'] = 1.0
    else: scores['gpa'] = 0.0
    all_s.append(scores)
  return render(request, 'check_my_score.html', context={'xh': number,'scores':all_s})

def check_my_table(request):
  # 判断逻辑，根据e表，如果匹配到学号且总评成绩为null则为这个学期选的课
  number = request.session.get('number')
  print("===========",number)
  student = models.student.objects.filter(xh=number)
  elect_course = models.e_table.objects.all().filter(xh=number).filter(zpcj__isnull=True)
  print(elect_course)
  num_list = []
  for every in elect_course:
    num = getattr(every,'kh')
    num = getattr(num, 'kh')
    num_list.append(num)
  print(num_list)
  all_course = models.course.objects.filter(kh__in=num_list)
  print(all_course)
  return render(request, 'check_my_table.html', context={'xm':student[0].xm,'all_course':all_course})


def select_course(request):
  cursor = connection.cursor()
  cursor.execute("select distinct xq,km,xf,kh_id,xm,gh,sksj "
                  "from system_open_course,system_teacher,system_course "
                  "where system_open_course.gh_id = system_teacher.gh "
                  "and system_open_course.kh_id = system_course.kh")
  open_course = cursor.fetchall()
  print(open_course)
  all = []
  for item in open_course:
    course = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
    course['xq'] = item[0]
    course['km'] = item[1]
    course['xf'] = item[2]
    course['kh_id'] = item[3]
    course['xm'] = item[4]
    course['gh'] = item[5]
    course['sksj'] = item[6]
    all.append(course)
  course_id = request.POST.get('course_id')
  print(course_id)
  teacher_id = request.POST.get('teacher_id')
  print(teacher_id)


  return render(request, 'select_course.html', context={'open_course': all})


def delete_course(request):
  return render(request, 'delete_course.html')

def check_my_course(request):
  return render(request, 'check_my_course.html')

def edit_score(request):
  return render(request,'edit_score.html')

def submit_score(request):
  return render(request,'submit_score.html')

def edit_student(request):
  return render(request,'edit_student.html')

def submit_student(request):
  return render(request,'submit_student.html')

def edit_course(request):
  return render(request,'edit_course.html')

def submit_course(request):
  return render(request,'submit_course.html')

