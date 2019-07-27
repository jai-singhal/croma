from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from django import forms
from .models import Registration,  YearEnding
from django.contrib.admin.forms import AdminAuthenticationForm

User = get_user_model()
def get_initial_session():
	try:
		return YearEnding.objects.order_by('-id')[0]
	except:
		return None


class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput,)
	session = forms.ModelChoiceField(YearEnding.objects.all().order_by('-to_dt'), \
								initial= get_initial_session())

	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"username"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"password"})

		self.fields['session'].widget.attrs.update({
		    'class': 'form-control',
		    "name":"session"})

	def clean(self, *args, **keyargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		session_id = self.cleaned_data.get("session")
		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("This user does not exists")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("User is no longer active")

		return super(UserLoginForm, self).clean(*args, **keyargs)



class UserRegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			"first_name",
			"last_name",
			"username",
			"password",
			"confirm_password"
		]
	password = forms.CharField(widget=forms.PasswordInput,)
	confirm_password = forms.CharField(widget=forms.PasswordInput,)
	
	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
		    'class': 'form-control',
		    "name": "username"})
		self.fields['password'].widget.attrs.update({
		    'class': 'form-control',
		    "name": "password"})
		self.fields['confirm_password'].widget.attrs.update({
		    'class': 'form-control',
		    "name": "Confirm Password"})
		self.fields['first_name'].widget.attrs.update({
			'class': 'form-control',
			"name": "First Name"})
		self.fields['last_name'].widget.attrs.update({
			'class': 'form-control',
			"name": "Last Name"})

	def clean(self, *args, **keyargs):
		pass1 = self.cleaned_data.get("password")
		pass2 = self.cleaned_data.get("confirm_password")
		if pass1 != pass2:
			raise forms.ValidationError("User is no longer active")

		return super(UserRegisterForm, self).clean(*args, **keyargs)


class CompanyRegistrationForm(forms.ModelForm):
	class Meta:
		model = Registration
		fields = "__all__"
		exclude = (
			"user_id",
			)
