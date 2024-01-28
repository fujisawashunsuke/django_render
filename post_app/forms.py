from django import forms
from .models import PostApp

class PostAppCreateForm(forms.ModelForm): #djangoですでにできているformsを継承
  class Meta: #予約されている変数の属性値を変える宣言
    model=PostApp
    fields=(
      'title',
      'content',
      'image1',
      'image2',
      'image3',
      'address'
      #タプルの最後はカンマを付ける(1個の時は必ず必要)
      #それぞれがテーブルのカラム
      
    ) #fieldsなどの変数はすでに予約されている
    widgets={
      'title':forms.Textarea(
        attrs={'rows':1,'cols':30,'placeholder':'ここに入力'}
      ), 
      'content':forms.Textarea(
        attrs={'rows':10,'cols':30,'placeholder':'ここに入力'} #デフォルトの表示
      ),
      'address':forms.Textarea(
        attrs={'rows':1,'cols':30,'placeholder':'ここに入力'}
      )
    }
    #GUIの部分