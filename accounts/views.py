from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
)
from django.urls import reverse_lazy, reverse
from .forms import SignUpForm, LoginForm,MyPasswordChangeForm
from dotenv import load_dotenv
from .models import User,Kiyaku
from shops.models import Shop, ShopTag # Shopモデルをインポート
from schedule.models import Schedule
from review.models import Review
from django.db.models import Avg, Q
from django.contrib import messages
from django.views import View

import os
import requests
import calendar
import datetime
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

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

class IndexView(ListView): 
    # ホームビュー
    template_name = 'index.html'
    model = User
    def get_context_data(self, **kwargs):
        load_dotenv(os.path.join(os.path.dirname(__file__), 'nagoyameshi/.env'))
        context = super().get_context_data(**kwargs)
        context['views_APIkey'] = os.getenv('env_APIkey')
        context['shoptag_list'] = ShopTag.objects.all()
        context['style_css_date'] = get_modified_date('css/top2.css')
        context['style_js_date'] = get_modified_date('js/map.js')
        return context
    #名前検索
    def get_queryset(self):
        query = self.request.GET.get('query')
        selectTag = self.request.GET.get('selectTag')
        
        #デフォルトは表示なし
        if not self.request.GET:
            shop_list = None
            return shop_list
        #検索条件に合わせて表示
        if selectTag != 'all':
            if query:
                if selectTag: #タグと名前検索に入力あり
                    shop_list = Shop.objects.filter(ShopTag=selectTag,shopName__icontains=query)
                else : #名前検索のみ
                    shop_list = Shop.objects.filter(shopName__icontains=query)
            else: #タグのみ
                shop_list = Shop.objects.filter(ShopTag=selectTag)
        else:
            if query: #タグが全店舗で名前検索に入力あり
                shop_list = Shop.objects.filter(shopName__icontains=query)
            else: #タグが全検索のとき
                shop_list = Shop.objects.all()
        return shop_list

class SignupAndLoginView(View):
    def get(self, request, *args, **kwargs):
        signup_form = SignUpForm()
        login_form = LoginForm()
        context = {
            'signup_form': signup_form,
            'login_form': login_form,
            'style_css_date': get_modified_date('css/signup_and_login.css'),
        }
        return render(request, 'accounts/signup_and_login.html', context)

    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(request.POST)
        login_form = LoginForm(request, data=request.POST)

        if 'signup' in request.POST:
            # サインアップフォームの送信処理
            if signup_form.is_valid():
                user = signup_form.save()
                account_id = signup_form.cleaned_data.get('account_id')
                password = signup_form.cleaned_data.get('password1')
                user = authenticate(account_id=account_id, password=password)
                if user is not None:
                    login(request, user)
                return redirect('accounts:index')

        elif 'login' in request.POST:
            # ログインフォームの送信処理
            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('accounts:index')

        # どちらかが無効の場合、再度フォームを表示
        return render(request, 'accounts/signup_and_login.html', {
            'signup_form': signup_form,
            'login_form': login_form,
        })

class LogoutView(BaseLogoutView):
    # ログアウトビュー
    success_url_= reverse_lazy('index') 


class Mypage(TemplateView):
    model = User
    template_name = 'accounts/mypage.html'
    def get(self, request, *args, **kwargs):
        d = datetime.today().date()
        t = datetime.today().time()
        # 親クラスのコンテキストを取得
        context = super().get_context_data(**kwargs)
        context['style_css_date'] = get_modified_date('css/mypage.css')
        context['style_js_date'] = get_modified_date('js/mypage.js')
        # ユーザー情報をコンテキストに追加
        context['user'] = self.request.user
        # お気に入り店舗情報
        favorite_shops = request.user.favorite_shop.all()
        context['favorite_shop_json'] = json.dumps(list(favorite_shops.values('shopName')))

        # 予約（今日以降）とレビューのリストをコンテキストに追加
        user = User.objects.get(pk=self.request.user.pk) 
        schedule_queryset = Schedule.objects.filter(account=user, startDate__gte=d)  
        # 今日日付で現在時刻より前の予約はキャンセル不可なので表示しない
        schedule_queryset=schedule_queryset.exclude(startDate=d,startHour__lte=t) 
        schedule_list = list(schedule_queryset.values('shop_name', 'startDate', 'startHour', 'name', 'numbers', 'pk'))
        review_queryset = Review.objects.filter(reviewUserName=request.user)
        review_list = []

        # 各スケジュールにキャンセルURLを追加
        for schedule in schedule_list:
            schedule['cancel_url'] = reverse('schedule:delete', args=[schedule['pk']])

        # 各レビューに編集URLを追加
        for review in review_queryset:
            review_list.append({
                'reviewShopName': review.reviewShopName.shopName,
                'reviewStar': review.reviewStar,
                'reviewComment': review.reviewComment,
                'cancel_url_review': reverse('review:UpdateReview', args=[review.pk])   
            })

        context['schedule_list'] = schedule_list
        context['review_list_json'] = json.dumps(review_list, cls=DjangoJSONEncoder)
        context['schedule_list_json'] = json.dumps(schedule_list, cls=DjangoJSONEncoder)
        return render(request, self.template_name, context)
        
    def post(self, request, *args, **kwargs):
        user = User.objects.get(account_id = request.user)
        # お気に入り店舗を削除
        if 'delete-favorite-shop' in request.POST:
            delete_shop_name = request.POST.get('delete-shop')
            delete_shop_id = Shop.objects.get(shopName=delete_shop_name).id
            user.favorite_shop.remove(delete_shop_id)
            user.save()
            return redirect('accounts:mypage')
        elif 'withdrawal-membership' in request.POST:
            # ユーザー自身による退会処理
            user.delete()
            return redirect('accounts:index')
        
def followShop(request, pk):
    f_shop = get_object_or_404(Shop, pk=pk)
    request.user.favorite_shop.add(f_shop)
    return redirect('accounts:mypage')

class CountMember(TemplateView):    
    template_name = 'accounts/kanrisha.html'
    def get(self, request, *args, **kwargs):
        context = {
            'style_css_date': get_modified_date('css/kanrisha.css'),
            'dateUser': '-',
            'allShop': Shop.objects.count(),
            'Shops': Shop.objects.all(),
            'countTag': ShopTag.objects.count(),
            'allTag': ShopTag.objects.all(),
        }
        return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        model = User
        context = super().get_context_data(**kwargs)
        context = {
            'style_css_date': get_modified_date('css/kanrisha.css'),
            'dateUser': '-',
            'allShop': Shop.objects.count(),
            'Shops': Shop.objects.all(),
            'countTag': ShopTag.objects.count(),
            'allTag': ShopTag.objects.all(),
        }
        if 'numberSearch' in request.POST:
            #入力された年月日を受け取りmodelを検索する
            inputYear = request.POST.get('inputYear')
            inputMonth = request.POST.get('inputMonth')
            inputDate = request.POST.get('inputDate')
            inputSubscription = request.POST.get('subscription')
            if inputSubscription == 'True':
                resultSubscription = '無料会員'
            else:
                resultSubscription = '有料会員'
            #年単位/月単位/日単位の判定
            #年の入力判定
            if inputYear == '':
                #全期間
                if inputSubscription == 'all':
                    context['errMsg'] = '全期間の全会員で検索'
                    context['dateUser'] = User.objects.count() 
                    return render(request, self.template_name, context)
                else:
                    context['errMsg'] = f'全期間の{resultSubscription}で検索'
                    context['dateUser'] = User.objects.filter(rank_is_free=inputSubscription).count() 
                    return render(request, self.template_name, context)
            else:
                #年OK
                resultYear = inputYear
                #月の入力判定
                if inputMonth == 'all':
                    #入力された年の1月1日から12月31日まで
                    startRange = f"{resultYear}-01-01"
                    endRange = f"{resultYear}-12-31"
                    if inputSubscription == 'all':
                        context['errMsg'] = f"{resultYear}年の1年間に登録された会員数"
                        context['dateUser'] = User.objects.filter(created_at__gte=startRange,created_at__lte=endRange).count() 
                        return render(request, self.template_name, context)
                    else:
                        context['errMsg'] = f"{resultYear}年の1年間に登録された{resultSubscription}の会員数"
                        context['dateUser'] = User.objects.filter(created_at__gte=startRange,created_at__lte=endRange,rank_is_free=inputSubscription).count() 
                        return render(request, self.template_name, context)
                else:
                    #月OK
                    resultMonth = inputMonth
                    #日の判定
                    if inputDate == 'all':
                        #入力された月の月末まで
                        startRange = f"{resultYear}-{resultMonth}-01"
                        monthEnd = calendar.monthrange(int(resultYear),int(resultMonth))[1]
                        endRange = f"{resultYear}-{resultMonth}-{monthEnd}"
                        if inputSubscription == 'all':
                            context['errMsg'] = f'{resultYear}年{resultMonth}月の1か月間に登録された会員数'
                            context['dateUser'] = User.objects.filter(created_at__gte=startRange,created_at__lte=endRange).count() 
                            return render(request, self.template_name, context)
                        else:
                            context['errMsg'] = f'{resultYear}年{resultMonth}月の1か月間に登録された{resultSubscription}の会員数'
                            context['dateUser'] = User.objects.filter(created_at__gte=startRange,created_at__lte=endRange,rank_is_free=inputSubscription).count() 
                            return render(request, self.template_name, context)
                    else:
                        #年OK月OK日OK
                        resultDate = inputDate
                        resultInput = f"{resultYear}-{resultMonth}-{resultDate}"
                        if inputSubscription == 'all':
                            context['errMsg'] = f'{resultYear}年{resultMonth}月{resultDate}日の1日間に登録された会員数'
                            context['dateUser'] = User.objects.filter(created_at=resultInput).count() 
                            return render(request, self.template_name, context)      
                        else:
                            context['errMsg'] = f'{resultYear}年{resultMonth}月{resultDate}日の1日間に登録された{resultSubscription}の会員数'
                            context['dateUser'] = User.objects.filter(created_at=resultInput,rank_is_free=inputSubscription).count() 
                            return render(request, self.template_name, context)
        elif 'memberSearch' in request.POST:
            searchContext = request.POST.get('memberSearchContext')
            if not searchContext:
                context['errMsg1'] = '検索語句が入力されていません'
                return render(request, self.template_name, context)
            else:
                context['searchResult'] = User.objects.filter(
                    Q(account_id__icontains = searchContext) |
                    Q(email__icontains = searchContext) |
                    Q(first_name__icontains = searchContext) |
                    Q(last_name__icontains = searchContext) 
                ).distinct()
            return render(request, self.template_name, context)
        elif 'tagSearch' in request.POST:
            #カテゴリ検索
            searchTag = request.POST.get('tagSearchContext')
            context = {
                'countTag': ShopTag.objects.count(),
                'allTag': ShopTag.objects.all(),
            }
            context['resultTag'] = ShopTag.objects.filter(tag__icontains=searchTag)
            return render(request, self.template_name, context)
        elif 'tagDelete' in request.POST:
            #カテゴリ削除
            delteteTagPK = request.POST.get('targetTagPK')
            ShopTag.objects.get(pk=delteteTagPK).delete()
            context['sucMsg'] = 'カテゴリを削除しました。'
            return render(request, self.template_name, context)
        elif 'tagEdit' in request.POST:
            #カテゴリ編集
            editTagPK = request.POST.get('targetTagPK')
            editTagContext = request.POST.get('targetTagContext')
            if editTagContext:
                targetTag = ShopTag.objects.get(pk=editTagPK)
                targetTag.tag = editTagContext
                targetTag.save()
                context['sucMsg'] = 'カテゴリ名を変更しました。'
                return render(request, self.template_name, context)
            else:
                context['sucMsg'] = '空白のカテゴリ名は登録出来ません。'
                return render(request, self.template_name, context)
        elif 'tagAdd' in request.POST:
            #カテゴリ追加
            addTagContext = request.POST.get('addTagContext')
            if addTagContext:
                newTag = ShopTag()
                newTag.tag = addTagContext
                newTag.save()
                context['sucMsg'] = 'カテゴリを追加しました。追加されたカテゴリを店舗に付与する場合は店舗編集画面で追加してください。'
                return render(request, self.template_name, context)

    
    
class memberDelete(DeleteView):
    # 管理者によるユーザー削除
    model = User
    template_name = 'accounts/member_delete.html'  
    def get_context_data(self, **kwargs):
        # デフォルトのコンテキストデータを取得
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        context['targetUser'] = User.objects.get(pk=pk)
        return context
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        if 'memberDelete' in request.POST:
            targetUser = User.objects.get(pk=pk)
            targetUser.delete()
            context['resMsg'] = f'{targetUser.account_id}を削除しました'
            return render(request, 'accounts/kanrisha.html',context)

class memberUpdate(UpdateView):
    model = User
    fields = (
        'account_id',
        'email',
        'first_name',
        'last_name',
        'birth_date',
    )
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('shops:success') 
    def get_context_data(self, **kwargs):
        # 親クラスのコンテキストを取得
        context = super().get_context_data(**kwargs)
        context['style_css_date'] = get_modified_date('css/member_update.css')
        return context


        

class kiyaku(TemplateView):
    #規約は１つだけ
    model = Kiyaku
    template_name = 'accounts/kiyaku.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['original_kiyaku'] = Kiyaku.objects.get(kiyakuName='基本規約')
        context['style_css_date'] = get_modified_date('css/kiyaku2.css')
        context['style_js_date'] = get_modified_date('js/kiyaku.js')
        return context
    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        inputKiyaku = self.request.POST.get('inputKiyaku')
        originalKiyaku = Kiyaku.objects.get(kiyakuName='基本規約')
        originalKiyaku.kiyakuContent = inputKiyaku
        lastUpdater = self.request.POST.get('updater')
        originalKiyaku.lastUpdater = User.objects.get(account_id=lastUpdater)
        originalKiyaku.save()
        context['msg'] = '編集完了'
        context['original_kiyaku'] = Kiyaku.objects.get(kiyakuName='基本規約')
        context['style_css_date'] = get_modified_date('css/kiyaku2.css')
        context['style_js_date'] = get_modified_date('js/kiyaku.js')
        return render(request, 'accounts/kiyaku.html', context)

class passwordChange(PasswordChangeView):
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'

class passwordChangeDone(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
