from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import User


class UserCreationForm(BaseUserCreationForm[User]):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ("email",)


class UserChangeForm(BaseUserChangeForm[User]):
    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = ("email",)