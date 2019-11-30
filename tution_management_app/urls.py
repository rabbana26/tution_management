from django.urls import path, include
from rest_framework import routers
from .views import *
from . import views

router = routers.DefaultRouter()
router.register('subjects', SubjectViewSet)
router.register('teachers', TeacherViewSet)
router.register('students', StudentViewSet)


urlpatterns = [
    path('user/login/',views.login, name='login'),
    path('user/signup/', views.signup, name='signup'),
    path('students/', views.students, name='students'),
    path('api/', include(router.urls)),
    
]