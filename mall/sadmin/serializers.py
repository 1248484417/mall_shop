from rest_framework import serializers
from sadmin.models import *
from werkzeug.security import generate_password_hash, check_password_hash

#获取商品
class GoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = "__all__"

#获取SKU库存
class PmsSkuStockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsSkuStock
        fields = "__all__"

#获取品牌
class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = brand
        fields = "__all__"

#获取分类
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = "__all__"
    
#获取类型
class goods_typeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = goods_type
        fields = "__all__"

#获取类型属性
class Goods_type_attributeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = goods_type_attribute
        fields = "__all__"

#获取广告
class AdvertisingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = "__all__"

#获取会员
class Member_gradeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = member_grade
        fields = "__all__"

#获取活动
class CeckilModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceckil
        fields = "__all__"

#获取秒杀活动
class CeckilactivityModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceckil_activity
        fields = "__all__"

#获取订单设置
class DingdansettingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dingdan_setting
        fields = "__all__"

#获取优惠卷
class CouponModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = coupon
        fields = "__all__"

#添加类型
class AddbrandSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=50)
    first = serializers.CharField(required=True, max_length=100)
    logo = serializers.CharField(required=True, max_length=255)
    b_logo = serializers.CharField(required=True, max_length=255)
    story = serializers.CharField(required=True, max_length=255)
    sort = serializers.IntegerField(required=True)
    is_show = serializers.IntegerField(required=True)
    is_company = serializers.IntegerField(required=True)
    
    def create(self, validated_data):
        return brand.objects.create(**validated_data)

#添加类型
class Goods_typeSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    
    def create(self, validated_data):
        return goods_type.objects.create(**validated_data)

#添加类型属性
class AddgoodstypeSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    filter_type = serializers.IntegerField(required=True)
    is_select = serializers.IntegerField(required=True)
    related_status = serializers.IntegerField(required=True)
    select_type = serializers.IntegerField(required=True)
    input_type = serializers.IntegerField(required=True)
    input_list = serializers.CharField(default='')
    hand_add_status = serializers.IntegerField(required=True)
    sort = serializers.IntegerField(required=True)
    type = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return goods_type_attribute.objects.create(type_id=self.context["g"],**validated_data)


#添加分类
class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=100)
    level = serializers.IntegerField(required=True)
    parent_id = serializers.IntegerField(required=True)
    is_nav_status = serializers.IntegerField(required=True)
    status = serializers.IntegerField(required=True)
    sort = serializers.IntegerField(required=True)
    image = serializers.CharField(required=True, max_length=100)
    keyword = serializers.CharField(required=True, max_length=100)
    descrip = serializers.CharField(required=True, max_length=255)
    count_danwei = serializers.CharField(required=True, max_length=255)
    
    def create(self, validated_data):
        return category.objects.create(**validated_data)

#添加广告
class AdvertisingSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255)
    type = serializers.IntegerField(required=True)
    pic = serializers.CharField(required=True, max_length=255)
    startTime = serializers.CharField(required=True, max_length=255)
    endTime = serializers.CharField(required=True, max_length=255)
    url = serializers.CharField(required=True, max_length=255)
    status = serializers.IntegerField(required=True)
    note = serializers.CharField(required=True, max_length=255)
    sort = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Advertising.objects.create(**validated_data)

#添加活动
class CeckilSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=30)
    startDate = serializers.DateTimeField(required=True,)
    endDate = serializers.DateTimeField(required=True,)
    status = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Ceckil.objects.create(**validated_data)

#添加秒杀活动
class CeckilactivitySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=30)
    startTime = serializers.DateTimeField(required=True,)
    endTime = serializers.DateTimeField(required=True,)
    status = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Ceckil_activity.objects.create(**validated_data)

#添加订单设置
class OrdersettingSerializer(serializers.Serializer):
    flashOrderOvertime = serializers.IntegerField(required=True)
    normalOrderOvertime = serializers.IntegerField(required=True)
    confirmOvertime = serializers.IntegerField(required=True)
    finishOvertime = serializers.IntegerField(required=True)
    commentOvertime = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Order_setting.objects.create(**validated_data)

#添加优惠卷表
class couponSerializer(serializers.Serializer):
    type = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True, max_length=100)
    platform = serializers.IntegerField(required=True)
    publishCount = serializers.IntegerField(required=True)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
    perLimit = serializers.IntegerField(required=True)
    minPoint = serializers.DecimalField(max_digits=8, decimal_places=2)
    startTime = serializers.DateTimeField(required=True,)
    endTime = serializers.DateTimeField(required=True,)
    note = serializers.CharField(required=True, max_length=255)
    useType = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return coupon.objects.create(**validated_data)

#添加分类优惠卷表
class couponcateSerializer(serializers.Serializer):
    coupon_id_id = serializers.IntegerField(required=True)
    cate_id_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return coupon_cate.objects.create(**validated_data)

