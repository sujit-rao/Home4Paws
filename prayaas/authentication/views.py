from django.shortcuts import render, redirect
from .models import user_data
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import os
from PIL import Image
from django.urls import reverse

# Create your views here.
def signup(request):
    if request.method=="POST":
        u_name = request.POST.get("name")
        u_email = request.POST.get("email")
        u_password = request.POST.get("password")
        u_phone = request.POST.get("phoneNumber")
        u_address = request.POST.get("address")
        u_country = request.POST.get("country")
        u_city=request.POST.get("city")
        u_city=u_city.lower()

        #HASHING THE PASSWORD
        hashed_u_password = make_password(u_password)
        #FETCHING THE VALUES FROM THE SIGNUP PAGE
        print(u_name+", "+u_email+", "+u_password+", "+u_phone+", "+u_address+", "+u_country)
        # Query the database to check if the email exists in the user_data model
        existing_user = user_data.objects.filter(email=u_email).exists()

        if existing_user:
                # Email exists in the database (User is already registered)
                # print("Email exists.")
                #Message to be sent to user (Email already registered)
            messages.error(request,"The Email provided is already in use")
        else:
                # Email does not exist in the database
                # print("Email does not exist.")
                #Creating a Model Object and setting the data
            u=user_data()
            u.name=u_name
            u.email=u_email
            u.phone=u_phone
            u.password=hashed_u_password
            u.phone=u_phone
            u.address=u_address
            u.country=u_country
            u.city=u_city

                #SAVE the data
            u.save()

                #Message to be sent to user (Signup Success)
            messages.success(request,"Signup was Success, Now you can Login.")
                # print("Signup is Success")

                #Redirecting to Login Page after successful Signup
            return redirect('/auth/signin/')
        return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')
    



def signin(request):
    if request.method=="POST":
        login_email = request.POST.get("email")
        login_password = request.POST.get("password")
        print(login_email+", "+login_password)

        #Checking if the email provided is registered or not
        existing_user = user_data.objects.filter(email=login_email).exists()

        if existing_user:
            #Fetching the password from the DB associated to the provided email
            user = user_data.objects.get(email=login_email)
            db_password = user.password
            if check_password(login_password, db_password):
                #Storing the EMAIL of user in the SESSION
                request.session['loggedin_email'] = login_email
                print(request.session.get('loggedin_email'))
                return redirect("/home/")
            # Passwords match, proceed with login
            else:
                #Passing Message (WRONG PASSWORD)
                messages.error(request,"Wrong Email or Password")
        else:
            # Email does not exist in the database (NO USER FOUND)
            # print("Email does not exist.")
            #Passing Message (Email Does not exist
            messages.error(request,"Wrong Email or Password")
        return render(request, 'signin.html')
    else:
        return render(request, 'signin.html')
    


def logout(request):
    if 'loggedin_email' in request.session:
        del request.session['loggedin_email']
        return redirect('/home/')
    else:
        return redirect('/home/')


