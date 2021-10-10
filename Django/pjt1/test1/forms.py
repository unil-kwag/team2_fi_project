from django.db.models.base import Model
from django.forms import ModelForm
from .models import *

class Form(ModelForm):
    class Meta:
        model = Bus
        fields = '__all__'