from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User
from django import forms
from django.utils.translation import gettext_lazy as _

import re

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "account_id",
            "email",
        )
        labels = {
            'account_id':'アカウント名',
            'email':'メールアドレス'
        }
    def clean_account_id(self):
        account_id = self.cleaned_data['account_id']
        if contains_disallowed_chars(account_id):
            raise forms.ValidationError("ユーザー名に禁止文字「@」が含まれています。")
        return account_id
    
def contains_disallowed_chars(username):
    disallowed_chars = re.compile(r'[@]')
    return bool(disallowed_chars.search(username))


# ログインフォームを追加
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = (
            'account_id',
            'password',
        )


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
