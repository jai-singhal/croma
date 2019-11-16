// Foreign Key edit popup function
function showAddEditPopup(url, title = "Edit Form", h = 500, w = 800) {
    var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
    var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

    var left = ((width / 2) - (w / 2));
    var top = ((height / 2) - (h / 2));
    var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);

    if (window.focus) {
        newWindow.focus();
    }
    return false;
}
// Foreign Key ADD popup function
function showAddPopup(triggeringLink, title = "Add Form", h = 500, w = 800) {
    var name = triggeringLink.id.replace(/^add_/, '');
    console.log("in add form")
    url = triggeringLink.href;
    
    var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
    var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;
    var left = ((width / 2) - (w / 2));
    var top = ((height / 2) - (h / 2));
    var newWindow = window.open(url, title, 'scrollbars=yes, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
    if (window.focus) {
        newWindow.focus();
    }
    return false;
}
// Foreign Key CLOSE popup function
function closeAddPopup(win, newID, newRepr, id) {
    $(id).val(newRepr)
    win.close();
}
//GENERATE CSRF TOKEN
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$(document).ready(function(){
    $('ul.dropdown-menu [data-toggle=dropdown]').on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        $(this).parent().siblings().removeClass('open');
        $(this).parent().toggleClass('open');
    });
    $('input[type=text]').keyup(function() {
        $(this).css("text-transform", "uppercase");
        var v = $(this).val();
        var u = v.toUpperCase();
        if( v != u ) $(this).val( u );

    })
    $("input[type='text'], input[type='number']").focus(function () {
       $(this).select();
    });

});

String.prototype.toTitleCase = function() {
    var i, j, str, lowers, uppers;
    str = this.replace(/([^\W_]+[^\s-]*) */g, function(txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
  
    // Certain minor words should be left lowercase unless 
    // they are the first or last words in the string
    lowers = ['A', 'An', 'The', 'And', 'But', 'Or', 'For', 'Nor', 'As', 'At', 
    'By', 'For', 'From', 'In', 'Into', 'Near', 'Of', 'On', 'Onto', 'To', 'With'];
    for (i = 0, j = lowers.length; i < j; i++)
      str = str.replace(new RegExp('\\s' + lowers[i] + '\\s', 'g'), 
        function(txt) {
          return txt.toLowerCase();
        });
  
    // Certain words such as initialisms or acronyms should be left uppercase
    uppers = ['Id', 'Tv'];
    for (i = 0, j = uppers.length; i < j; i++)
      str = str.replace(new RegExp('\\b' + uppers[i] + '\\b', 'g'), 
        uppers[i].toUpperCase());
  
    return str;
  }

function ItemAutoComplete(itemData, idName = "#id_item_id"){
    $(idName).autocomplete({
      lookup: itemData,
      preventBadQueries: true,
      lookupLimit: 100,
      minChars: 1,
      autoSelectFirst : false,
      showNoSuggestionNotice:  true,

      onSelect: function(suggestion) {
            ItemOnSelect(suggestion) ;
            $("#item_id_field").val(suggestion.id)
      },
      onHint: function (hint) {
          $('#item-hint').val(hint);
       },
      lookupFilter: function (suggestion, query, queryLowerCase) {
     		return suggestion.value.toLowerCase().indexOf(queryLowerCase) == 0;
 		},
  });
}


function LoadAutoCompleteItemData(idName = "#id_item_id"){
  var itemData = JSON.parse(localStorage.getItem('itemData'));

  if (!itemData){
    $("#gif_load_iten_batches").attr("display", "inline-block");
    $.getJSON('/item/api/list/?format=json', function (data) {
      itemData = localStorage.setItem('itemData', JSON.stringify(data));
      ItemAutoComplete(data, idName);
    });
  }
  else
    ItemAutoComplete(itemData, idName);
}


function AutoCompleteUtil(data, idName, lookupLimit, minChars){
    $(idName).autocomplete({
        lookup: data,
        lookupLimit: lookupLimit,
        minChars: minChars,
        lookupFilter: function (suggestion, query, queryLowerCase) {
            return suggestion.value.toLowerCase().indexOf(queryLowerCase) == 0;
        },
    });
}

function AutoCompleteData(apiURL, keyName, idName, lookupLimit, minChars){
    var storageData = JSON.parse(localStorage.getItem(keyName));
    if (!storageData){
        $.getJSON(apiURL, function (newData) {
            storageData = localStorage.setItem(keyName, JSON.stringify(newData));
            AutoCompleteUtil(newData, idName, lookupLimit, minChars);
        });
    }
    else
        AutoCompleteUtil(storageData, idName, lookupLimit, minChars);
}
function expiryValidations() {
    var expiry_selector = $("#expiry");
    var expiry = expiry_selector.val();
    var CurrentDate = new Date();
    var batch_date = expiry_selector.val();
    batch_date = batch_date.slice(3, 7) + "-" + batch_date.slice(0, 2);
    var SelectedDate = new Date(Date.parse(batch_date));

    if (CurrentDate >= SelectedDate) { //validate expiry
        expiry_selector.focus();
        expiry_selector.val('');
        alert("Expired Batch not allowed!!");
        return false;
    }

    if ((! /(([0][1-9])\/([2][0][0-9][0-9]))/.test(expiry) &&
        ! /(([1][0-2])\/([2][0][0-9][0-9]))/.test(expiry)) &&
        !/(([2][0][0-9][0-9])\-([0-1][0-9])\-([0-3][0-9]))/.test(expiry) &&
        ! /(([2][0][0-9][0-9])\-([0-1][0-9]))/.test(expiry) && expiry != "") {
        expiry_selector.focus();
        expiry_selector.val('');
        alert("Expiry Format is Wrong");
        return false;
    }
}

$("#expiry").focus(function () {
    $(this).select();
    $("#expiry").keypress(function (e) {
        var text = $(this).val();
        var len = text.length;
        if (len == 2) $(this).val(text + "/");
        if (len == 1)
            if (parseInt(text) != 0 && parseInt(text) != 1) $(this).val("0" + text + "/");
        if (len > 2)
            if (len == 5 && e.which == 13) $(this).val(text.slice(0, 3) + "20" + text.slice(3, 5));
    })
})


function daysInMonth(month, year) {
    return new Date(year, month, 0).getDate();
}


$(document).ready(function(){
    $('input:text:visible:first').focus();
    $("#close").click(function(){
        window.location.href='/'
        var $this = $(this);
        $this.button('loading');
    })
})

$("#prev").click(function(){
	var $this = $(this);
	$this.button('loading');
	window.location.href = $this.attr("prev-url");
})

$("#next").click(function(){
	var $this = $(this);
	$this.button('loading');
	window.location.href= $this.attr("next-url");
})

$("#add").click(function(){
	window.location.href='/sales/create'
	var $this = $(this);
	$this.button('loading');
})

$("#cancel").click(function(){
	var $this = $(this);
	$this.button('loading');
	window.location.href = $this.attr("cancel-url");
})

$("#edit").click(function(){
	var $this = $(this);
	$this.button('loading');
	window.location.href=$this.attr("edit-url")
})
