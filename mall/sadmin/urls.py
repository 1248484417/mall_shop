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
from sadmin import views

urlpatterns = [
    #分类列表二级分类封装
    path('type/', views.Type_list.as_view()),
    path('add_type/',views.Add_type.as_view()),
    path('add_property/', views.Add_property.as_view()),

    path('delete_pro/', views.Delete_pro.as_view()),
    path('jia_leixing/', views.Jia_leixing.as_view()),
    path('shop_type/', views.Shop_type.as_view()),
    path('delete_type_list/', views.Delete_type_list.as_view()),
    

    path('shop_type_cate/', views.Shop_type_cate.as_view()),
    
    #品牌列表不分页
    path('brand_list/', views.Brand_list.as_view()),
    #修改商品是否新品推荐
    path('goods_xin_update/', views.Goods_xin_update.as_view()),
    #删除新品推荐商品
    path('goods_xinpin_delete/', views.Goods_xinpin_delete.as_view()),
    #修改新品推荐商品
    path('goods_xinpin_update/', views.Goods_xinpin_update.as_view()),
    #修改新品推荐商品列表
    path('goods_xinpinlist_update/', views.Goods_xinpinlist_update.as_view()),
    #展示新品推荐商品列表
    path('goods_xinpin/', views.Goods_xinpin.as_view()),
    #修改新品推荐商品排序
    path('goods_xinpin_sort/', views.Goods_xinpin_sort.as_view()),
    #展示商品列表
    path('goods_list/', views.Goods_list.as_view()),
    #删除商品
    path('goods_delete/', views.Goods_delete.as_view()),
    #编辑商品库存
    path('goods_bianji/', views.Goods_bianji.as_view()),
    #修改商品上架状态
    path('goods_status_update/', views.Goods_status_update.as_view()),
    #分类是否显示
    path('cate_show/', views.Cate_show.as_view()),
    #添加品牌
    path('add_brand/', views.Add_brand.as_view()),
    #类型加属性
    path('type_shuxing/', views.Type_shuxing.as_view()),
    #品牌管理
    path('brand_lods', views.Shop_guan.as_view()),
    #添加到品牌推荐
    path('add_brand_show/',views.Add_brand_show.as_view()),
    #品牌是否显示
    path('brand_show',views.Brand_show.as_view()),
    #品牌管理详情页
    path('brand__detail',views.Brand_detail.as_view()),
    #删除类型
    path('del_brand', views.Del_brand.as_view()),
    #删除品牌
    path('del_pinpai', views.Del_pinpai.as_view()),
    #品牌排序
    path('pinpai_sort/', views.Pinpai_sort.as_view()),
    #品牌推荐列表
    path('pinpai_list/', views.Pinpai_list.as_view()),
    #品牌是否推荐
    path('pinpai_tuijian/', views.Pinpai_tuijian.as_view()),
    #上传图片
    path('image/', views.Image.as_view()),
    #添加广告
    path('add_guanggao/', views.Add_guanggao.as_view()),
    #查询广告
    path('guanggao_list/', views.Guanggao_list.as_view()),
    #修改广告上线下线
    path('guanggao_show/', views.Guanggao_show.as_view()),
    #删除广告
    path('guanggao_delete/', views.Guanggao_delete.as_view()),
    #查询会员
    path('huiyuan_list/', views.Huiyuan_list.as_view()),
    #添加商品
    path('add_shop/', views.Add_shop.as_view()),
    #添加优惠卷
    path('add_coupon/', views.Add_coupon.as_view()),
    #添加活动
    path('add_huodong/', views.Add_huodong.as_view()),
    #活动列表
    path('huodong_list/', views.Huodong_list.as_view()),
    #删除活动
    path('huodong_delete/', views.Huodong_delete.as_view()),
    #修改活动状态
    path('huodong_status_show/', views.Huodong_status_show.as_view()),
    #添加秒杀活动
    path('add_miaoshahuodong/', views.Add_miaoshahuodong.as_view()),
    #秒杀活动列表
    path('miaoshahuodong_list/', views.Miaoshahuodong_list.as_view()),
    #修改秒杀活动
    path('update_miaoshahuodong/', views.Update_miaoshahuodong.as_view()),
    #删除秒杀活动
    path('miaoshahuodong_delete/', views.Miaoshahuodong_delete.as_view()),
    #订单设置
    path('order_setting/', views.Order_setting.as_view()),
    #订单设置列表
    path('dingdan_setting_list/', views.Dingdan_setting_list.as_view()),
    #优惠卷列表
    path('coupon_list/', views.Coupon_list.as_view()),
    #修改优惠卷
    path('coupon_update/', views.Coupon_update.as_view()),
    #删除优惠卷
    path('coupon_delete/', views.Coupon_delete.as_view()),
    #查询商品
    path('goods_query/', views.Goods_query.as_view()),

]
