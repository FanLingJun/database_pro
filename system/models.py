from django.db import models

class department(models.Model):
  yxh = models.CharField(max_length=8,primary_key=True)
  mc = models.CharField(max_length=16)
  dz = models.CharField(max_length=25)
  lxdh = models.CharField(max_length=19)

# 学生表
class student(models.Model):
  xh = models.CharField(primary_key=True, max_length=6)
  xm = models.CharField(max_length=8)
  xb = models.CharField(max_length=4)
  csrq = models.DateField(max_length=12)
  jg = models.CharField(max_length=12)
  sjhm = models.CharField(max_length=8)
  yxh = models.ForeignKey(to = department, on_delete=models.CASCADE)
  pwd = models.CharField(max_length=6)

class teacher(models.Model):
  gh = models.CharField(primary_key=True, max_length=6)
  xm = models.CharField(max_length=8)
  xb = models.CharField(max_length=4)
  csrq = models.DateField(max_length=12)
  xl = models.CharField(max_length=12)
  jbgz = models.CharField(max_length=8)
  yxh = models.ForeignKey(to=department, on_delete=models.CASCADE)
  pwd = models.CharField(max_length=6)

class admin(models.Model):
  gh = models.CharField(primary_key=True, max_length=6)
  xm = models.CharField(max_length=8)
  xb = models.CharField(max_length=4)
  pwd = models.CharField(max_length=6)

class course(models.Model):
  kh = models.CharField(primary_key=True, max_length=16)
  km = models.CharField(max_length=16)
  xf = models.IntegerField()
  xs = models.IntegerField()
  yxh = models.ForeignKey(to=department, on_delete=models.CASCADE)

class e_table(models.Model):
  xh = models.ForeignKey(to = student, on_delete=models.CASCADE)
  xq = models.CharField(max_length=20)
  kh = models.ForeignKey(to = course, on_delete=models.CASCADE)
  gh = models.ForeignKey(to = teacher, on_delete=models.CASCADE)
  pscj = models.CharField(max_length=10,null=True)
  kscj = models.CharField(max_length=10,null=True)
  zpcj = models.CharField(max_length=10,null=True)

class open_course(models.Model):
  xq = models.CharField(max_length=20)
  kh = models.ForeignKey(to = course, on_delete=models.CASCADE)
  gh = models.ForeignKey(to = teacher, on_delete=models.CASCADE)
  sksj = models.CharField(max_length=20)

class stu_status(models.Model):
  xh = models.ForeignKey(to = student, on_delete=models.CASCADE)
  xm = models.CharField(max_length=20)
  yxh = models.ForeignKey(to=department, on_delete=models.CASCADE)
  bsrq = models.DateField(max_length=12)
  zk = models.CharField(max_length=10)
  tw = models.CharField(max_length=5)


class tea_status(models.Model):
  gh = models.ForeignKey(to = teacher, on_delete=models.CASCADE)
  xm = models.CharField(max_length=20)
  yxh = models.ForeignKey(to=department, on_delete=models.CASCADE)
  bsrq = models.DateField(max_length=12)
  zk = models.CharField(max_length=10)
  tw = models.CharField(max_length=5)
  

