  //地图脚本
 function init() {
  var myLatlng = new soso.maps.LatLng(longtitude,latitude);
  var myOptions = {
    zoom: 12,
    center: myLatlng,
    mapTypeId: soso.maps.MapTypeId.ROADMAP
  };

  var map = new soso.maps.Map(document.getElementById("map-container"), myOptions);
  var navControl = new soso.maps.NavigationControl({
        align: soso.maps.ALIGN.TOP_LEFT,
        margin: new soso.maps.Size(0, 10),
        map: map
    });
  var marker = new soso.maps.Marker({
        position: myLatlng,
        map: map
    });
  var info = new soso.maps.InfoWindow({
        map: map
    });
  soso.maps.event.addListener(marker, 'click', function() {
        info.open(); 
        info.setContent('<div style="text-align:center;white-space:nowrap;'+
        'margin:10px;">{$bridge_info[name]}</div>');
        info.setPosition(myLatlng); 
    });
 }
  
 function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://map.soso.com/api/v2/main.js?callback=init";
  document.body.appendChild(script);
 }
  
 window.onload = loadScript;
