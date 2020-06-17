from django.shortcuts import render, redirect
from django.contrib import messages
from system import models # 引入对象模型
from django.db import connection


def page_not_found(request, **kwargs):
  return redirect('/login/')

def logout(request):
  request.session['number'] = None
  return redirect('/login/')
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
                return render(request, 'login.html', {'script': "alert", 'wrong': '密码错误'})
        # 账号或密码不存在
        else:
            return render(request, 'login.html', {'script': "alert", 'wrong': '账号或密码不存在'})


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
  cursor.execute("select kh,km,xf,zpcj from system_course,system_e_table "
                 "where system_e_table.kh_id = system_course.kh "
                 "and xh_id = %s and zpcj is not null and zpcj != ''", [number])
  all_scores = cursor.fetchall()  # 读取所有
  print(all_scores, type(all_scores))
  all_s = []
  for item in all_scores:
    scores = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
    scores['kh'] = item[0]
    scores['km'] = item[1]
    scores['xf'] = item[2]
    scores['zpcj'] = item[3]
    if item[3] != '':
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
      else:
        scores['gpa'] = 0.0
    all_s.append(scores)
  return render(request, 'check_my_score.html', context={'xh': number, 'scores': all_s})

'''
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
  return render(request, 'check_my_table.html', context={'xh':number,'xm':student[0].xm,'all_course':all_course})
'''

def check_my_table(request):
  number = request.session.get('number')
  cursor = connection.cursor()
  cursor.execute("select distinct kh,km,xf,sksj,system_e_table.xq,system_e_table.gh_id,xs,xm "
                 "from system_course,system_e_table,system_open_course,system_teacher "
                 "where xh_id = %s "
                 "and system_course.kh = system_e_table.kh_id "
                 "and system_open_course.kh_id =  system_e_table.kh_id "
                 "and system_teacher.gh = system_e_table.gh_id "
                 "and zpcj is null",[number])
  info = cursor.fetchall()
  all = []
  for item in info:
    temp = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
    temp['kh'] = item[0]
    temp['km'] = item[1]
    temp['xf'] = item[2]
    temp['sksj'] = item[3]
    temp['xq'] = item[4]
    temp['gh'] = item[5]
    temp['xs'] = item[6]
    temp['xm'] = item[7]
    all.append(temp)
  return render(request, 'check_my_table.html', context={'xh': number, 'all_course':all})

def select_course(request):
  number = request.session.get('number')
  cursor = connection.cursor()
  cursor.execute("select distinct xq,km,xf,kh_id,xm,gh,sksj "
                 "from system_open_course,system_teacher,system_course "
                 "where system_open_course.gh_id = system_teacher.gh "
                 "and system_open_course.kh_id = system_course.kh "
                 "and xq='2020-2021秋季'")
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
  if request.method == 'POST':
    print('post')
    km = request.POST.get('km')
    print(km)
    course_id = request.POST.get('course_id')
    print(course_id)
    teacher_id = request.POST.get('teacher_id')
    print(teacher_id)
    if km:
      # 搜索课程
      cursor = connection.cursor()
      cursor.execute("select kh_id,km,gh_id,xm,xf,sksj "
                     "from system_open_course,system_teacher,system_course "
                     "where system_open_course.gh_id = system_teacher.gh "
                     "and system_open_course.kh_id = system_course.kh and km = %s "
                     "and xq='2020-2021秋季'", [km])
      course_data = cursor.fetchall()
      print(course_data)
      all_data = []
      for item in course_data:
        course = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
        course['kh'] = item[0]
        course['km'] = item[1]
        course['gh'] = item[2]
        course['xm'] = item[3]
        course['xf'] = item[4]
        course['sksj'] = item[5]
        all_data.append(course)
      return render(request, 'select_course.html', context={'xh':number,'course_data': all_data, 'open_course': all})
    if course_id and teacher_id:
      models.e_table.objects.create(xq='2020-2021秋季', xh_id=number, kh_id=course_id, gh_id=teacher_id)
      # messages.success(request, '选课成功啦~~~~~~')
      return redirect('/select_course/')
  else:
    return render(request, 'select_course.html', context={'xh':number,'open_course': all})

def delete_course(request):
    number = request.session.get('number')
    kh = request.GET.get('kh')
    cursor = connection.cursor()
    cursor.execute(
      "select kh,km,gh,xm,xf "
      "from system_course,system_e_table,system_teacher "
      "where system_e_table.kh_id = system_course.kh "
      "and system_e_table.gh_id = system_teacher.gh "
      "and xh_id = %s and zpcj is null",
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
    if kh:
      # 如果获取到了内容
      models.e_table.objects.filter(xh_id=number, kh_id=kh).delete()
      # messages.success(request, '退课成功啦~~~~~~')
      return redirect('/delete_course/')

    return render(request, 'delete_course.html', context={'xh':number,'selected_course': selected_c})

'''
    if request.method == 'GET':
      return render(request, 'delete_course.html', context={'selected_course': selected_c})
    else:
      course_id = request.POST.get('course_id')
      # 先选中，再删除
      models.e_table.objects.filter(xh_id=number, kh_id=course_id).delete()
      # messages.success(request, '退课成功啦~~~~~~')
      return redirect('/delete_course/')
'''

def teacher_course(request):
  number = request.session.get('number')
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
  return render(request, 'teacher_course.html',context={'gh':number,'courses_data':courses_data})

def teacher_edit_score(request):
  number = request.session.get('number')
  cursor = connection.cursor()
  # 查询这个老师教的学生的成绩
  cursor.execute(
    "select distinct kh,km,xh,xm,pscj,kscj,zpcj,xq from system_course,system_e_table,system_student "
    "where system_e_table.kh_id = system_course.kh and system_student.xh = system_e_table.xh_id "
    "and system_e_table.gh_id = %s", [number])
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
    temp['xq'] = item[7]
    teacher_student_data.append(temp)
  print(teacher_student_data)
  return render(request, 'teacher_edit_score.html',context={'gh':number,'student_data':teacher_student_data})

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
  if request.method == 'POST':
    # 先找到对应数据，再update
    models.e_table.objects.filter(gh_id=number, kh_id=kh, xh_id=xh).update(pscj=pscj, kscj=kscj, zpcj=zpcj)
    return redirect('/teacher_edit_score/')
  else:
    return render(request, 'teacher_mod_score.html', context={'gh':number,'xh': xh, 'xm': xm, 'km': km})

def admin_edit_student(request):
  gh = request.session.get('number')
  cursor = connection.cursor()
  # 查询操作
  cursor.execute("select xh,xm,xb,csrq,jg,sjhm,mc from system_student,system_department "
                 "where system_student.yxh_id = system_department.yxh")
  student_info = cursor.fetchall()  # 读取所有
  all_student = []
  for item in student_info:
    temp = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
    temp['xh'] = item[0]
    temp['xm'] = item[1]
    temp['xb'] = item[2]
    temp['csrq'] = item[3]
    temp['jg'] = item[4]
    temp['sjhm'] = item[5]
    temp['mc'] = item[6]
    all_student.append(temp)
  # all_student = models.student.objects.all()

  if request.method == 'POST':
    xh = request.POST.get('xh')
    xm = request.POST.get('xm')
    jg = request.POST.get('jg')
    sjhm = request.POST.get('sjhm')
    xb = request.POST.get('xb')
    csrq = request.POST.get('csrq')
    print(csrq, type(csrq))
    yxh = request.POST.get('mc')

    print("now is student")
    print(xh,xm,jg,xb,sjhm,yxh)
    models.student.objects.create(xh=xh, xm=xm, jg=jg,csrq=csrq,xb=xb, sjhm=sjhm,pwd='student',yxh_id=yxh)
    return redirect('/admin_edit_student/')
  else:
    return render(request, 'admin_edit_student.html', context={'gh':gh,'all_student': all_student})


def admin_edit_teacher(request):
  gh = request.session.get('number')
  cursor = connection.cursor()
  # 查询操作
  cursor.execute("select gh,xm,xb,xl,csrq,mc from system_teacher,system_department "
                 "where system_teacher.yxh_id = system_department.yxh")
  teacher_info = cursor.fetchall()  # 读取所有
  all_teacher = []
  for item in teacher_info:
    temp = dict()  # 注意这里一定要放在循环之内！！！！！！！！！！！！
    temp['gh'] = item[0]
    temp['xm'] = item[1]
    temp['xb'] = item[2]
    temp['xl'] = item[3]
    temp['csrq'] = item[4]
    temp['mc'] = item[5]
    all_teacher.append(temp)
  # all_teacher = models.teacher.objects.all()
  if request.method == 'POST':
    gh = request.POST.get('gh')
    xm = request.POST.get('xm')
    xl = request.POST.get('xl')
    xb = request.POST.get('xb')
    csrq = request.POST.get('csrq')
    print(csrq, type(csrq))
    yxh = request.POST.get('mc')
    print("now is teacher")
    print(gh,xm,xl,csrq,xb,yxh)
    models.teacher.objects.create(gh=gh, xm=xm, xl=xl, csrq=csrq, xb=xb, jbgz='8000', pwd='teacher',yxh_id=yxh)
    return redirect('/admin_edit_teacher/')
  else:
    return render(request, 'admin_edit_teacher.html', context={'gh':gh,'all_teacher': all_teacher})


def admin_mod_student(request):
  gh = request.session.get('number')
  xh = request.GET.get('xh')
  isdel = request.GET.get('isdel')
  student_info = models.student.objects.filter(xh=xh).first()
  if (int(isdel) == 1):
    models.student.objects.filter(xh=xh).delete()
    return redirect('/admin_edit_student/')
  else:
    if request.method == 'POST':
      department = models.department.objects.filter(yxh=student_info.yxh_id).first()
      print(department.mc, type(department.mc))
      xm = request.POST.get('xm')
      xb = request.POST.get('xb')
      csrq = request.POST.get('csrq')
      jg = request.POST.get('jg')
      sjhm = request.POST.get('sjhm')
      yxh = request.POST.get('mc')
      if not yxh:
        yxh = student_info.yxh_id
      models.student.objects.filter(xh=xh).update(xm=xm,xb=xb,jg=jg,sjhm=sjhm,yxh_id=yxh,pwd = 'student')
      # return render(request, 'admin_mod_user.html', context={'xm':xm,'xh':xh,'jg':jg,'sjhm':sjhm,'csrq':csrq,'xb':xb,'yxh':yxh})
      return redirect('/admin_edit_student/')
  return render(request, 'admin_mod_student.html', context={'xm':student_info.xm,'xh':student_info.xh,
                                                         'jg':student_info.jg,'sjhm':student_info.sjhm,
                                                         'csrq':student_info.csrq,'xb':student_info.xb,
                                                         'yxh':student_info.yxh_id,'gh':gh})

def admin_mod_teacher(request):
  number = request.session.get('number')
  gh = request.GET.get('gh')
  isdel = request.GET.get('isdel')
  teacher_info = models.teacher.objects.filter(gh=gh).first()
  print("=====",gh)
  print(teacher_info)
  if (int(isdel) == 1):
    models.teacher.objects.filter(gh=gh).delete()
    return redirect('/admin_edit_teacher/')
  else:
    if request.method == 'POST':
      department = models.department.objects.filter(yxh=teacher_info.yxh_id).first()
      print(department.mc, type(department.mc))
      xm = request.POST.get('xm')
      xb = request.POST.get('xb')
      xl = request.POST.get('xl')
      if not xl:
        xl = teacher_info.xl
      jbgz = request.POST.get('jbgz')
      yxh = request.POST.get('mc')
      if not yxh:
        yxh = teacher_info.yxh
      models.teacher.objects.filter(gh=gh).update(xm=xm, xb=xb, xl=xl,jbgz=jbgz,yxh_id=yxh)
      return redirect('/admin_edit_teacher/')

  return render(request, 'admin_mod_teacher.html', context={'xm': teacher_info.xm, 'gh': teacher_info.gh,
                                                         'xl': teacher_info.xl, 'jbgz':teacher_info.jbgz,
                                                         'csrq': teacher_info.csrq, 'xb': teacher_info.xb,
                                                         'admin_gh':number})

def admin_edit_course(request):
  gh = request.session.get('number')
  cursor = connection.cursor()
  cursor.execute("select distinct xq,km,xf,kh_id,xm,gh,sksj,xq "
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
    course['xq'] = item[7]
    all.append(course)
  if request.method == 'POST':
    kh = request.POST.get('kh')
    km = request.POST.get('km')
    xf = request.POST.get('xf')
    gh = request.POST.get('gh')
    sksj = request.POST.get('sksj')
    xq = request.POST.get('xq')
    xs = request.POST.get('xs')
    yxh = request.POST.get('mc')
    if (models.course.objects.filter(kh=kh)):
      # 有这门课了
      models.open_course.objects.create(xq=xq, kh_id=kh, gh_id=gh, sksj=sksj)
      return redirect('/admin_edit_course/')
    else:
      models.course.objects.create(kh=kh, km=km, xf=xf, xs=xs, yxh_id=yxh)
      models.open_course.objects.create(xq=xq, kh_id=kh, gh_id=gh, sksj=sksj)
      return redirect('/admin_edit_course/')
  else:
    return render(request, 'admin_edit_course.html', context={'gh':gh,'open_course': all})

def admin_mod_course(request):
  gh = request.session.get('number')
  kh = request.GET.get('kh_id')
  isdel = request.GET.get('isdel')
  course_info = models.course.objects.filter(kh=kh).first()
  print(kh,type(kh),isdel,type(isdel))
  if (int(isdel) == 1):
    models.course.objects.filter(kh=kh).delete()
    return redirect('/admin_edit_course/')
  else:
    if request.method == 'POST':
      department = models.department.objects.filter(yxh=course_info.yxh_id).first()
      print(department.mc,type(department.mc))
      km = request.POST.get('km')
      xf = request.POST.get('xf')
      xs = request.POST.get('xs')
      yxh = request.POST.get('mc')
      if not yxh:
        yxh = course_info.yxh_id
      models.course.objects.filter(kh=kh).update(km=km,xf=xf,xs=xs,yxh_id=yxh)
      return render(request, 'admin_mod_course.html', context={'gh':gh,'kh': kh,'km':km,'xf':xf,'xs':xs,'yxh':yxh})

  return render(request, 'admin_mod_course.html',context={'gh':gh,'kh':kh,'km':course_info.km,'xf':course_info.xf,'xs':course_info.xs})

def teacher_daily_post(request):
  gh = request.session.get('number')
  tea_info = models.teacher.objects.filter(gh=gh).first()
  if request.method == 'POST':
    bsrq = request.POST.get('bsrq')
    zk = request.POST.get('zk')
    tw = request.POST.get('tw')
    print (gh, tea_info.xm, tea_info.yxh.yxh, bsrq, zk, tw)
    models.tea_status.objects.create(gh_id=gh, xm=tea_info.xm, yxh_id=tea_info.yxh.yxh, bsrq=bsrq, zk=zk, tw=tw)
    return redirect('/teacher_index/')
  else:
    return render(request, 'teacher_daily_post.html', context={'gh': gh, 'xm': tea_info.xm})

def student_daily_post(request):
    # 不需要学生写学号姓名这些信息了
    xh = request.session.get('number')
    stu_info = models.student.objects.filter(xh=xh).first()
    if request.method == 'POST':
      bsrq = request.POST.get('bsrq')
      zk = request.POST.get('zk')
      tw = request.POST.get('tw')
      print (xh,stu_info.xm,stu_info.yxh.yxh,bsrq,zk,tw)
      models.stu_status.objects.create(xh_id=xh,xm=stu_info.xm,yxh_id=stu_info.yxh.yxh,bsrq=bsrq,zk=zk,tw=tw)
      return redirect('/student_index/')
    else:
      return render(request,'student_daily_post.html',context={'xh':stu_info.xh,'xm':stu_info.xm})

def admin_daily_post(request):
    gh = request.session.get('number')
    admin_info = models.admin.objects.filter(gh=gh)
    # 管理员不需要报送体温
    # 管理员需要查看体温不正常的人群，过高或者过低
    cursor = connection.cursor()
    cursor.execute("select distinct xh_id,xm,mc,bsrq,zk,tw "
                   "from system_stu_status,system_department "
                   "where (system_department.yxh=system_stu_status.yxh_id) "
                   "and (zk = '不适' or cast(tw as float) > 37 or cast(tw as float) < 35)")
    select_users = cursor.fetchall()
    # print(open_course)
    all_student = []
    for item in select_users:
      temp = dict()
      temp['xh'] = item[0]
      temp['xm'] = item[1]
      temp['mc'] = item[2]
      temp['bsrq'] = item[3]
      temp['zk'] = item[4]
      temp['tw'] = item[5]
      all_student.append(temp)
    print (all_student)

    cursor.execute("select distinct gh_id,xm,mc,bsrq,zk,tw "
                   "from system_tea_status,system_department "
                   "where (system_department.yxh=system_tea_status.yxh_id) "
                   "and (zk = '不适' or cast(tw as float) > 37 or cast(tw as float) < 35)")
    select_users = cursor.fetchall()
    all_teacher = []
    for item in select_users:
      temp = dict()
      temp['gh'] = item[0]
      temp['xm'] = item[1]
      temp['mc'] = item[2]
      temp['bsrq'] = item[3]
      temp['zk'] = item[4]
      temp['tw'] = item[5]
      all_teacher.append(temp)
    print (all_teacher)
    return render(request,'admin_daily_post.html',context={'gh':gh,'all_student':all_student,'all_teacher':all_teacher})
