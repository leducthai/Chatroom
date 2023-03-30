from django.forms import ModelForm
from .models import room as Room , message
from django.contrib.auth.models import User

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
            'username',
            'email'
        ]