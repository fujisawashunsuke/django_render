from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin #認証

from django.utils import timezone
from django.utils.translation import gettext_lazy as _ #名前長いので置き換え #gettext_lazyは多言語に対応するためのもの
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')

        if not email:
            raise ValueError('The given email must be set')

        user = self.model(username=self.model.normalize_username(username), email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(username, email, password, **extra_fields)
# Create your models here.
class User(AbstractBaseUser,PermissionsMixin): #多重継承 #設定できるのはis_superuserだけ
  username = models.CharField(max_length=25, unique=True)
  email = models.EmailField(unique=True)
  icon = models.ImageField(blank=True, null=True)
  introduction = models.CharField(max_length=75,blank=True,null=True)
  followers=models.ManyToManyField('self',blank=True,symmetrical=False,related_name="user_followers") #とってくるときの名前付け
  #多対多の関係
  #symmetrical…一方的なフォロー（片方がフォローするだけの時がある）
  followees=models.ManyToManyField('self',blank=True,symmetrical=False,related_name="user_followees")
  is_staff=models.BooleanField(
    _('staff status'), #_はgettext_lazy
    default=False,
    help_text=_('Desigmates whether the user can log into this admin site. '),
  )
  is_active=models.BooleanField(
    _('active'), #関数を省略できるのは引数が単一文字列の場合のみ
    default=True,
    help_text=_(
      'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
    ),
  )
  
  date_joined=models.DateTimeField(default=timezone.now)
  objects = UserManager()
  

  EMAIL_FIELD = 'email'
  USERNAME_FIELD = 'username'
  #コマンドラインでcreatesuperuserとするときに求められるフィールド
  REQUIRED_FIELDS = ['email']

  class Meta:
      verbose_name = _('user') #予約されている表示名を書き換える
      verbose_name_plural = _('users')
