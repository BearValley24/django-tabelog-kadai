from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Review
from django import forms

import re

class ReviewCreateForm(UserCreationForm):
    class Meta:
        model = Review
        fields = (
            'reviewStar',
            'reviewComment',
        )