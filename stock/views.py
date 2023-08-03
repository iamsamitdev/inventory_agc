from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
import random

# Import OpenCV library
import cv2

# Import Product model and DataPoint model
from .models import Product, DataPoint


# สร้างฟังก์ชันเรียกหน้า html ที่เราสร้างขึ้นมา
def index(request):
    return render(request, 'frontend/index.html')


# สร้างฟังก์ชัน login_request with authenticate LoginForm
def login_request(request):
    # เช็คว่าผู้ใช้ submit form มาหรือไม่
    if request.method == 'POST':
        # สร้างฟอร์ม LoginForm และส่งข้อมูลที่ผู้ใช้กรอกเข้าไป
        form = LoginForm(request, data=request.POST)

        # เช็คความถูกต้องของข้อมูล
        if form.is_valid():
            # ดึงข้อมูลผู้ใช้จาก form.cleaned_data ที่ผ่านการตรวจสอบแล้ว
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # ตรวจสอบว่า username และ password ถูกต้องหรือไม่
            user = authenticate(username=username, password=password)

            # ถ้า username และ password ถูกต้อง
            if user is not None:
                # สร้าง session ให้ผู้ใช้
                login(request, user)

                # ส่งกลับไปหน้า dashboard
                return redirect('dashboard')
    else:
        # สร้างฟอร์ม LoginForm
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


# ฟังก์ชัน register_request with RegisterForm
def register_request(request):

    # เช็คว่าผู้ใช้ submit form มาหรือไม่
    if request.method == 'POST':
        # สร้างฟอร์มจากคลาส RegisterForm
        form = RegisterForm(request.POST)

        # เช็คความถูกต้องของข้อมูล
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


# ฟังก์ชันเรียกหน้า dashboard.html
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'backend/dashboard.html')


# ฟังก์ชันเรียกหน้า product.html
@login_required(login_url='login')
def product(request):
    # ดึงข้อมูลสินค้าทั้งหมด
    # products = Product.objects.all()  # select * from product
    # products = Product.objects.filter(product_price__gt=1000 , product_qty__lt=10)
    products = Product.objects.filter(
        Q(product_price__gt=1000) | Q(product_qty__lt=10))
    return render(request, 'backend/product.html', {'products': products})


# ฟังก์ชันเรียกหน้า create_product.html
@login_required(login_url='login')
def create_product(request):
    if request.method != 'POST':
        # Render the form to create a new product
        return render(request, 'backend/create_product.html')
    # Retrieve data from the request
    product_name = request.POST['product_name']
    product_detail = request.POST['product_detail']
    product_barcode = request.POST['product_barcode']
    product_qty = request.POST['product_qty']
    product_price = request.POST['product_price']
    product_image = request.POST['product_image']
    product_status = request.POST['product_status']

    # Create a new product instance
    product = Product(
        product_name=product_name,
        product_detail=product_detail,
        product_barcode=product_barcode,
        product_qty=product_qty,
        product_price=product_price,
        product_image=product_image,
        product_status=product_status
    )

    # Save the product to the database
    product.save()

    # Optionally, you can redirect to a success page or return a response
    return redirect('product')


# ฟังก์ชันออกจากระบบ
@login_required(login_url='login')
def logout_request(request):
    # ออกจากระบบ
    logout(request)
    # ส่งกลับไปหน้า login
    return redirect('login')


# ฟังก์ชันแสดง chart
@login_required(login_url='login')
def chart(request):

    # ดึงข้อมูลจาก DataPoint ทั้งหมด
    data_points = DataPoint.objects.all()

    # ดึงค่า x_value มาเก็บใน list [1,2,3,4,5]
    x_values = [dp.x_value for dp in data_points]

    # ดึงค่า y_value มาเก็บใน list  [100,200,300,400,500]
    y_values = [dp.y_value for dp in data_points]

    return render(request, 'backend/chart.html', {'x_values': x_values, 'y_values': y_values})


# ฟังก์ชันแสดง video webcam
@login_required(login_url='login')
def capture(request):
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Read a frame from the webcam
    ret, frame = cap.read()

    # Release the webcam
    cap.release()

    # Convert the frame to JPEG format
    _, jpeg_image = cv2.imencode('.jpg', frame)

    # Create the HTTP response with the image
    response = HttpResponse(content_type='image/jpeg')
    # Save the image to a static path
    # random name for image with random number
    image_name = f'{random.randint(1, 100000)}.jpg'
    cv2.imwrite(f'static/images/{image_name}', frame)

    # return response
    return render(request, 'backend/capture.html', {'image_data': response})
