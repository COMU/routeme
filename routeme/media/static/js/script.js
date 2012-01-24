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
  var latlng = new google.maps.LatLng(39.57, 32.51);
  var mapOptions = {
    zoom: 4,
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

//shows selected route on map 
function showSelectedRouteOnMap(data){
    alert(Number(data.coordinates[3][1]));
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
            optimizeWaypoints: true,
            travelMode: google.maps.DirectionsTravelMode.DRIVING
        };
        var direction = new google.maps.DirectionsRenderer({markerOptions: {visible: false}});
        directionRenderers.push(direction);
	direction.setMap(map);
        drawRoute(request, direction);
     } 
}

//While user creating a route when #show button is clicked route will be displayed on map.
function showRouteOnMap(){
  var start = $("#where").val();
  var end = $("#to").val();
  var request = {
    origin: start,
    destination: end,
    travelMode: google.maps.TravelMode.DRIVING
  };
  drawRoute(request, directionDisplay);
}

$(document).ready(function (){
    $("#createRouteSubmit").attr('disabled', true);//diabled button to save route without directions.
    $("#show").click(showRouteOnMap);
    $("#sroute").click(searchRoute);

    $("#id_date").datepicker({dateFormat: 'yy-mm-dd'});//when user click textfield jquery-ui
    $("#id_time").timepicker({timeFormat: 'h:m'});//datepicker or timepicker will be displayed on screen.
});





















