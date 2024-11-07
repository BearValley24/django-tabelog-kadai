import base64
from django import template

register = template.Library()

@register.filter(name='b64encode')
def b64encode(value):
    # バイナリデータをBase64エンコードして文字列として返す
    return base64.b64encode(value).decode('utf-8')