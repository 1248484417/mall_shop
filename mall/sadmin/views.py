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
import datetime
from rest_framework.pagination import PageNumberPagination	
# Create your views here.

# Create your views here.
def upload_allimg(img):
    f = open(os.path.join(settings.UPLOAD_ROOT,'',img.name),'wb')
    #写文件 遍历图片文件流
    for chunk in img.chunks():
        f.write(chunk)
        #关闭文件流
    f.close()


#序列化自定义分页
class GoodsPagination(PageNumberPagination):
    page_size = 5 #每页多少条
    page_size_query_param = 'page_size'
    page_query_param = 'pageNum'
    max_page_size = 100 #最大限度多少页


class Image(APIView):
    def post(self, request):
        name = request.FILES.get('img')
        mes = {}
        try:
            upload_allimg(name)
            image = "http://127.0.0.1:8000/upload/" + name.name
            mes['image'] = image
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)


#分类列表二级分类
class Type_list(APIView):
    def get(self, request):
        id = request.GET.get('id')
        if id:
            res = category.objects.filter(parent_id=id).all()
            b = CategoryModelSerializer(res, many=True)
        else:
            res = category.objects.filter(level=0).all()
            b = CategoryModelSerializer(res, many=True)
        list1 = []
        for i in res:
            to_dict = {}
            to_dict['id'] = i.id
            to_dict['name'] = i.name
            cate = category.objects.filter(parent_id=i.id).all()
            list2 = []
            for a in cate:
                dict1 = {}
                dict1['id'] = a.id
                dict1['name'] = a.name
                list2.append(dict1)
            to_dict['children'] = list2
            list1.append(to_dict)
        mes = {}
        mes['code'] = 200
        mes['list'] = b.data
        mes['list1'] = list1
        return Response(mes)

#删除分类列表
class Delete_type_list(APIView):
    def get(self, request):
        id = request.GET.get('id')
        mes = {}
        try:
            cate_attribute.objects.filter(cate_id_id=id).delete()
            category.objects.filter(id=id).delete()
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

class Cate_show(APIView):
    def get(self, request):
        id = request.GET.get('ids')
        is_nav_status = request.GET.get('is_nav_status')
        status = request.GET.get('status')
        if is_nav_status:
            category.objects.filter(id=id).update(is_nav_status=is_nav_status)
        elif status:
            category.objects.filter(id=id).update(status=status)
        mes = {}
        mes['code'] = 200
        return Response(mes)

#添加分类
class Add_type(APIView):
    def post(self, request):
        id = request.GET.get('id')
        data = request.data
        mes = {}
        if id:
            cate = category.objects.filter(id=id).update(name=data['name'], level=data['level'], parent_id=data['level'], is_nav_status=data['is_nav_status'], status=data['status'], sort=data['sort'], image=data['icon'], keyword=data['keyword'], descrip=data['descrip'], count_danwei=data['count_danwei'])
            for i in data['productAttributeIdList']:
                cate_attribute.objects.filter(cate_id_id=cate.id, goods_type_attribute_id_id=i).delete()
                a = cate_attribute(cate_id_id=cate.id, goods_type_attribute_id_id=i)
                a.save()
            mes['code'] = 200
            mes['mess'] = '修改成功'
        else:
            if data['parent_id'] == 0:
                data['level'] = 0
                ser = CategorySerializer(data=data)
            else:
                data['level'] = 1
                ser = CategorySerializer(data=data)
            if ser.is_valid():
                a = ser.save()
                for i in data['productAttributeIdList']:
                    a = cate_attribute(cate_id_id=a.id, goods_type_attribute_id_id=i)
                    a.save()
                mes['code'] = 200
                mes['mess'] = '添加成功'
            else:
                print(ser.errors)
                mes['code'] = 10010
                mes['erro'] = '添加失败'
        return Response(mes)


#添加数据类型属性
class Add_property(APIView):
    def post(self, request):
        data = request.data
        id = request.GET.get('id')
        print(data)
        mes = {}
        if id:
            goods_type_attribute.objects.filter(id=id).update(name=data['name'],filter_type=data['filter_type'],is_select=data['is_select'],related_status=data['related_status'],select_type=data['select_type'],input_type=data['input_type'], input_list=data['input_list'],hand_add_status=data['hand_add_status'],sort=data['sort'],type=data['type'])
        else:
            g = goods_type.objects.filter(id=data['productAttributeCategoryId']).first()
            if data['input_list'] == '':
                del data['input_list']
            ser = AddgoodstypeSerializer(data=data, context={"g": g})
            if ser.is_valid():
                ser.save()
                
                if data['type'] == 0:
                    good = goods_type.objects.filter(id=data['productAttributeCategoryId']).first()
                    good.attribute_count = good.attribute_count + 1
                    good.save()
                else:
                    good = goods_type.objects.filter(id=data['productAttributeCategoryId']).first()
                    
                    good.param_count = good.param_count + 1
                    good.save()
            else:
                print(ser.errors)
        mes['code'] = 200
        return Response(mes)

#查询类型属性
class Type_shuxing(APIView):
    def get(self, request):
        g = goods_type.objects.filter()
        good = goods_typeModelSerializer(g, many=True)
        mes = {}
        mes['code'] = 200
        mes['list'] = good.data

        return Response(mes)

#删除数据类型属性
class Delete_pro(APIView): 
    def post(self, request):
        data = request.data['ids']
        data = ''.join(data).split(',')
        print(data[0])
        mes = {}
        try:
            cate_attribute.objects.filter(goods_type_attribute_id=data[0]).delete()
            goods_type_attribute.objects.get(id=data[0]).delete()
            mes['code'] = 200
            a = goods_type.objects.filter(id=data[1]).first()
            
            if data[1] == 0:
                a.attribute_count = a.attribute_count - 1
                a.save()
            else:
                a.param_count = a.param_count - 1
                a.save()
        except Exception as e:
            print(e)
            mes['code'] = 10010
        return Response(mes)


#添加数据类型
class Jia_leixing(APIView):
    def post(self, request):
        mes = {}
        mes['code'] = 200
        return Response(mes)

#商品分类下的类型
class Shop_type_cate(APIView):
    def get(self, request):
        id = request.GET.get('id')
        mes = {}
        if not id:
            goods = goods_type.objects.all()
            g = goods_typeModelSerializer(goods, many=True)
            mes['code'] = 200
            mes['list'] = g.data
        return Response(mes)

#品牌列表不分页
class Brand_list(APIView):
    def get(self, request):
        mes = {}
        br = brand.objects.all()
        b = BrandModelSerializer(br,many=True)
        mes['code'] = 200
        mes['list'] =b.data
        return Response(mes)

#商品类型
class Shop_type(APIView):
    def get(self, request):
        id = request.GET.get('id')
        name = request.GET.get('name')
        type1 = request.GET.get('type')
        mes = {}
        if not id:
            goods = goods_type.objects.all()
            g = goods_typeModelSerializer(goods, many=True)
            list2 = []
            for i in goods:
                dict1 = i.to_dict()
                a = goods_type_attribute.objects.filter(type_id=i.id, type=0).all()
                list1 = []
                for c in a:
                    dict2 = c.to_dict()
                    list1.append(dict2)
                dict1['productAttributeList'] = list1
                list2.append(dict1)
            mes['code'] = 200
            mes['list'] = g.data
            mes['list1'] = list2
        else:
            if name:
                goods = goods_type_attribute.objects.filter(type_id=id, type=name).all()
                g = Goods_type_attributeModelSerializer(goods, many=True)
            else:
                goods = goods_type_attribute.objects.filter(id=id).all()
                g = Goods_type_attributeModelSerializer(goods, many=True)
            mes['code'] = 200
            mes['list'] = g.data
        return Response(mes)



#添加商品类型
class Add_brand(APIView):
    def post(self, request):
        id = request.GET.get('id', '')
        data = request.data
        if id != 'null':
            goods_type.objects.filter(id=id).update(name=request.data['name'])
        else:
            rand = Goods_typeSerializer(data=request.data)
            if rand.is_valid():
                rand.save()
        mes = {}
        mes['code'] = 200
        return Response(mes)

#品牌推荐列表
class Pinpai_list(APIView):
    def get(self, request):
        mes = {}
        b = brand.objects.filter(is_recommend=1).all()
        b = BrandModelSerializer(b, many=True)
        mes['code'] = 200
        mes['list'] = b.data
        return Response(mes)

#品牌管理
class Shop_guan(APIView):
    def get(self, request):
        a = request.GET.get('name')
        pageSize = request.GET.get('pageSize')  #每页有多少条
        pages = GoodsPagination()
        pages.page_size=int(pageSize)
        if a != 'null' and a != None:
            res = brand.objects.filter(name__icontains=a).all()
        else:
            res = brand.objects.all()
        page_roles = pages.paginate_queryset(queryset=res,request=request, view=self)
        roles_ser = BrandModelSerializer(instance=page_roles, many=True)
        return pages.get_paginated_response(roles_ser.data)

#品牌排序
class Pinpai_sort(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        try:
            brand.objects.filter(id=data['id']).update(sort=data['sort'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#品牌管理
class Add_brand_show(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        try:
            for i in data:
                brand.objects.filter(id=i['brandId']).update(is_show=1)
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

class Pinpai_tuijian(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        is_recommend = request.GET.get('is_recommend')
        print(id,is_recommend)
        try:
            brand.objects.filter(id=int(id)).update(is_recommend=int(is_recommend))
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

class Brand_show(APIView):
    def get(self, request):
        id = request.GET.get('ids').split(',')
        is_company = request.GET.get('is_company')
        is_show = request.GET.get('is_show')
        mes = {}
        if id:
            if is_company:
                brand.objects.filter(id__in=id).update(is_company=is_company)
                mes['code'] = 200
            else:
                mes['code'] = 10010
            if is_show:
                brand.objects.filter(id__in=id).update(is_show=is_show)
                mes['code'] = 200
            else:
                mes['code'] = 10010
        else:
            mes['code'] = 10010

        return Response(mes)

#品牌管理详情页
class Brand_detail(APIView):
    def get(self, request):
        id = request.GET.get('id')

        res = brand.objects.filter(id=id).all()
        b = BrandModelSerializer(res, many=True)
        mes = {}
        mes['code'] = 200
        mes['list'] = b.data
        return Response(mes)
 
    def post(self, request):
        name = request.data
        id = request.GET.get('id')
        mes = {}
        if id:
            brand.objects.filter(id=id).update(name=name['name'],first=name['first'],logo=name['logo'],b_logo=name['b_logo'],story=name['story'],sort=name['sort'],is_show=name['is_show'],is_company=name['is_company'])
        else:
            rand = AddbrandSerializer(data=name)
            if rand.is_valid():
                rand.save()
                mes['code'] = 200
        
        return Response(mes)

#删除方法
class Del_pinpai(APIView):
    def get(self,request):
        id = request.GET.get('id')
        brand.objects.filter(id=id).delete()
        mes = {}
        mes['code'] = 200
        return Response(mes)
        

#删除方法
class Del_brand(APIView):
    def get(self,request):
        id = int(request.GET.get('id'))
        goods_type.objects.filter(id=id).delete()
        mes = {}
        mes['code'] = 200
        return Response(mes)

#添加广告
class Add_guanggao(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        a = Advertising.objects.filter(id=id).all()
        adver = AdvertisingModelSerializer(a, many=True)
        mes['list'] = adver.data
        mes['code'] = 200
        return Response(mes)
        
    def post(self, request):
        mes = {}
        gg = AdvertisingSerializer(data=request.data)
        if gg.is_valid():
            gg.save()
            mes['code'] = 200
        else:
            print(gg.errors)
            mes['code'] = 10010
            mes['erro'] = '添加失败'
        return Response(mes)

#广告列表
class Guanggao_list(APIView):
    def get(self, request):
        mes = {}
        a = Advertising.objects.all()
        adver = AdvertisingModelSerializer(a, many=True)
        mes['list'] = adver.data
        return Response(mes)

#修改广告上线下线
class Guanggao_show(APIView):
    def post(self, request):
        mes = {}
        id = request.GET.get('id')
        data = request.data
        try:
            Advertising.objects.filter(id=id).update(status=data['status'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
            mes['erro'] = '修改失败'
        return Response(mes)

#删除广告
class Guanggao_delete(APIView):
    def post(self, request):
        mes = {}
        data = request.data['ids'].split(',')
    
        try:
            for i in data:
                Advertising.objects.filter(id=int(i)).delete()
                mes['code'] = 200
        except:
            mes['code'] = 10010
            mes['erro'] = '删除失败'
        return Response(mes)

#查询会员
class Huiyuan_list(APIView):
    def get(self, request):
        mes = {}
        a = member_grade.objects.filter().all()
        adver = Member_gradeModelSerializer(a, many=True)
        mes['code'] = 200
        mes['list'] = adver.data
        mes['length'] = len(a)
        return Response(mes)

#添加商品
class Add_shop(APIView):
    def post(self,request):
        mes={}
        data = request.data
        print(data)
        #如果等于零是没有优惠
        goods=Goods(brandId=data['brandId'],    #品牌id
        productCategoryId=data['productCategoryId'],    #商品分类id
        feightTemplateId=data['feightTemplateId'],     
        productAttributeCategoryId=data['productAttributeCategoryId'],     #属性类型id
        name=data['name'],    #商品名字
        pic=data['pic'],      #图片链接
        productSn=data['productSn'],    # 货号
        deleteStatus=data['deleteStatus'],     # 删除状态: 0.未删除 1.已删除
        publishStatus=data['publishStatus'],  # 上架状态：0->下架；1->上架
        newStatus=data['newStatus'],   # 新品状态:0->不是新品；1->新品
        recommandStatus=data['recommandStatus'],   # 推荐状态；0->不推荐；1->推荐
        verifyStatus=data['verifyStatus'],   # 审核状态：0->未审核；1->审核通过
        sort=data['sort'],   # 排序
        sale=data['sale'],    # 销量
        price=data['price'],    #价格
        giftGrowth=data['giftGrowth'],    # 赠送的成长值
        giftPoint=data['giftPoint'],    # 赠送的积分
        usePointLimit=data['usePointLimit'],   # 限制使用的积分数
        subTitle=data['subTitle'],    # 副标题
        description=data['description'],    # 商品描述
        originalPrice=data['originalPrice'],  # 市场价
        stock=data['stock'],   # 库存
        lowStock=data['lowStock'],    # 库存预警值
        unit=data['unit'],   # 单位
        weight=data['weight'],   # 商品重量，默认为克
        previewStatus=data['previewStatus'],   # 是否为预告商品：0->不是；1->是
        serviceIds=str(data['serviceIds'].strip(',').split(',')),   # 以逗号分割的产品服务：1->无忧退货；2->快速退款；3->免费包邮
        keywords=data['keywords'],   #关键字
        note=data['note'],    #商品备注
        albumPics=data['albumPics'],    # 画册图片，连产品图片限制为5张，以逗号分割
        detailTitle=data['detailTitle'],      #详细页标题
        detailDesc=data['detailDesc'],     #详细页描述
        detailHtml=data['detailHtml'],     #电脑端详情
        detailMobileHtml=data['detailMobileHtml'],     #移动端详情
        promotionType=data['promotionType'],    # 促销类型：0->没有促销使用原价;1->使用促销价；2->使用会员价；3->使用阶梯价格；4->使用满减价格；5->限时购
        brandName=data['brandName'],      # 品牌名称
        productCategoryName=data['productCategoryName'])   # 产品分类名称
        goods.save()
        if data['promotionType']==1:       #type等于1 说明是特惠价格  入特惠价格表
            data['promotionEndTime']=time.time()
            data['promotionEndTime']=time.localtime()
            data['promotionEndTime']=time.strftime('%Y-%m-%d %H:%M:%S',data['promotionEndTime'])
            #转换时间格式
            data['promotionStartTime']=time.time()
            data['promotionStartTime']=time.localtime()
            data['promotionStartTime']=time.strftime('%Y-%m-%d %H:%M:%S',data['promotionStartTime'])
            goods_sales_price=Goods_sales_price(goods_id=goods.id,promotionPrice=data['promotionPrice'],promotionStartTime=data['promotionStartTime'],promotionEndTime=data['promotionEndTime'])
            goods_sales_price.save()
        elif data['promotionType']==2:       #type等于2   是会员价格  入会员价格表
            for i in data['memberPriceList']:
                goods_member=Goods_member_price(goods_id=goods.id,member_level_id=i['memberLevelId'],price=i['memberPrice'],Member_level_name=i['memberLevelName'])
                goods_member.save()
        elif data['promotionType']==3:   #type等于3   是阶梯价格   入阶梯价格表
            for i in data['productLadderList']:
                goods_fight=Goods_fight(product_id=goods.id,
                pro_count=int(i['count']),
                discount=float(i['discount']),
                price=float(i['discount'])*goods.price)
                goods_fight.save()
        elif data['promotionType']==4:   #type等于4   是满减价格    入满减价格表
            for i in data['productFullReductionList']:
                goods_full_price=Goods_full_price(product_id=goods.id,full_price=i['fullPrice'],reduce_price=i['reducePrice'])
                goods_full_price.save()
        for i in data['skuStockList']:
            
            p = PmsSkuStock(sp1=i['sp1'], sp2=i['sp2'], pic=i['pic'], product_id=goods.id,price=i['price'],stock=i['stock'],lowStock=i['lowStock'],skuCode=i['skuCode'])
            p.save()
            
        mes['code']=200
        return Response(mes)

#商品列表
class Goods_list(APIView):
    def get(self, request):
        mes = {}
        g = Goods.objects.all()
        good = GoodsModelSerializer(g,many=True)
        mes['code'] = 200
        mes['list'] = good.data
        return Response(mes)

#编辑商品库存
class Goods_bianji(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        print(id)
        good = PmsSkuStock.objects.filter(product_id=int(id)).all()
        g = PmsSkuStockModelSerializer(good,many=True)
        mes['code'] = 200
        mes['list'] = g.data
        print(mes)
        return Response(mes)

#删除商品
class Goods_delete(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        try:
            Goods.objects.filter(id=id).delete()
            PmsSkuStock.filter(product_id=id).delete()
            mes['code'] = 200
        except:
            mes['code'] = 10010
        
        return Response(mes)

#新品推荐商品列表
class Goods_xinpin(APIView):
    def get(self, request):
        mes = {}
        g = Goods.objects.filter(recommandStatus=1).all()
        good = GoodsModelSerializer(g,many=True)
        mes['code'] = 200
        mes['list'] = good.data
        return Response(mes)

#修改新品推荐商品
class Goods_xinpin_update(APIView):
    def post(self, request):
        data = request.data
        mes = {}
        try:  
            Goods.objects.filter(id=int(data['ids'])).update(recommandStatus=int(data['recommendStatus']))
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#修改新品推荐商品列表
class Goods_xinpinlist_update(APIView):
    def post(self, request):
        data = request.data
        mes = {}
        try:
            for i in data:
                Goods.objects.filter(id=int(i['productId'])).update(recommandStatus=1)
                mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#修改新品推荐商品排序
class Goods_xinpin_sort(APIView):
    def post(self, request):
        mes = {}
        params = request.query_params
        id = request.GET.get('id')
        try:
            Goods.objects.filter(id=int(id)).update(sort=params['sort'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#修改商品是否新品推荐
class Goods_xin_update(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        try:
            Goods.objects.filter(id=data['ids']).update(newStatus=data['newStatus'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)


#修改商品上架状态
class Goods_status_update(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        try:
            Goods.objects.filter(id=data['ids']).update(publishStatus=data['publishStatus'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#删除商品
class Goods_xinpin_delete(APIView):
    def post(self, request):
        mes = {}
        id = request.data
        try:
            Goods.objects.filter(id=data['ids']).delete()
            mes['code'] = 200
        except:
            mes['code'] = 10010
        
        return Response(mes)


#优惠卷表
class Coupon_list(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        if id:
            c = coupon.objects.filter(id=id).all()
        else:
            c = coupon.objects.all()
        ceck = CouponModelSerializer(c, many=True)
        mes['code'] = 200
        mes['list'] = ceck.data
        return Response(mes)

#添加优惠卷
class Add_coupon(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        print(data)
        cac = couponSerializer(data=data)
        if cac.is_valid():
            a = cac.save()
            if data['useType'] == 1:
                for i in data['productCategoryRelationList']:
                    c = {'coupon_id_id':a.id,'cate_id_id':i['productCategoryId']}
                    cou = couponcateSerializer(data=c)
                    if cou.is_valid():
                        cou.save()
                        mes['code'] = 200
                        mes['message'] = '添加成功'
                    else:
                        print(cou.errors)
                        mes['code'] = 10010
            # elif data['useType'] == 2:
            #     for i in data['productCategoryRelationList']:
            #         c = {'coupon_id_id':a.id,'cate_id_id':i['productCategoryId']}
            #         cou = couponcateSerializer(data=c)
            #         if cou.is_valid():
            #             cou.save()
            #             mes['code'] = 200
            #             mes['message'] = '添加成功'
            #         else:
            #             print(cou.errors)
            #             mes['code'] = 10010
        else:
            print(cac.errors)
            mes['code'] = 10010
        return Response(mes)

#查询商品
class Goods_query(APIView):
    def get(self, request):
        mes = {}
        params = request.query_params
        good = Goods.objects.filter(name__icontains=params['keyword']).all()
        g = GoodsModelSerializer(good,many=True)
        mes['code'] = 200
        mes['list'] = g.data
        return Response(mes)

#删除优惠卷
class Coupon_delete(APIView):
    def get(self, request):
        id = request.GET.get('id')
        mes = {}
        try:
            cou = coupon.objects.filter(id=id).first()
            if cou.useType == 1:
                coupon_cate.objects.filter(coupon_id=cou.id).delete()
            elif cou.useType == 2:
                pass
            else:
                pass
            coupon.objects.filter(id=id).delete()
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#修改优惠卷
class Coupon_update(APIView):
    def post(self, request):
        mes = {}
        id = request.GET.get('id')
        data = request.data
        try:
            coupon.objects.filter(id=id).update(type=data['type'], name=data['name'], platform=data['platform'], publishCount=data['publishCount'], amount=data['amount'], perLimit=data['perLimit'], minPoint=data['minPoint'], startTime=data['startTime'], endTime=data['endTime'], note=data['note'])
            goods_coupon.objects.filter(coupon_id_id=id).delete()
            for i in data['productCategoryRelationList']:
                c = {'coupon_id_id':id,'cate_id_id':i['productCategoryId']}
                cou = couponcateSerializer(data=c)
                if cou.is_valid():
                    cou.save()
                    mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)


#活动列表
class Huodong_list(APIView):
    def get(self, request):
        mes = {}
        c = Ceckil.objects.all()
        ceck = CeckilModelSerializer(c, many=True)
        mes['code'] = 200
        mes['list'] = ceck.data
        return Response(mes)

#添加活动
class Add_huodong(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        cac = CeckilSerializer(data=data)
        if cac.is_valid():
            cac.save()
            mes['code'] = 200
            mes['message'] = '添加成功'
        else:
            print(cac.errors)
            mes['code'] = 10010
        return Response(mes)

#删除活动
class Huodong_delete(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        try:
            Ceckil.objects.filter(id=id).delete()
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#修改活动状态
class Huodong_status_show(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        id = request.GET.get('id')
        try:
            Ceckil.objects.filter(id=id).update(status=data['status'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#添加秒杀活动
class Add_miaoshahuodong(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        cac = CeckilactivitySerializer(data=data)
        if cac.is_valid():
            cac.save()
            mes['code'] = 200
            mes['message'] = '添加成功'
        else:
            print(cac.errors)
            mes['code'] = 10010
        return Response(mes)

#秒杀活动列表
class Miaoshahuodong_list(APIView):
    def get(self, request):
        mes = {}
        data = request.query_params
        if data:
            c = Ceckil_activity.objects.filter(status=data['flashPromotionId']).all()
        else:
            c = Ceckil_activity.objects.all()
        ceck = CeckilactivityModelSerializer(c, many=True)
        mes['code'] = 200
        mes['list'] = ceck.data
        return Response(mes)

#秒杀活动状态
class Update_miaoshahuodong(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        id = request.GET.get('id')
        try:
            Ceckil_activity.objects.filter(id=id).update(status=data['status'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#删除秒杀活动
class Miaoshahuodong_delete(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        try:
            Ceckil_activity.objects.filter(id=id).delete()
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#订单设置
class Order_setting(APIView):
    def post(self, request):
        mes = {}
        data = request.data
        id = request.GET.get('id')
        try:
            Dingdan_setting.objects.filter(id=id).update(flashOrderOvertime=data['flashOrderOvertime'], normalOrderOvertime=data['normalOrderOvertime'], confirmOvertime=data['confirmOvertime'], finishOvertime=data['finishOvertime'], commentOvertime=data['commentOvertime'])
            mes['code'] = 200
        except:
            mes['code'] = 10010
        return Response(mes)

#订单设置列表
class Dingdan_setting_list(APIView):
    def get(self, request):
        mes = {}
        id = request.GET.get('id')
        o = Dingdan_setting.objects.filter(id=id).all()
        s = DingdansettingModelSerializer(o, many=True)
        mes['code'] = 200
        mes['list'] = s.data
        return Response(mes)
