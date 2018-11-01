import hashlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models


class User(AbstractUser):
    icon = models.CharField(max_length=100, default='default.jpg')
    # collect_posts = models.ManyToManyField(Posts)

    def create_token(self):
        u = uuid.uuid4()
        m = hashlib.md5()
        m.update(str(u).encode(encoding='utf-8'))
        sign = m.hexdigest()
        cache.set(sign, self.id, 600)  # token放入缓存，设置存活时间十分钟
        return sign

    @classmethod
    def Useractivate(cls, token):
        try:
            # print(token)
            id = cache.get(token)
            # print(id)
            u = User.objects.get(pk=int(id))
            u.is_active = True
            u.save()
            return True
        except:
            return False

    class Meta:
        db_table = 'user'
        # app_label = 'App'


class Posts(models.Model):
    title = models.CharField(max_length=30)
    article = models.TextField()
    visit = models.IntegerField(default=0)
    upload_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='send_user')
    collect_user = models.ManyToManyField(User)

    class Meta:
        db_table = 'posts'
        # app_label = 'App'

    # def is_favourite(self, user):
    #     u = User.objects.all()
    #     for i in u:
    #         if user == i:
    #             return True
    #     return False
