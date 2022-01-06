var COLS;
var final_list={}; //stores the all the booked slots of the user as a 2D array
var temp_list=[]; //stores the current selected blocks before pressing submit

//method to handle after clumns have been selected
$("#submit_cols").on("click",function(){
    let v=$("#col_num").val();   //number of olumns entered in the input box
    let val=parseInt(v);
    COLS=val;
    $(".inner_rows").each((ind,ele)=>{
        $(ele).empty();    //making the inside empty to clear the blocks
        for(let i=0;i<val;i++)
            $(ele).append($("<div>", {class: "cols"}));
    });
    initialiseCols();
    $("#outer").show();
    // $("#preview").hide();
});

function initialiseCols(){
    $(".cols").each((ind,item)=>{
        $(item).val(ind);  //setting value of the block as their index to be stored in the list
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
    final_list[v]=temp_list;  //saving into final list
    temp_list.forEach((value)=>{                         
        $(".cols").eq(value).toggleClass('toggle_class');      //making the blocks to the original color
    });
    temp_list=[];
    console.log(final_list);
});

function processFile(s){
    let arr=s.split("\r\n");
    for(let i=0;i<arr.length;i++){
        if(arr[i]=="")continue;
        let key=arr[i++];
        final_list[key]=[];
        COLS=0;
        while(arr[i]!=""){
            let c=parseInt(arr[i][2])+1;
            COLS=Math.max(COLS,c);
            i++;
        }
    }
    for(let i=0;i<arr.length;i++){
        if(arr[i]=="")continue;
        let key=arr[i++];
        final_list[key]=[];
        while(arr[i]!=""){
            let r=parseInt(arr[i][0]);
            let c=parseInt(arr[i][2]);
            final_list[key].push(r*COLS+c);
            i++;
        }
    }
    console.log(final_list);
}
$('#prev_file').on('change', function () {
    var fileReader = new FileReader();  //for reading the file
    fileReader.onload=function(){
        processFile(fileReader.result);          
    }
    fileReader.readAsText($('#prev_file').prop('files')[0]);
});