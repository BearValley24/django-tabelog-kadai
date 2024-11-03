from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import  TemplateView, ListView, DetailView, UpdateView
from django.views.generic.edit import  CreateView, DeletionMixin
from dotenv import load_dotenv
from django.urls import reverse_lazy
from .models import Shop, ShopTag
from schedule.models import Schedule
from accounts.models import User, Yoyaku_ID
from review.models import Review
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.templatetags.static import static
from django.conf import settings
from .forms import createForm

import requests 


# Create your views here.

#staticのファイル更新日時を取得
#各Views.pyでcontext['style_???_date'] = get_modified_date('css/???.css')
#各TemplateのStaticのリンクの末尾に{% if style_css_date %}?={{ style_css_date }}{% endif %}を追記
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
#ここまで    

class TopView(TemplateView):
    template_name = 'base.html' 
    def get_context_data(self, **kwargs):
        load_dotenv()
        context = super().get_context_data(**kwargs)
        context['style_css_date'] = get_modified_date('css/base2.css')
        #context['shop_list'] = Shop.objects.all()
        context['shop1'] = Shop.objects.get(pk=1)
        return context
        # template_name変数で表示したいHTMLを名称指定する


class ShopListView(ListView):
    model = Shop
    template_name = "list.html"
    #context_object_name = 'shops_list'
    #paginate_by = 3

class ShopCreateView(CreateView):
    model = Shop
    #fields = '__all__'
    form_class = createForm
    template_name = 'shops/shop_create.html'
    success_url_= reverse_lazy('shops:shop_create') 
    success_message = '新規店舗追加成功！'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['style_css_date'] = get_modified_date('css/create.css')
        return context


    
class ShopDetailView3(DetailView):
    model = Shop
    template_name = 'shops/shop_detail_second.html'
    context_object_name = 'shop_detail'
    schedule_data = Schedule.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        td = datetime.today()
        days0 = td.strftime('%Y-%m-%d')
        days1b = td + timedelta(days=1)
        days1 = days1b.strftime('%Y-%m-%d')
        days2b = td + timedelta(days=2)
        days2 = days2b.strftime('%Y-%m-%d')
        context['days'] = {
            'days0': days0,
            'days1': days1,
            'days2': days2,
        }
        context['review_list'] = Review.objects.all()
        context['style_js_date'] = get_modified_date('js/shop_detail.js')
        context['style_css_date'] = get_modified_date('css/shop_detail.css')
        return context
    
    
    def post(self, request, *args, **kwargs):
        td = datetime.today()

        #受け取るもの
        favorite_shop_name = request.POST.get('favorite_shop_name')
        

        #お気に入り店舗の登録
        if favorite_shop_name is not None:
            user = User.objects.get(account_id=request.POST.get('favorite_shop_user'))
            user_favorite_shop = Shop.objects.get(shopName=favorite_shop_name)
            user.favorite_shop.add(user_favorite_shop)
            user.save()
            return redirect('accounts:mypage')
        
        #コメントの登録
        if 'review-create' in request.POST: 
            shopReview_star = request.POST.get('review-star')
            shopReview_comment = request.POST.get('review-comment')
            user = User.objects.get(account_id=request.POST.get('review-user'))
            user_review_shop = Shop.objects.get(shopName=request.POST.get('review-shop'))

            #Reviewオブジェクトの新規作成
            review = Review()  # Reviewのインスタンスを作成
            review.reviewShopName = user_review_shop
            review.reviewUserName = user
            review.reviewStar = shopReview_star
            review.reviewComment = shopReview_comment
            review.save()  # オブジェクトを保存
            return redirect('shops:success')  
        elif 'yoyaku' in request.POST:
            print('yoyaku')
            yoyaku_Date = request.POST.get('yoyaku_form1') #予約日
            yoyaku_Hour = request.POST.get('yoyaku_form2') #予約時
            yoyaku_Memb = int(request.POST.get('yoyaku_form3')) #予約人数
            yoyaku_User = User.objects.get(account_id=request.POST.get('yoyaku_form4')) #予約者名
            yoyaku_Shop = Shop.objects.get(shopName=request.POST.get('yoyaku_form5')) #予約店名   

            #Scheduleオブジェクトを新規作成
            schedule = Schedule()
            schedule.startDate = yoyaku_Date 
            schedule.startHour = yoyaku_Hour
            schedule.name = f"{yoyaku_User.first_name}　{yoyaku_User.last_name}"
            schedule.shop_name = yoyaku_Shop.shopName
            schedule.account = yoyaku_User
            schedule.numbers = yoyaku_Memb
            schedule.save()
            return redirect('accounts:mypage')               

class ResultSuccessView(TemplateView):
    template_name = 'shops/result_success.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['style_css_date'] = get_modified_date('css/success.css')
        return context

class ResultFailureView(TemplateView):
    template_name = 'shops/result_failure.html'

class ShopUpdateView(UpdateView,DeletionMixin):
    model = Shop
    fields = (
        'ShopTag', 
        'shopName', 
        'phoneNumber', 
        'address', 
        'addressLat', 
        'addressLng', 
        'startHour1',
        'endHour1',
        'startHour2',
        'endHour2',
        'image',
        'introduction',
        'regularHoliday',
        )
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('accounts:kanrisha')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['style_css_date'] = get_modified_date('css/shop_update.css')
        return context

class YoyakuCheck(TemplateView):
    #'shop_detail'から営業時間を引っ張る
    def post(self, request, *args, **kwargs):
        if 'yoyaku' in request.POST: #submitにname="yoyaku"を入れる
            model = Shop
            template_name = 'shops/shop_detail_second.html'
            yoyaku_start_time = request.POST.get('yoyaku_start_time')
            use_time = request.POST.get('use_time')
            object_pk = request.POST.get('object_pk')
            yoyaku_shop_name = request.POST.get('shop_name')
            yoyaku_user = request.POST.get('yoyaku_user')
            yoyaku_day_check = request.POST.get('yoyaku_day')
            yoyaku_number = request.POST.get('yoyaku_number')

