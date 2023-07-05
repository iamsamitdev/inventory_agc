from django.shortcuts import render

# สร้างฟังก์ชันเรียกหน้า html ที่เราสร้างขึ้นมา
def index(request):
    return render(request, 'frontend/index.html')

# ฟังก์ชันเรียกหน้า login.html
def login(request):
    return render(request, 'auth/login.html')
