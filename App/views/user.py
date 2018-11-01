import random
import time
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
import os
from App.models import User
from django.conf import settings


def Login(req):
    if req.method == 'GET':
        return render(req, 'home/login.html')
    if req.method == 'POST':
        u = authenticate(username=req.POST.get('username'), password=req.POST.get('password'))
        randcode = req.POST.get('randcode')
        verify = req.session.get('verify')
        if verify.lower() == randcode.lower():
            if u:
                if u.is_active:
                    login(req, u)
                    info = '登陆成功！'
                    # req.session['info'] = info
                    return redirect(reverse('App:index'))
                info = '账户未激活！'
                return render(req, 'home/login.html', {'info': info})
            info = '密码错误！'
            return render(req, 'home/login.html', {'info': info})
        info = '验证码错误'
        return render(req, 'home/login.html', {'info': info})


def Logout(req):
    logout(req)
    return redirect(reverse('App:index'))


def upload(req):
    if req.method == 'GET':
        user = req.user
        user.icon = '/upload/' + user.icon
        return render(req, 'home/upload.html', {'user': user})
    if req.method == 'POST':
        icon = req.FILES.get('icon')
        ext = os.path.splitext(icon.name)[1]
        fn = time.strftime('%Y%m%d%H%M%S')
        fn = fn + '_%d' % random.randint(0, 100)
        icon.name = fn + ext
        u = req.user
        u.icon = icon.name
        u.save()
        savePath = os.path.join(settings.MDEIA_ROOT, icon.name)
        with open(savePath, 'wb') as f:
            # f.write(file.read())
            if icon.multiple_chunks():
                for myf in icon.chunks():
                    f.write(myf)
                # print('大于2.5')
            else:
                # print('小于2.5')
                f.write(icon.read())
        info = '头像上传成功！'
        return render(req, 'home/upload.html', {'info': info})


def register(req):
    if req.method == 'GET':
        return render(req, 'home/register.html')
    if req.method == 'POST':
        username = req.POST.get('username')
        # print(username)
        if User.objects.filter(username=username):
            info = '用户名已存在！'
            return render(req, 'home/register.html', {'info': info})
        password = req.POST.get('password')
        confirm = req.POST.get('confirm')
        email = req.POST.get('email')
        if password == confirm:
            info = '注册成功！'
            u = User.objects.create_user(username=username, password=password, email=email)
            u.save()
            token = u.create_token()

            #邮箱激活
            href = 'http://' + req.get_host() + reverse('App:userActivate', args=[token])
            subject, from_email, to = '账号激活', '490511323@qq.com', u.email
            text_content = 'This is an important message.'
            html_content = loader.get_template('home/userActivate.html').render({'username': u.username, 'href': href})
            msg = EmailMultiAlternatives(subject, text_content, from_email=from_email, to=[to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(req, 'home/index.html', {'info': info})
        else:
            info = '两次输入密码不一致！'
            return render(req, 'home/register.html', {'info': info})


def userActivate(req, token):
    if User.Useractivate(token):
        info = '激活成功！'
        return render(req, 'home/index.html', {'info': info})
    else:
        info = '激活码已失效，请重新激活！'
        return render(req, 'home/index.html', {'info': info})


def verifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    font = ImageFont.truetype(r'C:\webprojects\fonts\ADOBEARABIC-BOLDITALIC.OTF', 40)
    # 构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verify'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
