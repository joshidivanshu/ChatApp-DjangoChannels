from .models import ChatGroup
from django import forms

class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = "__all__"