from django.contrib.auth import password_validation

from .models import CustomUser
from django.core import mail
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomForm(forms.ModelForm):
    error_messages={
        'password_mismatch': "The two password fields didn't match.",
    }
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder":"Username"}),

    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder":"Email"})
    )
    phone = forms.CharField(
        widget=forms.NumberInput(attrs={"placeholder":"Phone"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"Password"}),
        error_messages={'required':'input miss match'}
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}),
        error_messages={'required': 'input miss match'}
    )

    class Meta:
        model = CustomUser
        fields = ('username','email','phone','password','password2')

    def __init__(self, *args, **kwargs):
        super(CustomForm, self).__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self,datas):
        u = CustomUser.objects.create_user(
            datas['username'],
            datas['email'],
            datas['password']
        )
        u.is_active = False
        u.phone = datas['phone']
        u.activationKey = datas['activationKey']
        u.save()
        return u
    def send_email(self,datas):
        connection = mail.get_connection(fail_silently=False)
        connection.open()
        message = mail.EmailMessage(
            'Hello',
            'http://127.0.0.1:8080/auth/verify/' + datas['activationKey'],
            'carrymartes@gmail.com',
            [datas['email']],
            connection=connection,
        )
        connection.send_messages([message])
        connection.close()


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'placeholder':'Login'}
        )
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
