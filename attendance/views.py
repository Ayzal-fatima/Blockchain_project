from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from blockchain.services import mark_attendance
from django.contrib.auth.decorators import login_required

from .forms import  LoginFaceForm
from .models import BiometricData, AttendanceRecord
from blockchain.facial_recognition_service import compare_faces
from django.contrib.auth import authenticate



from django.core.exceptions import ObjectDoesNotExist  # Import the exception

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginFaceForm
from .models import BiometricData
from blockchain.facial_recognition_service import compare_faces
import os  # Add this import for checking file existence

def login_face_view(request):
    if request.method == "POST":
        form = LoginFaceForm(request, request.POST, request.FILES)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                image = form.cleaned_data['image']

                try:
                    user_biometric = BiometricData.objects.get(user=user)
                except BiometricData.DoesNotExist:
                    user_biometric = None

                known_face_encoding = user_biometric.get_encoding()
                if known_face_encoding:

                    if compare_faces(known_face_encoding, image.read()):
                        login(request, user)
                        return redirect('dashboard')
                    else:
                        form.add_error('image', 'Face not recognized. Please try again.')
                        print("Face not recognized. Please try again.")
                else:
                    form.add_error(None, 'Biometric data not found for the user.')
                    print("Biometric data not found for the user.")
            else:
                form.add_error(None, 'Invalid username or password')
                print("Invalid username or password")
    else:
        form = LoginFaceForm()
    return render(request, 'attendance/login_face.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('login_face')


@login_required
def dashboard(request):
    if request.user.is_authenticated:
        user_attendance_records = AttendanceRecord.objects.filter(user=request.user).order_by('-date')
        context = {
            'attendance_records': user_attendance_records
        }
        return render(request, 'attendance/dashboard.html', context)
    else:
        return redirect('login_face')



@login_required
def mark_attendance_view(request):
    if request.method == "POST":
        form = LoginFaceForm(request, request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            date_today = date.today()

            # Check if a record already exists for the user and date
            existing_record = AttendanceRecord.objects.filter(user=user, date=date_today).first()

            if existing_record:
                # If a record exists, you can display a message or take any other action
                form.add_error('image', 'Attendance already marked for today.')
                return render(request, 'attendance/mark_attendance.html', {'form': form})

            # Create a new record
            AttendanceRecord.objects.create(user=user, date=date_today, authentication_method='facial', status='P')

            tx_hash = mark_attendance(str(user.id), str(date_today))
            return redirect('dashboard')
        else:
            form.add_error('image', 'Face not recognized. Please try again.')
    else:
        form = LoginFaceForm()

    return render(request, 'attendance/mark_attendance.html', {'form': form})
