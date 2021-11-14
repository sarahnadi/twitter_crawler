$(document).ready(function(){
    $("#search-btn-1").click(function(){
    // htmlobj=$.ajax({url:"/jquery/test1.txt",async:false});
    // $("#myDiv").html(htmlobj.responseText);
    var keyword = $("#keyword-box-1").val();
    if (keyword == ""){
        alert('please type a keyword!');
        return;
    }
    var data = {keyword:keyword};
    $.bootstrapLoading.start({ loadingTips: "go take a cup of coffee and come back...." });
    $.ajax({
        type: "POST",
        url: "http://0.0.0.0:32032/first",
        data: JSON.stringify(data),
        dataType : 'json',
        success:function(data){
            if (data.first.length == 0){
                alert('oops, no data!');
                $.bootstrapLoading.end();
                $("#table-twitter-1").bootstrapTable("destroy");
                
                $("#table-hashtag-1").bootstrapTable("destroy");
                $("#table-twitter-1").bootstrapTable({});
                $("#table-hashtag-1").bootstrapTable({});
            }
            else{
                //console.log(data.first);
                $.bootstrapLoading.end();
                console.log(data.second);
                $("#table-twitter-1").bootstrapTable("load", data.first);
                $("#table-hashtag-1").bootstrapTable("load", data.second);
            }
        },
     });
    });

    $("#search-btn-2").click(function(){
        // htmlobj=$.ajax({url:"/jquery/test1.txt",async:false});
        // $("#myDiv").html(htmlobj.responseText);
        var region = $("#region-select").val();
        var keyword = $("#keyword-box-2").val();
        if (keyword == ""){
            alert('please type a keyword!');
            return;
        }
        var data = {
            region:region,
            keyword:keyword
        };
        $.bootstrapLoading.start({ loadingTips: "go take a cup of coffee and come back...." });
        $.ajax({
            type: "POST",
            url: "http://0.0.0.0:32032/second",
            data: JSON.stringify(data),
            dataType : 'json',
            success:function(data){
                if (data.first.length == 0){
                    alert('oops, no data!');   
                    $.bootstrapLoading.end();                
                    $("#table-twitter-2").bootstrapTable("destroy");
                    $("#table-hashtag-2").bootstrapTable("destroy");                  
                    $("#table-twitter-2").bootstrapTable({});
                    $("#table-hashtag-2").bootstrapTable({});
                    
                    
                }
                else{
                    //console.log(data.first);
                    $.bootstrapLoading.end();
                    console.log(data.second);
                    $("#table-twitter-2").bootstrapTable("load", data.first);
                    $("#table-hashtag-2").bootstrapTable("load", data.second);
                }
            },
         });
    });

    $("#search-btn-3").click(function(){
        // htmlobj=$.ajax({url:"/jquery/test1.txt",async:false});
        // $("#myDiv").html(htmlobj.responseText);
        var keyword = $("#keyword-box-3").val();
        if (keyword == ""){
            alert('please type a keyword!');
            return;
        }
        var data = {
            keyword:keyword
        };
        $.bootstrapLoading.start({ loadingTips: "go take a cup of coffee and come back...." });
        $.ajax({
            type: "POST",
            url: "http://0.0.0.0:32032/third",
            data: JSON.stringify(data),
            dataType : 'json',
            success:function(data){
                if (data.length == 0){
                    alert('oops, no data!');
                    $.bootstrapLoading.end();
                    $("#table-twitter-3").bootstrapTable("destroy");
                    $("#table-twitter-3").bootstrapTable({});
                }
                else{
                    $.bootstrapLoading.end();
                    $("#table-twitter-3").bootstrapTable("load", data);
                }
            },
         });
    });

});