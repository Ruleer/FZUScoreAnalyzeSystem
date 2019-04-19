function getPersonScore(a,b){

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
            return msg;
        },
        error:function(xml){
            return xml.status;
        }
    });
}