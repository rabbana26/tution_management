from rest_framework import serializers
from .models import *


def get_record(model, record_id):
    return model.objects.get(pk=record_id)

def get_teacher_detail(teacher_ids):

    teachers = []

    for teacher_id in teacher_ids:
        teacher = get_record(User, teacher_id)
        subjects = [get_record(Subject, subject["subjects"]).name for subject in list(Teacher.objects.filter(name=teacher.id).values("subjects"))] 
        teachers.append({'name': teacher.name, 'id': teacher.id,"subjects":subjects})

    return teachers

def get_user_details(student_id):
	if student_id is None:
		return None

	created_by = get_record(User, student_id)
	return {'name': created_by.name, 'id': created_by.id}

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):

	def to_representation(self, instance):
		response = super(TeacherSerializer, self).to_representation(instance)
		response['name'] = get_user_details(response['name'])
		response['subjects'] = [get_record(Subject, subject).name for subject in response['subjects'] ]
		return response
	class Meta:
		model = Teacher
		fields = "__all__"

class StudentSerializer(serializers.ModelSerializer):

	def to_representation(self, instance):
		response = super(StudentSerializer, self).to_representation(instance)
		response['teachers'] = get_teacher_detail(response['teachers'])
		response['student_name'] = get_user_details(response['student_name'])
		return response
	class Meta:
		model = Student
		fields = "__all__"
