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


//点击切换
    var page = $(".nav-item");
    console.log(page[1]);
    //班级概况
    $(page[0]).click(function(){
        $(".container1").fadeIn(300);
        $(".container2").hide();
        page.css("background-color","#263238");
        page.find("a").css("color","#ABB1B7");
        $(page[0]).css("background-color","rgba(255,255,255,.1)");
        $(page[0]).find("a").css("color","white");
        //成绩比例
        //总成绩
        var doughnutData = [
            {
                value: 20,
                color:"#F7464A",
                highlight: "#FF5A5E",
            },{
                value: 40,
                color: "#4D5360",
                highlight: "#616774",
            },{
                value: 40,
                color: "#4D3560",
                highlight: "#616774",
            }
        ];

        //总成绩
        var ctx = document.getElementById("chart-area").getContext("2d");
        window.myDoughnut = new Chart(ctx).Doughnut(doughnutData, {
            responsive : true
        });

        //柱状图体现成绩分布
        var barChartData = {
            labels : ["不及格","及格","良好","优秀"],
            datasets : [
                {
                    fillColor : "rgba(220,220,220,0.5)",
                    strokeColor : "rgba(220,220,220,0.8)",
                    highlightFill: "rgba(220,220,220,0.75)",
                    highlightStroke: "rgba(220,220,220,1)",
                    data : [2,14,18,2]
                },
            ]
        }

        var ctx = document.getElementById("canvas1").getContext("2d");
        window.myBar = new Chart(ctx).Bar(barChartData, {
            responsive : true
        });
    });
    //成绩汇总
    $(page[1]).click(function(){
        console.log("aaa");
        $(".container1").hide();
        $(".container2").fadeIn(300);
        page.css("background-color","#263238");
        page.find("a").css("color","#ABB1B7");
        $(page[1]).css("background-color","rgba(255,255,255,.1)");
        $(page[1]).find("a").css("color","white");
    });
    
    //console.log(page[3]);
    $(page[2]).click(function(){
        window.location.href = "studenReport.html";
    })