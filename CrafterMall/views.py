from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def login(request):
    return render(request, 'login.html')
    
def register(request):
    errors=Users.objects.count_Vald(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['pw_input']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = Users.objects.create(
        first_name = request.POST['first_name_input'],
        last_name = request.POST['last_name_input'],
        email = request.POST['email_input'],
        password = pw_hash,
        birthdate = request.POST['bday_input']
    )
    request.session['userid'] = new_user.id
    return redirect('/success')
    
def log(request):
    user = Users.objects.filter(email=request.POST['email_input']) 
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['pw_input'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/success')
        return redirect("/")
    else:
        return redirect('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def delete(request, val):
    this_guy = Users.objects.get(id=val)
    this_guy.delete()
    return redirect('/')
    
def success(request):
    context ={
        'logged_in': Users.objects.get(id=request.session['userid']),
        'users_db': Users.objects.all()
    }
    return render(request, 'success.html',context)