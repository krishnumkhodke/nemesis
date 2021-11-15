from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Profile

class UserForm(forms.ModelForm):
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	address = forms.CharField()
	class Meta:
		model = User
		fields = ['username', 'password', 'confirm_password', 'email', 'address']

		widgets = {
			'password': forms.PasswordInput(),
		}

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get("password")
		confirm_password = cleaned_data.get("confirm_password")
		print(password, 'ef')
		if password != confirm_password:
			raise forms.ValidationError("password and confirm_password does not match")

class UserUpdateForm(forms.ModelForm):
	address = forms.CharField()
	class Meta:
		model = User
		fields = ['username', 'email', 'address']

