from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from .forms import UserLoginForm, UserRegisterForm, CompanyRegistrationForm
from .models import Registration, YearEnding
from salt_master.models import Salt
from unit_master.models import Unit
from company_master.models import Company, Supplier
from godown_master.models import Godown
from purchase.models import PurchaseInvHrd
from sales.models import SalesInvHrd
import datetime

class loginView(View):
	formClass = UserLoginForm
	template_name = "accounts/account_form.html"
	session_redirect_url = "/account/session/expire"
	model = None
	register_url = "/account/company/register"
	success_url = "/"
	User = get_user_model()
 
	@staticmethod
	def sessionExpirationCheck():
		currDate = datetime.date.today()
		lastEnding = YearEnding.objects.all().last()
		if not lastEnding:
			return True
		if currDate > lastEnding.to_dt:
			return True
		else:
			return False

	def get(self, *args, **kwargs):
		user_qs = self.User.objects.all()
		register_qs = Registration.objects.all()
		if not user_qs:
			messages.warning(self.request, 'You have to first register yourself')
			return HttpResponseRedirect("/account/register")

		if not register_qs :
			return HttpResponseRedirect(self.register_url)

		if self.sessionExpirationCheck():
			return redirect(self.session_redirect_url)

		context = {
			"form" : self.formClass(),
			"title" : "User Login",
			"btn_txt": "Login"
		}

		return render(self.request, self.template_name, context)
	
	def post(self, *args, **kwargs):
		form = self.formClass(self.request.POST)
		register_qs = Registration.objects.all()
		if form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password")
			session = form.cleaned_data.get("session")  
			self.request.session['session'] = session.id
			user = authenticate(username = username, password = password)
			login(self.request, user)
			if register_qs.count() == 0:
				return HttpResponseRedirect(self.register_url)
			return redirect(self.success_url)
		return HttpResponseRedirect("/account/login")

def register_view(request):
	User = get_user_model()
	user_qs = User.objects.all()
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save()
		password = form.cleaned_data.get("password")	
		user.set_password(password)
		user.is_staff = True
		user.save()
		new_user = authenticate(username = user.username, password = password)
		login(request, new_user)
		return redirect("/account/company/register")
	return render(request, "accounts/account_form.html", {
		"title" : "User Register",
		"form" : form,
		"btn_txt": "Register",
		"sessionExpire": False
	})


def logout_view(request):
	logout(request)
	try:
	  del request.session['session']
	except:
		pass
	return HttpResponseRedirect("/")


def initializeRegistration(company_instance,  today_date, end_date):
	YearEnding.objects.create(code = "DB1",
						year_pur_id=0, year_sale_id=0,
													from_dt=today_date, to_dt=end_date, 
						registration_id=company_instance)
	# Godown.objects.create(name = "GODOWN")
	# Supplier.objects.create(name = "SELF")
	# Company.objects.create(name = "AVENTIS PASTEUR")
	# Unit.objects.create(name = "1*10", unit = 10)
	# Salt.objects.create(name = "TELMISARTAN")




def companyRegistrationView(request):
	reg_qs = Registration.objects.all()
	if reg_qs.count() > 0:
		messages.warning(request, 'Only one Company can register.')
		return HttpResponseRedirect("/account/login")

	User = get_user_model()
	user_qs = User.objects.all()
	if user_qs.count() == 0:
		messages.warning(request, 'Register the user first')
		return HttpResponseRedirect("/account/register")

	messages.warning(request, 'Register Your Company Now.')
	form = CompanyRegistrationForm(request.POST or None)
	if form.is_valid():
		company_instance = form.save()
		today_date = datetime.date.today()
		end_date = today_date + datetime.timedelta(days=365)

		initializeRegistration(company_instance, today_date, end_date)

		messages.warning(request, 'Login')
		return redirect("/account/login")
	return render(request, "accounts/account_form.html", {
		"form" : form,
		"title" : "Company Registration",
		"btn_txt": "Register"
	})



class sessionExpireView(View):
	template_name = "accounts/session.html"
	success_url = "/account/login"

	@staticmethod
	def sessionExpirationCheck():
		currDate = datetime.date.today()
		lastEnding = YearEnding.objects.all().last()
		if not lastEnding:
			return True
		if currDate > lastEnding.to_dt:
			return True
		else:
			return False

	def get(self, *args, **kwargs):
		if not self.sessionExpirationCheck():
			return redirect("/account/login")

		return render(self.request, self.template_name, {
			"lastEnding": YearEnding.objects.all().last()
		})	

	def post(self, *args, **kwargs):
		lastEnding = YearEnding.objects.all().last()
		lastPurchase = PurchaseInvHrd.objects.all().last().id
		lastSales = SalesInvHrd.objects.all().last().id
		to_dt = lastEnding.to_dt
		to_dt = datetime.date(year=to_dt.year+1, month = 3, day = 31)
		yeobj = YearEnding(
			code = f"DB{lastEnding.id+1}",
			year_pur_id = lastPurchase + 1,
			year_sale_id = lastSales + 1,
			from_dt = lastEnding.to_dt + datetime.timedelta(days=1),
			to_dt = to_dt,
			registration_id = Registration.objects.first(),
		)
		yeobj.save()
		return redirect(self.success_url)


