from django.shortcuts import render

# สร้างฟังก์ชันเรียกหน้า html ที่เราสร้างขึ้นมา
def index(request):
    return render(request, 'frontend/index.html')

# ฟังก์ชันเรียกหน้า login.html
def login(request):
    return render(request, 'auth/login.html')

# ฟังก์ชันเรียกหน้า register.html
def register(request):
    return render(request, 'auth/register.html')

# ฟังก์ชันเรียกหน้า dashboard.html
def dashboard(request):
    return render(request, 'backend/dashboard.html')

# ฟังก์ชันเรียกหน้า product.html
def product(request):
    return render(request, 'backend/product.html')