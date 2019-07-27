
var skip_pages = 5; //change your number accordingly you want to show number
var factor = Math.floor(current_page/skip_pages);

$(".page_number").each(function(i, obj) {   //Showing the discrete numbers
      var page = factor*(skip_pages) + i + 1;
      if(current_page%skip_pages == 0)
        page = (factor-1)*skip_pages + i + 1;
      if(page - 1 < total_pages){
        $(this).html(page);
        $(this).attr("href", "?page=" + page);
      }
      else{
        var x = i+1;
        $('li[data=' + x + ']').css("display", "none");
      }
});
  var page = current_page%skip_pages;
  if(page == 0)
    page = skip_pages;
  $('li[data=' + page + ']').each(function(){   //Deciding the active class
    $('li[data=' + page + ']').addClass("active");
  });

$(".skip_next").click(function(){   //Skip next ... Function
    if(current_page%skip_pages == 0)
      factor = factor-1;
    var page = (factor+1)*skip_pages + 1;
    if(page < total_pages)
      $(this).attr("href", "?page=" + page);
    else
      $(this).attr("href", "?page=" + total_pages);
})
$(".skip_prev").click(function(){ //Skip Previous ... Function
    if(current_page%skip_pages == 0)
      factor = factor-1;
    var page = skip_pages*(factor-1) + 1;
    if(page > 0)
      $(this).attr("href", "?page=" + page);
    else
      $(this).attr("href", "?page=" + "1");
})
