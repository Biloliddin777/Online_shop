from django import forms
from django.contrib.auth.models import User

from online_shop.models import Comment, Order, Product

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = ['name','email','body']
        exclude = ('product',)

    def clean_email(self):
        email = self.data.get('email')
        if Comment.objects.filter(email=email).exists():
            raise forms.ValidationError(f'This {email} is already used')
        return email

    def clean_body(self):
        negative_message = ['']
        body = self.data.get('body')
        if negative_message in body.split(' '):
            raise
        return body


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean_username(self):
        username = self.data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'That user {username} not found')
        return username