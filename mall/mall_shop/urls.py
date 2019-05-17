"""mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from mall_shop import views

urlpatterns = [

    #轮播图列表
    path('slideshow_list', views.Slideshow_list.as_view()),
    #新闻列表
    path('news_list', views.News_list.as_view()),
    #品牌列表
    path('brand_list', views.Brand_list.as_view()),
    #更多品牌列表
    path('brand_recommend', views.Brand_recommend.as_view()),
    #更多商品新鲜好物推荐列表
    path('goods_product_list', views.Goods_product_list.as_view()),
    #商品新鲜好物推荐列表
    path('goods_product', views.Goods_product.as_view()),
    #更多人气推荐列表
    path('goods_popularity_list', views.Goods_popularity_list.as_view()),
    #人气推荐列表
    path('goods_popularity', views.Goods_popularity.as_view()),
    #猜你喜欢列表
    path('guess_like_list', views.Guess_like_list.as_view()),
    #专题列表
    path('special_list', views.Special_list.as_view()),
    #秒杀列表
    path('indexFlashProduct', views.IndexFlashProduct.as_view()),
    #分类列表
    path('category_list', views.Category_list.as_view()),
    #专题页面
    path('special_specate_list', views.Special_specate_list.as_view()),
    #专题详情页
    path('special_detail_list', views.Special_detail_list.as_view()),
    #话题首页
    path('topic_list', views.Topic_list.as_view()),
    #热门话题首页
    path('hot_topic_list', views.Hot_topic_list.as_view()),
    #话题详情页
    path('topic_detail_list', views.Topic_detail_list.as_view()),
    #优选页面
    path('optimization_list', views.Optimization_list.as_view()),
    #优选详情页面
    path('optimization_detail_list', views.Optimization_detail_list.as_view()),
    #特惠首页
    path('preference_list', views.Preference_list.as_view()),
    #商品详情页
    path('goods_list', views.Goods_list.as_view()),
    #分类下的商品
    path('category_goods_list', views.Category_goods_list.as_view()),


]
