from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "shops"

urlpatterns = [
    #path('', views.TopView.as_view(), name='index'),
    path('shop_create/',views.ShopCreateView.as_view(), name='shop_create'),
    #path('shop_detail/<int:pk>/', views.ShopDetailView.as_view(), name='shop_detail'),
    #path('shop_detail/<int:pk>/', views.ShopDetailView2.as_view(), name='shop_detail'),
    path('shop_detail/<int:pk>/', views.ShopDetailView3.as_view(), name='shop_detail'),
    path('result_success/', views.ResultSuccessView.as_view(), name='success'),
    path('result_failure/', views.ResultFailureView.as_view(), name='failure'),
    path('shop_update_form/<int:pk>',views.ShopUpdateView.as_view(), name='shop_update'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)