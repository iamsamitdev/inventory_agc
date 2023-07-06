from django import forms

# สร้างคลาส RegisterForm สำหรับใช้ในการ validate ข้อมูลจากฟอร์ม
class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


# สร้างคลาส LoginForm สำหรับใช้ในการ validate ข้อมูลจากฟอร์ม
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)