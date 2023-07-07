from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
import csv
import subprocess

# Import Product model
from .models import Product, DataPoint, Person

# สร้างฟังก์ชันเรียกหน้า html ที่เราสร้างขึ้นมา
def index(request):
    return render(request, 'frontend/index.html')


# สร้างฟังก์ชัน login_request with authenticate LoginForm
def login_request(request):

    # ถ้าล็อกอินแล้วให้ไปหน้า dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    # เช็คว่าผู้ใช้ submit form มาหรือไม่
    if request.method == 'POST':
        # สร้างฟอร์มจากคลาส LoginForm
        form = LoginForm(request, data=request.POST)

        # เช็คความถูกต้องของข้อมูล
        if form.is_valid():
            # ดึงข้อมูลจากฟอร์ม
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # ตรวจสอบว่า username และ password ถูกต้องหรือไม่
            user = authenticate(username=username, password=password)
            if user is not None:

                login(request, user)
                # สร้าง session สำหรับเก็บข้อมูลผู้ใช้
                # request.session['username'] = user.username
                # request.session['firstname'] = user.first_name
                # request.session['lastname'] = user.last_name

                # ส่งกลับไปหน้า dashboard
                return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


# ฟังก์ชัน register_request with RegisterForm
def register_request(request):

    # ถ้าล็อกอินแล้วให้ไปหน้า dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    
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


# helper function for pass session to template
def get_session_data(request):
    username = request.session.get('username')
    firstname = request.session.get('firstname')
    lastname = request.session.get('lastname')
    return {'username': username, 'firstname': firstname, 'lastname': lastname}


# ฟังก์ชัน dashboard
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'backend/dashboard.html')


# ฟังก์ชัน product แสดงรายการสินค้าทั้งหมด
@login_required(login_url='login')
def product(request):

    # Read all product from database
    products = Product.objects.all()

    # Retrive data from form
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_detail = request.POST.get('product_detail')
        product_barcode = request.POST.get('product_barcode')
        product_qty = request.POST.get('product_qty')
        product_price = request.POST.get('product_price')
        product_image = request.POST.get('product_image')
        product_status = request.POST.get('product_status')

        # Create Product
        product = Product(
            product_name=product_name,
            product_detail=product_detail,
            product_barcode=product_barcode,
            product_qty=product_qty,
            product_price=product_price,
            product_image=product_image,
            product_status=product_status
        )

        product.save()
        messages.success(request, 'Product has been created successfully.')

    return render(request, 'backend/product.html', {'products': products})


# ฟังก์ชันเพิ่มสินค้า
@login_required(login_url='login')
def create_product(request):
    if request.method == 'POST':
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
    else:
        # Render the form to create a new product
        return render(request, 'backend/create_product.html')


# ฟังก์ชันดึงสินค้าตาม id
@login_required(login_url='login')
def get_product(request, product_id):
    # Retrieve the product with the given ID
    product = get_object_or_404(Product, pk=product_id)

    # Render the product details
    return render(request, 'backend/product_detail.html', {'product': product})


# ฟังก์ชันแก้ไขสินค้า
@login_required(login_url='login')
def update_product(request, product_id):
    # Retrieve the product with the given ID
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Update the product fields
        product.product_name = request.POST['product_name']
        product.product_detail = request.POST['product_detail']
        product.product_barcode = request.POST['product_barcode']
        product.product_qty = request.POST['product_qty']
        product.product_price = request.POST['product_price']
        product.product_image = request.POST['product_image']
        product.product_status = request.POST['product_status']

        # Save the updated product to the database
        product.save()

        # Optionally, you can redirect to a success page or return a response
        return redirect('product', product_id=product_id)
    else:
        # Render the form to update the product
        return render(request, 'backend/update_product.html', {'product': product})


# ฟังก์ชันลบสินค้า
@login_required(login_url='login')
def delete_product(request, product_id):
    # Retrieve the product with the given ID
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Delete the product
        product.delete()

        # Optionally, you can redirect to a success page or return a response
        return redirect('product')
    else:
        # Render the confirmation page to delete the product
        return render(request, 'backend/delete_product.html', {'product': product})


# ฟังก์ชันออกจากระบบ
@login_required(login_url='login')
def logout_request(request):
    # ออกจากระบบ
    logout(request) 

    # ลบ session ทั้งหมด
    request.session.flush()

    # ส่งกลับไปหน้า login
    return redirect('login')


# chart_view
@login_required(login_url='login')
def chart_view(request):

    # ดึงข้อมูลจากฐานข้อมูล
    data_points = DataPoint.objects.all()

    x_values = [dp.x_value for dp in data_points] # ดึงข้อมูล x_value มาเก็บไว้ในตัวแปร x_values
    y_values = [dp.y_value for dp in data_points] # ดึงข้อมูล y_value มาเก็บไว้ในตัวแปร y_values

    return render(request, 'backend/chart.html', {'x_values': x_values, 'y_values': y_values})


# Import CSV Data
@login_required(login_url='login')
def import_csv(request):
    #  Open CSV file in static folder
    with open('static/csv/file.csv', 'r') as file:
        # Read CSV file
        reader = csv.DictReader(file)

        # Skip the header row
        next(reader)

        # Loop over each row in the CSV file
        for row in reader:
            Person.objects.create(
                name=row['name'],
                age=row['age'],
                gender=row['gender']
            )

# Realtime Streamlit
@login_required(login_url='login')
def dashboardrealtime(request):
    subprocess.Popen["streamlit", "run", "dashboardrealtime.py"]
    return render(request, 'backend/dashboardrealtime.html')