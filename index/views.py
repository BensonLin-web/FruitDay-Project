import json

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.
def login_views(request):
    if request.method == 'GET':
        #獲取來訪地址，如果沒有則設置為/
        url = request.META.get('HTTP_REFERER','/')
        #get請求  -  判斷session，判斷cookie，登入頁
        #先判斷session中是否有登入信息
        if 'uid' in request.session and 'uphone' in request.session:
            #從那來回那去
            resp = HttpResponseRedirect(url)
            return resp
        else:
            #沒有登入信息保存在session，繼續判斷cookies中是否有登入信息
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                #cookies中有登入信息  -  曾經記住過密碼
                #將cookies中的信息取出保存進session，在返回到首頁
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid'] = uid
                request.session['uphone'] = uphone
                #從那來回那去
                resp = HttpResponseRedirect(url)
                return resp
            else:
                # 創建LoginForm的對象併發送給login.html
                form = LoginForm()
                # 將來訪地址保存進cookies中
                resp = render(request,'login.html',locals())
                resp.set_cookie('url',url)
                return resp

    else:
        #post請求  - 實現登入操作
        #先獲取手機號和密碼
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        #判斷手機號和密碼是否存在(登入是否成功)
        users = User.objects.filter(uphone=uphone,upwd=upwd)
        if users:
            #登入成功：先存進session
            request.session['uid'] = users[0].id
            request.session['uphone'] = uphone
            #聲明響應對象:從那來回那去
            url = request.COOKIES.get('url','/')
            resp = redirect(url)
            #將url從cookies中刪除出去
            if 'url' in request.COOKIES:
                resp.delete_cookie('url')
            #判斷是否要存進cookies
            if 'isSaved' in request.POST:
                expire = 60*60*24*90
                resp.set_cookie('uid',users[0].id,expire)
                resp.set_cookie('uphone',uphone, expire)
            return resp
        else:
            #登入失敗
            errMsg = '您輸入的電話或密碼不正確'
            form = LoginForm()
            return render(request,'login.html',locals())


#http://localhost:8000/register
def register_views(request):
    #判斷是get請求或post請求，得到用戶的請求意圖
    if request.method == 'GET':
        # 獲取來訪地址，如果沒有則設置為/
        url = request.META.get('HTTP_REFERER','/')
        resp = render(request,'register.html')
        resp.set_cookie('url',url)
        return resp
    else:
        #先驗證手機號在數據庫是否存在
        uphone = request.POST['uphone']
        #users = User.objects.filter(uphone=uphone)
        #if users:
            #uphone已經存在
            #errMsg = '手機號碼已經存在'
            #return  render(request,'register.html',locals())
        #接收數據，插入到數據庫中
        user = User()
        user.uphone = uphone
        user.upwd = request.POST['upwd']
        user.uname = request.POST['uname']
        user.uemail = request.POST['uemail']
        user.save()
        #取出user中的id 和 uphone的值保存進session
        request.session['uid'] = user.id
        request.session['uphone'] = user.uphone
        # 聲明響應對象:從那來回那去
        url = request.COOKIES.get('url','/')
        resp = redirect(url)
        #將url從cookies中刪除
        if 'url' in request.COOKIES:
            resp.delete_cookie('url')
        #resp功能待實現

        return HttpResponse("註冊成功")

def index_views(request):
    return render(request,'index.html',locals())

#檢查手機號是否被註冊
def checkuphone_views(request):
    #接收前端傳遞過來的數據-uphone
    uphone = request.GET['uphone']
    users = User.objects.filter(uphone=uphone)
    if users:
        status = 1
        msg = '手機號碼已經存在'
    else:
        status = 0
        msg = '通過'
    dic = {
        'status':status,
        'msg':msg,
    }
    return HttpResponse(json.dumps(dic))

#檢查session中是否有登入信息，如果有就獲取對應數據uname的值
def check_login_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        loginStatus = 1
        #通過uid的值獲取uname
        id = request.session['uid']
        uname = User.objects.get(id=id).uname
        #通過id獲取用戶購物車總數量
        num = CartInfo.objects.filter(user_id=id).count()
        dic = {
            'loginStatus':loginStatus,
            'uname':uname,
            'num':num
        }
        return HttpResponse(json.dumps(dic))
    else:
        dic = {
            'loginStatus':0
        }
        return HttpResponse(json.dumps(dic))

#退出
def logout_views(request):
    #判斷session中是否有登入信息，有的話則清除
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
        #構建響應對象:那發出的退出請求，則返回到哪去
        url = request.META.get('HTTP_REFERER','/')
        resp = HttpResponseRedirect(url)
        #判斷cookies中是否有登入信息，有的話則刪除
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            resp.delete_cookie('uid')
            resp.delete_cookie('uphone')
            return resp
    return redirect('/')

#加載所有的商品類型以及對應的每個類型下的前10條數據
def type_goods_views(request):
    #加載所有的商品類型
    types = GoodsType.objects.all()
    all_list = []
    for type in types:
        dic = {}
        type_json = json.dumps(type.to_dict())
        #獲取 type類型下10的最新條數據
        g_list = type.goods_set.filter(isActive=True).order_by("-id")[0:10]
        #將g_list轉換為json
        g_list_json = serializers.serialize('json',g_list)
        #將type_json和g_list_json封裝到一個字典中
        dic["type"] = type_json
        dic["goods"] = g_list_json
        #將dic字典追加到all_list列表裡
        all_list.append(dic)
    return HttpResponse(json.dumps(all_list))

#將商品添加置購物車 或 更新現有商品數量
def add_cart_views(request):
    #獲取商品id,獲取用戶id,購買數量默認為1
    goods_id = request.GET['gid']
    user_id = request.session['uid']
    ccount = 1
    #查看購物車中是否有相同用戶購買的相同商品
    cart_list = CartInfo.objects.filter(user_id=user_id,goods_id=goods_id)
    if cart_list:
        #已經有相同用戶購買過相同產品,更新商品數量
        cartinfo = cart_list[0]
        cartinfo.ccount = cartinfo.ccount + ccount
        cartinfo.save()
        dic = {
            'status':1,
            'statusText':'更新數量成功'
        }
    else:
        #沒有對應的用戶以及對應的商品
        cartinfo = CartInfo()
        cartinfo.user_id = user_id
        cartinfo.goods_id = goods_id
        cartinfo.ccount = ccount
        cartinfo.save()
        dic = {
            'status':1,
            'statusText':'添加購物車成功'
        }
    return HttpResponse(json.dumps(dic))

def cart_views(request):
    return render(request,'cart.html',locals())

def load_cart_views(request):
    #找出session中的uid查詢對應的用戶的購物車信息
    uid = request.session['uid']
    cart_info = CartInfo.objects.filter(user_id=uid)
    print(cart_info)
    list = []
    #便歷用戶的購物車信息
    for cart in cart_info:
        dic = {}
        #利用cart.goods_id找出goods對象並序列化
        goods = Goods.objects.filter(id=cart.goods_id)
        ser_goods = serializers.serialize('json',goods)
        #為dic字典賦值並加入到列表裡
        dic['goods'] = ser_goods
        dic['ccount'] = cart.ccount
        list.append(dic)
    return HttpResponse(json.dumps(list))

def delete_cartInfo_views(request):
    goods_id = request.GET['goods_id']
    goods = CartInfo.objects.filter(goods_id=goods_id)
    goods.delete()
    return redirect('/cart/')


