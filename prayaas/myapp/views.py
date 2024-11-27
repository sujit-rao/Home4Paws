from django.shortcuts import render, redirect
import os
from PIL import Image
from django.contrib import messages
from .models import pet_data
from authentication.models import user_data

# Create your views here.


def home(request):
    return render(request, 'home.html')


# Constants
MAX_FILE_SIZE = 1024 * 1024  # 1MB

def rehome(request):
    if 'loggedin_email' not in request.session:
        return render(request, 'home.html')
    print("Received request method:", request.method)  # Debugging statement

    if request.method == "POST":
        pet_pic = request.FILES.get('petPic')
        print("Uploaded file:", pet_pic)  # Debugging statement

        # Check if the file is provided
        if not pet_pic:
            messages.error(request, "All the image fields must be filled")
            print("No pet picture provided.")  # Debugging statement
            return redirect('/rehome/')

        # Check file size
        print("File size:", pet_pic.size)  # Debugging statement
        if pet_pic.size > MAX_FILE_SIZE:
            messages.error(request, "The files uploaded should not be greater than 1MB")
            print("File size exceeds 1MB.")  # Debugging statement
            return redirect('/rehome/')

        # Try to open the image file
        try:
            with Image.open(pet_pic) as img:
                print("Image opened successfully.")  # Debugging statement

                # Retrieve pet details
                pet_name = request.POST.get("petName", "").strip()
                pet_type = request.POST.get("petType", "").strip()
                pet_breed = request.POST.get("petBreed", "").strip()
                pet_age = request.POST.get("petAge", "").strip()
                pet_gender = request.POST.get("petGender", "").strip()
                pet_desc = request.POST.get("petDescription", "").strip()

                # Debugging print statements for retrieved data
                print("Retrieved pet details:")
                print(f"Name: {pet_name}, Type: {pet_type}, Breed: {pet_breed}, Age: {pet_age}, Gender: {pet_gender}, Description: {pet_desc}")

                # Check if all fields are filled
                if not all([pet_name, pet_type, pet_breed, pet_age, pet_gender, pet_desc]):
                    messages.error(request, "All pet details must be provided.")
                    print("Missing pet detail fields.")  # Debugging statement
                    return redirect('/rehome/')

                # Here you would typically save the data to the database
                print("Data is valid and ready to be processed.")  # Debugging statement

                #SESSION EMAIL
                current_email = request.session.get('loggedin_email')

                #Fetching location Of user using the SESSION EMAIL
                tempuserobj = user_data.objects.get(email=current_email)
                print(tempuserobj.city)
                pet_city=tempuserobj.city.lower()
                #INSERTING THE DATA TO DB
                #Creating a Model Object and setting the data
                p=pet_data()
                p.useremail=current_email
                p.petname=pet_name
                p.pettype=pet_type
                p.petbreed=pet_breed
                p.petgender=pet_gender
                p.petage=pet_age
                p.petdesc=pet_desc
                p.petpic=pet_pic
                p.petcity=pet_city

                #SAVE the data
                p.save()

                #Message to be sent to user (DATA UPLOADED)
                messages.success(request,"New Post Uploaded Successfully")

        except (IOError, SyntaxError, ValueError) as e:
            messages.error(request, "Only IMAGE type file formats are supported")
            print(f"Invalid image format: {e}")  # Debugging statement


    # If the request method is not POST, or after handling POST request
    print("Rendering rehome.html")  # Debugging statement
    return render(request, 'rehome.html')





def findapet(request, location):
    print(location)
    if request.method == "POST":
        custom_location = request.POST.get("customLocation", "").strip()
        custom_location=custom_location.lower()
        print(custom_location)
        petobj = pet_data.objects.filter(petcity=custom_location)
        context={'petobj': petobj}
        return render(request, 'findapet.html', context)
    else:
        petobj = pet_data.objects.filter(petcity=location)
        context={'petobj': petobj}
        return render(request, 'findapet.html', context)

def petdetail(request, post_id):
    print(type(post_id))
    print(post_id)
    petobj = pet_data.objects.get(id=post_id)
    userobj=user_data.objects.get(email=petobj.useremail)
    print("User Object: ")
    print(userobj.name)
    context={'petobj':petobj, 'userobj':userobj}
    print(petobj.petpic)
    print(petobj.petpic.url)
    return render(request, 'petdetail.html', context)

def profile(request):
    if 'loggedin_email' not in request.session:
        return redirect('/home/')
    #SESSION EMAIL
    current_email = request.session.get('loggedin_email')
    petobj = pet_data.objects.filter(useremail=current_email)
    userobj=user_data.objects.get(email=current_email)
    context={'petobj': petobj, 'userobj': userobj}
    return render(request, 'profile.html', context)



def deletepost(request, post_id):
    current_email = request.session.get('loggedin_email')
    #AUTHORIZING THE USER
    auth_user=pet_data.objects.filter(useremail=current_email).filter(id=post_id)
    if auth_user:
        # post_id=int(post_id)
        # print(type(post_id))
        # DELETING THE IMAGES OF THAT ROW
        my_obj=pet_data.objects.get(id=post_id)
        os.remove(my_obj.petpic.path)
        #----------------------------------
        pet_data.objects.filter(id=post_id).delete()
        messages.success(request, "Post Deleted Successfully")
        return redirect('/profile/')
    else:
        return redirect('/home/')
    


def editpost(request, post_id):
    if 'loggedin_email' not in request.session:
        return redirect('/home/')
    current_email = request.session.get('loggedin_email')
    #AUTHORIZING THE USER
    auth_user=pet_data.objects.filter(useremail=current_email).filter(id=post_id)
    
    if auth_user:
        # post_id=int(post_id)
        # print(type(post_id))
        # DELETING THE IMAGES OF THAT ROW
        my_obj=pet_data.objects.get(id=post_id)
        context={'my_obj':my_obj}
        # --------------------------------------------
        if request.method == "POST":
            if 'petPic' in request.FILES:
                pet_pic = request.FILES['petPic']
                if pet_pic.size > 0 and pet_pic.size <= 1024 * 1024:
                    # print("Has a file")
                    os.remove(my_obj.petpic.path)
                    print("Old Pic removed")
                else:
                    messages.error(request, "The Image size should not be more than 1MB")
                    return redirect('/editpost/'+ post_id)
                # my_obj.petpic=pet_pic
                my_obj.petpic=pet_pic
            pet_name=request.POST.get("petName")
            pet_type=request.POST.get("petType")
            pet_breed=request.POST.get("petBreed")
            pet_age=request.POST.get("petAge")
            pet_gender=request.POST.get("petGender")
            pet_desc=request.POST.get("petDescription")

            my_obj.petname=pet_name
            my_obj.pettype=pet_type
            my_obj.petbreed=pet_breed
            my_obj.petage=pet_age
            my_obj.petgender=pet_gender
            my_obj.petdesc=pet_desc
                
            # my_obj.useremail=my_obj.useremail
            # my_obj.petcity=my_obj.petcity

            my_obj.save()
            print("New data updated")
            messages.success(request, "Data Updated Successfully")
            return redirect('/profile/')

        # ----------------------------------------------
        return render(request, 'edit.html', context)
    else:
        return redirect('/home/')

def delallpet(request):
    pet_data.objects.all().delete()
    return redirect('/home/')

def delalluser(request):
    user_data.objects.all().delete()
    return redirect('/home/')