const COLS=8;
var final_list=[]; //stores the all the booked slots of the user as a 2D array
var temp_list=[]; //stores the current selected blocks before pressing submit

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

$("#submit").on('click',function() {
    final_list.push(temp_list);
    temp_list.forEach((value)=>{
        $(".cols").eq(value).toggleClass('toggle_class');
    });
    temp_list=[];
});