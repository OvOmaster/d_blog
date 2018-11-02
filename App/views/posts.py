from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Q
from App.models import Posts


@login_required(login_url='/login/')
def send_posts(req):
    if req.method == 'GET':
        return render(req, 'home/send_posts.html')
    if req.method == 'POST':
        title = req.POST.get('title')
        article = req.POST.get('article')
        user = req.user
        if len(title) <= 20:
            p = Posts(title=title, article=article, user=user)
            p.save()
            # info = '博客发表成功！'
            return redirect(reverse('App:index'))
        info = '标题必须在20字以内！！！'
        return render(req, 'home/send_posts.html', {'info': info})


def search_posts(req):
    if req.method == 'POST':
        words = req.POST.get('search')
        data = Posts.objects.filter(Q(title__contains=words) | Q(article__contains=words))
        pagination = Paginator(data, 5)
        try:
            nowPage = int(req.GET.get('page'))
        except:
            nowPage = 1
        page = pagination.page(nowPage)
        for post in page.object_list:
            post.user.icon = '/upload/' + post.user.icon
        return render(req, 'home/search_posts.html', {'page': page, 'words': words})


def update_posts(req):
    if req.method == 'GET':
        posts_id = req.GET.get('id')
        posts = Posts.objects.filter(id=posts_id).first()
        return render(req, 'home/update_posts.html', {'posts': posts})
    if req.method == 'POST':
        posts_id = req.GET.get('id')
        posts = Posts.objects.filter(id=posts_id).first()
        title = req.POST.get('title')
        article = req.POST.get('article')
        if len(title) >= 20:
            info = '标题必须在20字以内！'
            return render(req, 'home/update_posts.html', {'info': info, 'posts':posts})
        posts.title = title
        posts.article = article
        posts.save()
        # req.session['info'] = '修改成功！'
        return redirect(reverse('App:posts_manager'))


def delete_posts(req):
    posts_id = req.GET.get('id')
    posts = Posts.objects.filter(id=posts_id).first()
    posts.delete()
    # req.session['info'] = '删除成功！'
    return redirect(reverse('App:posts_manager'))


@login_required(login_url='/login/')
def posts_detail(req):
    posts_id = req.GET.get('id')
    posts = Posts.objects.filter(id=posts_id).first()
    cusers = posts.collect_user.all()
    comments = posts.comment_set.all().order_by('create_time')
    for comment in comments:
        comment.from_user.icon = '/upload/' + comment.from_user.icon
    posts.visit += 1
    posts.save()
    return render(req, 'home/posts_detail.html', {'posts': posts, 'cusers': cusers, 'comments': comments})


def posts_manager(req):
    if req.method == 'GET':
        u = req.user
        data = u.send_user.all().order_by('-id')
        return render(req, 'home/posts_manager.html', {'data': data})
    if req.method == 'POST':
        word = req.POST.get('titleword')
        data = req.user.send_user.filter(title__contains=word)
        return render(req, 'home/posts_manager.html', {'data': data, 'word': word})


def do_favourite(req):
    try:
        pid = int(req.GET.get('pid'))
        posts = Posts.objects.filter(id=pid).first()
        # print(pid)
        if req.user in posts.collect_user.all():
            #取消收藏
            posts.collect_user.remove(req.user)
            # print('delete_favorite')
        else:
            #添加收藏
            posts.collect_user.add(req.user)
            # print('add_favorite')
        return JsonResponse({'res': 200})
    except:
        return JsonResponse({'res': 500})


def delete_favourite(req):
    pid = int(req.GET.get('id'))
    posts = Posts.objects.filter(id=pid).first()
    posts.collect_user.remove(req.user)
    return redirect(reverse('App:my_favourite'))
