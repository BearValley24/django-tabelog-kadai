from django.urls import path
from . import views
from django.conf import settings            
from django.conf.urls.static import static  

app_name = "credit"

urlpatterns = [
    path('credit/', views.ProductTopPageView.as_view(), name='product_top_page'),
    path("success/", views.SuccessPageView.as_view(), name="success"),                                                   # 決済成功時にリダイレクト先
    path("cancel/", views.CancelPageView.as_view(), name="cancel"), 
    path("create-checkout-session/<pk>/", views.CreateCheckoutSessionView.as_view(), name="create-checkout-session"),    # 個別商品決済画面
    path("webhook/", views.stripe_webhook, name="webhook"),   
]

# メディア表示
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)