from django.db import models


class Post(models.Model):
    """
    文章的存储model
    """

    """
    title:标题
    body:主体
    pub_time:发布时间
    tag:标签,多对多
    author:作者,一对多
    """
    title = models.CharField(max_length=100, blank=True, default='')
    body = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField('Tag', related_name='posts', blank=True)
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pub_time',)

    # 文章摘要
    def get_excerpt(self):
        excerpt = str(self.body)
        if excerpt.__len__() > 50:
            excerpt = excerpt[:50]+'...'
        return excerpt

    def __str__(self):
        return str(self.author)+" "+str(self.get_excerpt())


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)
