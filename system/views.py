from django.shortcuts import render, redirect
from django.contrib import messages
from system import models # 引入对象模型

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
    student = models.student.objects.filter(xh=number)
    return render(request, 'student_index.html', context={'xh': number, 'xm': student[0].xm,
                                                          'xb': student[0].xb, 'csrq': student[0].csrq,
                                                          'jg': student[0].jg,'sjhm' : student[0].sjhm
                                                          })


def teacher_index(request):
  number = request.session.get('number')
  teacher = models.teacher.objects.filter(gh=number)
  return render(request, 'teacher_index.html', context={'gh': number, 'xm': teacher[0].xm,
                                                        'xb': teacher[0].xb, 'csrq': teacher[0].csrq,
                                                        'xl': teacher[0].xl, 'jbgz': teacher[0].jbgz
                                                        })

def admin_index(request):
  number = request.session.get('number')
  admin = models.admin.objects.filter(gh=number)
  return render(request, 'admin_index.html', context={'gh': number, 'xm': admin[0].xm, 'xb': admin[0].xb
                                                        })

def student_coursetable(request):  #课表
    return render(request, 'student_coursetable.html')

def student_choose(request):  #选课
    return render(request, 'student_choose.html')

def student_drop(request):  #退课
    return render(request, 'student_drop.html')