from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import transaction
from django.contrib.staticfiles.templatetags.staticfiles import static
from .decorators import is_user_authenticated
from .models import *
from datetime import datetime, timezone
from datetime import time
from datetime import date
from .serializers import *
from rest_framework import viewsets
import numpy

# Create your views here.

def get_record(model, record_id):
    return model.objects.get(pk=record_id)


@csrf_exempt
def login(request):

    if request.method != 'POST':
        return JsonResponse({'success': False, "code": 1, 'error': f'method {request.method} is not allowed'})
    user_data = json.loads(request.body)
    print(user_data)
    if User.objects.filter(email=user_data['email']).exists():
        user = User.objects.get(email=user_data['email'])
        userData = user.to_dict()
        
        if user.check_password(user_data['password']):
            return JsonResponse({"success": True, "code": 0, "status": "Login Successfull", "data":{"user": userData, 'access_token':user.token}})
        else:
            return JsonResponse({"success" : False, "code": 1, "status":"Email/password did not match"})    
    else:
        return JsonResponse({"success" : False, "code": 1, "status":"Email does not exist"})

@csrf_exempt
@transaction.atomic
def signup(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, "code": 1, 'status': f'method {request.method} is not allowed'})
    print("signup in")
    user_data = json.loads(request.body)
    if User.objects.filter(email=user_data['email']).exists():
        print("1")
        return JsonResponse({"success" : False, "code": 1, "status":"Email alreay exists."})
    else:
        try:
            print("2", user_data)
            with transaction.atomic():
                user = User.objects.create_user(user_data["email"], user_data["password"])
                user.name = user_data["name"]
#                user.location = Point(user_data["location"]["longitude"],user_data["location"]["latitude"])
                user.email = user_data["email"]
                user.save()
                userData = user.to_dict()
                

                return JsonResponse({"success": True, "code": 0, "status": "Successfully registered", "data":{"user": userData, "access_token": user.token}})
        except Exception as e:
            print("3")
            print(str(e))
            return JsonResponse({"success": False, "code": 2, "status":str(e)})


def students(request):
    students = Student.objects.all()
    students = [getStudentDict(student) for student in students]
    return render(request, 'tution_management_app/students.html',{"students":students})

def getStudentDict(student):
    teachers = ','.join([get_record(Teacher,teacher.id).name.name for teacher in student.teachers.all()])
    subjects = ','.join(numpy.concatenate([[subjects.name for subjects in get_record(Teacher,teacher.id).subjects.all()] for teacher in student.teachers.all()]))
    return {"student_name":student.student_name,"teachers":teachers,"subjects":subjects,"id":student.id}

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer





