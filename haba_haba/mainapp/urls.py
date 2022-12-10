from django.urls import path, re_path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', MainappHome.as_view(), name='home'),
    path('post/<slug:slug>/', ShowPost.as_view(), name='post'),
    path('cat/<slug:slug>', PostCategory.as_view(), name='category'),
    path('comments/<slug:slug>', ShowComments.as_view(), name='comment'),
    path('comment/delete/', delete_comment, name='delete_comment'),
    path('comment/add/', add_comment, name='add_comment'),
    path('cat/<slug:slug>/', site_category, name='category'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    # path('update_post/<str:pk>', views.update_post, name='update_post'),
]

