from django.urls import path

from . import views

#classver

app_name='post_app'

urlpatterns=[
  path('', views.PostListView.as_view(), name='post_list'),
  path('post_create/', views.PostCreateView.as_view(),
     name='post_create'),
  #path('',views.post_list,name='post_list'), #ただのlocalhost:8000でアクセスされたときメインのページに飛ぶ
  #path('post_create/',views.post_create,name='post_create'),
  path('post_detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'), #pkには記事の通し番号が入る
  path('post_update/<int:pk>/', views.PostUpdateView.as_view(), name='post_update'),
  path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
]
#urlの最初にpost_createときたらpost_createにアクセス