window.onload = function(){
	//1. 獲取元素節點
	var currentAddr = document.getElementsByClassName('currentAddress')[0];
	var select = document.getElementsByClassName('select')[0];

	//獲取內層列表中地址項
	var address = select.children;
	//為每一項添加點擊事件
	for(var i = 0; i <address.length; i ++){
		address[i].onclick = function(){
			//傳值
			currentAddr.innerHTML = this.innerHTML;
		};
	}

	/*-----------圖片輪播--------------*/
	//1. 獲取圖片數組
	//2. 定時器實現圖片切換
	//3. 圖片切換主要切換數組下標，防止數組越界

	var banner = document.getElementsByClassName('wrapper')[0];
	var imgs = banner.children; //圖片數組
	var imgNav = document.getElementsByClassName('imgNav')[0];
	var indInfo = imgNav.children; //索引數組
	var imgIndex = 0;  //初始下標
	var timer;
	timer = setInterval(autoPlay,2000); //定時器
	function autoPlay(){
		//設置元素隱藏與顯示，設置為none在文檔中不佔位
		imgs[imgIndex].style.display = 'none'; 
		/*
		++ imgIndex;
		if(imgIndex == imgs.length){
			imgIndex = 0;
		}*/
		//三目運算
		imgIndex = ++ imgIndex == imgs.length ? 0 : imgIndex;
		imgs[imgIndex].style.display = "block";

		for(var i = 0; i < indInfo.length; i ++){
			indInfo[i].style.background = "gray";
		}
		//切換索引 切換背景色
		indInfo[imgIndex].style.background = "red";
		}
		banner.onmouseover = function(){
			//停止定時器
			clearInterval(timer);
		};
		banner.onmouseout = function(){
			timer = setInterval(autoPlay,2000);
		};



	};

//異步向服務器發送請求，檢查用戶是否登入狀態
function check_login(){
    // 向/check_login/發送請求
    $.get('/check_login/',function(data){
    var html = '';
        if(data.loginStatus == 0){
            html +=	"<a href='/login'>[登入]</a>";
			html += "<a href='/register'>[註冊,有驚喜]</a>";
        }else{
            html += "歡迎：" + data.uname;
		    html += '<a href="/logout/">'+'&nbsp;&nbsp;退出</a>';
		    var show = '';
		    show += "<a href='/cart/'>我的購物車(" + data.num + ")</a>";
		    $("#cart").html(show);
        }
        	$("#login").html(html);
    },'json');
}

//加載所有的商品分類以及商品信息(每個分類取前10個)
function loadGoods(){
    $.get('/load_type_goods/',function(data){
    //data就是響應回來的JSON對象
        var show = '';
        $.each(data,function(i,obj){
            //從obj中取出type並轉換為json對象(因type的值為字符串)
            var jsonType = JSON.parse(obj.type);
            //加載type的信息
            show += "<div class='item' style='overflow:hidden;'>";
                show += "<p class='goodsClass'>";
                    show += "<img src='/" + jsonType.picture + "'>";
                    show += "<a href='#'>更多</a>";
                show += "</p>";
                //加載ul以及li們
                show += "<ul>";
                    var jsonGoods = JSON.parse(obj.goods);
                    $.each(jsonGoods,function(i,good){
                        //創建li
                        show += "<li ";
                        if((i+1)%5 == 0){
                            show += "class='no-margin'";
                        }
                        show += ">";
                            //拼p標記表示商品的圖片
                            show += "<p>";
                                show += "<img src='/" + good.fields.picture + "'>";
                            show += "</p>";
                            //拼div標記來表示商品詳細描述
                            show += "<div class='content'>";
                                show += "<a href='javascript:add_cart(" + good.pk + ");'>";
                                    show += "<img src='/static/images/cart.png'>";
                                show += "</a>";
                                show += "<p>" + good.fields.title + "</p>";
                                show += "<span>";
                                    show += "&yen;" +good.fields.price +"/"+good.fields.spec;
                                show += "</span>";
                            show += "</div>";
                        show += "</li>";
                    });
                show += "</ul>";
            show += "</div>";
           });
        $("#main").html(show);
    },'json');
}

//添加商品到購物車
//gid表示要添加到購物車的ID
function add_cart(gid){
    //1.驗證登入帳戶，如果沒有用戶登入則給出相應的提示
    $.get('/check_login/',function(data){
        if(data.loginStatus == 0){
            alert("請先登入在購買商品...");
        }else{
            //2.有用戶登入的話，將商品加入至購物車
            $.get('/add_cart/',{'gid':gid},function(data){
                if(data.status == 1){
                    alert(data.statusText);
                }else{
                    alert("添加購物車失敗")
                }
            },'json');
        }
    },'json');
}



$(function(){
    //調用check_login檢查登入狀態
    check_login();
    //調用loadGoods函數得到所有的類型和商品
    loadGoods();
});