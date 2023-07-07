from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 

# สร้างคลาส LoginForm สำหรับใช้ในการ validate ข้อมูลจากฟอร์ม
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control form-control-user", "placeholder": "Username"}),
        error_messages={
            'required': 'กรุณากรอกชื่อผู้ใช้',
        }
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-user", "placeholder": "Password"}),
        error_messages={
            'required': 'กรุณากรอกรหัสผ่าน',
        }
    )
    model = User
    fields = ['username', 'password']

    # Custom error message
    error_messages = {
        'invalid_login': 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง',
        'inactive': 'บัญชีนี้ถูกปิดใช้งาน',
    }

# สร้างคลาส RegisterForm สำหรับใช้ในการ validate ข้อมูลจากฟอร์ม
class RegisterForm(UserCreationForm):
    firstname = forms.CharField(
        label="Firstname",
        widget=forms.TextInput(attrs={"class": "form-control form-control-user", "placeholder": "Firstname"}),
        error_messages={
            'required': 'กรุณากรอกชื่อ',
        }
    )
    lastname = forms.CharField(
        label="Lastname",
        widget=forms.TextInput(attrs={"class": "form-control form-control-user", "placeholder": "Lastname"}),
        error_messages={
            'required': 'กรุณากรอกนามสกุล',
        }
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control form-control-user", "placeholder": "Email"}),
        error_messages={
            'required': 'กรุณากรอกอีเมล',
            'invalid': 'กรุณากรอกอีเมลให้ถูกต้อง'
        }
    )

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control form-control-user", "placeholder": "Username"}),
        error_messages={
            'required': 'กรุณากรอกชื่อผู้ใช้',
        }
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-user", "placeholder": "Password"}),
        error_messages={
            'required': 'กรุณากรอกรหัสผ่าน',
        }
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control form-control-user", "placeholder": "Confirm Password"}),
        error_messages={
            'required': 'กรุณากรอกรหัสผ่านอีกครั้ง',
        }
    )

    model = User
    fields = ['username', 'firstname', 'lastname', 'email', 'password1', 'password2']

    # Custom error message
    error_messages = {
        'password_mismatch': 'รหัสผ่านไม่ตรงกัน',
    }

    # override save method
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

