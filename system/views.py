from django.shortcuts import render, redirect
from django.contrib import messages
from system import models # 引入对象模型
from django.db import connection


def page_not_found(request, **kwargs):
  return render(request,'error.html')

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
    number = request.session.get('number')
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
    if request.method == 'GET':
      return render(request, 'select_course.html', context={'open_course': all})
    else:
      course_id = request.POST.get('course_id')
      print(course_id)
      teacher_id = request.POST.get('teacher_id')
      print(teacher_id)
      models.e_table.objects.create(xq='2019-2020春季', xh_id=number, kh_id=course_id, gh_id=teacher_id)
      # messages.success(request, '选课成功啦~~~~~~')
      return redirect('/select_course.html/')

def delete_course(request):
    number = request.session.get('number')
    cursor = connection.cursor()
    cursor.execute(
      "select kh,km,gh,xm,xf "
      "from system_course,system_e_table,system_teacher "
      "where system_e_table.kh_id = system_course.kh "
      "and system_e_table.gh_id = system_teacher.gh "
      "and xh_id = %s and zpcj is not null",
      [number])
    all_course = cursor.fetchall()  # 读取所有
    # print(all_scores, type(all_scores))
    selected_c = []
    for item in all_course:
      s_c = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
      s_c['kh'] = item[0]
      s_c['km'] = item[1]
      s_c['gh'] = item[2]
      s_c['xm'] = item[3]
      s_c['xf'] = item[4]
      selected_c.append(s_c)
    if request.method == 'GET':
      return render(request, 'delete_course.html', context={'selected_course': selected_c})
    else:
      course_id = request.POST.get('course_id')
      # 先选中，再删除
      models.e_table.objects.filter(xh_id=number, kh_id=course_id).delete()
      # messages.success(request, '退课成功啦~~~~~~')
      return redirect('/delete_course.html/')

def teacher_course(request):
  cursor = connection.cursor()
  cursor.execute(
    "select distinct kh,km,xf from system_course,system_e_table "
    "where system_e_table.kh_id = system_course.kh"
    " and zpcj is null")
  all_info = cursor.fetchall()  # 读取所有
  courses_data = []
  for item in all_info:
    temp = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
    temp['kh'] = item[0]
    temp['km'] = item[1]
    temp['xf'] = item[2]
    courses_data.append(temp)
  return render(request, 'teacher_course.html',context={'courses_data':courses_data})

def teacher_edit_score(request):
  number = request.session.get('number')
  cursor = connection.cursor()
  # 查询这个老师教的学生的成绩
  cursor.execute(
    "select distinct kh,km,xh,xm,pscj,kscj,zpcj from system_course,system_e_table,system_student "
    "where system_e_table.kh_id = system_course.kh and system_student.xh = system_e_table.xh_id"
    " and zpcj is null and system_e_table.gh_id = %s", [number])
  all_info = cursor.fetchall()  # 读取所有
  teacher_student_data = []
  for item in all_info:
    temp = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
    temp['kh'] = item[0]
    temp['km'] = item[1]
    temp['xh'] = item[2]
    temp['xm'] = item[3]
    temp['pscj'] = item[4]
    temp['kscj'] = item[5]
    temp['zpcj'] = item[6]
    teacher_student_data.append(temp)
  print(teacher_student_data)
  return render(request, 'teacher_edit_score.html',context={'student_data':teacher_student_data})

def teacher_mod_score(request):
  # 教师提交学生成绩
  number = request.session.get('number')
  kh = request.GET.get('kh')
  xh = request.GET.get('xh')
  print("course id and student id",kh,xh)
  km = models.course.objects.filter(kh=kh)
  km = km[0].km
  xm = models.student.objects.filter(xh=xh)
  xm = xm[0].xm
  print(km,xm)
  pscj = request.POST.get('pscj')
  kscj = request.POST.get('kscj')
  zpcj = request.POST.get('zpcj')
  print("the input is:",pscj,kscj,zpcj)
  if request.method == 'GET':
    return render(request, 'teacher_mod_score.html',context={'xh':xh,'xm':xm,'km':km})
  else:
    # 先找到对应数据，再update
    models.e_table.objects.filter(gh_id=number, kh_id=kh, xh_id=xh).update(pscj=pscj, kscj=kscj, zpcj=zpcj)
    return render(request, 'teacher_mod_score.html', context={'xh': xh, 'xm': xm, 'km': km})

def admin_edit_user(request):
  all_student = models.student.objects.all()
  all_teacher = models.student.objects.all()
  if request.method == 'GET':
    return render(request,'admin_edit_user.html',context={'all_student':all_student,'all_teacher':all_teacher})
  else:
    xh = request.POST.get('xh')
    xm = request.POST.get('xm')
    jg = request.POST.get('jg')
    sjhm = request.POST.get('sjhm')
    # 这里还需要三个字段！
    models.student.objects.create(xh=xh, xm=xm, jg=jg,csrq='1999-2-28',xb='女', sjhm=sjhm,pwd='student',yxh_id='01')
    return render(request, 'admin_edit_user.html', context={'all_student': all_student, 'all_teacher': all_teacher})

def admin_mod_user(request):
  xh = request.GET.get('xh')
  isdel = request.GET.get('isdel')
  if (isdel == 1):
    models.student.objects.filter(xh=xh).delete()
    return redirect('/admin_mod_user.html/')
  else:
    student_info = models.student.objects.filter(xh=xh)
    department = models.department.objects.filter(yxh = student_info.yxh)
    department = department.mc
    xm = request.POST.get('xm')
    xb = request.POST.get('xb')
    sjhm = request.POST.get('sjhm')
    jg = request.POST.get('jg')
    yxh = request.POST.get('yxh')
    models.student.objects.filter(xh=xh).update(xm=xm,xb=xb,sjhm=sjhm,jg=jg,yxh=yxh)

  return render(request,'admin_mod_user.html',context={'xh':student_info[0].xh,'xm':student_info[0].xm,
                                                       'sjhm':student_info[0].sjhm,'department':department,
                                                       'jg':student_info[0].jg,'xb':student_info[0].xb,
                                                       'yxh':student_info[0].yxh})

def admin_edit_course(request):
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
  if request.method == 'GET':
    return render(request,'admin_edit_course.html',context={'open_course': all})
  else:
    kh = request.POST.get('kh')
    km = request.POST.get('km')
    xf = request.POST.get('xf')
    gh = request.POST.get('gh')
    sksj = request.POST.get('sksj')
    xq = request.POST.get('xq')
    xs = request.POST.get('xs')
    if (models.course.objects.filter(kh=kh)):
      # 有这门课了
      models.open_course.objects.create(xq=xq, kh_id=kh, gh_id=gh, sksj=sksj)
      return redirect('/admin_edit_course.html/')
    else:
      models.course.objects.create(kh=kh, km=km, xf=xf, xs=xs, yxh_id='01')
      models.open_course.objects.create(xq=xq, kh_id=kh, gh_id=gh, sksj=sksj)
    return render(request, 'admin_edit_course.html', context={'open_course': all})

def admin_mod_course(request):
  kh = request.GET.get('kh_id')
  isdel = request.GET.get('isdel')
  if (isdel == 1):
    models.course.objects.filter(kh=kh).delete()
    return redirect('/admin_mod_course.html/')
  else:
    course_info = models.student.objects.filter(kh=kh)
    department = models.department.objects.filter(yxh=course_info.yxh)
    department = department.mc
    km = request.POST.get('km')
    xf = request.POST.get('xf')
    xs = request.POST.get('xs')
    yxh = request.POST.get('yxh')
    models.student.objects.filter(kh=kh).update(km=km,xf=xf,xs=xs,yxh=yxh)

  return render(request, 'admin_mod_course.html', context={'kh': course_info[0].kh, 'km': course_info[0].km,
                                                         'xf': course_info[0].xf, 'department': department,
                                                         'xs': course_info[0].xs, 'yxh': course_info[0].yxh})


