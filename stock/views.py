from django.shortcuts import render
from .models import User
from .forms import RegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages

# สร้างฟังก์ชันเรียกหน้า html ที่เราสร้างขึ้นมา
def index(request):
    return render(request, 'frontend/index.html')

# ฟังก์ชันเรียกหน้า login.html
def login(request):
    return render(request, 'auth/login.html')

# ฟังก์ชันเรียกหน้า register.html
def register(request):
    # เช็คว่าผู้ใช้ submit form มาหรือไม่
    if request.method == 'POST':
        # สร้างฟอร์มจากคลาส RegistrationForm
        form = RegisterForm(request.POST)

        # เช็คความถูกต้องของข้อมูล
        if form.is_valid():
            # ดึงข้อมูลจากฟอร์ม
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = make_password(form.cleaned_data['password'])

            # บันทึกข้อมูลลงฐานข้อมูล
            user = User(
                firstname=firstname,
                lastname=lastname,
                email=email,
                username=username,
                password=password
            )
            user.save()

            # แสดงข้อความแจ้งเตือน
            messages.success(request, '<div class="alert alert-success text-center">บันทึกข้อมูลเรียบร้อยแล้ว</div>')
        else:
            form = RegisterForm()
            messages.error(request, '<div class="alert alert-danger text-center">ข้อมูลไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง</div>')

    return render(request, 'auth/register.html')

# ฟังก์ชันเรียกหน้า dashboard.html
def dashboard(request):
    return render(request, 'backend/dashboard.html')

# ฟังก์ชันเรียกหน้า product.html
def product(request):
    return render(request, 'backend/product.html')