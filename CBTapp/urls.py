from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('contact/',views.contact,name='contact'),
    path('signUp/',views.signUp,name='signUp'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('changePassword/',views.changePassword,name='changePassword'),
    path('facultyIndex/',views.facultyIndex,name='facultyIndex'),
    path('facultyChangePassword/',views.facultyChangePassword,name='facultyChangePassword'),
    path('students/',views.students,name='students'),
    path('course/',views.course,name='course'),
    path('deleteIndex/',views.editCourse,name='editCourse'),
    path('courseList/',views.courseList,name='courseList'),
    path('courseDetails/',views.courseDetails,name='courseDetails'),
    path('Exam/',views.addExam,name='addExam'),
    path('Question/',views.addQuestion,name='addQuestion'),
    path('examDetails/',views.examDetails,name='examDetails'),
    path('examination/',views.examination,name='examination'),
    path('ajax/studentStatus/',views.studentStatus,name='studentStatus'),
]