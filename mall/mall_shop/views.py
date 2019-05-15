from django.shortcuts import render,redirect

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.views import APIView
from sadmin.models import *
import json, os
from mall import settings
from datetime import datetime
from .serializers import *
from rest_framework.response import Response
import time
from datetime import datetime
# Create your views here.


class Slideshow_list(APIView):
    """
    轮播图列表
    """
    def get(self, request):
        mes = {}
        sld = Advertising.objects.all()[:5]
        adv = AdvertisingModelSerializer(sld,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class News_list(APIView):
    """
    新闻列表
    """
    def get(self, request):
        mes = {}
        sld = News.objects.all()[:5]
        new = NewsModelSerializer(sld,many=True)
        mes['code'] = 200
        mes['list'] = new.data
        return Response(mes)

class Brand_list(APIView):
    """
    品牌列表
    """
    def get(self, request):
        mes = {}
        b = brand.objects.filter(is_recommend=1).all()[:5]
        adv = BrandModelSerializer(b,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class Goods_product_list(APIView):
    """
    商品新品推荐
    """
    def get(self, request):
        mes = {}
        b = Goods.objects.filter(newStatus=1).all()[:2]
        adv = GoodsModelSerializer(b,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class Goods_popularity_list(APIView):
    """
    人气推荐
    """
    def get(self, request):
        mes = {}
        b = Goods.objects.order_by('-popularity')[:3]
        adv = GoodsModelSerializer(b,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class Guess_like_list(APIView):
    """
    猜你喜欢列表
    """
    def get(self, request):
        mes = {}
        b = Guess_like.objects.all()[:3]
        adv = Guess_likeModelSerializer(b,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class Special_list(APIView):
    """
    首页专题
    """
    def get(self, request):
        mes = {}
        b = Special.objects.filter(show_status=1).all()[:1]
        adv = SpecialModelSerializer(b,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class IndexFlashProduct(APIView):
    """
    首页秒杀专区
    """
    def get(self, request):
        mes = {}
        todaydate = datetime.now().strftime("%Y-%m-%d")
        flashdate = Ceckil_activity.objects.filter(
        startTime__lte=todaydate, endTime__gte=todaydate).all()
        flashdateidlist = []
        for i in flashdate:
            flashdateidlist.append(i.id)
        flashtime = Quentum.objects.all()
        flashtimeidlist = []
        for i in flashtime:
            flashtimeidlist.append(i.id)
        flashproduct = Ceckil_goods_relation.objects.filter(activity_id_id__in=flashdateidlist,quentum_id_id__in=flashtimeidlist).all()
        flashproduct_serializer = FlashProductModelSerializer(flashproduct, many=True)
        mes['code'] = 200
        mes['message'] = '操作成功'
        mes['list'] = flashproduct_serializer.data
        return Response(mes)

class Category_list(APIView):
    """
    分类列表
    """
    def get(self, request):
        mes = {}
        b = category.objects.filter(level=0).all()
        adv = CategorylistModelSerializer(b,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class Special_specate_list(APIView):
    """
    专题页面
    """
    def get(self, request):
        mes = {}
        b = special_category.objects.all()
        adv = SpecialcategoryModelSerializer(b,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class Special_detail_list(APIView):
    """
    专题详情页面：需要传递专题ID
    ?ids=id
    """
    def get(self, request):
        mes = {}
        ids = request.GET.get('ids',1)
        if ids:
            spec = Special_shop.objects.filter(special_id_id=ids).all()
            special_detail = SpecialshopModelSerializer(spec,many=True)
            mes['code'] = 200
            mes['list'] = special_detail.data
        return Response(mes)

class Hot_topic_list(APIView):
    """
    热门话题首页    """
    def get(self, request):
        mes = {}
        spec = discourse_detail.objects.order_by('-collect_sum')[:5]
        print(spec)
        special_detail = DiscoursedetailModelSerializer(spec,many=True)
        mes['code'] = 200
        mes['list'] = special_detail.data
        return Response(mes)

class Topic_list(APIView):
    """
    话题首页
    """
    def get(self, request):
        mes = {}
        spec = discourse_detail.objects.all()
        print(spec)
        special_detail = DiscourseModelSerializer(spec,many=True)
        mes['code'] = 200
        mes['list'] = special_detail.data
        return Response(mes)

class Topic_detail_list(APIView):
    """
    话题详情页面 需要传递参数话题ID
    ?ids=id
    """
    def get(self,request):
        mes = {}
        ids = request.GET.get('ids',1)
        if ids:
            spec = discourse_detail.objects.all()
            special_detail = DiscoursedetailModelSerializer(spec,many=True)
            mes['code'] = 200
            mes['list'] = special_detail.data
        return Response(mes)
