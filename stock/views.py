from django.shortcuts import render, redirect
from .models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

# สร้างฟังก์ชันเรียกหน้า html ที่เราสร้างขึ้นมา
def index(request):
    return render(request, 'frontend/index.html')

# ฟังก์ชันเรียกหน้า login.html
def login(request):
    # เช็คว่าผู้ใช้ submit form มาหรือไม่
    if request.method == 'POST':
        # สร้างฟอร์มจากคลาส LoginForm
        form = LoginForm(request.POST)

        # เช็คความถูกต้องของข้อมูล
        if form.is_valid():
            # ดึงข้อมูลจากฟอร์ม
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # ตรวจสอบว่า username และ password ถูกต้องหรือไม่
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):

                    # แสดงข้อความแจ้งเตือน
                    messages.success(request, '<div class="alert alert-success text-center">เข้าสู่ระบบเรียบร้อยแล้ว</div>')

                    # สร้าง session สำหรับเก็บข้อมูลผู้ใช้
                    request.session['username'] = user.username
                    request.session['firstname'] = user.firstname
                    request.session['lastname'] = user.lastname

                    # ส่งกลับไปหน้า dashboard
                    return redirect('dashboard')
                else:
                    # แสดงข้อความแจ้งเตือน
                    messages.error(request, '<div class="alert alert-danger text-center">ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง</div>')
            except User.DoesNotExist:
                # แสดงข้อความแจ้งเตือน
                messages.error(request, '<div class="alert alert-danger text-center">ไม่พบชื่อผู้ใช้</div>')
        else:
            form = LoginForm()
            # แสดงข้อความแจ้งเตือน
            messages.error(request, '<div class="alert alert-danger text-center">กรุณากรอกข้อมูลก่อน</div>')

    return render(request, 'auth/login.html')

# ฟังก์ชันเรียกหน้า register.html
def register(request):
    # เช็คว่าผู้ใช้ submit form มาหรือไม่
    if request.method == 'POST':
        # สร้างฟอร์มจากคลาส RegisterForm
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
    # เช็คว่ามี session username อยู่หรือไม่
    if not request.session.get('username'):
        return redirect('login')
    else:
        params = {
            'firstname': request.session.get('firstname'),
            'lastname': request.session.get('lastname')
        }
        return render(request, 'backend/dashboard.html', {'params': params})

# ฟังก์ชันเรียกหน้า product.html
def product(request):
    # เช็คว่ามี session username อยู่หรือไม่
    if not request.session.get('username'):
        return redirect('login')
    else:
        params = {
            'firstname': request.session.get('firstname'),
            'lastname': request.session.get('lastname')
        }
        return render(request, 'backend/product.html', {'params': params})


# ฟังก์ชันออกจากระบบ
def logout(request):
    # ลบ session ทั้งหมด
    request.session.flush()
    # ส่งกลับไปหน้า login
    return redirect('login')