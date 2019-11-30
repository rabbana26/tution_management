from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)
import jwt
from django.conf import settings
from datetime import datetime, timedelta



class UserManager(BaseUserManager):
	def create_user(self, email, password):
		#create and return user with email, username and password
		if email is None:
			raise TypeError('User must have an email')
		if password is None:
			raise TypeError('User must have a password')

		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, password):
		#create and return user with superuser (admin) permission 
		if password is None:
			raise TypeError('Superuser must have a password')
		user = self.create_user(email, password)
		user.is_superuser = True
		user.is_staff = True
		if password is not None:
			user.set_password(password)
		user.save()

		return user

class User(AbstractBaseUser, PermissionsMixin):
	# Avoid deleting accounts since they may be associated with some data.
	# this will indicate if some account has been deactivated.
	is_active = models.BooleanField(default=True)

	# The `is_staff` flag is expected by Django to determine who can and cannot
	# log into the Django admin site. For most users this flag will always be
	# false.
	is_staff = models.BooleanField(default=False)

	# A timestamp representing when this object was created.
	created_at = models.DateTimeField(auto_now_add=True)

	# A timestamp reprensenting when this object was last updated.
	updated_at = models.DateTimeField(auto_now=True)

	# This token is used when we have implement reset password functionality
	reset_token = models.CharField(max_length=1000, null=True, blank=True)

	name = models.CharField(max_length=100, null=True, blank=True)

	# The email field will act as the username field for this application
	email = models.EmailField(db_index=True, unique=True, max_length=100)

	

	# The `USERNAME_FIELD` property tells us which field we will use to log in.
	# In this case we want it to be the email field.
	USERNAME_FIELD = 'email'

	# Tells Django that the UserManager class defined above should manage
	# objects of this type.
	objects = UserManager()

	def __str__(self):
		"""
		Returns a string representation of this `User`.

		This string is used when a `User` is printed in the console.
		"""
		return self.email

	def get_full_name(self):
		"""
		This method is required by Django for things like handling emails.
		Typically this would be the user's first and last name. Since we do
		not store the user's real name, we return their username instead.
		"""
		return self.email

	def get_short_name(self):
		"""
		This method is required by Django for things like handling emails.
		Typically, this would be the user's first name. Since we do not store
		the user's real name, we return their username instead.
		"""
		return self.email

	@property
	def token(self):
		"""
		Allows us to get a user's token by calling `user.token` instead of
		`user.generate_jwt_token().

		The `@property` decorator above makes this possible. `token` is called
		a "dynamic property".
		"""
		return self._generate_jwt_token()

	def _generate_jwt_token(self):
		"""
		Generates a JSON Web Token that stores this user's ID and has an expiry
		date set to 60 days into the future.
		"""
		dt = datetime.now() + timedelta(days=60)

		token = jwt.encode({
			'id': self.pk,
			'exp': int(dt.strftime('%s'))
		}, settings.SECRET_KEY, algorithm='HS256')

		return token.decode('utf-8')

	def to_dict(self):
		return {"email":self.email}





class Subject(models.Model):
	name = models.CharField(max_length=200,blank=False)

	def __str__(self):
		return self.name

class Teacher(models.Model):
	name = models.OneToOneField(User, on_delete=models.CASCADE,blank=False,null=True,related_name="teacher_name")
	subjects = models.ManyToManyField(Subject)

	def __str__(self):
		return self.name.name


class Student(models.Model):
	student_name = models.OneToOneField(User, on_delete=models.CASCADE,blank=False,null=True,related_name="student_name")
	teachers = models.ManyToManyField(User)

	def __str__(self):
		return self.student_name.name




