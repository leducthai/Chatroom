from django.forms import ModelForm
from .models import room as Room , message, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'name',
            'username',
            'email',
            'password1',
            'password2',
        ]
class roomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = [
            'host',
            'participants' 
            ]

class messForm(ModelForm):
    class Meta:
        model = message
        fields = '__all__'
        exclude = [
            'user',
            'room'
        ]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'avatar',
            'name',
            'username',
            'email',
            'bio'
        ]