var req;

function toggle_form_visibility(id1) {
   var item = document.getElementById(id1);
   if(item.style.display == 'none'){
      	item.style.display = 'inline';
      }
   else{
   	  	item.style.display = 'none';
   }   
   console.log(item);
}

function requestNotifications(){
	if (window.XMLHttpRequest) {
	   req = new XMLHttpRequest();
	} else {
	    req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	resetThisTimer = 1;
	req.onreadystatechange = updateNotifications;
	req.open("GET", "/userNotifications", true);
	req.send(); 
}
window.setInterval(requestNotifications,5000);

function updateNotifications() {
	if (req.readyState != 4 || req.status != 200) {
        return;
    }   
 
    var list = document.getElementById("listOfNotifications");
    var badge = document.getElementById("counter");
    var electric = document.getElementById("counterGlyph");
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild);
    }

    var items = JSON.parse(req.responseText);
    badge.innerText = items.length
    if (items.length == 0){
    	var newItem = document.createElement("li");
        newItem.innerHTML = "<a href=\"#\">No new notifications<button type=\"submit\" class=\"btn btn-default btn-sm\"><span class=\"glyphicon glyphicon-refresh\"></span></button></a>"
        list.appendChild(newItem);
    }
    else{
    	electric.className += " yellow";
    	for (var i = 0; i < items.length; ++i) {
        	var id = items[i]["pk"];
        	console.log(id);
        	var title = items[i]["fields"]["title"];
  
        	var newItem = document.createElement("li");
        	newItem.innerHTML = "<a href=\"/profile/notification/"+id+"\">"+title+"</a>";
        	list.appendChild(newItem);
    	}
    }
}

$(document).ready(function() {
	if (window.XMLHttpRequest) {
	    req = new XMLHttpRequest();
	} else {
	    req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	resetThisTimer = 1;
	req.onreadystatechange = updateNotifications;
	req.open("GET", "/updateStatuses", true);
	req.send(); 

	var hideWidth = '-170px'; //width that will be hidden
	var collapsibleEl = $('.collapsible'); //collapsible element
	var buttonEl =  $(".collapsible #main"); //big button 
	var winHeight = $(window).height()*.93; 
	var expanded = false;

	collapsibleEl.css({'position':'fixed','right': hideWidth,'height': winHeight});
	buttonEl.css({'height': winHeight-10});

	$(buttonEl).click(function()
	{
	    if(expanded)
	    {
	        $(this).parent().animate({right: hideWidth}, 300 );
	        $(this).html('&laquo;'); //change text of button
	        expanded = false;
	    }else{
	        $(this).parent().animate({right: "0"}, 300 ); 
	        $(this).html('&raquo;'); //change text of button
	        expanded = true;
	    }
	});

	$( window ).resize(function() {
		winHeight = $(window).height()*.93;
	});

	var visButton = $('.visButton');
	var priceButton= $('.priceButton');
	
	$(visButton).click(function()
	{
		var bid_id = this.id.split("_")[1];
		priceButton_id = "#priceButton_" + bid_id
		priceSubmit_id = "#priceSubmit_" + bid_id

		var thisPriceButton = $(priceButton_id);		
		var thisPriceSubmit = $(priceSubmit_id);

		$(this).css({'display':'none'});
		thisPriceSubmit.css({'display':'block'});
		thisPriceButton.css({'display':'block'});
	});

	$(priceButton).click(function()
	{
		var bid_id = this.id.split("_")[1];
		visButton_id = "#visButton_" + bid_id
		priceSubmit_id = "#priceSubmit_" + bid_id

		var thisVisButton = $(visButton_id);		
		var thisPriceSubmit = $(priceSubmit_id);

		thisVisButton.css({'display':'block'});
		$(this).css({'display':'none'});
		thisPriceSubmit.css({'display':'none'});

		numField_id = "#priceInput_"+bid_id;
		var new_price = $(numField_id).val();		

		priceRequest(bid_id,new_price);
	});
});

var priceReq;
function priceRequest(bid_id,new_price) {
	if(window.XMLHttpRequest){
		priceReq = new XMLHttpRequest();
	}
	else {
		priceReq = new ActiveXObject("Microsoft.XMLHTTP");
	}

	priceReq.onreadystatechange = priceResponse;
	priceReq.open("GET", "/updateBidPrice/"+bid_id+"/"+new_price, true);
	priceReq.send();
}

function priceResponse(){
	if (priceReq.readyState != 4 || priceReq.status != 200){
		return;
	}

	var bidData = JSON.parse(priceReq.responseText)
	for(var i = 0; i < bidData.length; i++){
		var b_id = bidData[i]["pk"];
		var p_id = "price_" + b_id;
		var price = parseInt(bidData[i]["fields"]["price"]);


		$('#'+p_id).text('Your Offer: $'+price)
	}
}


var trackReq;
function trackerRequest() {
	if(window.XMLHttpRequest){
		trackReq = new XMLHttpRequest();
	}
	else {
		trackReq = new ActiveXObject("Microsoft.XMLHTTP");
	}

	trackReq.onreadystatechange = trackerResponse;
	trackReq.open("GET", "/userBidsTrack", true);
	trackReq.send();
}

window.setInterval(trackerRequest,1000);

function trackerResponse(){
	if (trackReq.readyState != 4 || trackReq.status != 200){
		return;
	}

	var bidData = JSON.parse(trackReq.responseText)
	for(var i = 0; i < bidData.length; i++){
		var b_id = bidData[i]["pk"];
		var track_id = "tracker_" + b_id;
		var status = parseInt(bidData[i]["fields"]["status"]);

		if(status == 1 || status == 0){
			var t = document.getElementById(track_id).parentNode.parentNode;
			t.style.background = "rgba(113,188,120,0.65)";
		}
		else{
			var t = document.getElementById(track_id).parentNode.parentNode;
			t.style.background = "rgba(120, 120, 120,0.85)";
		}
	}
}
