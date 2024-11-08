from django.shortcuts import render, redirect
from django.views.generic import  TemplateView, ListView, CreateView, DeleteView, UpdateView
from accounts.models import User
from shops.models import Shop
from .models import Review
from .forms import ReviewCreateForm
from django.views.generic.edit import FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages

import datetime
import requests

# Create your views here.
from django.templatetags.static import static
from django.conf import settings
from datetime import datetime, timedelta, timezone
import os
def get_modified_date(filepath):
    try:
        static_file_path = static(filepath)
        base_dir = settings.BASE_DIR
        static_file_url = os.path.join(base_dir, *static_file_path.split("/"))

        modified_serial_time = os.path.getmtime(static_file_url)
        modified_date = datetime.fromtimestamp(modified_serial_time).strftime("%Y%m%d%H%M%S")

        return modified_date

    except:
        return ''

from django.utils import timezone

class reviewUpdate(UpdateView):
    template_name = 'review/review_update.html'
    model = Review
    #fields = '__all__'
    fields = (
            'reviewStar',
            'reviewComment',
        )
    def post(self, request, *args, **kwargs):
        #削除処理
        if 'review-delete' in request.POST:
            self.object = self.get_object()  
            self.object.delete()
            context = {'suc':'レビューを削除しました。'}
            return render(request,'shops/result_success.html', context)
        #アップデート処理
        self.object = self.get_object()
        self.object.reviewStar = request.POST.get('reviewStar')
        self.object.reviewComment = request.POST.get('reviewComment')
        self.object.reviewUpdated = timezone.now()
        self.object.save()
        context = {'suc':'レビューの編集が完了しました。'}
        return render(request,'shops/result_success.html', context)

class reviewDelete(DeleteView):
    template_name = 'review/review_delete.html'
    model = Review
    

class reviewDisplay(TemplateView):
    template_name = 'review/review_display.html'
    model = Review
    context_object_name = 'reviews'  # テンプレートで使用するコンテキスト名を指定
    #kokomade ok
    
    def get_queryset(self):
        # URLのpkからユーザーを取得し、そのユーザーに関連するレビューのみを返す
        user_pk = self.kwargs.get('pk')
        user = User.objects.get(pk=user_pk)
        return Review.objects.filter(reviewUserName=user)

    def get_context_data(self, **kwargs):
        # デフォルトのコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        # ユーザーオブジェクトをコンテキストに追加
        user = User.objects.get(pk=self.kwargs.get('pk'))
        context['user'] = user
        context['reviews'] = Review.objects.filter(reviewUserName=user)
        context['style_css_date'] = get_modified_date('css/review_display.css')
        return context
        
    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs.get('pk')
        reviewPk = request.POST.get('commentDelete')
        if not reviewPk :
            messages.error(request, '削除するコメントを選択して下さい')
            return redirect(reverse('review:DisplayReview', args=[user_pk]))
        else:
            #選択されたレビューの完全削除
            targetReview = Review.objects.get(pk=reviewPk)
            targetReview.delete()
            return redirect(reverse('review:DisplayReview', args=[user_pk]))

                
    def display_review(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('pk')
        context = self.get_context_data(**kwargs)

        # messagesをデバッグ表示
        print(messages.get_messages(request))  # これでメッセージの内容を確認
        return render(request, 'review/display_review.html', context)