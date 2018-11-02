from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from App.models import Posts, Comment


@login_required(login_url='/login/')
def send_comment(req):
    if req.method == 'POST':
        content = req.POST.get('content')
        pid = req.GET.get('pid')
        u = req.user
        posts = Posts.objects.filter(id=pid).first()
        if len(content) > 120:
            info = '评论必须在120字以内！'
            return render(req, 'home/posts_detail.html', {'posts': posts, 'info': info})
        comment = Comment(from_posts=posts, from_user=u, content=content)
        comment.save()
        return redirect(reverse('App:index'))

