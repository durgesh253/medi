from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import *
from random import randint
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta

from django.contrib.auth.models import User

# # Create your views here.


def IndexPage(request):
    return render(request, "index.html")


def dashboard_view(request):
    return render(request, 'dashboard.html')

def login_view(request):
    if request.method == 'POST':
        staff_id = request.POST['staff_id']
        password = request.POST['password']
        try:
            CHECK_STAFF = staff.objects.get(staff_id=staff_id)
        except staff.DoesNotExist:
            messages.info(request, "User doesn't exist")
            return redirect('login_view')
        else:
            if CHECK_STAFF.staff_id == staff_id and CHECK_STAFF.password == password:
                request.session['staff_id'] = staff_id
                employee_data = staff.objects.get(staff_id=staff_id)
                request.session['role'] = employee_data.role.name
                request.session['first_name'] = employee_data.first_name
                request.session['last_name'] = employee_data.last_name
                request.session['email'] = employee_data.email
                request.session['mobile'] = employee_data.mobile
                return redirect('dashboard_view')
            else:
                messages.error(request, "Staff ID or password doesn't match")
                return redirect('login_view')
    return render(request, 'login.html')


def logout(request):
    del request.session['staff_id']
    messages.success(request, 'Now you are logged out')
    return redirect(login_view)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            CHECK_STAFF = staff.objects.get(email=email)
        except staff.DoesNotExist:
            messages.info(request, "User doesn't exist")
            return redirect('login_view')
        else:
            otp = random.randint(111111, 999999)
            subject  = 'OTP for fogot password'
            message =  f"""
            Your OTP is : {otp}
            """
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [f"{email}"]
            send_mail(subject, message, from_email, recipient_list)
            CHECK_STAFF.otp = otp
            CHECK_STAFF.save()
            context = {
                'email':email
            }
            messages.success(request, 'Please, check your mail. OTP sent successfully')
            return render(request, 'otp-verification.html', context)
    return render(request, 'forgot-password.html')

def otp_verification(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        try:
            CHECK_STAFF = staff.objects.get(email=email)
            context = {
                'email':email
            }
        except staff.DoesNotExist:
            messages.info(request, "User doesn't exist")
            return redirect('login_view')
        else:
            if CHECK_STAFF.otp == otp:
                if new_password == confirm_password:
                    CHECK_STAFF.password = new_password
                    CHECK_STAFF.save()
                    messages.success(request, 'Password Changed')
                    return redirect('login_view')
                else:
                    messages.error(request, "New password and Confirm password doesn't match")
                    return render(request, 'otp-verification.html', context)
            else:
                messages.error(request, "Invalid OTP!!!")
                return render(request, 'otp-verification.html', context)
    return render(request, 'otp-verification.html')




# def register_view(request):
#     if request.method == 'POST':
#         role_name = request.POST['role']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         cpassword = request.POST['cpassword']

#         # Check if the email already exists
#         user_exists = staff.objects.filter(email=email).exists()

#         if user_exists:
#             message = "User already exists"
#             return render(request, "register.html", {'msg': message})
#         else:
#             if password == cpassword:
#                 otp = randint(000000, 999999)
#                 subject = "otp for registration"
#                 message = f"Your OTP is: {otp}"
#                 from_email = settings.EMAIL_HOST_USER
#                 recipient_list = [email]
#                 send_mail(subject, message, from_email, recipient_list)

#                 # Create a new user with the provided details
#                 newuser = staff.objects.create(
#                     role=role.objects.get(name=role_name),
#                     otp=otp,
#                     email=email,
#                     password=password,
#                     first_name=first_name,
#                     last_name=last_name
#                 )

#                 # Create a Doctor instance associated with the new user
#                 newdoctor = Doctor.objects.create(
#                     # staff_id=newuser,
#                     firstname=first_name,
#                     last_name=last_name,
#                     contact='',  # Add appropriate values for these fields
#                     age=0,  # Provide a default age value
#                     address='',
#                     total_patient=0,
#                     summary='',
#                     profile_pic=''  # Add appropriate default image path
#                 )

#                 # Create a Patient instance associated with the new user
#                 newpatient = Patient.objects.create(
#                     # staff_id=newuser,
#                     firstname=first_name,
#                     last_name=last_name,
#                     contact='',  # Add appropriate values for these fields
#                     age=0,
#                     doctor_id =newdoctor,  # Provide a default age value
#                     address='',

#                 )

#                 messages.success(request, 'Please, check your mail. OTP sent successfully')
#                 return render(request, "otp-verification.html", {'email': email})
#             else:
#                 message = "Password and confirm password do not match"
#                 return render(request, "register.html", {'msg': message})

#     return render(request, 'register.html')

def update_profile(request,staff_id):
    get_staff = staff.objects.get(staff_id=staff_id)
    if request.method == "POST":
        first_name_ = request.POST['first_name']
        last_name_ = request.POST['last_name']
        email_ = request.POST['email']
        mobile_ = request.POST['mobile']

        get_staff.first_name = first_name_
        get_staff.last_name = last_name_
        get_staff.email = email_
        get_staff.mobile = mobile_
        get_staff.save()
        print("Staff Data Updated")
        return redirect("dashboard_view")
    
    context = {
        'staff' : get_staff

    }
    return render(request, "update_profile.html",context)





def doctor_view(request):
    doctors_list = Doctor.objects.all()
    paginator = Paginator(doctors_list, 10)  # Show 10 doctors per page

    page = request.GET.get('page')
    try:
        doctors = paginator.page(page)
    except PageNotAnInteger:
        doctors = paginator.page(1)
    except EmptyPage:
        doctors = paginator.page(paginator.num_pages)

    context = {
        'doctors': doctors,
    }
    return render(request, "doctors.html", context)





def add_patient(request):
    if request.method == 'POST':
        # Retrieve data from the form
        firstname = request.POST.get('firstname')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        age = request.POST.get('age')
        doctor_id = request.POST.get('doctor_id')
        address = request.POST.get('address')

        # Retrieve the Doctor instance using the selected doctor_id
        doctor = Doctor.objects.get(pk=doctor_id)

        # Create a new patient object
        patient = Patient.objects.create(
            firstname=firstname,
            last_name=last_name,
            contact=contact,
            age=age,
            doctor_id=doctor,  # Assign the Doctor instance
            address=address
        )
        patient.save()
        return redirect('dashboard_view')  # Adjust the redirect URL as needed

    doctors = Doctor.objects.all()
    context = {
        'doctors': doctors
    }

    return render(request, 'patient.html', context)

def update_patient(request, patient_id):
    if request.method == 'POST':
        try:
            # Retrieve data from the form
            firstname = request.POST.get('firstname')
            last_name = request.POST.get('last_name')
            contact = request.POST.get('contact')
            age = request.POST.get('age')
            doctor_id = request.POST.get('doctor_id')
            address = request.POST.get('address')

            # Validate required fields
            if not (firstname and last_name and contact and age and doctor_id and address):
                raise ValueError("All fields are required")

            # Retrieve the Doctor instance using the selected doctor_id
            doctor = get_object_or_404(Doctor, pk=doctor_id)

            # Retrieve the patient to update
            patient = get_object_or_404(Patient, pk=patient_id)

            # Update the patient details
            patient.firstname = firstname
            patient.last_name = last_name
            patient.contact = contact
            patient.age = age
            patient.doctor = doctor
            patient.address = address

            patient.save()

            return redirect('patient_list')  # Adjust the redirect URL as needed

        except ValueError as e:
            return HttpResponseBadRequest(f"Error: {e}")

    # If the request method is not POST, render the form with the existing patient details
    patient = get_object_or_404(Patient, pk=patient_id)
    doctors = Doctor.objects.all()
    context = {
        'doctors': doctors,
        'patient': patient,
    }

    return render(request, 'update_patients.html', context)

def delete_patient(request,patient_id):
    get_patient = Patient.objects.get(id=patient_id)
    get_patient.delete()
    print("patient Deleted")
    return redirect('patient_list')


def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


def create_doctor(request):
    if request.method == 'POST':
        # Retrieve data from the form
        firstname = request.POST.get('firstname')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        age = request.POST.get('age')
        address = request.POST.get('address')
        total_patient = request.POST.get('total_patient')
        summary = request.POST.get('summary')

        # Create a new doctor object and save it to the database
        doctor = Doctor.objects.create(
            firstname=firstname,
            last_name=last_name,
            contact=contact,
            age=age,
            address=address,
            total_patient=total_patient,
            summary=summary,
            # Assuming 'profile_pic' is the name attribute of your file input
            profile_pic=request.FILES.get('profile_pic')
        )
        
        return redirect('doctors_view')  # Adjust the redirect URL as needed

    return render(request, 'create_doctor.html')