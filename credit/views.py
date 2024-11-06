from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.views.generic import TemplateView, UpdateView
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Subscription, SubscriptionPrice
from .models import Transaction 
from accounts.models import User
from django.shortcuts import render, get_object_or_404

import json
import stripe
import os

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

import datetime 

# STRIPEのシークレットキー
stripe.api_key = settings.STRIPE_SECRET_KEY

# WEBHOOKのシークレットキー
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class ProductTopPageView(ListView):
    # 商品マスタ
    model = Subscription
    # ページリンク
    template_name = 'credit/product_top.html'
    #レコード情報をテンプレートに渡すオブジェクト
    context_object_name = "product_list"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['style_css_date'] = get_modified_date('css/product_top.css')
        return context


# 決済画面
class CreateCheckoutSessionView(View):
    
    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # 二重でサブスクリプションに契約することを防止
        if Transaction.objects.filter(user_connection=self.request.user):
            context['err'] = 'あなたは既にサブスクリプションを契約しています。'
            print(context)
            return render(request, 'shops/result_failure.html', context)

        # 商品マスタ呼出
        product = Subscription.objects.get(id=self.kwargs["pk"])
        price   = SubscriptionPrice.objects.get(product=product)

        # ドメイン 検証と本番を分ける
        if os.getenv('DJANGO_ENV') == 'development':
            YOUR_DOMAIN = 'http://127.0.0.1:8000'
        else:
            YOUR_DOMAIN = 'https://nagoyameshi-rk3942-2c70d196cf95.herokuapp.com'

        # 決済用セッション
        checkout_session = stripe.checkout.Session.create(
            # 決済方法
            payment_method_types=['card'],
            # 決済詳細
            line_items=[
                {
                    'price': price.stripe_price_id,       # 価格IDを指定
                    'quantity': 1,                        # 数量
                },
            ],
            # POSTリクエスト時にメタデータ取得
            metadata = {
                        "product_id":product.id,
                       },
            mode='subscription',                               # 決済手段（一括）
            customer_email = request.user.email,               # メールアドレスはログインしたユーザーのを固定
            success_url=YOUR_DOMAIN + '/shops/result_success/',        # 決済成功時のリダイレクト先
            cancel_url=YOUR_DOMAIN + '/shops/result_failure/',          # 決済キャンセル時のリダイレクト先
        )
        return redirect(checkout_session.url)
    
# イベントハンドラ
@csrf_exempt
def stripe_webhook(request):
    print('phase1')
    print(request.headers)
    # サーバーのイベントログからの出力ステートメント
    #payload = request.body
    payload = request.body.decode('utf-8')
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, 
            sig_header, 
            endpoint_secret
            )
        print('phase2')
    except ValueError as e:
        # 有効でないpayload
        print('pattern1')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # 有効でない署名
        print('pattern2')
        return HttpResponse(status=400)

    # checkout.session.completedイベント検知
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # イベント情報取得
        customer_name  = session["customer_details"]["name"]     # 顧客名
        customer_email = session["customer_details"]["email"]    # 顧客メール
        product_id     = session["metadata"]["product_id"]       # 購入商品ID
        product        = Subscription.objects.get(id=product_id)      # 購入商品情報
        product_name   = product.name                            # 購入した商品名
        amount         = session["amount_total"]                 # 購入金額（手数料抜き）
        customer_id    = session["customer"]                     # customer_id
        # DBに結果を保存 
        print('SaveTransactionStart')
        transaction, created = SaveTransaction(product_name, customer_name, customer_email, amount, customer_id)
        print('SaveTransactionComplete')

        # 結果確認
        print(session)

        # Userの情報を更新
        user = User.objects.filter(email=customer_email).update(rank_is_free=False)
        user.save()
        print('rank変更完了')

        # user_connection情報を更新
        user_instance = User.objects.filter(email=customer_email).first()
        transaction.user_connection = user_instance
        transaction.save()
        print('紐づけ完了')

    return HttpResponse(status=200)


# 顧客の商品購入履歴を保存
def SaveTransaction(product_name, customer_name, customer_email, amount, customer_id):
    # DB保存
    saveData = Transaction.objects.get_or_create(
                        product_name   =  product_name,
                        date           = datetime.datetime.now(),
                        customer_name  = customer_name,
                        email          = customer_email,
                        product_amount = amount,
                        customer_id = customer_id
                        )
    return saveData

# 新規追加
class SubscriptionCancel(View):
    def get(self, request, *args, **kwargs):
        context = {'style_css_date': get_modified_date('css/subscription.css')}
        return render(request, 'credit/subscription.html', context)
    # サブスクリプションの解除だけでクレジットカード情報はstripeに残る
    def post(self, request, *args, **kwargs):
        context = {'style_css_date': get_modified_date('css/subscription.css')}
        kokyaku_pk = request.POST.get('kokyaku-pk') # リクエストしてきたユーザーのPKを取得
        kokyaku = get_object_or_404(User, pk=kokyaku_pk)
        transactions = Transaction.objects.filter(user_connection=kokyaku)
        if transactions.exists(): 
            targetTransaction = Transaction.objects.filter(user_connection=kokyaku)
            kokyaku.rank_is_free = True # 会員ランクを変更
            kokyaku.save()
            # Stripeの処理（例: Stripe APIを使ったキャンセル処理）
            for transaction in transactions:
                 stripe.Subscription.delete(transaction.customer_id)

            # トランザクションを削除
            transactions.delete()
            # modelから削除
            targetTransaction.delete() 

            context = {'suc': 'サブスクリプションを解約しました。'}
            return render(request, 'credit/subscription.html', context)
        else:
            kokyaku.rank_is_free = True # 会員ランクを変更
            kokyaku.save()  
            context = {'err': 'あなたに紐づくサブスクリプションはありませんでした。'}          
            return render(request, 'credit/subscription.html', context)

class CardinfoUpdateAndDelete(View):
    # 現在のカード情報を取得
    def get(self, request, *args, **kwargs):
        context = {'style_css_date': get_modified_date('css/cardinfo.css')}
        # 顧客の PK を取得し、データベースから顧客を特定
        kokyaku_pk = kwargs.get('kokyaku_pk')
        kokyaku = get_object_or_404(User, pk=kokyaku_pk)
        transaction = Transaction.objects.filter(user_connection=kokyaku).first()

        if not transaction:
            context = {'fatal_err': 'サブスクリプション契約情報が見つかりませんでした。'}
            return render(request, 'credit/cardinfo.html', context)

        customer_id = transaction.customer_id

        try:
            # 顧客に紐づくカード情報を取得
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card"
            )

            if not payment_methods['data']:
                context = {'err': 'カード情報が登録されていません。'}
                return render(request, 'credit/cardinfo.html', context)

            # デフォルトの支払い方法が指定されているかチェック
            default_payment_method_id = stripe.Customer.retrieve(customer_id).invoice_settings.default_payment_method
            default_payment_method = None
            for pm in payment_methods['data']:
                if pm.id == default_payment_method_id:
                    default_payment_method = pm
                    break
            if default_payment_method is None:
                default_payment_method = payment_methods['data'][0]  # 一番目のカードを表示

            # カード情報をコンテキストに格納
            context = {
                'card': {
                    'brand': default_payment_method.card.brand,  # カードブランド
                    'last4': default_payment_method.card.last4,  # カード番号の下4桁
                    'exp_month': default_payment_method.card.exp_month,  # 有効期限の月
                    'exp_year': default_payment_method.card.exp_year,    # 有効期限の年
                }
            }
            return render(request, 'credit/cardinfo.html', context)

        except stripe.error.StripeError as e:
            context = {'err': f'エラーが発生しました: {e.user_message}'}
            return render(request, 'shops/result_failure.html', context)
    
    # 新しいクレジットカード情報をデフォルト設定で追加する（古いクレジットカード情報は残る）
    def post(self, request, *args, **kwargs):
        context = {'style_css_date': get_modified_date('css/cardinfo.css')}
        kokyaku_pk = request.POST.get('kokyaku-pk')
        kokyaku = get_object_or_404(User, pk=kokyaku_pk)
        transaction = Transaction.objects.filter(user_connection=kokyaku).first()

        if not transaction:
            context = {'err': '顧客情報が見つかりませんでした。'}
            return render(request, 'credit/cardinfo.html', context)

        target_customer_id = transaction.customer_id
        
        if 'cardinfo-update' in request.POST:
            # 新しいカード情報を受け取る
            number = request.POST.get('card-number')   # 16桁のカード番号
            exp_month = request.POST.get('exp-month')  # 1-12の数値
            exp_year = request.POST.get('exp-year')    # 2桁の年数(下2桁)
            cvc = request.POST.get('cvc')              # 3桁のCVC

            try:
                # 新しいカード情報を作成
                new_payment_method = stripe.PaymentMethod.create(
                    type="card",
                    card={
                        "number": number,
                        "exp_month": exp_month,
                        "exp_year": exp_year,
                        "cvc": cvc,
                    },
                )

                # 新しいカード情報を顧客に紐づける
                stripe.PaymentMethod.attach(
                    new_payment_method.id,
                    customer=target_customer_id,
                )

                # 新しいカード情報をデフォルトに設定する
                stripe.Customer.modify(
                    target_customer_id,
                    invoice_settings={
                        'default_payment_method': new_payment_method.id,
                    }
                )

                context = {'suc': 'クレジットカード情報を更新しました。'}
                return render(request, 'credit/cardinfo.html', context)

            except stripe.error.StripeError as e:
                context = {'err': f'エラーが発生しました。: {e.user_message}'}
                return render(request, 'credit/cardinfo.html', context)
            
        elif 'cardinfo-delete' in request.POST:
            # stripeからリクエストしてきた顧客情報をクレジットカード情報ごと削除する
            try:
                # Stripe上の顧客情報を削除
                stripe.Customer.delete(target_customer_id)
                context = {'suc': 'クレジットカード情報を削除しました。'}
                return render(request, 'credit/cardinfo.html', context)

            except stripe.error.StripeError as e:
                context = {'err': f'エラーが発生しました。: {e.user_message}'}
                return render(request, 'credit/cardinfo.html', context)

