from django.urls import path
from . import views
from django.conf import settings            
from django.conf.urls.static import static  

app_name = "review"

urlpatterns = [
    path('review_update/<int:pk>', views.reviewUpdate.as_view(), name='UpdateReview'),
    path('review_display/<int:pk>', views.reviewDisplay.as_view(), name='DisplayReview'),
    path('review_delete', views.reviewDelete.as_view(), name='DeleteReview'),
]

# メディア表示
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)