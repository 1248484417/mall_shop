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
from datetime import timedelta
from django_redis import get_redis_connection
import ast
import json
# Create your views here.

def addpros():
    timeminusone = timedelta(hours=1)
    totimedate1 = datetime.now()-timeminusone
    totimedate = totimedate1.strftime("%H:%M:%S")  #当前时间减去一小时
    
    timeminusthree = timedelta(hours=3)
    totimedate2 = datetime.now()+timeminusthree
    totime = totimedate2.strftime("%H:%M:%S")  #当前时间加三小时
    
    todaydate = datetime.now().strftime("%Y-%m-%d")
    timedate3 = datetime.now().strftime("%H:%M:%S")

    conn = get_redis_connection('default')

    list1 = []
    try:
        quen = Quentum.objects.filter(start_time__gte=totimedate,end_time__lte=totime).order_by("-start_time")[:1]  #属于秒杀开始前一小时
        for i in quen:
            list1.append(i.id)
        
    except:
        print('获取当前时间失败')

    list2 = []
    try:
        flashdate = Ceckil_activity.objects.filter(startTime__lte=todaydate, endTime__gte=todaydate).order_by("-startTime")[:1]
        for i in flashdate:
            list2.append(i.id)
    except:
        print('获取当前月份失败')

    try:
        ceck = Ceckil_goods_relation.objects.filter(quentum_id_id__in=list1, activity_id_id__in=list2).all()
        for i in ceck:
            good_list = conn.hget("shop_" + str(i.goods_id.id), '1')

            if good_list:
                print('aaaaaaaaa')
                pass
            else:
                flashdate = Goods.objects.filter(id=i.goods_id.id).all()
                good = GoodslistModelSerializer(flashdate, many=True)
                f = goods_seckillModelSerializer(ceck,many=True)
                conn.hset("shop_" + str(i.goods_id.id), "1", {'goods': json.dumps(good.data), "seckill": json.dumps(f.data)})
                
    except:
        print('存入redis失败')

    list1 = []
    quen = Quentum.objects.filter(end_time__lt=timedate3).all()  
    
    for i in quen:
        list1.append(i.id)
    flashdate = Ceckil_activity.objects.filter(startTime__lte=todaydate, endTime__gte=todaydate).all()
    list2 = []
    for i in flashdate:
        list2.append(i.id)
    
    ceck = Ceckil_goods_relation.objects.filter(quentum_id_id__in=list1, activity_id_id__in=list2).all()
    for i in ceck:
        conn.delete("shop_" + str(i.goods_id.id), "1")
    
    return Response({})

class Slideshow_list(APIView):
    """
    轮播图列表
    """
    def get(self, request):
        mes = {}
        try:
            sld = Advertising.objects.all()[:5]
            adv = AdvertisingModelSerializer(sld,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
        return Response(mes)

class News_list(APIView):
    """
    新闻列表
    """
    def get(self, request):
        mes = {}
        try:
            sld = News.objects.all()[:5]
            new = NewsModelSerializer(sld,many=True)
            mes['code'] = 200
            mes['list'] = new.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
        return Response(mes)

class Brand_list(APIView):
    """
    品牌列表
    """
    def get(self, request):
        mes = {}
        try:
            b = brand.objects.filter(is_recommend=1).all()[:5]
            adv = BrandModelSerializer(b,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
        return Response(mes)

class Brand_recommend(APIView):
    """
    更多品牌列表
    """
    def get(self, request):
        mes = {}
        try:
            b = brand.objects.filter(is_recommend=1).all()
            adv = BrandModelSerializer(b,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
        return Response(mes)

class Goods_product(APIView):
    """
    新鲜好物推荐
    """
    def get(self, request):
        mes = {}
        try:
            b = Goods.objects.filter(newStatus=1).all()[:2]
            adv = GoodsModelSerializer(b,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'

        return Response(mes)

class Goods_product_list(APIView):
    """
    更多新鲜好物推荐
    """
    def get(self, request):
        mes = {}
        try:
            b = Goods.objects.filter(newStatus=1).order_by("-sort")
            adv = GoodsModelSerializer(b,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
        return Response(mes)


class Goods_popularity(APIView):
    """
    人气推荐
    """
    def get(self, request):
        mes = {}
        try:
            b = Goods.objects.filter(popularity=1)[:3]
            adv = GoodsModelSerializer(b,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
        return Response(mes)

class Goods_popularity_list(APIView):
    """
    更多人气推荐
    """
    def get(self, request):
        mes = {}
        try:
            b = Goods.objects.filter(popularity=1).order_by("-sort")
            adv = GoodsModelSerializer(b,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
        return Response(mes)


class Guess_like_list(APIView):
    """
    猜你喜欢列表
    """
    def get(self, request):
        mes = {}
        try:
            b = Guess_like.objects.all()[:3]
            adv = Guess_likeModelSerializer(b,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
        return Response(mes)

class Special_list(APIView):
    """
    首页专题
    """
    def get(self, request):
        mes = {}
        try:
            b = Special.objects.filter(show_status=1).all()[:1]
            adv = SpecialModelSerializer(b,many=True)
            mes['code'] = 200
            mes['list'] = adv.data
        except:
            mes['code'] = 10010
            mes['erro'] = '查询错误'
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
    商品分类列表
    """
    def get(self, request):
        mes = {}
        b = category.objects.filter(level=0).all()
        adv = CategorylistModelSerializer(b,many=True)
        mes['code'] = 200
        mes['list'] = adv.data
        return Response(mes)

class Category_goods_list(APIView):
    """
    分类下的商品列表：需要传递分类ID
    ?ids=id
    """
    def get(self, request):
        mes = {}
        ids = request.GET.get('ids', 1)
        if ids:
            b = category.objects.filter(id=ids).all()
            adv = CategorygoodslistModelSerializer(b,many=True)
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
        ids = request.GET.get('ids', 1)
        ip = request.META['REMOTE_ADDR']
        conn = get_redis_connection('default')
        if ids:
            spec = Special_shop.objects.filter(special_id_id=ids).all()
            special_detail = SpecialshopModelSerializer(spec, many=True)
            special = conn.hget("special_" + str(ip), "1")
            if special:
                pass
            else:
                
                spe = Special.objects.filter(id=ids).first()
                spe.read_count = spe.read_count + 1
                spe.save()
                conn.hset("special_" + str(ip), "1", {"beizhu": '专题'})
            mes['code'] = 200
            mes['list'] = special_detail.data
        else:
            mes['code'] = 10010
            mes['erro'] = '没有传递参数'
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
        ids = request.GET.get('ids', 1)
        ip = request.META['REMOTE_ADDR']
        conn = get_redis_connection('default')
        if ids:
            spec = discourse_detail.objects.filter(id=ids).all()
            special_detail = DiscoursedetailModelSerializer(spec, many=True)
            topic = conn.hget("topic_" + str(ip), "1")
            if topic:
                mes['code'] = 200
                mes['list'] = special_detail.data
            else:
                for i in spec:
                    i.read_sum = i.read_sum + 1
                    i.save()
                mes['code'] = 200
                mes['list'] = special_detail.data
                conn.hset("topic_" + str(ip), "1",{"beizhu":'话题'})
        else:
            mes['code'] = 10010
            mes['erro'] = '没有传递参数'
            
        return Response(mes)

class Optimization_list(APIView):
    """
    优选页面
    """
    def get(self,request):
        mes = {}
        spec = Super_goods.objects.all()
        special_detail = SupergoodsModelSerializer(spec,many=True)
        mes['code'] = 200
        mes['list'] = special_detail.data
        return Response(mes)

class Optimization_detail_list(APIView):
    """
    优选详情页面 需要传递参数优选ID
    ?ids=id
    """
    def get(self,request):
        mes = {}
        ids = request.GET.get('ids',1)
        if ids:
            spec = Super_goods.objects.filter(super_id=ids).all()
            special_detail = SupergoodsModelSerializer(spec,many=True)
            mes['code'] = 200
            mes['list'] = special_detail.data
        return Response(mes)


class Preference_list(APIView):
    """
    特惠首页
    """
    def get(self,request):
        mes = {}
        todaydate = datetime.now().strftime("%Y-%m-%d")
        flashdate = Goods.objects.filter(
        promotionStartTime__lte=todaydate, promotionEndTime__gte=todaydate).all()
        good = GoodsModelSerializer(flashdate, many=True)
        mes['code'] = 200
        mes['list'] = good.data
        return Response(mes)

class Goods_list(APIView):
    """
    商品详情页面 需要传递参数商品ID
    ?ids=id
    """
    def get(self,request):
        mes = {}
        ids = request.GET.get('ids', 53467)
        # conn = get_redis_connection('default')
        # good_list = conn.hget("shop_" + str(ids), '1')
        if ids:
            # if good_list:
            #     goodlist = eval(good_list)
            #     goods = json.loads(goodlist['goods'])
            #     seckill = json.loads(goodlist['seckill'])
            #     mes['code'] = 200
            #     mes['list'] = goods
            #     mes['seckill'] = seckill
            # else:
            flashdate = Goods.objects.filter(id=ids).all()
            good = GoodslistModelSerializer(flashdate, many=True)
            mes['code'] = 200
            mes['list'] = good.data
                
        else:
            mes['code'] = 10010
            mes['error'] = '没有商品id'
        
        return Response(mes)

class Goods_pics(APIView):
    """
    商品图文详情 需要传递参数商品ID
    ?ids=id
    """
    def get(self,request):
        ids = request.GET.get('ids',1)
        mes = {}
        g = goods_pics.objects.filter(goods_id=ids).all()
        good = GoodspicsModelSerializer(g, many=True)
        mes['code'] = 200
        mes['list'] = good.data
        return Response(mes)

class Goods_special(APIView):
    """
    商品相关专题 需要传递参数商品ID
    ?ids=id
    """
    def get(self,request):
        ids = request.GET.get('ids',1)
        mes = {}
        g = Special_shop.objects.filter(goods_id_id=ids).all()
        good = SpeciaslModelSerializer(g, many=True)
        mes['code'] = 200
        mes['list'] = good.data
        return Response(mes)


class Goods_shopping(APIView):
    """
    购物车页面 需要传递参数商品ID
    data:data data是一个字典{"ids":id}
    """
    def post(self, request):
        data = request.data
        mes = {}
        conn = get_redis_connection('default')
        good_list = conn.hget("cart_1", '1')
        if good_list:
            g = cart.objects.filter(goods_id=1,user_id=1).all()
            good = cartModelSerializer(g, many=True)
            mes['code'] = 200
            mes['seckil'] = eval(good_list)
            mes['list'] = good.data
        else:
            g = cart.objects.filter(goods_id=1,user_id=1).all()
            good = cartModelSerializer(g, many=True)
            mes['code'] = 200
            mes['list'] = good.data
        return Response(mes)

class Add_cart(APIView):
    """
    加入购物车
    data:data {'list':list,'seckil':seckil}   如果seckil没有值就传递空值
    """
    def post(self, request):
        data = request.data
        mes = {}
        conn = get_redis_connection('default')
        if not data['seckil']:
            good = Goods.objects.filter(id=data['goods_id']).first()
            if good:
                if good.stock > data['count']:
                    cart = CartSerializer(data=data)
                    if cart.is_valid():
                        cart.save()
                        mes['code'] = 200
                        mes['erro'] = '成功加入购物车'
                    else:
                        mes['code'] = 10010
                        mes['erro'] = '加入购物车失败'
                else:
                    mes['code'] = 10010
                    mes['erro'] = '库存不足'
            else:
                mes['code'] = 10010
                mes['erro'] = '没有此商品'
        else:
            conn.hset("cart_1", "1", {'list': data['list'], "seckil": data['seckil']})
            mes['code'] = 200
            mes['erro'] = '秒杀产品成功加入购物车'
            
        return Response(mes)

class Goods_comment1(APIView):
    """
    商品评价页面 需要传递参数商品ID
    ?ids=id
    """
    def get(self, request):
        ids = request.GET.get('ids',1)
        mes = {}
        g = Goods_comment.objects.filter(goods_id=ids).all()
        good = GoodscommentModelSerializer(g, many=True)
        mes['code'] = 200
        mes['list'] = good.data
        return Response(mes)

class Order_address(APIView):
    """
    订单的用户地址信息
    """
    def post(self, request):
        user = 1
        mes = {}
        adres = address.objects.filter(user_id=user,is_default=1).all()
        orcart = AddressModelSerializer(adres, many=True)
        mes['code'] = 200
        mes['list'] = orcart.data
        return Response(mes)

class Order_goods(APIView):
    """
    订单的商品信息 需要传递购物车信息
    data:{'ids':[1,2,3]}
    """
    def post(self, request):
        ids = request.data
        user = 1
        mes = {}
        c = cart.objects.filter(user_id=user,id=1).all()
        cardetail = cartModelSerializer(c,many=True)
        mes['code'] = 200
        mes['list'] = cardetail.data
        return Response(mes)

class Order_score(APIView):
    """
    用户积分表
    """
    def get(self, request):
        ids = request.data
        user = 1
        mes = {}
        c = score.objects.filter(user_id=user).all()
        cardetail = scoreModelSerializer(c,many=True)
        mes['code'] = 200
        mes['list'] = cardetail.data
        return Response(mes)

class Order_discounts(APIView):
    """
    优惠卷表
    """
    def get(self, request):
        ids = request.data
        user = 1
        mes = {}
        c = user_label.objects.filter(user_id=user).all()
        cardetail = User_labelModelSerializer(c,many=True)
        mes['code'] = 200
        mes['list'] = cardetail.data
        return Response(mes)


