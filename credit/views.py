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

# stripeのAPIキーを渡す
stripe_APIKey = settings.STRIPE_PUBLIC_KEY

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
        # 二重でサブスクリプションに契約することを防止
        if Transaction.objects.filter(user_connection=self.request.user):
            context = {'err': 'あなたは既にサブスクリプションを契約しています。'}
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
        User.objects.filter(email=customer_email).update(rank_is_free=False)
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
        kokyaku_pk = request.POST.get('kokyaku-pk') # リクエストしてきたユーザーのPKを取得
        kokyaku = get_object_or_404(User, pk=kokyaku_pk)
        transactions = Transaction.objects.filter(user_connection=kokyaku)

        if transactions.exists(): 
            targetTransaction = Transaction.objects.filter(user_connection=kokyaku)
            kokyaku.rank_is_free = True # 会員ランクを変更
            kokyaku.save()
            # トランザクションごとに処理
            for transaction in transactions:
                try:
                    # 顧客IDに関連するサブスクリプションを取得
                    subscriptions = stripe.Subscription.list(customer=transaction.customer_id)

                    for subscription in subscriptions.auto_paging_iter():
                        # サブスクリプションIDを取得して削除
                        stripe.Subscription.delete(subscription.id)

                except stripe.error.StripeError as e:
                    # Stripeのエラーを処理
                    print(f"Stripe error: {e}")

            # トランザクションを削除
            transactions.delete()
            # modelから削除
            targetTransaction.delete() 

            context = {
                'suc': 'サブスクリプションを解約しました。',
                'style_css_date': get_modified_date('css/subscription.css')
            }
            return render(request, 'credit/subscription.html', context)
        else:
            kokyaku.rank_is_free = True # 会員ランクを変更
            kokyaku.save()  
            context = {
                'err': 'あなたに紐づくサブスクリプションはありませんでした。',
                'style_css_date': get_modified_date('css/subscription.css')
            }          
            return render(request, 'credit/subscription.html', context)

class CardinfoUpdateAndDelete(View):
    # 現在のカード情報を取得
    def get(self, request, *args, **kwargs):    
        
        # 顧客の PK を取得し、データベースから顧客を特定
        kokyaku_pk = kwargs.get('kokyaku_pk')
        kokyaku = get_object_or_404(User, pk=kokyaku_pk)
        transaction = Transaction.objects.filter(user_connection=kokyaku).first()

        if not transaction:
            context = {'fatal_err': 'サブスクリプション契約情報が見つかりませんでした。', 'stripe_APIKey': stripe_APIKey}
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
                },
                'style_css_date': get_modified_date('css/cardinfo.css'),
                'style_js_date': get_modified_date('js/cardinfo.js'),
                'stripe_APIKey': stripe_APIKey
            }

            return render(request, 'credit/cardinfo.html', context)

        except stripe.error.StripeError as e:
            context = {'err': f'エラーが発生しました: {e.user_message}'}
            return render(request, 'shops/result_failure.html', context)
    
    # 新しいクレジットカード情報をデフォルト設定で追加する（古いクレジットカード情報は残る）
    def post(self, request, *args, **kwargs):
        kokyaku_pk = request.POST.get('kokyaku-pk')
        kokyaku = get_object_or_404(User, pk=kokyaku_pk)
        transaction = Transaction.objects.filter(user_connection=kokyaku).first()

        if not transaction:
            context = {'err': '顧客情報が見つかりませんでした。'}
            return render(request, 'credit/cardinfo.html', context)

        target_customer_id = transaction.customer_id 
            
        if 'cardinfo-delete' in request.POST:
            # stripeからリクエストしてきた顧客情報をクレジットカード情報ごと削除する
            try:
                # Stripe上の顧客情報を削除
                stripe.Customer.delete(target_customer_id)
                transaction.delete()
                # 会員ランクを変更
                kokyaku.rank_is_free = True 
                kokyaku.save()
                context = {'suc': 'クレジットカード情報の削除とサブスクリプションの解約をしました。'}
                return render(request, 'credit/cardinfo.html', context)

            except stripe.error.StripeError as e:
                context = {'err': f'エラーが発生しました。: {e.user_message}'}
                return render(request, 'credit/cardinfo.html', context)
            
   
@csrf_exempt
def update_card(request):
    if request.method == 'POST':
        try:
            # JSONデータの取得
            data = json.loads(request.body)
            token = data.get('token')
            kokyaku_pk = data.get('kokyaku_pk')  # JSONからkokyaku-pkを取得

            if not token or not kokyaku_pk:
                return JsonResponse({'success': False, 'message': 'トークンまたは顧客IDが提供されていません。'}, status=400)

            kokyaku = get_object_or_404(User, pk=kokyaku_pk)
            transaction = Transaction.objects.filter(user_connection=kokyaku).first()

            if not transaction:
                return JsonResponse({'success': False, 'message': '指定された顧客に関連するトランザクションが見つかりません。'}, status=404)

            customer_id = transaction.customer_id

            # 怪しいポイント
            print(token)
            payment_method = stripe.PaymentMethod.create(
                type="card",
                card={"token": token}  # `token` には `tok_xxx` の形式のトークンを指定
            )
            stripe.PaymentMethod.attach(
                payment_method.id,  # 新しいトークン
                customer = customer_id
            )

            # Stripeで顧客のデフォルトカード情報を更新
            customer = stripe.Customer.modify(
                customer_id,
                source=token  # 新しいトークンでデフォルトカードを更新
            )
            
            return JsonResponse({'success': True, 'message': 'カード情報が更新されました。'})

        except stripe.error.StripeError as e:
            return JsonResponse({'success': False, 'message': f'Stripe APIエラー: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'予期しないエラーが発生しました: {str(e)}'}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method. POSTのみ対応しています。'}, status=400)    