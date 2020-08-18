$("#sub").click(function(){

    var x = $("#myRange").val();
    if(x == "0"){
      $("#rate").text("Oops! You can not rate 0");
      return false;
    }
});
