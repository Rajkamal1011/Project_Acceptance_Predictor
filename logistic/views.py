import math

from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ProjectDB

from . import pred_xgb, pred_lr, pred_dl

# Landing Page
def landing(request):
    return render(request, 'landing.html')

# HOME PAGE
@login_required
def home(request):
    if request.method == 'POST':
        title = request.POST.get('projtitle')
        essay = request.POST.get('essay')
        ss = request.POST.get('ss')
        tp = request.POST.get('tp')
        pgc = request.POST.get('projgradecat')
        cc = request.POST.get('cc')
        csc = request.POST.get('csc')
        price = request.POST.get('price')
        tpp = request.POST.get('tpp')       
        
        try:
            price = float(price)
        except ValueError:
            messages.error(request, "<strong>Price</strong> should be a number.")
            return render(request, 'inputform/index2.html')
        
        try:
            tpp = int(tpp)
        except ValueError:
            messages.error(request, "<strong>Previously Submitted Paper</strong> should be a number.")
            return render(request, 'inputform/index2.html')

        inputs = {
            "essay" : essay,
            "ss" : ss,
            "tp" :tp,
            "pgc" : pgc,
            "cc" : cc,
            "csc" : csc,
            "price" : price,
            "tpp" : tpp,
        }
        
        resultXGB = pred_xgb.mainPredict(inputs)
        resultLR = pred_lr.mainPredict(inputs)
        resultDL = pred_dl.mainPredict(inputs)

        # choosing the better probability to store in Database
        largest_result = resultXGB
        if resultLR[0][1] > largest_result[0][1]:
            largest_result = resultLR
        if resultDL[0][1] > largest_result[0][1]:
            largest_result = resultDL

        # Saving in Database
        saveInProjectDB = ProjectDB(user=request.user, title=title, essay=essay, price=price, probability=math.ceil(largest_result[0][1]*100))
        saveInProjectDB.save()

        messages.success(request, "<strong>Project Details saved in Dashboard!!</strong>")

        # return render(request, 'inputform/index4.html')

        return render(request, 'inputform/index4.html', {'resultLR' : math.ceil(resultLR[0][1]*100), 'resultXGB' : math.ceil(resultXGB[0][1]*100), 'resultDL' : math.ceil(resultDL[0][1]*100)})
    return render(request, 'inputform/index2.html')


# User Dashboard Page
@login_required
def dashboard(request):
    context = {}
    all = ProjectDB.objects.filter(user__username = request.user.username)
    context["projects"] = all
    return render(request, 'inputform/dashboard.html', context)

# Result Page
def resultPage(request):
    # if request.method == "GET":
    #     title = request.GET.get('title')
    #     return render(request, 'inputform/index4.html', {'result':title})

    return render(request, 'inputform/index4.html', {'result':10})


# Login Page
def login(request):

    if request.user.is_authenticated:
        return redirect('/home')

    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "<strong>Successfully LoggedIn !!</strong>")
            return redirect('/home')
        else:
            messages.warning(request, "<strong>Incorrect Password or UserName</strong>. Please Try Again.")
            return redirect('/login')

    return render(request, 'auth/login.html')


# Signup Page
def signup(request):
    
    if request.user.is_authenticated:
        return redirect('/home')

    # TODO : add examples below input fields 
    if request.method == "POST":
        username = request.POST['username']
        completename = request.POST['completename']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # username already exist check
        duplicateUserName = User.objects.filter(username=username).exists()
        if duplicateUserName == True:
            messages.warning(request, "<strong>UserName Already Exists !!</strong>")
            return redirect('/signup')
        
        else:

            if password != cpassword:
                messages.error(request, "<strong>Passwords</strong> do not match.")
                return redirect('/signup')
            else:
                newUser = User.objects.create_user(username=username, email=email, password=cpassword)
                newUser.first_name = completename
                newUser.save()
                auth_login(request, newUser)
                messages.success(request, "<strong>Signup Successful</strong>")
                return redirect('/home')

    return render(request, 'auth/signup.html')


# Logout Page
@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')


