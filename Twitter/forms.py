from django import forms
from Main.models import UserProfile, Tweet
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	website = forms.URLField(required=False)
	class Meta:
		model = UserProfile
		fields = ('website',)


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ["user", 'date', 'favourite', 'retweet', 'replies','username', "is_ret", "retweeter"]

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)
