//详细用户信息
var userIfo = $(".userIfo");
//设置位置
userIfo.css("left",window.innerWidth-330);
userIfo.hide();
//移入显示
var userHead = $(".navbar .right img");
userHead.mouseenter(function () { 
    userIfo.slideDown();
    userHead.attr("src","/static/img/user-fill(white).png");
});
//移除隐藏
$(".container").mouseenter(function(){
    userIfo.slideUp();
    userHead.attr("src","/static/img/user-line(white).png");
})

//获取一下id
var id = searchCookie("id");

//点击切换
    var page = $(".nav-item");
    console.log(page[1]);

    //成绩概览
    $(page[0]).click(function(){
        $(".second").hide();
        $(".fifth").hide();
        $(".sixth").hide();
        $(".seventh").hide();
        $(".first").fadeIn(300);
        $(".third").fadeIn(300);
        $(".forth").fadeIn(300);
        page.css("background-color","#263238");
        page.find("a").css("color","#ABB1B7");
        $(page[0]).css("background-color","rgba(255,255,255,.1)");
        $(page[0]).find("a").css("color","white");
        
        //获取总成绩
        var term = $('input#countrySelect')[0].value;
        $.ajax({
            type:"get",
            url:"/self",
            data:{
                "username":id,
                "term":term,
                "parameter":"report_card"
            },
            dataType:"json",
            success:function(msg){
                console.log(msg);
            },
            error:function(xml){
                console.log(xml.status);
            }
        });

        //总成绩
        var doughnutData = [
            {
                value: 150,
                color:"#F7464A",
                highlight: "#FF5A5E",
            },{
                value: 450,
                color: "#4D5360",
                highlight: "#616774",
            }
        ];
        var ctx = document.getElementById("chart-area").getContext("2d");
        window.myDoughnut = new Chart(ctx).Doughnut(doughnutData, {
            responsive : true
        });

        //各科成绩
        var barChartData = {
            labels : ["科目","科目","科目","科目","科目","科目","科目"],
            datasets : [
                {
                    fillColor : "rgba(220,220,220,0.5)",
                    strokeColor : "rgba(220,220,220,0.8)",
                    highlightFill: "rgba(220,220,220,0.75)",
                    highlightStroke: "rgba(220,220,220,1)",
                    data : [60,60,60,60,60,60,60]
                },
                {
                    fillColor : "rgba(151,187,205,0.5)",
                    strokeColor : "rgba(151,187,205,0.8)",
                    highlightFill : "rgba(151,187,205,0.75)",
                    highlightStroke : "rgba(151,187,205,1)",
                    data : [80,80,80,80,80,80,80]
                }
            ]
        }
        var ctx = document.getElementById("canvas1").getContext("2d");
        window.myBar = new Chart(ctx).Bar(barChartData, {
            responsive : true
        });
    });

    //学科分析
    $(page[1]).click(function(){
        console.log("bbb");
        $(".first").hide();
        $(".third").hide();
        $(".forth").hide();
        $(".sixth").hide();
        $(".seventh").hide();
        $(".second").fadeIn(300);
        $(".fifth").fadeIn(300);
        page.css("background-color","#263238");
        page.find("a").css("color","#ABB1B7");
        
        $(page[1]).css("background-color","rgba(255,255,255,.1)");
        console.log("test");
        //获取请求的学期
        var term = $('input#countrySelect')[0].value;
        console.log($('input#countrySelect')[0].value);
        //获取优劣势
        $.ajax({
            type:"get",
            url:"/self",
            data:{
                "username":id,
                "term":term,
                "parameter":"weak_and_best"
            },
            dataType:"json",
            success:function(msg){
                console.log(msg);
            },
            error:function(xml){
                console.log(xml.status);
            }
        });
        console.log("enter weak");

        //雷达图
        var radarChartData = {
            labels: ["a", "b", "c", "d", "e", "f"],
            datasets: [{
                label: "scoreAnalyze",
                fillColor: "rgba(1,70,138,0.5)",
                strokeColor: "rgba(1,70,138,0.6)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "rgba(1,70,138,0.6)",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(1,70,138,0.6)",
                data: [65,88,90,76,56,99]
    
            }]
        };
        window.myRadar = new Chart(document.getElementById("subject").getContext("2d")).Radar(radarChartData,{
            responsive: true,
            pointLabelFontSize: 25,
        });
    });

    //排名曲线
    $(page[2]).click(function(){
        console.log("aaa");
        $(".first").hide();
        $(".second").hide();
        $(".third").hide();
        $(".forth").hide();
        $(".fifth").hide();
        $(".sixth").fadeIn(300);
        $(".seventh").fadeIn(300);
        page.css("background-color","#263238");
        page.find("a").css("color","#ABB1B7");
        $(page[2]).css("background-color","rgba(255,255,255,.1)");
        $(page[2]).find("a").css("color","white");

        //获取请求的学期
        var term = $('input#countrySelect')[0].value;
        //console.log($('input#countrySelect')[0].value);
        //获取进步排名
        $.ajax({
            type:"get",
            url:"/self",
            data:{
                "username":id,
                "term":term,
                "parameter":"progress"
            },
            dataType:"json",
            success:function(msg){
                console.log(msg);
            },
            error:function(xml){
                console.log(xml.status);
            }
        });
        


        //排名统计
        var lineChartData = {
            labels : ["大一上","大一下"],
            datasets : [{
                label: "My First dataset",
                fillColor : "rgba(220,220,220,0.2)",
                strokeColor : "rgba(1,70,138,0.8)",
                pointColor : "rgba(1,70,138,0.9)",
                pointStrokeColor : "#fff",
                pointHighlightFill : "#fff",
                pointHighlightStroke : "rgba(220,220,220,1)",
                data : [10,22]
            }]
        }
        var ctx = document.getElementById("line").getContext("2d");
        window.myLine = new Chart(ctx).Line(lineChartData, {
            responsive: true,
            scaleFontSize : 25,
        });

    })
    
    //console.log(page[3]);
    $(page[3]).click(function(){
        window.location.href = "mointor.html";
    })