from django.db import models
from django import forms
from django.forms import ModelForm
from django.conf import settings
from .generator import short_token, long_token, get_code_expiry, get_token_expiry

try:
    from django.utils import timezone
except ImportError:
    timezone = None

SCOPE = (
    ('EMAIL', 'email'),
    ('FIRSTNAME', 'first_name'),
    ('LASNAME', 'last_name'),
)


class UserData(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()

    def __str__(self):
        return self.user_id


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserData
        fields = ('login', 'password', 'first_name', 'last_name', 'email')


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    url = models.URLField(help_text="Your main application's URL.")
    redirect_uri = models.URLField(help_text="Your application's callback URL")
    client_id = models.CharField(max_length=255, default=short_token)
    client_secret = models.CharField(max_length=255, default=long_token)

    def __str__(self):
        return self.redirect_uri


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'url', 'redirect_uri']


class Grant(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    code = models.CharField(max_length=255, default=long_token)
    expires = models.DateTimeField(default=get_code_expiry)
    redirect_uri = models.CharField(max_length=255, blank=True)
    scope = models.CharField(max_length=50, choices=SCOPE)

    class Meta:
        unique_together = ('code', 'user', 'client',)

    def __str__(self):
        return self.code


class AccessToken(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, default=long_token, db_index=True)
    expires = models.DateTimeField(default=get_token_expiry)
    scope = models.CharField(max_length=50, choices=SCOPE)

    def __str__(self):
        return self.token


class RefreshToken(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, default=long_token)
    access_token = models.OneToOneField(AccessToken,
                                        related_name='refresh_token', on_delete=models.CASCADE)
    expired = models.BooleanField(default=False)

    def __str__(self):
        return self.token
