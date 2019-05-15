from rest_framework import serializers
from sadmin.models import *
from werkzeug.security import generate_password_hash, check_password_hash

#获取商品
class GoodsModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Goods
        fields = ('id', 'name', 'price','note','pic')

#获取SKU库存
class PmsSkuStockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PmsSkuStock
        fields = "__all__"

#首页专题
class SpecialModelSerializer(serializers.ModelSerializer):
    special_cate = serializers.SerializerMethodField()

    class Meta:
        model = Special
        fields = "__all__"

    def get_special_cate(self, obj):
        spe_c = special_category.objects.filter().all()
        spe_cate = SpecialcategoryModelSerializer(spe_c, many=True)
        return spe_cate.data


#专题页面
class SpecialcateModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Special
        fields = '__all__'

#专题评论
class SpecialcommentModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Special_comment
        fields = '__all__'


#专题分类
class SpecialcategoryModelSerializer(serializers.ModelSerializer):
    special_detail = serializers.SerializerMethodField()

    class Meta:
        model = special_category
        fields = ("__all__")
    
    def get_special_detail(self, obj):
        
        special_detail1 = Special.objects.filter(special_cate_id=obj.id).all()
        special_serializer = SpecialcateModelSerializer(special_detail1,many=True)
        return special_serializer.data
     
#获取专题商品
class SpecialshopModelSerializer(serializers.ModelSerializer):
    special_detail = serializers.SerializerMethodField()
    special_shop_detail = serializers.SerializerMethodField()

    class Meta:
        model = Special_shop
        fields = "__all__"
    
    def get_special_detail(self, obj):
        special_detail1 = Special.objects.filter(id=obj.special_id_id).all()
        special_serializer = SpecialcateModelSerializer(special_detail1, many=True)
        for i in special_detail1:
            special_com = Special_comment.objects.filter(discourse_id=i.id).all()
            special_com_serializer = SpecialcommentModelSerializer(special_com, many=True)
        return {"special":special_serializer.data,"special_detail":special_com_serializer.data}
    
    def get_special_shop_detail(self, obj):
        special_detail1 = Goods.objects.filter(id=obj.goods_id_id).all()
        special_serializer = GoodsModelSerializer(special_detail1, many=True)
        return special_serializer.data

#获取猜你喜欢
class Guess_likeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess_like
        fields = "__all__"

#获取秒杀时间段
class QuentumModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quentum
        fields = ('id','start_time','end_time')

# 首页秒杀列表
class FlashProductModelSerializer(serializers.ModelSerializer):
    product_detail = serializers.SerializerMethodField()

    class Meta:
        model = Ceckil_goods_relation
        fields = ('__all__')

    def get_product_detail(self, obj):
        product = Goods.objects.filter(id=obj.goods_id_id).all()
        product_serializer = GoodsModelSerializer(product,many=True)
        q = Quentum.objects.filter(id=obj.quentum_id_id).all()
        quen1 = QuentumModelSerializer(q, many=True)
        return {"seckill_time":quen1.data,"Goods":product_serializer.data}


#获取品牌
class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = brand
        fields = ('id', 'name', 'logo','min_price')

#获取分类
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id','name','image')
    
#获取分类与二级分类
class CategorylistModelSerializer(serializers.ModelSerializer):
    category_level = serializers.SerializerMethodField()

    class Meta:
        model = category
        fields = ('__all__')

    def get_category_level(self, obj):
        print(obj.name, '=============')
        b = category.objects.filter(parent_id=obj.id).all()
        adv = CategoryModelSerializer(b,many=True)
        return adv.data


#获取类型
class goods_typeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = goods_type
        fields = "__all__"

#获取标签
class labelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = label
        fields = "__all__"

#获取话题图片
class Discourse_comment_imgModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = discourse_comment_img
        fields = ("id","pic")

#获取话题标签
class DiscourselabelModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = discourse_label
        fields = ("__all__")

#获取话题评论
class Discourse_commentModelSerializer(serializers.ModelSerializer):
    discourse_comment_imgage = serializers.SerializerMethodField()

    class Meta:
        model = discourse_comment
        fields = "__all__"
    
    def get_discourse_comment_imgage(self, obj):
        dis_cate = discourse_comment_img.objects.filter(discourse_comment_id=obj.id).all()
        discou_cate = Discourse_comment_imgModelSerializer(dis_cate,many=True)
        return discou_cate.data

#获取话题
class DiscourseModelSerializer(serializers.ModelSerializer):
    discourse_cate = serializers.SerializerMethodField()
    discourse_label = serializers.SerializerMethodField()
    discourse_comment = serializers.SerializerMethodField()

    class Meta:
        model = discourse_detail
        fields = "__all__"
    
    def get_discourse_cate(self, obj):
        dis_cate = discourse_category.objects.filter(id=obj.dc_id).all()
        discou_cate = DiscoursecategoryModelSerializer(dis_cate,many=True)
        return discou_cate.data

    def get_discourse_label(self, obj):
        dis_lab = discourse_label.objects.filter(discourse_detail_id_id=obj.id).all()
        for i in dis_lab:
            return {"label": i.label_id.labelname}
    
    def get_discourse_comment(self, obj):
        dis_com = discourse_comment.objects.filter(discourse_id=obj.id).order_by("-evaluate_sum")[:1]
        discou_comm = Discourse_commentModelSerializer(dis_com, many=True)
        return discou_comm.data

#获取话题分类
class DiscoursecategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = discourse_category
        fields = ("id","name")



#获取话题详情
class DiscoursedetailModelSerializer(serializers.ModelSerializer):
    discourse_cate = serializers.SerializerMethodField()
    discourse_label = serializers.SerializerMethodField()
    discourse_comment = serializers.SerializerMethodField()

    class Meta:
        model = discourse_detail
        fields = "__all__"
    
    def get_discourse_cate(self, obj):
        dis_cate = discourse_category.objects.filter(id=obj.dc_id).all()
        discou_cate = DiscoursecategoryModelSerializer(dis_cate,many=True)
        return discou_cate.data

    def get_discourse_label(self, obj):
        dis_lab = discourse_label.objects.filter(discourse_detail_id_id=obj.id).all()
        for i in dis_lab:
            return {"label": i.label_id.labelname}
    
    def get_discourse_comment(self, obj):
        dis_com = discourse_comment.objects.filter(discourse_id=obj.id).order_by("-evaluate_sum")[:3]
        discou_comm = Discourse_commentModelSerializer(dis_com, many=True)
        discour_c = discourse_comment.objects.filter(discourse_id=obj.id).all()
        discourse_comm = Discourse_commentModelSerializer(discour_c, many=True)
        return {"hot_discourse":discou_comm.data,"discourse_list":discourse_comm.data}
        

















#获取类型属性
class Goods_type_attributeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = goods_type_attribute
        fields = "__all__"

#获取广告
class AdvertisingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = ('id', 'name', 'pic')

#获取新闻
class NewsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
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

