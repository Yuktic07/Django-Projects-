from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login,logout,authenticate
from random import randrange
from django.core.mail import send_mail


def home(request):
	if request.user.is_authenticated:
		if request.method=="POST":
			num=int(request.POST.get("num"))
			if num % 2 == 0:
				res="even"
			else:
				res="odd"
			return render(request, "home.html",{"msg":res})
		else:
			return render(request,"home.html")
	else:
		return redirect("ulogin")


def ulogin(request):
	if request.user.is_authenticated:
		return redirect("home")
	elif request.method == "POST":
		un = request.POST.get("un")
		pw = request.POST.get("pw")
		usr = authenticate(username=un, password=pw)
		if usr is not None:
			login(request, usr)
			return redirect("home")
		else:
			return render(request, "login.html",{"msg":"Invalid Username or Password"})
	else:
		return render(request, "login.html")

def usignup(request):
	if request.user.is_authenticated:
		return redirect("home")
	if request.method == "POST":
		un = request.POST.get("un")
		try:
			usr=User.objects.get(username=un)
			return render(request, "signup.html",{"msg":"Username already exists"})
		except User.DoesNotExist:
			pw=""
			text="123456789"
			for i in range(4):
				pw = pw + text[randrange(len(text))]
			print(pw)
			subject = "Welcome to Yukti App"
			text = "Your password is " + str(pw)
			from_email = "kunal.tester24aug22@gmail.com"
			to_email = [str(un)]
			send_mail(subject,text,from_email,to_email)
			usr = User.objects.create_user(username=un,password=pw)
			usr.save();
			return redirect("ulogin")
	else:
		return render(request, "signup.html")

def ulogout(request):
	logout(request)
	return redirect("ulogin")
