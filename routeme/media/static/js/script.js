
var map;
var directionService = new google.maps.DirectionsService();
var directionDisplay;
var geocoder;
var directionRenderers = [];

//direction will be draggable
var directionOptions = {
  draggable: true
};

//map will be ready to use
function initializeMap(){
  directionDisplay = new google.maps.DirectionsRenderer(directionOptions);
  var latlng;
  if (google.loader.ClientLocation != null){
      latlng = new google.maps.LatLng(google.loader.ClientLocation.latitude, google.loader.ClientLocation.longitude);
  }else{
      latlng = new google.maps.LatLng(39.57, 32.51);
  }
  var mapOptions = {
    zoom: 7,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map"), mapOptions);
  google.maps.event.addListener(directionDisplay, "directions_changed", function(){
     saveResultAsStr(directionDisplay.directions);
  });

  directionDisplay.setMap(map);
  geocoder = new google.maps.Geocoder();
}

function drawRoute(request, directionDisplay){
  directionService.route(request, function(result, status){
      if (status == google.maps.DirectionsStatus.OK){
        $("#createRouteSubmit").attr('disabled', false);
            directionDisplay.setDirections(result);
      }
  });
}



//this method pushs direction coordinates(waypoints) into hidden text field.
function saveResultAsStr(result){
    var legs = result.routes[0].legs[0];
    seconds = result.routes[0].legs[0].duration.value;
    hours = parseInt(seconds / 3600);
    mins = parseInt((seconds - (hours * 3600)) / 60);
    $('#id_arrivalTime').val(hours + ":" + mins);
    $('#id_arrivalTime').attr("readonly", "readonly");
    var route = [];

    for(var i = 0; i < legs.steps.length; i++){
        route.push(legs.steps[i].start_point.lat() + "," + legs.steps[i].start_point.lng());
        route.push(legs.steps[i].end_point.lat() + "," + legs.steps[i].end_point.lng());
    }
    $('#id_route').val(route.join("\n"));
}

//this method returns coordinates of given place
function findPosition(address, callback){
    geocoder.geocode({'address': address}, function(results, status){
        if(status = google.maps.GeocoderStatus.OK){
            var position = results[0].geometry.location;
            callback(position);
        }
    });
}


//finds coords of startpoint and endpoint then inserts into hidden text fields
//#id_start and #id_end 
function searchRoute(){
    var start = $("#id_where").val();
    var to = $("#id_to").val();

    geocoder.geocode({'address': start}, function(results, status){
        if(status = google.maps.GeocoderStatus.OK){
            var start_position = results[0].geometry.location;
            geocoder.geocode({'address': to}, function(results, status){
                if(status = google.maps.GeocoderStatus.OK){
                    var end_position = results[0].geometry.location;
                    $('#id_start').val(start_position.lat()+","+start_position.lng());//
                    $('#id_end').val(end_position.lat()+","+end_position.lng());
	            
                    $('#searchRouteForm').submit();
                }});
        }});

}


function removeRenderers(){
    if (directionRenderers.length != 0){
        for(var i=0; i < directionRenderers.length; i++){
	    directionRenderers[i].setMap(null);
	}
        directionRenderers = []
    }
}

var sayac=0;
var geocoder;
function selectStartPoint(routeId,n){
 	//TODO code may be more efficent
	google.maps.event.addListener(map, "click", function (e) {
	if(sayac<3){
	    var lat = e.latLng.lat();
	    var lng = e.latLng.lng();
	    point=lat+","+lng;
	    geocoder = new google.maps.Geocoder();
	    var onay = window.confirm("if You Are Sure Please Click Ok Button"); 
            if(onay){
		if(sayac==0){
		  alert("start"+point);
	    	  var latlng = new google.maps.LatLng(Number(lat), Number(lng));
                  geocoder.geocode({'latLng':latlng},function(result,status){
	   	     if (status == google.maps.GeocoderStatus.OK){
		        if(result[1]){
			  sayac=sayac+1; 
			  $('#'+n).find('#id_startaddress').val(result[1].formatted_address);			   
		        } 
		     }
                  });
		  $('#'+n).find('#id_startpoint').val(point);
		}
		else if(sayac==1){
		  alert("stop"+point);
                  var latlng = new google.maps.LatLng(Number(lat), Number(lng));
                  geocoder.geocode({'latLng':latlng},function(result,status){
	   	     if (status == google.maps.GeocoderStatus.OK){
		        if(result[1]){
			   alert(result[1].formatted_address);
		  	   sayac=sayac+1;
			   $('#'+n).find('#id_stopaddress').val(result[1].formatted_address);	  
			   $('#'+n).find('#id_routeowner').val(routeId); 
		        }
		     }
                  });
		  $('#'+n).find('#id_endpoint').val(point);
		}
		else{
		  return -1;
		}	       
	    }
            else{
                selectStartPoint();
	    }
	}

});
	
}
var marker;
//shows selected route on map 
function showSelectedRouteOnMap(data,path,name,lastname,n){
    if (marker!=null){
	marker.setMap(null);
    }
    var waypts = [];
    for(i=0;i<data.coordinates.length;i++){
        var c1=Number(data.coordinates[i][0]);
        var c2=Number(data.coordinates[i][1]);
	stop = new google.maps.LatLng(c1,c2);
	waypts.push({location:stop, stopover:true});
    }
    removeRenderers(); 
    //TODO kod optimize edilebilir.
    for(var i = 0; i < waypts.length; i = i + 8){
        var j;
        if (i + 8 <= waypts.length - 1){
             j = i + 8;
        }else{
             j = waypts.length -1 ;
        }
        var request = {
            origin:  waypts[i].location,
            destination: waypts[j].location,
            waypoints: waypts.slice(i, j),
            //optimizeWaypoints: true,
            travelMode: google.maps.DirectionsTravelMode.DRIVING
        };
        var direction = new google.maps.DirectionsRenderer({markerOptions: {visible: false}});
        directionRenderers.push(direction);
	direction.setMap(map);
	var c1=Number(data.coordinates[0][0]);
        var c2=Number(data.coordinates[0][1]);
  	var myLatlng = new google.maps.LatLng(c1,c2);
	drawRoute(request, direction);
    } 
	var myLatlng = new google.maps.LatLng(c1,c2)
	var pimage = 'static/images/'+path;
	var image = new google.maps.MarkerImage(pimage)
	contentString="<html><div><img width='42' height='48' src="+pimage+">"+"  "+name+" " + lastname+"</div></html>"
	var infowindow = new google.maps.InfoWindow({
    		content: contentString,
		pixelOffset: new google.maps.Size(0, 0)
	
});

	marker = new google.maps.Marker({
    		position: myLatlng,
    		map: map
	});
	infowindow.open(map,marker);
	google.maps.event.addListener(marker, 'click', function() {
  	   infowindow.open(map,marker);
	});

    	$('#selectPointButton'+n).attr('disabled',false);
}

//While user creating a route when #show button is clicked route will be displayed on map.
function showRouteOnMap(){
  var start = $("#where").val();
  var end = $("#to").val();
  $('#id_start').val(start);
  $('#id_end').val(end);
  var request = {
    origin: start,
    destination: end,
    travelMode: google.maps.TravelMode.DRIVING
  };
  drawRoute(request, directionDisplay);
}

function updateRoute(formId){
    $('#'+formId).submit();
    $('#modal').modal("hide");
}

function sendRequest(id, n){
    $('#' + id).submit();
    $('#' + n).modal("hide");
}

$(document).ready(function (){
    $("#createRouteSubmit").attr('disabled', true);//diabled button to save route without directions.
    $("#show").click(showRouteOnMap);
    $("#sroute").click(searchRoute);
    $("#id_date").datepicker({dateFormat: 'yy-mm-dd', minDate: 0 });//when user click textfield jquery-ui this is createRoute's date.
    $("#id_birthdate").datepicker({dateFormat: 'yy-mm-dd', changeMonth: true, changeYear: true});//when user click textfield jquery-ui
    $("#id_time").timepicker({timeFormat:'hh:mm'});//datepicker or timepicker will be displayed on screen.

   
});



$(document).ajaxSend(function(event, xhr, settings) {
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
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if 

(!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
