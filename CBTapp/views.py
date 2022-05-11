
from twilio.rest import Client

from urllib import request
from venv import create
from django.shortcuts import render,redirect
from .models import *

from django.conf import settings
from django.core.mail import send_mail

import os



def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def signUp(request):
    if request.method == "POST":
        if request.POST["fname"]=="" or request.POST["lname"]=="" or request.POST["mobile"]==None or request.POST["email"]=="" or request.POST["password"]=="":
            return render(request,'signUp.html' , {"msg":"All the fields are compulsory"})
        else:
            try:
                user=User.objects.get(email=request.POST["email"])
                return render(request,'signUp.html' , {"msg":"Email id already registered"})
            except:
                if request.POST["password"]==request.POST["cpassword"]:
                    User.objects.create(
                        fname=request.POST["fname"],
                        lname=request.POST["lname"],
                        mobile=request.POST["mobile"],
                        email=request.POST["email"],
                        password=request.POST["password"],
                        profilePic=request.FILES["profilePic"],
                        userType=request.POST['userType']
                    )
                    return render(request,'signUp.html' , {"msg":"SignUp Successfull"})
                else:
                    return render(request,'signUp.html' , {"msg":"Password and confirm password should be same"})
    else:
        return render(request,'signUp.html')


def login(request):
    if request.method=="POST":
        if request.POST["email"]=="" or request.POST["password"]=="":
            if request.POST["email"]=="":
                return render(request,'login.html' , {"msg":"Please enter Email Id"})
            else:
                return render(request,'login.html' , {"msg":"Please enter Password"})
        else:
            try:
                user=User.objects.get(email=request.POST["email"],password=request.POST["password"])
                if user.status=="approved":
                    if user.userType == "student":
                        request.session['email']=user.email
                        request.session['fname']=user.fname
                        request.session['profilePic']=user.profilePic.url
                        return render(request,'index.html')
                    else:
                        request.session['email']=user.email
                        request.session['fname']=user.fname
                        request.session['profilePic']=user.profilePic.url
                        return render(request,'facultyIndex.html')
                else:
                    return render(request,'login.html' , {"msg":"Status not Approved by faculty"})
                    
            except:
                    return render(request,'login.html' , {"msg":"Wrond EmailId or Password"})
    else:
        return render(request,'login.html')


def logout(request):
    del request.session["email"]
    del request.session["fname"]
    return render(request,'login.html')

def changePassword(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.session['email'],password=request.POST["opassword"])
            if request.POST["npassword"]==request.POST["cnpassword"]:
                user.password=request.POST["npassword"]
                user.save()
                return redirect('logout')
            else:
                return render(request,'changePassword.html' ,{"msg":"Password & Confirm Password does not Match"})
        except:
            return render(request,'changePassword.html' ,{"msg":"Current Password is wrong"})
    return render(request,'changePassword.html')

def facultyIndex(request):
    return render(request,'facultyIndex.html')

def facultyChangePassword(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.session['email'],password=request.POST["opassword"])
            if request.POST["npassword"]==request.POST["cnpassword"]:
                user.password=request.POST["npassword"]
                user.save()
                return redirect('logout')
            else:
                return render(request,'facultyChangePassword.html' ,{"msg":"Password & Confirm Password does not Match"})
        except:
            return render(request,'facultyChangePassword.html' ,{"msg":"Current Password is wrong"})
    return render(request,'facultyChangePassword.html')

def students(request):
    studentList=User.objects.filter(userType="student")
    return render(request,'students.html',{"students":studentList})

def course(request):
    faculty=User.objects.get(email=request.session['email'])
    msg=""
    courseWithExam=[]
    if request.method=="POST":
        try:
            Course.objects.get(cname=request.POST["cname"])
            msg="Course already exist"
        except Exception as e:
            print( e)
            Course.objects.create(
                faculty=faculty,
                cname=request.POST["cname"]
            )
            msg="Course added"
    
    try:
        allCourses=Course.objects.all().filter(faculty=faculty)
        for x in allCourses:
            courseWithExam.append([x,len(Exam.objects.all().filter(cname=x))])
    except Exception as e:
        print(e)
    return render(request,'course.html',{'allMessage':courseWithExam,"msg":msg})

def editCourse(request):
    if request.method=="GET":
        try:
           
            c=Course.objects.get(pk= request.GET["addExamCourseId"])
            return render(request,'addExam.html',{"course":c.pk})
        except:
            print("exception")
            courseToBeDeleted=Course.objects.all().filter(pk=request.GET["deleteCourseId"])
            courseToBeDeleted.delete()
            return redirect('course')


def courseDetails(request):
    print(request.POST["courseId"])
    return render(request,"courseDetails.html")

def addExam(request):
    if request.method=="POST":
        c=Course.objects.get(pk=request.POST["courseId"])
        e=Exam.objects.create(
            cname=c,
            examName=request.POST["ename"],
            examTime=request.POST["etime"],
            examTotalMarks=request.POST["emarks"]
        )
        return render(request,'addExam.html',{"msg":"Exam added","exam":e})
    return render(request,"addExam.html")


def examDetails(request):
    allCourseWithExam={}
    faculty=User.objects.get(email=request.session["email"])
    course=Course.objects.all().filter(faculty=faculty)
    for x in course:
        try:
            exam=Exam.objects.all().filter(cname=x)
            allCourseWithExam[x]=exam
        except:
            allCourseWithExam[x]=""
    if request.method=="POST":
        cname=request.POST["btn"].split(',')[0]
        ename=request.POST["btn"].split(',')[1]
        print(cname,ename)
        return render(request,'addQuestion.html',{'cname':cname,'ename':ename,'allQuestion':questionList(request,cname,ename)})
    return render(request,'examDetails.html',{"course":allCourseWithExam})

def addQuestion(request):
    if request.method=="POST":
        cname=request.POST["cname"]
        ename=request.POST["ename"]
        faculty=User.objects.get(email=request.session['email'])
        course=Course.objects.get(faculty=faculty,cname=cname)
        exam=Exam.objects.get(cname=course,examName=ename)
        Question.objects.create(
            ename=exam,
            ques=request.POST["ques"],
            opt1=request.POST["opt1"],
            opt2=request.POST["opt2"],
            opt3=request.POST["opt3"],
            opt4=request.POST["opt4"],
            answer=request.POST["ans"],
        )
        return render(request,'addQuestion.html',{'cname':cname,'ename':ename,'allQuestion':questionList(request,cname,ename)})
    # print(request.GET["cname"])
    # return render(request,'addQuestion.html')

def questionList(request,cname,ename):
    faculty=User.objects.get(email=request.session['email'])
    course=Course.objects.get(faculty=faculty,cname=cname)
    exam=Exam.objects.get(cname=course,examName=ename)
    allQuestion=Question.objects.all().filter(ename=exam)
    return allQuestion
    # return []

def courseList(request):
    allMessage={}
    try:
        allCourses=Course.objects.all()
        for x in allCourses:
            allMessage[x]=Exam.objects.all().filter(cname=x)
    except:
        pass
    if request.method=="POST":
        pk=request.POST["cId"]
        # ename=request.POST["ename"]
        # print(questionList(request,cname,ename))
        exam=Exam.objects.get(pk=pk)
        allQuestion=Question.objects.all().filter(ename=exam)
        print(allQuestion)
        return render(request,'examination.html',{'allQuestion':allQuestion,'exam':exam})      
    return render(request,'courseList.html',{'allMessage':allMessage})

def examination(request):
    if request.method=="POST":
        ansCouter=0
        quesCouter=0
        exam=Exam.objects.get(pk=request.POST["exampk"])
        allQuestion=Question.objects.all().filter(ename=exam)
        for ques in allQuestion:
            quesCouter+=1
            try:
                if ques.answer == request.POST["ans-"+str(ques.pk)]:
                    ansCouter+=1
            except Exception as a:
                print(a)
        subject = 'Test result '
        message = f'You have scored {ansCouter} out of {quesCouter} in {exam.cname},{exam.examName}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.session['email'], ]
        send_mail( subject, message, email_from, recipient_list )


        account_sid = 'ACcc804d60ba60cb8009c1cd5123d604a6'
        auth_token = 'd636fe15f9a5f35228b742bb1d21e30c'
        client = Client(account_sid, auth_token)
        message = client.messages \
                .create(
                     body=f'You have scored {ansCouter} out of {quesCouter} in {exam.cname},{exam.examName}.',
                     from_='+19706140260',
                     to='+919898499257'
                 )

        print(message.sid)

    return render(request,'examination.html',{'quesCounter':quesCouter,"ansCounter":ansCouter})