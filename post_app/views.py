from django.shortcuts import render,redirect
from .forms import PostAppCreateForm
from .models import PostApp #モデルのクラス
from django.contrib.auth.decorators import login_required

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import PostAppCreateForm
from .models import PostApp
from django.contrib import messages
from django.db.models import Q
#classで作るver
class PostListView(generic.ListView):
    model=PostApp
    template_name = "post_app/post_list.html"

    #テンプレートに渡すデータを設定
    '''
    def get_context_data(self, **kwargs): #データの順番、形式をかえるだけ
      #親クラスからcontextデータを取得
      context = super(PostListView, self).get_context_data(**kwargs)
      #オーバーライド(最初は空のリストがかえる)
      #モデルのオブジェクトすべてを渡す
      post_l = PostApp.objects.all()
      context.update({'post_list': post_l}) #辞書データをアップデート
      #ここのpost_listがpost_list.htmlのfor文に入っている
      #contextデータをリターン
      print('テスト1')
      return context
     ''' 
     #親クラスですでにcontext_dataがあるのでわざわざupdateしなくてOK
     
    def get_queryset(self): #出すデータを指定
      print('テスト2')
      q_word = self.request.GET.get('query')
      q_name = self.request.GET.get('name')

      if q_word or q_name:
        q_word_l=q_word.split()
        q=Q()
        for w in q_word_l:
          q&=(Q(title__icontains=w)|Q(content__icontains=w))
        if q_name:
          q&=Q(created_by__username__exact=q_name)
        object_list=PostApp.objects.filter(q)
      else:
        object_list=PostApp.objects.all()
      return object_list

class PostCreateView(LoginRequiredMixin, generic.FormView): #ログインしているときしか入れない(デコレータと同じ役割)
    model = PostApp
    template_name = "post_app/post_create.html"
    form_class = PostAppCreateForm
    success_url = reverse_lazy('post_app:post_list')

    def form_valid(self, form): #formへのアクセスが成功した場合
        print('test')
        #save()はformに結びつけられたモデルのインスタンスを返す
        #commit=Falseでデータベースには保存しないようにする(基本連動している)
        #https://djangoproject.jp/doc/ja/1.0/topics/forms/modelforms.html        
        post_f = form.save(commit=False) #インスタンスがほしいだけ
        #投稿者(ユーザーモデル)を設定する
        post_f.created_by = self.request.user #post_fが記事のモデル
        #データベースに保存
        post_f.save()
        #多対多のデータはここで保存する
        form.save_m2m() #フォロー関係など
        return super().form_valid(form)

# Create your views here.
def post_list(request):
  context={
   'post_list':PostApp.objects.all(), 
  } #辞書型になっている(全てを取得)
  return render(request,'post_app/post_list.html',context) #html二からのデータを渡している
 #閲覧時の処理で必要 


 
@login_required  
def post_create(request):
  if request.method=="POST": #requestの中にmethodの種類が入っている
    form=PostAppCreateForm(request.POST) #POSTは辞書型
    if form.is_valid():
      form.save() #contentと連動している
      return redirect('post_app:post_list') #urls.pyで指定したpost_listとついたurlにアクセス⇒hello djangoが表示
  else:
    form=PostAppCreateForm()
  return render(request,'post_app/post_create.html',{'form':form})
  #formという名前(辞書の１個目)で入力のHTMLのformクラスにアクセス
  #2個目のformはPostAppCreateForm()を表す
  #renderが「表示」
  #最初urlにアクセスした段階で一度elseのほうに入る
  
class PostDetailView(generic.DetailView):
    model = PostApp #ここではユーザーではなく記事が１つのモデル
    template_name = 'post_app/post_detail.html'
    
class PostUpdateView(generic.UpdateView):
    model = PostApp
    template_name = 'post_app/post_update.html'
    form_class = PostAppCreateForm

    def get_success_url(self):
        return reverse_lazy('post_app:post_detail', kwargs={'pk':self.kwargs['pk']}) #post_updateの引数のpkをself.kwargsでとってきて、その番号をpost_detailの引数に渡している
      
    def form_valid(self, form):
        messages.success(self.request, '投稿を更新しました。')
        return super().form_valid(form)
      #もともとのform_validをオーバーライドしている

    def form_invalid(self, form):
        messages.error(self.request, '投稿の更新に失敗しました。')
        return super().form_invalid(form)
      
class PostDeleteView(generic.DeleteView):
    model = PostApp
    template_name = 'post_app/post_delete.html'

    def get_success_url(self):
        return reverse_lazy('accounts:user_profile', kwargs={'pk':self.object.created_by.pk}) #削除が完了したら個人のプロフィールページに飛ぶので、ユーザーモデルのpkで指定する

    def delete(self,request,*args,**kwargs):
        messages.success(self.request, '日記を削除しました。')
        return super().delete(request,*args,**kwargs)