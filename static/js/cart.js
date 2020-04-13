// /**
//  * Created by tarena on 18-8-3.
//  */

$(function(){
  //检查登录状态
  check_login();
  //獲取購物車數據
  load_cart();
});

/**
 * 异步向服务器发送请求，检查用户是否处于登录状态
 * */
function check_login(){
  $.get('/check_login/',function(data){
    var html = "";
    if(data.loginStatus == 0){
      html += "<a href='/login/'>[登录]</a>,";
      html += "<a href='/register/'>[注册有惊喜]</a>";
    }else{
      html += "歡迎："+data.uname;
      html += "<a href='/logout/'>&nbsp;&nbsp;退出</a>";
    }
    $("#login").html(html);
  },'json');
}

/* 異步的向服務器發送請求，獲取購物車數據*/
function load_cart(){
    $.get('/load_cart/',function(data){
        //data就是響應回來的JSON對象
        var show = '';
        $.each(data,function(i,obj){
            //從obj中取出goods並轉換為json對象(因goods的值為字符串)
            var jsonGoods = JSON.parse(obj.goods);
            $.each(jsonGoods,function(i,good){
            show += "<div class='g-item'>";
                show += "<p class='check-box'>";
                    show += "<input type='checkbox' style='margin-bottom:35px;'>";
                    show += "<img src='/" + good.fields.picture + "' width='80'>";
                show += "</p>";
                show += "<p class='goods'>";
                    show += good.fields.title;
                show += "</p>";
                show += "<p class='price'>";
                    show += '&yen;'+good.fields.price;
                show += "</p>";
                show += "<p class='quantity'>";
                    show += obj.ccount;
                show += "</p>";
                show += "<p class='t-sum'>";
                    show += "<b>" + '&yen;' + (Number(good.fields.price)*obj.ccount) +"</b>";
                show += "</p>";
                show += "<p class='action'>";
                    show += "<a href='/delete_cartInfo?goods_id=" + good.pk + "'>移除</a>";
                show += "</p>";
            show += "</div>";
            $("#good-content").html(show);
            });
        });
    },'json');
}


