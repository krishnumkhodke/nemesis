from django.shortcuts import render, redirect
from . models import Profile
from . forms import UserForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . serializers import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.

def signUp(request):
	form = UserForm()

	if request.method == 'POST':
		form = UserForm(request.POST)

		if form.is_valid():
			user = User.objects.create_user(username = form.cleaned_data['username'],
						 password = form.cleaned_data['password'], email = form.cleaned_data['email'])

			profile = Profile.objects.create(user = user, address = form.cleaned_data['address'])
			return redirect('UserDetail', id = user.id)

	return render(request, 'users/signup.html', {'form' : form})

def allUsers(request):
	data = Profile.objects.all()
	return render(request, 'users/all_users.html', {'profiles' : data})	

def loginUser(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)
		if user is not None:
			print("Success")
			messages.success(request, 'Logged In')
			login(request, user)
			return redirect('AllUsers')
		else:
			messages.error(request, 'Username or Password invalid')

	return render(request, 'users/login.html')

def logoutUser(request):
	logout(request)
	messages.success(request, 'Logged Out')
	return redirect('AllUsers')

def userDetail(request, id):
	print(id)
	user = User.objects.get(id = id)
	
	form = UserUpdateForm(instance = user)

	if request.method == 'POST':
		form = UserUpdateForm(request.POST, instance = user)
		if form.is_valid():
			if User.objects.filter(username=form.cleaned_data['username']).exists() == True:
				messages.error(request, "Username Already In Use")
				return redirect('UserDetail', id = user.id)
			else :
				form.save()
				user.profile.save()
				print(user.username)
	return render(request, 'users/user_detail.html', {'user' : user, 'form': form})

def editUserDetail(request, id, field):
	user = User.objects.get(id = id)
	new_data = ''
	if request.method == 'POST':
		new_data = request.POST['new_data']


		if field == 'address':
			user.profile.address = new_data
		elif field == 'username':
			if User.objects.filter(username=new_data).exists():
				messages.error(request, "Username Already In Use")
			else:
				user.username = new_data
		else:
			user.email = new_data

		user.save()
		user.profile.save()
		return redirect('UserDetail', id = user.id)

	return render(request, 'users/edit_user_details.html', {'form' : 0, 'user' : user})

def deleteUser(request, id):
	user = User.objects.get(id = id)
	try:
		u = User.objects.get(username = user.username)
		u.delete()
		messages.success(request, "The user is deleted")            
	
	except User.DoesNotExist:
		messages.error(request, "User doesnot exist")

	return redirect('SignUp')

class ProfileApi(APIView):

	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def get(self, request):
		profiles = Profile.objects.all()
		serializer = ProfileSerializer(profiles, many=True)
		return Response({'status':200, 'payload': serializer.data})

	def post(self, request):
		serializer = ProfileSerializer(data = request.data)

		if not serializer.is_valid():
			print(serializer.errors)
			return Response({'status' :403, 'errors': serializer.errors, 'message': 'error'})

		serializer.save()
		return Response({'status':200, 'payload': serializer.data, 'message': 'success'})

	def put(self, request):
		pass

	def patch(self, request):
		pass

	def delete(self, request):
		pass