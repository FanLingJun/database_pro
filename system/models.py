from django.db import models

# 创建模型，对应数据库的表
class user(models.Model):   #
    number = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=8)
    department = models.CharField(max_length=10)
    usertype = models.CharField(max_length=10)
    sex = models.CharField(max_length=2)
    age = models.CharField(max_length=2)
    pswd = models.CharField(max_length=8)

# 学生表
class student(models.Model):
  xh = models.CharField(primary_key=True, max_length=6)
  xm = models.CharField(max_length=8)
  xb = models.CharField(max_length=4)
  csrq = models.DateField(max_length=12)
  jg = models.CharField(max_length=12)
  sjhm = models.CharField(max_length=8)
  yxh = models.CharField(max_length=8)
  pwd = models.CharField(max_length=6)

class teacher(models.Model):
  gh = models.CharField(primary_key=True, max_length=6)
  xm = models.CharField(max_length=8)
  xb = models.CharField(max_length=4)
  csrq = models.DateField(max_length=12)
  xl = models.CharField(max_length=12)
  jbgz = models.CharField(max_length=8)
  yxh = models.CharField(max_length=8)
  pwd = models.CharField(max_length=6)

class admin(models.Model):
  gh = models.CharField(primary_key=True, max_length=6)
  xm = models.CharField(max_length=8)
  xb = models.CharField(max_length=4)
  pwd = models.CharField(max_length=6)


