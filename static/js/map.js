// Mapの表示、開始地点は名古屋駅
// 開始地点を可変にするのは後→検索ボックスに住所の入力があれば緯度経度を検索する
/*
console.log(document.getElementById('shopLat').textContent);
console.log(document.getElementById('shopLng').textContent);


var center = new google.maps.LatLng(35.17070,136.88196);
var opts = {
    center: center,
    zoom: 16,
    mapTypeId: 'roadmap',
    // mapの表示スタイル　https://www.tam-tam.co.jp/tipsnote/html_css/post14880.html
    styles: [
        {
          "featureType": "administrative.land_parcel",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "administrative.neighborhood",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "landscape.man_made",
          "elementType": "geometry.stroke",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "landscape.man_made",
          "elementType": "labels.text",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "poi.business",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "poi.park",
          "elementType": "labels.text",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "labels",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "road.arterial",
          "elementType": "labels",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "road.highway",
          "elementType": "labels",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "road.local",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "water",
          "elementType": "labels.text",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        }
      ]
} 

//マーカーを立てる位置 ループで取得する
var Mlat = document.getElementById('shopLat').textContent;
var Mlng = document.getElementById('shopLng').textContent;

var marker = new google.maps.LatLng(
    Mlat,
    Mlng
);
var mopts = {
    position: marker,
    map: map
};

var map = new google.maps.Map(document.getElementById('map'), opts)
var markerMap = new google.maps.Marker(mopts);

//marker.setMap(null)
// データベースに登録された店舗の名前緯度経度の情報からピンを立てる

//document.getElementById('shopLat').textContent, //35.16831,
//document.getElementById('shopLng').textContent //136.87863
*/



$(function(){
	$('#select').on('change', function(){
        if($(this).val() == "0"){
            $(this).css('color','#CCC')
        } else {
            $(this).css('color','#1A1A1A')
        }
    });
});