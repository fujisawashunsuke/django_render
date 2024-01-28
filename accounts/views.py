
# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin #authが権限のモジュール
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

'''
def user_profile(request, username):
    context = {
        'User': get_user_model().objects.get(username=username),
    } #Userがキー、templateのところで使ってログイン中のユーザーモデルをとってこれる
    #ログイン中のユーザーのユーザーネームを引数⇒そのモデルを取得
    return render(request, 'accounts/user_profile.html', context)
'''
import django.http
import accounts.models
import accounts.forms
from django.shortcuts import render,redirect
import uuid
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

def login_user(request): #ユーザーがログインしようとするとき
    if request.method == 'POST':
        login_form = accounts.forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        ret=0
        try:
            user = get_user_model().objects.get(username=username)
            if user is not None:
                django_login(request, user)
                ret = redirect('post_app:post_create')
                #パスワードが正しいとき
        except get_user_model().DoesNotExist:
            login_form.add_error(None, "ユーザー名またはパスワードが異なります。")
            ret = render(request, 'registration/login.html', {'login_form': login_form})
        return ret
    else:
        login_form = accounts.forms.LoginForm()
        ret = render(request, 'registration/login.html', {'login_form': login_form})
    return ret
    #アカウントとパスワードが合致したら、その人専用の投稿画面に遷移する
    #アカウントとパスワードが合致しなかったら、エラーメッセージ付きのログイン画面に遷移する
 
 #djangoが管理してるのでdjangoにログアウトしたことを伝える   
def logout_user(request):
    django_logout(request)
    ret=render(request,'registration/logout.html',{})
    return ret

#registration関連
from django.db import IntegrityError

def has_digit(text):
    if re.search("\d", text):
        return True
    return False

def has_alphabet(text):
    if re.search("[a-zA-Z]", text):
        return True
    return False

def registration_user(request):
    if request.method == 'POST':
        registration_form = accounts.forms.RegistrationForm(request.POST)
        password = request.POST['password']
        if len(password) < 8:
            registration_form.add_error('password', "文字数が8文字未満です。")
        if not has_digit(password):
            registration_form.add_error('password',"数字が含まれていません")
        if not has_alphabet(password):
            registration_form.add_error('password',"アルファベットが含まれていません")
        if registration_form.has_error('password'):
            return render(request, 'registration/user_create.html', {'registration_form': registration_form})

        try:
            user = get_user_model().objects.create_user(username=request.POST['username'], password=password, email=request.POST['email'])
        except IntegrityError as e:
            registration_form.add_error('username',"すでに登録されているユーザー名またはメールアドレスです")
            return render(request, 'registration/user_create.html', {'registration_form': registration_form})
        return render(request, 'registration/user_create_done.html', {'registration_form': registration_form})
    else:
        registration_form = accounts.forms.RegistrationForm()
    return render(request, 'registration/user_create.html', {'registration_form': registration_form})


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True #403 forbiddenのページ

    def test_func(self):  #オーバーライド
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser
    #自分の名前が見たいと指定した人の名前と一致しているor自分がスーパーユーザー
    
class UserProfileView(LoginRequiredMixin,generic.DetailView): 
    #onliyoumixinを継承→自分しか見れないようにロック
    #詳細を表示させるときはDetailViewをよく使う
    #ユーザーモデル
    model = get_user_model()
    slug_field = 'pk'
    slug_url_kwarg = 'pk'
    template_name = "accounts/user_profile.html"
    
    
from .forms import UserProfileUpdateForm
from django.shortcuts import resolve_url

class UserProfileUpdateView(OnlyYouMixin, generic.UpdateView):
    #ユーザーモデル
    model = get_user_model()
    slug_field = 'pk'
    slug_url_kwarg = 'pk' #勝手に通し番号が入る
    template_name = "accounts/user_profile_update.html"
    form_class = UserProfileUpdateForm

    def get_success_url(self):
        return resolve_url('accounts:user_profile', pk=self.kwargs['pk'])
    #成功したらuser_profile画面に飛ぶ
    #pkの値によってurlが変わる(動的)

@login_required #ログインしている人のみ(デコレータ)
def users_follow(request, pk): #見たい人のpk
    """フォロー機能"""
    login_user = request.user
    user = get_user_model().objects.get(pk=pk)
    followers = login_user.followers.all()
    #既にフォローしていれば解除、していなければフォロー
    if user in followers:
        login_user.followers.remove(user)
        user.followees.remove(login_user) #プログラムの中ならいじれる
        messages.success(request, 'フォローを解除しました')
    else:
        login_user.followers.add(user)
        user.followees.add(login_user)
        messages.success(request, 'フォローしました')

    user.save()
    login_user.save()
    return redirect('accounts:user_profile', pk=pk) #画面更新