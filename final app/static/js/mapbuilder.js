
        function stringBuilder(list){
            var st = "<div class=\"informWindow\"><p>" + "NETID: " + list[0] + "</p>" + "<p>" + "Name: " + list[1] + "</p>" + "<p>" + "Email: " + list[2] + "</p>" + "<p>" + "Phone: " +
            list[3] + "</p>" + "<p>" + "Description: " + list[4] + "</p> <button type=\"button\" class=\"btn\" onclick=\"openMsgBox('" + list[0] + "')\">Send Message</button></div>";
            return st;
          }
  
          function toString(item) {
            return item.toString()
  
          }
          var infowindow;
  
  
  
  
          function addMarker(coordinates, map, info, image){
            var marker = new google.maps.Marker({
              position: coordinates,
              map: map,
              icon: image
              // add tiger icon
            });
  
            // var infowindow = new google.maps.InfoWindow({
            //   content: info
            // });
            marker.addListener('click', function() {
              infowindow.setContent(info);
              infowindow.open(map, marker);
              });
            console.log('success')
          }
  
  
          function initMap() {
            // Create a new StyledMapType object, passing it an array of styles,
            // and the name to be displayed on the map type control.
            var styledMapType = new google.maps.StyledMapType(
              [
                {
                  "elementType": "geometry",
                  "stylers": [
                    {
                      "color": "#f5f5f5"
                    }
                  ]
                },
                {
                  "elementType": "labels.icon",
                  "stylers": [
                    {
                      "visibility": "off"
                    }
                  ]
                },
                {
                  "elementType": "labels.text.fill",
                  "stylers": [
                    {
                      "color": "#616161"
                    }
                  ]
                },
                {
                  "elementType": "labels.text.stroke",
                  "stylers": [
                    {
                      "color": "#f5f5f5"
                    }
                  ]
                },
                {
                  "featureType": "administrative.land_parcel",
                  "elementType": "labels.text.fill",
                  "stylers": [
                    {
                      "color": "#bdbdbd"
                    }
                  ]
                },
                {
                  "featureType": "poi",
                  "elementType": "geometry",
                  "stylers": [
                    {
                      "color": "#eeeeee"
                    }
                  ]
                },
                {
                  "featureType": "poi",
                  "elementType": "labels.text.fill",
                  "stylers": [
                    {
                      "color": "#757575"
                    }
                  ]
                },
                {
                  "featureType": "poi.park",
                  "elementType": "geometry",
                  "stylers": [
                    {
                      "color": "#e5e5e5"
                    }
                  ]
                },
                {
                  "featureType": "poi.park",
                  "elementType": "labels.text.fill",
                  "stylers": [
                    {
                      "color": "#9e9e9e"
                    }
                  ]
                },
                {
                  "featureType": "road",
                  "elementType": "geometry",
                  "stylers": [
                    {
                      "color": "#ffffff"
                    }
                  ]
                },
                {
                  "featureType": "road.arterial",
                  "elementType": "labels.text.fill",
                  "stylers": [
                    {
                      "color": "#757575"
                    }
                  ]
                },
                {
                  "featureType": "road.highway",
                  "elementType": "geometry",
                  "stylers": [
                    {
                      "color": "#dadada"
                    }
                  ]
                },
                {
                  "featureType": "road.highway",
                  "elementType": "labels.text.fill",
                  "stylers": [
                    {
                      "color": "#616161"
                    }
                  ]
                },
                {
                  "featureType": "road.local",
                  "elementType": "labels.text.fill",
                  "stylers": [
                    {
                      "color": "#9e9e9e"
                    }
                  ]
                },
                {
                  "featureType": "transit.line",
                  "elementType": "geometry",
                  "stylers": [
                    {
                      "color": "#e5e5e5"
                    }
                  ]
                },
                {
                  "featureType": "transit.station",
                  "elementType": "geometry",
                  "stylers": [
                    {
                      "color": "#eeeeee"
                    }
                  ]
                },
                {
                  "featureType": "water",
                  "elementType": "geometry",
                  "stylers": [
                    {
                      "color": "#c9c9c9"
                    }
                  ]
                },
                {
                  "featureType": "water",
                  "elementType": "labels.text.fill",
                  "stylers": [
                    {
                      "color": "#9e9e9e"
                    }
                  ]
                }
  
              ],
                {name: 'Styled Map'});
  
            // Create a map object, and include the MapTypeId to add
            // to the map type control.
  
  
            infowindow = new google.maps.InfoWindow();
            var map = new google.maps.Map(document.getElementById('map'), {
  
              center: new google.maps.LatLng(40.349990 ,-74.658580),
              zoom: 4,
              mapTypeControlOptions: {
                mapTypeIds: ['roadmap', 'satellite', 'hybrid', 'terrain',
                        'styled_map']
              }
            });
            var info = ""
            var image = {
            url: '/static/babytigericon.png',
            scaledSize: new google.maps.Size(32,28),
            // The origin for this image is (0, 0).
            origin: new google.maps.Point(0, 0),
            // The anchor for this image is the base of the tiger at (10, 32).
            anchor: new google.maps.Point(10, 32)
             };
  
             var yourImage = {
            url: '/static/whitetigericon.png',
            scaledSize: new google.maps.Size(32,28),
            // The origin for this image is (0, 0).
            origin: new google.maps.Point(0, 0),
            // The anchor for this image is the base of the tiger at (10, 32).
            anchor: new google.maps.Point(10, 32)
             };
  
            for (i = 0; i < data.length; i++) {
  
              if (data[i].length > 5){
                info = stringBuilder(data[i]);
  
                if (data[i][0] == userNetid) {
                addMarker({lat: data[i][5], lng: data[i][6]}, map, info, yourImage);
                } else {
                addMarker({lat: data[i][5], lng: data[i][6]}, map, info, image);
                }
              }
              }
            //Associate the styled map with the MapTypeId and set it to display.
            map.mapTypes.set('styled_map', styledMapType);
            map.setMapTypeId('roadmap');
            map.setOptions({minZoom: 3});
            google.maps.event.addListener(map, "click", function(event) {
              infowindow.close();
            });
  
  
            function initialize() {
          var input = document.getElementById('address');
          var autocomplete = new google.maps.places.Autocomplete(input);
          // changes whenever user selects new address in drop down
          google.maps.event.addListener(autocomplete, 'place_changed', function () {
                      var place = autocomplete.getPlace();
                  });
            }
  
          google.maps.event.addDomListener(window, 'load', initialize);
  
  
          }