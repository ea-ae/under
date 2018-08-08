from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import EmailField, EmailInput, BooleanField
from django.utils.translation import gettext_lazy as _


class CustomLoginForm(AuthenticationForm):
    remember_me = BooleanField(label=_('Remember Me'),
                               initial=False,
                               required=False)


class CustomUserCreationForm(UserCreationForm):
    email = EmailField(
        label=_('Email address (optional)'),
        widget=EmailInput,
        help_text=_('Enter your email address (optional).'),
        required=False,
    )
    remember_me = BooleanField(label=_('Remember Me'),
                               initial=False,
                               required=False)
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'username_blacklisted': _("This username is blacklisted."),
    }

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)
        field_classes = {'username': UsernameField}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
