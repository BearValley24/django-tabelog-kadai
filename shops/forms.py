from django import forms
from .models import Shop

class createForm(forms.ModelForm):
    class Meta:
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
            'regularHoliday'
        )
    def __init__(self, *args, **kwargs):
        # 任意のplaceholderテキスト
        super(createForm, self).__init__(*args, **kwargs)
        self.fields['phoneNumber'].widget.attrs.update({
            'placeholder': 'ハイフン不要'  
        })
        self.fields['address'].widget.attrs.update({
            'placeholder': '郵便番号と住所を入力'  
        })
        self.fields['addressLat'].widget.attrs.update({
            'placeholder': '住所の緯度を入力'  
        })
        self.fields['addressLng'].widget.attrs.update({
            'placeholder': '住所の経度を入力'  
        })
        self.fields['startHour1'].widget.attrs.update({
            'placeholder': 'HH:MM:SS'  
        })
        self.fields['endHour1'].widget.attrs.update({
            'placeholder': 'HH:MM:SS'  
        })
        self.fields['startHour2'].widget.attrs.update({
            'placeholder': 'HH:MM:SS'  
        })
        self.fields['endHour2'].widget.attrs.update({
            'placeholder': 'HH:MM:SS'  
        })
        self.fields['introduction'].widget.attrs.update({
            'placeholder': '店舗の紹介文を入力'  
        })
    