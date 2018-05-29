/*------------------------------
 * Copyright 2014 Pixelized
 * http://www.pixelized.cz
 *
 * Sitename theme v1.0
------------------------------*/
$(document).ready(function() {	
	


<!--Vegas background start -->
	$.vegas({
	  src:'static/Home/image/gotas.jpg'
	});
	
	$.vegas('overlay', {
	  src:'static/Home/overlays/05.png'
	});	
<!--Vegas background end -->
<!-- GOOGLE map initialization star-->
	var myLatlng = new google.maps.LatLng(-13.523533, -71.968838);
	var mapOptions = {
	  zoom: 17,
	  center: myLatlng,
	  navigationControl: false,
	  mapTypeControl: false,
	  scaleControl: false,
	  draggable: true,
	  scrollwheel: false
	}

	var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

	var marker = new google.maps.Marker({
		position: myLatlng,
		map: map,
		title:"Your Marker!"
	});

		
<!-- GOOGLE map initialization end-->

<!-- GOOGLE map modal fix start-->
	
	$("#contact").on("shown.bs.modal", function () {
		google.maps.event.trigger(map, "resize");
		map.setCenter(myLatlng);
	});
<!-- GOOGLE map modal fix end-->
	
});
/*
$(window).resize(function() {	
	$("#DateCountdown").TimeCircles().rebuild(); 
});*/


