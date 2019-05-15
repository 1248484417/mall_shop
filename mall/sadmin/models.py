from django.db import models

# Create your models here.
class BaseModel(models.Model):
    create_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
        
#后台用户表
class sadmins(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    image = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    login_time=models.DateTimeField()
    
    class Meta():
        db_table = 'sadmins'

#后台角色表
class roles(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    status = models.IntegerField(default=1)

    class Meta():
        db_table = 'roles'

#用户角色关联表
class admin_roles(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(roles, to_field='id', on_delete='CASCADE', related_name='role_res')
    admin_id = models.ForeignKey(sadmins, to_field='id', on_delete='CASCADE', related_name='admin_role')

    class Meta():
        db_table = 'admin_roles'

#权限表
class permission(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=255)
    url = models.CharField(max_length=100)
    status = models.IntegerField(default=1)

    class Meta():
        db_table = 'permission'

#角色权限表
class role_permission(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    role_id = models.ForeignKey(roles, to_field='id', on_delete='CASCADE', related_name='role_id')
    permission_id = models.ForeignKey(permission, to_field='id', on_delete='CASCADE', related_name='permission_id')

    class Meta():
        db_table = 'role_permission'

#分类表
class category(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=0)
    parent_id = models.IntegerField(default=0)
    is_nav_status = models.IntegerField(default=1)
    status = models.IntegerField(default=1)
    sort = models.IntegerField(default=0)
    image = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    descrip = models.CharField(max_length=255)
    count_danwei = models.CharField(max_length=255)

    class Meta():
        db_table = 'category'

#商品类型表
class goods_type(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    attribute_count = models.IntegerField(default=0)
    param_count = models.IntegerField(default=0)
    
    class Meta():
        db_table = 'goods_type'

    def to_dict(self):
        dict = {'id': self.id, 'name': self.name}
        return dict

#商品类型属性表
class goods_type_attribute(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type_id = models.ForeignKey(goods_type, to_field='id', on_delete='CASCADE', related_name='type_id')
    filter_type = models.IntegerField(default=1)
    is_select = models.IntegerField(default=0)
    related_status = models.IntegerField(default=0)
    select_type = models.IntegerField()
    input_type = models.IntegerField(default=0)
    input_list = models.CharField(max_length=255,default='')
    hand_add_status = models.IntegerField(default=0)
    sort = models.IntegerField()
    type = models.IntegerField()
    
    class Meta():
        db_table = 'goods_type_attribute'

    def to_dict(self):
        dict = {'id': self.id, 'name': self.name}
        return dict


#分类属性关联表
class cate_attribute(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    cate_id = models.ForeignKey(category, to_field='id', on_delete='CASCADE', related_name='cate_id')
    goods_type_attribute_id = models.ForeignKey(goods_type_attribute, to_field='id', on_delete='CASCADE', related_name='goods_type_attribute_id')

    class Meta():
        db_table = 'cate_attribute'

#品牌表
class brand(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    first = models.CharField(max_length=100)
    logo = models.CharField(max_length=255)
    b_logo = models.CharField(max_length=255)
    story = models.CharField(max_length=255)
    sort = models.IntegerField()
    is_show = models.IntegerField(default=0)
    is_company = models.IntegerField(default=0)
    is_recommend = models.IntegerField(default=0)
    min_price = models.IntegerField(default=0)

    class Meta:
        db_table = "brand"


#猜你喜欢表
class Guess_like(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    describe = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    price = models.IntegerField(default=0)

    class Meta:
        db_table = "guess_like"

#前台用户表
class user(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    login_count = models.IntegerField(default=0)

    class Meta:
        db_table = "user"

#用户信息表
class user_detail(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50)
    sex = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    birthday = models.DateTimeField()
    city = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    personalized = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    growth = models.IntegerField(default=0)

    class Meta:
        db_table = "user_detail"

#用户成长值表
class growth(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    descrip = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)

    class Meta:
        db_table = "growth"

#用户积分表
class score(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    descrip = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    action = models.IntegerField(default=0)

    class Meta:
        db_table = "score"

#标签表
class label(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    labelname = models.CharField(max_length=255)

    class Meta:
        db_table = "label"

#话题分类表
class discourse_category(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "discourse_category"

#话题详情表
class discourse_detail(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    user_id = models.IntegerField(default=0)
    user_name = models.CharField(max_length=255)
    user_head_image = models.CharField(max_length=255)
    is_hort = models.IntegerField(default=0)
    content = models.CharField(max_length=255)
    collect_sum = models.IntegerField(default=0)
    read_sum = models.IntegerField(default=0)
    evaluate_sum = models.IntegerField(default=0)
    is_show = models.IntegerField(default=0)
    dc_id = models.IntegerField(default=0) #所属分类id

    class Meta:
        db_table = "discourse_detail"

#话题标签表
class discourse_label(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    label_id = models.ForeignKey(label, to_field='id', on_delete='CASCADE', related_name='label_id')
    discourse_detail_id = models.ForeignKey(discourse_detail, to_field='id', on_delete='CASCADE', related_name='discourse_detail_id')

    class Meta():
        db_table = 'discourse_label'

#用户话题收藏表
class discourse_collect(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, to_field='id', on_delete='CASCADE', related_name='user_id')
    discourse_id = models.ForeignKey(discourse_detail, to_field='id', on_delete='CASCADE', related_name='discourse_id')
    Type = models.IntegerField(default=0) #1话题  2专题  3商品 4 品牌

    class Meta():
        db_table = 'discourse_collect'

#话题评论表
class discourse_comment(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    user_head_image = models.CharField(max_length=255)
    user_address = models.CharField(max_length=255)
    user_profession = models.CharField(max_length=255)
    discourse_id = models.IntegerField()
    content = models.CharField(max_length=255)
    pid = models.IntegerField(default=0)
    evaluate_sum = models.IntegerField(default=0)
    collect_sum = models.IntegerField(default=0)

    class Meta:
        db_table = "discourse_comment"

#话题评论图片表
class discourse_comment_img(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    discourse_comment_id = models.IntegerField()
    pic = models.CharField(max_length=255)

    class Meta:
        db_table = "discourse_comment_img"

#评论点赞表
class comment_zan(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, to_field='id', on_delete='CASCADE', related_name='u_id')
    discourse_comment_id = models.ForeignKey(discourse_comment, to_field='id', on_delete='CASCADE', related_name='dc_id')

    class Meta():
        db_table = 'comment_zan'

#话题评论表
class discourse_award(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    discourse_id = models.IntegerField()
    discrip = models.CharField(max_length=255)
    number = models.IntegerField(default=0)
    Type = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    label_id = models.CharField(max_length=255) 

    class Meta:
        db_table = "discourse_award"


#用户优惠卷表
class user_label(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    coupon_id = models.IntegerField()
    user_id = models.IntegerField()
    starttime = models.DateTimeField()
    stoptime = models.DateTimeField()
    coupon_code = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    
    class Meta:
        db_table = "user_label"

#喜欢的分类表
class like_category(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, to_field='id', on_delete='CASCADE', related_name='yonghu_id')
    category_id = models.ForeignKey(category, to_field='id', on_delete='CASCADE', related_name='c_id')

    
    class Meta:
        db_table = "like_category"

#用户关注的品牌
class user_concern_brand(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(user, to_field='id', on_delete='CASCADE', related_name='user_brand_id')
    brand_id = models.ForeignKey(brand, to_field='id', on_delete='CASCADE', related_name='brand_id')

    
    class Meta:
        db_table = "user_concern_brand"

# 商品信息表
class Goods(BaseModel,models.Model):
    id = models.BigAutoField(primary_key=True)
    brandId = models.BigIntegerField(blank=True, null=True) #品牌id
    productCategoryId = models.BigIntegerField(blank=True, null=True) #商品分类id
    feightTemplateId = models.BigIntegerField(blank=True, null=True) #
    productAttributeCategoryId = models.BigIntegerField(blank=True, null=True) #属性类型id
    name = models.CharField(max_length=64)
    pic = models.CharField(max_length=255, blank=True, null=True) #图片
    productSn = models.CharField(max_length=64) # 货号
    deleteStatus = models.IntegerField(blank=True, null=True) # 删除状态: 0.未删除 1.已删除
    publishStatus = models.IntegerField(blank=True, null=True) # 上架状态：0->下架；1->上架
    newStatus = models.IntegerField(blank=True, null=True) # 新品状态:0->不是新品；1->新品
    recommandStatus = models.IntegerField(blank=True, null=True) # 推荐状态；0->不推荐；1->推荐
    verifyStatus = models.IntegerField(blank=True, null=True) # 审核状态：0->未审核；1->审核通过
    sort = models.IntegerField(blank=True, null=True)# 排序
    sale = models.IntegerField(blank=True, null=True) # 销量
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) 
    promotionPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # 促销价格
    giftGrowth = models.IntegerField(blank=True, null=True) # 赠送的成长值
    giftPoint = models.IntegerField(blank=True, null=True) # 赠送的积分
    usePointLimit = models.IntegerField(blank=True, null=True) # 限制使用的积分数
    subTitle = models.CharField(max_length=255, blank=True, null=True) # 副标题
    description = models.TextField(blank=True, null=True) # 商品描述
    originalPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # 市场价
    stock = models.IntegerField(blank=True, null=True) # 库存
    lowStock = models.IntegerField(blank=True, null=True) # 库存预警值
    unit = models.CharField(max_length=16, blank=True, null=True) # 单位
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # 商品重量，默认为克
    previewStatus = models.IntegerField(blank=True, null=True) # 是否为预告商品：0->不是；1->是
    serviceIds = models.CharField(max_length=64, blank=True, null=True)# 以逗号分割的产品服务：1->无忧退货；2->快速退款；3->免费包邮
    keywords = models.CharField(max_length=255, blank=True, null=True) #关键字
    note = models.CharField(max_length=255, blank=True, null=True) #商品备注
    albumPics = models.CharField(max_length=255, blank=True, null=True) # 画册图片，连产品图片限制为5张，以逗号分割
    detailTitle = models.CharField(max_length=255, blank=True, null=True)
    detailDesc = models.TextField(blank=True, null=True)
    detailHtml = models.TextField(blank=True, null=True) # 产品详情网页内容
    detailMobileHtml = models.TextField(blank=True, null=True) # 移动端网页详情
    promotionStartTime = models.DateTimeField(blank=True, null=True) # 促销开始时间
    promotionPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # 促销价格
    promotionEndTime = models.DateTimeField(blank=True, null=True) # 促销结束时间
    promotionPerLimit = models.IntegerField(blank=True, null=True) # 活动限购数量
    promotionType = models.IntegerField(blank=True, null=True)# 促销类型：0->没有促销使用原价;1->使用促销价；2->使用会员价；3->使用阶梯价格4->使用满减价格；5->限时购
    brandName = models.CharField(max_length=255, blank=True, null=True) # 品牌名称
    productCategoryName = models.CharField(max_length=255, blank=True, null=True)  # 产品分类名称
    popularity = models.IntegerField(default=0) #人气推荐

    class Meta:
        db_table = 'goods'

# sku的库存
class PmsSkuStock(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_id = models.BigIntegerField(blank=True, null=True) #商品id
    skuCode = models.CharField(max_length=64) # sku编码
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #价格
    stock = models.IntegerField(blank=True, null=True) # 库存
    lowStock = models.IntegerField(blank=True, null=True) # 预警库存
    sp1 = models.CharField(max_length=64, blank=True, null=True) # 销售属性
    sp2 = models.CharField(max_length=64, blank=True, null=True)
    pic = models.CharField(max_length=255, blank=True, null=True) # 展示图片
    sale = models.IntegerField(blank=True, null=True,default=0) # 销量
    promotionPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # 单品促销价格

    class Meta:
        db_table = 'pms_sku_stock'

#商品促销价格
class Goods_sales_price(models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()       #商品id
    promotionPrice = models.DecimalField(max_digits=8,decimal_places=2, blank=True, null=True)    #促销价格
    promotionStartTime = models.DateTimeField(blank=True, null=True,auto_now_add=True)    #开始时间
    promotionEndTime = models.DateTimeField(blank=True, null=True,auto_now_add=True)     #结束时间

    class Meta:
        db_table = 'goods_sales_price'

#商品会员价格表
class Goods_member_price(models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()       #商品id
    member_level_id = models.IntegerField()      #会员等级id
    price = models.DecimalField(max_digits=8,decimal_places=2)     #会员价格
    Member_level_name = models.CharField(max_length=50)     #会员等级名称


    class Meta:
        db_table = 'goods_member_price'

#商品阶梯价格表
class Goods_fight(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()       #商品id
    pro_count = models.IntegerField()      #数量
    discount = models.DecimalField(max_digits=8,decimal_places=2)     #折扣
    price = models.DecimalField(max_digits=8,decimal_places=2)    #商品价格


    class Meta:
        db_table = 'goods_fight'

#商品满减表
class Goods_full_price(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField()       #商品id
    full_price = models.DecimalField(max_digits=8,decimal_places=2)      #满对少钱
    reduce_price = models.DecimalField(max_digits=8,decimal_places=2)    #减多少钱


    class Meta:
        db_table = 'goods_full_price'

#商品属性表
class goods_attribute_value(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.ForeignKey(Goods, to_field='id', on_delete='CASCADE', related_name='g_id')
    attribute_id = models.ForeignKey(goods_type_attribute, to_field='id', on_delete='CASCADE', related_name='attribute_id')

    class Meta:
        db_table = "goods_attribute_value"

#商品属性库存表
class goods_attribute_stock(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()
    sku_code = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField(default=0)
    low_stock = models.IntegerField(default=0)
    sp1 = models.CharField(max_length=255)
    sp2 = models.CharField(max_length=255)
    sp3 = models.CharField(max_length=255)
    sale = models.IntegerField(default=0)
    lock_stocp = models.IntegerField(default=0)

    class Meta:
        db_table = "goods_attribute_stock"

#商品相册表
class goods_pics(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()
    pic = models.CharField(max_length=255)

    class Meta:
        db_table = "goods_pics"

#优惠卷表
class coupon(models.Model):
    id = models.AutoField(primary_key=True)
    type=models.IntegerField(default=0)  #类型
    name = models.CharField(max_length=100)   #名称
    platform = models.IntegerField(default=0)  #适用平台
    publishCount = models.IntegerField(default=0)  #发行量
    amount = models.DecimalField(max_digits=8, decimal_places=2) #面额
    perLimit = models.IntegerField(default=0)  #限领
    minPoint = models.DecimalField(max_digits=8, decimal_places=2)  #门槛
    startTime = models.DateTimeField()    #开始时间
    endTime = models.DateTimeField()  #结束时间
    note = models.CharField(max_length=255)  #备注
    useType = models.IntegerField(default=0)  #可使用商品类型

    class Meta:
        db_table = 'coupon'

#指定商品优惠表
class goods_coupon(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    coupon_id = models.ForeignKey(coupon, to_field='id', on_delete='CASCADE', related_name='cou_id')
    goods_id = models.ForeignKey(Goods, to_field='id', on_delete='CASCADE', related_name='goods_id')

    class Meta:
        db_table = "goods_coupon"

#优惠卷分类表
class coupon_cate(BaseModel,models.Model):   
    id = models.AutoField(primary_key=True)
    coupon_id = models.ForeignKey(coupon, to_field='id', on_delete='CASCADE', related_name='coup_id')
    cate_id = models.ForeignKey(category, to_field='id', on_delete='CASCADE', related_name='category_id')

    class Meta():
        db_table = 'coupon_cate'

#省市区表
class area(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    pid = models.IntegerField(default=0)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "area"

#用户收获地址表
class address(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=255)
    country = models.IntegerField(default=0)
    city = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    telphone = models.CharField(max_length=255)
    is_default = models.IntegerField(default=0)

    class Meta:
        db_table = "address"

#购物车表
class cart(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    goods_id = models.IntegerField()
    goods_name = models.CharField(max_length=255)
    sp1 = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    img = models.CharField(max_length=255)

    class Meta:
        db_table = "cart"

#用户订单表
class user_orders(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    order_sn = models.CharField(max_length=255)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    total_money = models.DecimalField(max_digits=8, decimal_places=2)
    coupon_money = models.DecimalField(max_digits=8, decimal_places=2)
    actual_money = models.DecimalField(max_digits=8, decimal_places=2)
    pay_type = models.IntegerField(default=0)
    source = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    pay_code = models.CharField(max_length=255)

    class Meta:
        db_table = "user_orders"

#专题栏分类表
class special_category(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    img = models.CharField(max_length=255)
    recommend = models.IntegerField(default=0)

    class Meta:
        db_table = "special_category"

#专题表
class Special(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    min_price = models.IntegerField(default=0)
    #专题主图
    pic = models.CharField(max_length=255, blank=True, null=True)  
    # 副标题
    subheading = models.CharField(max_length=255, blank=True, null=True)
    #转发数
    forward_count = models.IntegerField(default=0)
    #画册图片用逗号分割
    album_pics = models.CharField(max_length=1000, blank=True, null=True)
    #显示状态：0->不显示；1->显示'
    show_status = models.IntegerField(blank=True, null=True)
    #阅读数
    read_count = models.IntegerField(blank=True, null=True)
    #内容数量
    comment_count = models.IntegerField(blank=True, null=True)
    #收藏数
    collect_count = models.IntegerField(blank=True, null=True)
    #专题分类id
    special_cate_id = models.IntegerField(blank=True, null=True)
    #当前时间
    current_time = models.DateTimeField(auto_now_add=True)
    #专题内容
    content = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "special"

#专题图片表
class special_pic(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    special_id = models.IntegerField()
    pic = models.CharField(max_length=255)

    class Meta:
        db_table = "special_pic"

#专题商品关系表
class Special_shop(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.ForeignKey(Goods, to_field='id', on_delete='CASCADE', related_name='goo_id')
    special_id = models.ForeignKey(Special, to_field='id', on_delete='CASCADE', related_name='spc_id')

    class Meta:
        db_table = "special_shop"

#专题评论表
class Special_comment(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    username = models.CharField(max_length=255)
    user_head_image = models.CharField(max_length=255)
    user_address = models.CharField(max_length=255)
    user_profession = models.CharField(max_length=255)
    discourse_id = models.IntegerField()
    content = models.CharField(max_length=255)
    pid = models.IntegerField(default=0)
    evaluate_sum = models.IntegerField(default=0)
    collect_sum = models.IntegerField(default=0)

    class Meta:
        db_table = "special_comment"


#优选表
class super(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    img = models.CharField(max_length=255)

    class Meta:
        db_table = "super"

#帮助/管理表
class manage(BaseModel,models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=255)

    class Meta:
        db_table = "manage"


#活动表
class Ceckil(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)   #名称
    startDate=models.DateTimeField()    #开始时间
    endDate=models.DateTimeField()     #结束时间
    status=models.IntegerField()    #状态（1是0否）

    class Meta:
        db_table = 'ceckil'

#秒杀活动表
class Ceckil_activity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)   #名称
    startTime=models.DateTimeField()    #开始时间
    endTime=models.DateTimeField()     #结束时间
    status=models.IntegerField()    #状态（1是0否）

    class Meta:
        db_table = 'ceckil_activity'


#秒杀时间段表
class Quentum(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)   #名称
    start_time=models.TimeField(max_length=100)    #开始时间
    end_time=models.TimeField(max_length=100)     #结束时间
    state=models.IntegerField()    #状态（1是0否）


    class Meta:
        db_table = 'quentum'

#秒杀商品表
class Ceckil_goods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)   #名称
    goods_code = models.CharField(max_length=50)  # 商品编号
    price = models.DecimalField(max_digits=8,decimal_places=2)  # 价格
    stock =  models.IntegerField() #库存
    ceckil_price= models.DecimalField(max_digits=8,decimal_places=2)  # 秒杀价格
    ceckil_number=models.IntegerField()     #秒杀数量
    limitation_number=models.IntegerField()   #限购数量
    sort = models.IntegerField()    #排序

    class Meta:
        db_table = 'ceckil_goods'

#秒杀时间段商品关系表
class Ceckil_goods_relation(models.Model):
    id = models.AutoField(primary_key=True)
    ceckil_price = models.DecimalField(max_digits=8, decimal_places=2)  # 秒杀价格
    goods_id = models.ForeignKey(Goods, to_field='id', on_delete='CASCADE', related_name='gd_id')
    quentum_id = models.ForeignKey(Quentum, to_field='id', on_delete='CASCADE', related_name='quentum_id')
    activity_id = models.ForeignKey(Ceckil_activity, to_field='id', on_delete='CASCADE', related_name='activity_id')


    class Meta:
        db_table = 'ceckil_goods_relation'

#广告
class Advertising(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)   
    type = models.IntegerField(default=0)
    pic = models.CharField(max_length=255)
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    url = models.CharField(max_length=255)
    note = models.CharField(max_length=255)
    sort = models.IntegerField(default=0)

    class Meta:
        db_table = 'advertising'

#订单设置
class Dingdan_setting(models.Model):
    id = models.AutoField(primary_key=True)
    flashOrderOvertime = models.IntegerField(default=0)
    normalOrderOvertime = models.IntegerField(default=0)
    confirmOvertime = models.IntegerField(default=0)
    finishOvertime = models.IntegerField(default=0)
    commentOvertime = models.IntegerField(default=0)

    class Meta:
        db_table = 'dingdan_setting'


#会员等级表
class member_grade(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)   

    class Meta:
        db_table = 'member_grade'

#新闻表
class News(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)   

    class Meta:
        db_table = 'news'