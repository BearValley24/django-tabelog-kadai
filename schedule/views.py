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

class Calendar(TemplateView):
    template_name = 'schedule/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today
        
        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for minute in range(9,18): # 店舗の営業時間ごとに可変にしたい
            row = {}
            for day in days:
                row[day] = True
            calendar[minute] = row

        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        #context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        
        return context
    

class Booking(CreateView):
    model = Schedule
    fields = ('name',)
    template_name = 'schedule/booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start = datetime.datetime(year=year, month=month, day=day, hour=hour)
        end = datetime.datetime(year=year, month=month, day=day, hour=hour + 1)
        if Schedule.objects.filter(start=start).exists():
            messages.error(self.request, 'すみません、入れ違いで予約がありました。別の日時はどうですか。')
        else:
            schedule = form.save(commit=False)
            schedule.start = start
            schedule.end = end
            schedule.save()
        return redirect('schedule:calendar', year=year, month=month, day=day)

class Calendar2(ListView):
    template_name = 'schedule/calendar.html'
    model = Shop
    context_object_name = 'shop'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()    

        print(self.kwargs['input_data']) # PKを取得
        idx = self.kwargs['input_data']
        res = Shop.objects.get(pk=int(idx))
        print(res.startHour)

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは2週間分表示するので、基準日から2週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(14)]
        start_day = days[0]
        end_day = days[-1]

        start_hour = res.startHour
        end_hour = res.endHour
        start_range = int(start_hour.hour)
        if start_hour <= end_hour:
            end_range = int(end_hour.hour)+1
        else:
            end_range = int(end_hour.hour)+25

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for minute in range(start_range, end_range): # 店舗の営業時間ごとに可変にしたい 深夜営業帯をどう定義するのか　深夜1時＝25時　Datetimeの場合はStarthour基準でEndhourが翌朝閉店なら日付を1日を追加
            row = {}
            for day in days:
                row[day] = True
            calendar[minute] = row 

        context['shop_name'] = res # ShopをCalendar2.htmlで使用可能にする
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        #context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        
        return context
    
class ScheduleDelete(DeleteView):
    model = Schedule
    success_url = reverse_lazy('accounts:mypage')
