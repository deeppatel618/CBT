from distutils.command.upload import upload
import email
from pyexpat import model
from django.db import models

class User(models.Model):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    profilePic=models.ImageField(upload_to="Profile/",default="/Default/defaultProfilePic.png")
    userType=models.CharField(max_length=100,default="student")
    status=models.CharField(max_length=100,default="pending")
    
    def __str__(self):
        return self.fname+" "+self.lname +" - " + self.userType +" - " + self.status

class Course(models.Model):
    faculty=models.ForeignKey(User,on_delete=models.CASCADE)
    cname=models.CharField(max_length=100)

    def __str__(self):
        return self.cname 

class Exam(models.Model):
    cname=models.ForeignKey(Course,on_delete=models.CASCADE)
    examName=models.CharField(max_length=100)
    examTime=models.IntegerField()
    examTotalMarks=models.IntegerField()

    def __str__(self):
        return self.examName + ","+self.cname.cname


class Question(models.Model):
    ename=models.ForeignKey(Exam,on_delete=models.CASCADE)
    ques=models.TextField()
    opt1=models.CharField(max_length=100)
    opt2=models.CharField(max_length=100)
    opt3=models.CharField(max_length=100)
    opt4=models.CharField(max_length=100)
    answer=models.CharField(max_length=100)

    def __str__(self):
        return self.ename.cname.cname+"-"+self.ename.examName