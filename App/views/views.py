from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from App.models import Posts
# Create your views here.


def index(req):
    # info = req.session.get('info')
    all_posts = Posts.objects.all().order_by('-upload_time')
    pagination = Paginator(all_posts, 5)
    try:
        now_page = int(req.GET.get('page'))
    except:
        now_page = 1
    page = pagination.page(now_page)
    for post in page.object_list:
        post.user.icon = '/upload/' + post.user.icon
    return render(req, 'home/index.html', {'page': page})


