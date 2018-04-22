var details = $("#details"), limits = [[33.1, -97], [32.6, -96.4]];

var map = L.map("map", {
	maxBounds: limits,
	maxBoundsViscosity: 1,
	zoomControl: false
}).setView([32.77, -96.79], 11);

var tiles = L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png', {
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>',
	subdomains: 'abcd',
	maxZoom: 18,
	minZoom: 10
}).addTo(map);

function isInside(lat, long) {
	if (districtBoundingBox) return districtBoundingBox.contains(L.latLng(lat, long));
	return !(lat > limits[0][0] || lat < limits[1][0] || long < limits[0][1] || long > limits[1][1]);
}

function yay(points) {
	var heat = L.heatLayer(points, {
		radius: 25,
		blur: 50,
		minOpacity: 0.5,
		gradient: {0: '#2c0e37', 0.2: '#690375', 1: '#cb429f'}
	}).addTo(map);
}

L.control.zoom({
	position: 'bottomright'
}).addTo(map);

var rainbow = new Rainbow();
rainbow.setSpectrum('#2c0e37', '#690375', '#cb429f');

var districts, districtBoundingBox;
function haha(data) {
	districts = L.geoJSON(null, {
		style: function(feature) {
			return {
				weight: 1,
				opacity: 0.5,
				fillOpacity: 0.2,
				color: "#"+rainbow.colourAt((Math.random()*100)|0)
			}
		},
		onEachFeature: function(feature, layer) {
			layer.on("click", function() {
				setTimeout(function() {
					details.find(".district strong").text("District "+layer.feature.properties.DISTRICT);
					details.find(".district span").text("Represented by "+layer.feature.properties.COUNCILPER);
				}, 300); // to make the animation smoother
			});
		}
	}).addTo(map);
	for (i in data.features) {
		var f = data.features[i];
		var toDraw = f;
		// toDraw.coordinates = f.geometry.coordinates[0];
		// toDraw.type = "LineString";
		districts.addData(toDraw);
	}
	districtBoundingBox = districts.getBounds();
	map.setMaxBounds(districtBoundingBox.pad(0.2));
	openBounds(districtBoundingBox);
	complete();
}

var waitingOn = 0, loadingSince = 0, stopAnimation;
function loading() {
	$("#loader").removeClass("loaded");
	waitingOn++;
	if (loadingSince == 0) loadingSince = new Date().getTime();
	if (stopAnimation) clearTimeout(stopAnimation);
}

function complete(all) {
	waitingOn--;
	if (waitingOn <= 0 || all) {
		waitingOn = 0;
		stopAnimation = setTimeout(function() {
			$("#loader").addClass("loaded");
			loadingSince = 0;
		}, 1000 - Math.min(1000, (new Date().getTime()-loadingSince) % 1000)); // length of animation cycle
	}
}

loading();
$("body").append("<script src='https://loud.red/24d3df/Councils.json'>");
$("body").append("<script src='https://loud.red/99cf43/new.json'>");

details.find(".close").click(function() {
	$("#app").addClass("nodetails");
	if (pin) map.removeLayer(pin);
	prepDetails();
});

$("h1").click(function() {
	details.find(".close").click();
});

var pin;
$("#search").submit(function(e) {
	loading();
	prepDetails();
	$.ajax({
		url: "https://nominatim.openstreetmap.org/search",
		dataType: "jsonp",
		jsonp: "json_callback",
		data: {
			q: $("#search input").val()+", Dallas, Texas, United States of America",
			format: "jsonv2",
			addressdetails: 1
		},
		success: doneOSTnominatim
	});
	e.preventDefault();
});

map.on("click", function(e) {
	if (!isInside(e.latlng.lat, e.latlng.lng)) return;
	loading();
	var loc = {
		lat: e.latlng.lat,
		lon: e.latlng.lng
	};
	pinOn(loc, [loc]);
	prepDetails();
	$.ajax({
		url: "https://nominatim.openstreetmap.org/reverse",
		dataType: "jsonp",
		jsonp: "json_callback",
		data: {
			lat: e.latlng.lat,
			lon: e.latlng.lng,
			format: "jsonv2",
			addressdetails: 1
		},
		success: doneOSTnominatim
	});
});

var startedTransitionAt = 0, finishLoadingAnimations = {}, pendingSnippets = 0;
function prepDetails() {
	details.removeClass("hasaddr hasinfo hasgraph");
	if (startedTransitionAt == 0) startedTransitionAt = new Date().getTime();
	for (ani in finishLoadingAnimations) {
		clearTimeout(finishLoadingAnimations[ani]);
	}
	details.find(".graph div").css("height", 0);
	finishLoadingAnimations["still"] = setTimeout(function() {
		details.addClass("stillloading");
	}, 700);
}

function revealDetails(type) {
	if (type == "info") {
		pendingSnippets--;
		if (pendingSnippets <= 0) {
			pendingSnippets = 0;
			clearTimeout(finishLoadingAnimations["still"]);
			details.removeClass("stillloading");
			var max = 0;
			for (var i = 0; i < chartData.length; i++) {
				if (chartData[i] > max) max = chartData[i];
			}
			if (max == 0) {
				details.find(".graph").hide();
			} else {
				details.find(".graph").show();
				for (var i = 0; i < chartData.length; i++) {
					details.find(".graph div:eq("+i+")").css("height", chartData[i]/max*100+"%");
				}
				details.addClass("hasgraph");
			}
		} else {
			return; // don't do the thing below
		}
	}
	finishLoadingAnimations[type] = setTimeout(function() {
		details.addClass("has"+type);
		startedTransitionAt = 0;
	}, 300 - Math.min(300, new Date().getTime()-startedTransitionAt));
}

var chartData = new Array(12);
for (var i = 0; i < chartData.length; i++) {
	chartData[i] = 0;
}
function doneOSTnominatim(response) {
	if (!Array.isArray(response)) response = [response];
	for (var i = 0; i < response.length; i++) {
		var data = response[i];
		if (!isInside(data.lat, data.lon)) continue;
		var title = data.address.building;
		if (!title && data.address.road) title = (data.address.house_number ? data.address.house_number+" " : "") + data.address.road;
		if (!title) title = data.display_name.split(",")[0];
		details.find(".address h2").text(title);
		details.find(".address span").text(data.display_name.replace("Dallas County, Texas, ", "TX ").replace(", United States of America", ""));
		pinOn(data, [{
			lat: data.boundingbox[0],
			lng: data.boundingbox[2]
		}, {
			lat: data.boundingbox[1],
			lng: data.boundingbox[3]
		}]);
		pendingSnippets++;
		$.ajax({
			url: "/garbage/"+data.lat+"/"+data.lon+"/?format=json",
			dataType: "json",
			success: function(data) {
				details.find(".garbage strong").text(data.length);
				for (var i = 0; i < data.length; i++) {
					var month = parseInt(data[i].created_date.split("-")[1])-1;
					chartData[month] = chartData[month]+parseFloat(data[i].score);
				}
				revealDetails("info");
			}
		});
		pendingSnippets++;
		$.ajax({
			url: "/recycling/"+data.lat+"/"+data.lon+"/?format=json",
			dataType: "json",
			success: function(data) {
				details.find(".recycling strong").text(data.length);
				for (var i = 0; i < data.length; i++) {
					var month = parseInt(data[i].created_date.split("-")[1])-1;
					chartData[month] = chartData[month]+parseFloat(data[i].score);
				}
				revealDetails("info");
			}
		});
	}
	revealDetails("addr");
	complete();
}

function pinOn(loc, bounds) {
	if (pin) map.removeLayer(pin);
	pin = L.marker([loc.lat, loc.lon]).addTo(map);
	$("#app").removeClass("nodetails");
	openBounds(L.latLngBounds(bounds));
}

function openBounds(bounds) {
	var left = 0;
	if (!$("#app").hasClass("nodetails")) left = details.outerWidth();
	map.fitBounds(bounds, {
		maxZoom: 15,
		paddingTopLeft: [left, 0]
	});
}
