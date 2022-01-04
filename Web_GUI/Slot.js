var COLS;
var final_list={}; //stores the all the booked slots of the user as a 2D array
var temp_list=[]; //stores the current selected blocks before pressing submit
$("#submit_cols").on("click",function(){
    let v=$("#col_num").val();
    let val=parseInt(v);
    COLS=val;
    $(".rows").each((ind,ele)=>{
        for(let i=0;i<val;i++)
            $(ele).append($("<div>", {class: "cols"}));
    });
    initialiseCols();
    $("#outer").show();
    $("#preview").hide();
});

function initialiseCols(){
    $(".cols").each((ind,item)=>{
        $(item).val(ind);
    });
    $(".cols").on('click', function (e) {
        var element = $(e.target);  //finding the clicked object
        element.toggleClass('toggle_class');  //toggling color on cliking
        let v=element.val();
        let ind=temp_list.indexOf(v);
        if(ind>-1)
            temp_list.splice(ind,1);
        else
            temp_list.push(v);
    });
}

$("#submit").on('click',function() {
    let v=$("#slot_name").val();
    $("#slot_name").val("");
    final_list[v]=temp_list;
    temp_list.forEach((value)=>{
        $(".cols").eq(value).toggleClass('toggle_class');
    });
    temp_list=[];
    console.log(final_list);
});