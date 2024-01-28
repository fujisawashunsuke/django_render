from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class PostApp(models.Model):
  title=models.TextField(blank=True,null=True)
  content=models.TextField() #カラムの型
  image1=models.ImageField(upload_to='images/',blank=True,null=True,verbose_name='投稿画像') #berbose_name:表示の名前
  image2=models.ImageField(upload_to='images/',blank=True,null=True,verbose_name='投稿画像') #berbose_name:表示の名前
  image3=models.ImageField(upload_to='images/',blank=True,null=True,verbose_name='投稿画像') #berbose_name:表示の名前
  #サーバーの中でimagesのパスのところに保存される
  address=models.CharField(blank=True,null=True,max_length=30)
  #CharFieldは長さが可変ではないので最大文字数を指定
  created_at=models.DateTimeField(auto_now_add=True) #投稿日時を勝手にいれてくれる
  created_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True) #ForeignKey…他のアプリケーション(accountsのほう）からテーブルごととってきている
  #CASCADE…ユーザーが削除されたら記事も削除する
  
  #これらはすべて主キーではない(同時の可能性もある)⇒通し番号が主キーになっている
  
  def __str__(self): #デバッグ用
    return self.content
  
