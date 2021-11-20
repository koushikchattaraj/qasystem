from rest_framework import response
from questions.models import Question
import accounts
import re
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import User, UserProfile
from answers.models import Answer
from .serializers import (
	UserLoginSerializer, UserCreateSerilizer, UserSerilizers, UserProfileSerilizer
	)
import string
import random
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

def token_generator(size=16, chars=string.ascii_uppercase + string.ascii_lowercase):
  return ''.join(random.choice(chars) for _ in range(size))


class LoginView(View):
	template_name = 'sign-in.html'

	def get(self, request):
		return render(request, self.template_name)
	
	def post(self, request):
		return render(request, self.template_name)

class AccountView(View):
	template_name = 'account.html'

	def get(self, request):
		return render(request, self.template_name)

class DriveView(View):
	template_name = 'drive.html'

	def get(self, request):
		return render(request, self.template_name)

class DashboardView(View):
	template_name = 'dashboard.html'

	def get(self, request):
		return render(request, self.template_name)

class TrashView(View):
	template_name = 'trash.html'

	def get(self, request):
		return render(request, self.template_name)

class StarredView(View):
	template_name = 'starred.html'

	def get(self, request):
		return render(request, self.template_name)

class RecentView(View):
	template_name = 'recent.html'

	def get(self, request):
		return render(request, self.template_name)


class CreateView(View):
	template_name = 'sign-up.html'

	def get(self, request):
		return render(request, self.template_name)

class IndexView(View):
	template_name = 'index.html'

	def get(self, request):
		return render(request, self.template_name)

class UserLoginView(RetrieveAPIView):

	permission_classes = (AllowAny,)
	serializer_class = UserLoginSerializer


	def post(self, request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):   
			response = {
				'success' : 'True',
				'status code' : status.HTTP_200_OK,
				'message': 'User logged in  successfully',
				'token' : serializer.data['token']
				}
			status_code = status.HTTP_200_OK
			return Response(response, status=status_code)	
		else:
			response = {
				'error': serializer.errors
			}
			return Response(response, status=status.HTTP_200_OK)

class UserCreateView(APIView):
	permission_classes = (AllowAny,)
	serializer_class = UserCreateSerilizer

	def post(self, request):
		create_user_serilizer = self.serializer_class(data=request.data)
		email = request.data.get('email')
		if User.objects.filter(email__iexact=email).exists():
			response = {
				'success' : 'False',
				'status code' : status.HTTP_400_BAD_REQUEST,
				'message': 'Email Id is already register.',
				}
			return Response(response, status=status.HTTP_400_BAD_REQUEST)
		else:		
			if create_user_serilizer.is_valid():
				create_user_serilizer.save()
				token = token_generator()
				user = User.objects.get(email=email)
				user_profile = UserProfile.objects.get(user=user)
				userprofile_serilizer = UserProfileSerilizer(user_profile, data={"token":token}, partial=True)
				if userprofile_serilizer.is_valid():
					userprofile_serilizer.save()
					subject = 'Account Verification'
					message = f'Hi {user.name}, Click Here to Verify your account : https://qasystemdrive.herokuapp.com/account_verification/{user.id}/{token}.'
					email_from = settings.EMAIL_HOST_USER
					recipient_list = [email, ]
					send_mail( subject, message, email_from, recipient_list )


				response = {
					'success' : 'True',
					'status code' : status.HTTP_200_OK,
					'message': 'User Sucessfully Created',

					}
				return Response(response, status=status.HTTP_200_OK)
			else:
				response = {
					'success' : 'True',
					'status code' : status.HTTP_400_BAD_REQUEST,
					'message': create_user_serilizer.errors
					}
				return Response(response, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (JSONWebTokenAuthentication,)

	def get(self, request):
		context = {}
		user = User.objects.filter(id=request.user.id)
		user_profile = UserProfile.objects.filter(user=request.user.id)
		user_serilizer = UserSerilizers(user, many=True)
		userprofile_serilizer = UserProfileSerilizer(user_profile, many=True)
		question = Question.objects.filter(user=request.user.id).count()
		answer = Answer.objects.filter(user=request.user.id).count()
		context['status'] = status.HTTP_200_OK
		return Response({'user_data':user_serilizer.data, 'user_profile':userprofile_serilizer.data, 'question_no':question, 'answer_no':answer}, status=status.HTTP_200_OK)

	def put(self, request):
		context = {}
		user_profile = UserProfile.objects.get(user=request.user.id)
		user_data = User.objects.get(id=request.user.id)

		userprofile_serilizer = UserProfileSerilizer(user_profile, data=request.data, partial=True)
		user_serilizer = UserSerilizers(user_data, data=request.data, partial=True)
		if userprofile_serilizer.is_valid():
			userprofile_serilizer.save()
			context['status'] = status.HTTP_200_OK
			context['data'] = userprofile_serilizer.data
			context['message'] = "Profile updated."
			if user_serilizer.is_valid():
				user_serilizer.save()
				context['user'] = user_serilizer.data
				return Response ({"user_profile":userprofile_serilizer.data,"user":user_serilizer.data}, status.HTTP_200_OK)
		else:
			context['status'] = status.HTTP_400_BAD_REQUEST
			context['message'] = "Profile Not updated."
			return Response (context, status.HTTP_400_BAD_REQUEST)

class AccountVerification(APIView):
	permission_classes = (AllowAny,)
	authentication_classes = (JSONWebTokenAuthentication,)
	def get(self, request, *args, **kwargs):
		try:
			user = User.objects.get(id=kwargs['user'])
			user_profile = UserProfile.objects.get(user=user,token=kwargs['token'])
			if user:
				if user_profile.is_active:
					messages.success(request,"Your account is already verify!!!")
					return redirect('/sign_in/')
			
			if user_profile:
				user.is_active = True
				user_profile.is_active = True
				user.save()
				user_profile.save()
				messages.success(request,"You have registered successfully, now login!")
				return redirect('/sign_in/')
			

		except Exception as e:
			print(e)

		return HttpResponse("Html")