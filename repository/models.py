from django.db import models

# Create your models here.
class UserInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32,null=True)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.CharField(verbose_name='头像',default='/static/imgs/avatar/default.png',max_length=255)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user', 'follower'))
    class Meta:
        verbose_name_plural ='用户表'
    def __str__(self):
        return self.username

class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)
    user = models.OneToOneField(to='UserInfo', to_field='nid')

class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主', to='UserInfo', to_field='nid', related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝', to='UserInfo', to_field='nid', related_name='followers')

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    caption = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
# class Category(models.Model):
#     caption = models.CharField(max_length = 32)

class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo', to_field='nid')
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]

class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复评论', to='self', related_name='back', null=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')

class ArticleContent(models.Model):
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容', )

class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    content = models.CharField(verbose_name='文章简介', max_length=255)

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    detail = models.OneToOneField(to=ArticleContent, to_field='nid', null=True)

    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    pick = models.NullBooleanField(null=True,default=False)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    category_choice = [
        (1,'Python'),
        (2,'Linux'),
        (3,'Html'),
        (4,'Ajax'),
    ]
    category_id = models.IntegerField(choices=category_choice,default=None)

class Article2Tag(models.Model):
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

class News(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='新闻标题', max_length=128)
    summary = models.CharField(verbose_name='新闻简介', max_length=255)
    author = models.ForeignKey(to='UserInfo',to_field='nid',related_name="auth_news")
    content = models.OneToOneField(to='NewsContent',to_field='nid',null=True)
    create_time = models.DateTimeField(auto_now_add=True)

class NewsContent(models.Model):
    nid = models.AutoField(primary_key=True)
    content = models.TextField(verbose_name='新闻内容', )

class Img(models.Model):
    src = models.FileField(max_length=32,verbose_name='图片路径',upload_to='static/imgs/photo')
    title = models.CharField(max_length=16,verbose_name='标题')
    summary = models.CharField(max_length=128,verbose_name='简介')

    class Meta:
        verbose_name_plural = '图片'
    def __str__(self):
        return self.title

class Trouble(models.Model):
    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    detail = models.TextField()
    user = models.ForeignKey(to=UserInfo,to_field='nid',related_name='u')
    ctime = models.DateTimeField(verbose_name='创建时间')
    status_choice = (
        (1,'未处理'),
        (2,'处理中'),
        (3,'已处理'),
    )
    status = models.IntegerField(choices=status_choice,default=1)
    processer = models.ForeignKey(to=UserInfo,related_name='p',null=True,blank=True)
    solution = models.TextField(null=True)
    ptime = models.DateTimeField(null=True)
    pj_choice = (
        (1,'不满意'),
        (2,'一般'),
        (3,'满意'),
    )
    pj = models.IntegerField(choices=pj_choice,null=True)


class Role(models.Model):
    caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural ='角色表'
    def __str__(self):
        return self.caption

class User2Role(models.Model):
    u = models.ForeignKey(UserInfo)
    r = models.ForeignKey(Role)

    class Meta:
        verbose_name_plural ='用户角色表'
        unique_together = [
            ('u', 'r'),
        ]
    def __str__(self):
        return '%s-%s' %(self.u.username,self.r.caption)

class Action(models.Model):
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural ='操作表'
    def __str__(self):
        return '%s-%s' %(self.caption,self.code)

class Menu(models.Model):
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self',related_name='p',null=True,blank=True)

    def __str__(self):
        return '%s' %(self.caption,)

class Permission(models.Model):
    caption = models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    menu = models.ForeignKey(Menu,null=True,blank=True)

    class Meta:
        verbose_name_plural ='URL表'
    def __str__(self):
        return '%s-%s' %(self.caption,self.url)

class Permission2Action(models.Model):
    p = models.ForeignKey(Permission)
    a = models.ForeignKey(Action)

    class Meta:
        verbose_name_plural ='权限表'
    def __str__(self):
        return '%s-%s:%s?t=%s' %(self.p.caption,self.a.caption,self.p.url,self.a.code)

class Permission2Action2Role(models.Model):
    p2a = models.ForeignKey(Permission2Action)
    r = models.ForeignKey(Role)

    class Meta:
        verbose_name_plural ='角色分配权限表'
    def __str__(self):
        return '%s--》%s' %(self.r.caption,self.p2a)