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
    title = models.CharField(max_length=100, blank=True, default="")
    body = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    author = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pub_time',)

    # 文章摘要
    def excerpt(self):
        excerpt = str(self.body)
        if excerpt.__len__() > 50:
            excerpt = excerpt[:50]+'...'
        return excerpt


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Comment(models.Model):
    user = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=300)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pub_time',)


class Reply(models.Model):
    user = models.ForeignKey('auth.User', related_name='replies', on_delete=models.CASCADE)
    pub_time = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=300)
    post = models.ForeignKey(Post, related_name='replies', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="replies", on_delete=models.CASCADE)

    class Meta:
        ordering = ('-pub_time',)

