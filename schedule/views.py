from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import  TemplateView, ListView, CreateView, DeleteView
from django.conf import settings
from django.contrib import messages
from .models import Schedule
from shops.models import Shop
from django.urls import reverse_lazy

import datetime

# Create your views here.
    
class ScheduleDelete(DeleteView):
    model = Schedule
    success_url = reverse_lazy('accounts:mypage')
