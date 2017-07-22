function dispose() {
    var height = document.getElementById("window").offsetHeight;
    var header = document.getElementById("header").offsetHeight;
    var footer = document.getElementById("footer").offsetHeight;
    var panelheight = height - header - footer;
    document.getElementById('content').style.height = panelheight + "px";
	if (document.getElementById("window").offsetWidth < 800) {
		document.getElementById('panel_items').className = "panel_items_vertical";
		document.getElementById('panel_info').className = "panel_info_vertical";
	}
	else {
		document.getElementById('panel_items').className = "panel_items";
		document.getElementById('panel_info').className = "panel_info";
	}
};

function replace_list(data, list) {
    for (var key in list) {
        var re = new RegExp("%" + key, "g");
        data = data.replace(re, list[key]);
    };
    return data;
};

function play_mode(url, title, player) {
    if (!new RegExp("^(.+://)").test(url)) {
        url = domain + "/local/" + encodeURIComponent(btoa(Utf8.encode(data.video_url))) + "/video.mp4";
    }
	else {
		var indirect_url = domain + "/proxy/" + encodeURIComponent(btoa(Utf8.encode(url))) + "/video.mp4";
	};

    if (settings.play_mode == 0 && indirect_url) {
        var lista = [];
        lista.push(replace_list(html.dialog.select.item, {
            "item_title": "Indirecto",
            "item_action": player + "('" + indirect_url + "','" + title + "')"
        }));
        lista.push(replace_list(html.dialog.select.item, {
            "item_title": "Directo",
            "item_action": player + "('" + url + "','" + title + "')"
        }));
        dialog.menu("Metodo de reproducción", btoa(lista.join("")));
    }
    else if (settings.play_mode == 1 && indirect_url) {
        eval(player)(indirect_url, title);
    }
    else {
        eval(player)(url, title);
    };
};

function play(url, title) {
    window.open(url);
}

function vlc_play(url, title) {
    var html_code = replace_list(html.vlc_player, {
        "video_url": url
    });
    dialog.player(title, html_code);
}

function flash_play(url, title) {
    var html_code = replace_list(html.flash_player, {
        "video_url": url
    });
    dialog.player(title, html_code);
}

function html_play(url, title) {
    var html_code = replace_list(html.html_player, {
        "video_url": url
    });
    dialog.player(title, html_code);
}

function set_category(category) {
    var el = document.getElementById("header");
    if (category) {
        el.getElementById("heading").innerHTML = "pelisalacarta / " + category;
        document.title = "pelisalacarta / " + category;
    }
    else {
        el.getElementById("heading").innerHTML = "pelisalacarta";
        document.title = "pelisalacarta";
    };
};

function focus_element(element) {
    element.focus()
};

function image_error(thumbnail) {
    var src = thumbnail.src;
    if (thumbnail.src.indexOf(domain) == 0) {
        thumbnail.src = "https://raw.githubusercontent.com/pelisalacarta-ce/media/master/pelisalacarta/thumb_folder.png";
    }
	else {
		thumbnail.src = domain + "/proxy/" + encodeURIComponent(btoa(thumbnail.src));
	}
	if (thumbnail.parentNode == document.activeElement && document.activeElement.className != "item_menu"){
		document.activeElement.onfocus();
	};
};

function show_images(){
	var container = document.getElementById("itemlist");
    var images = container.getElementsByTagName("img");
	var item_height =  images[0].parentNode.parentNode.offsetHeight;

	var first = Math.floor(container.scrollTop / item_height);
	var count = Math.ceil(container.offsetHeight / item_height + (container.scrollTop / item_height - first));
	
	for (var x = first; x < first + count; x++){
		var image = images[x]
		if (image && !image.src){
			image.src = image.parentNode.getElementsByClassName("thumbnail")[1].innerHTML;
			if (image.parentNode == document.activeElement){
				document.activeElement.onfocus();
			}; 
		};
	};
};

function load_info(item, viewmode) {
    var thumbnail = item.getElementsByClassName("thumbnail")[0];
    var fanart = item.getElementsByClassName("fanart")[0];
    var title = item.getElementsByClassName("label")[0];
    var plot = item.getElementsByClassName("plot")[0];
    var el = document.getElementById("media_info");

    el.getElementById("media_poster").src = thumbnail.src;
    el.getElementById("media_plot").innerHTML = plot.innerHTML.replace(/\n/g, "<br>");
    el.getElementById("media_title").innerHTML = title.innerHTML;

    if (fanart.innerHTML && settings.show_fanart) {
        document.getElementById("content").style.backgroundImage = "linear-gradient(rgba(255,255,255,0.5),rgba(255,255,255,0.5)), url(" + fanart.innerHTML + ")";
        document.getElementById("content").children[0].style.opacity = ".9";
        document.getElementById("content").children[1].style.opacity = ".9";
    }
    else {
        document.getElementById("content").style.backgroundImage = "";
        document.getElementById("content").children[0].style.opacity = "";
        document.getElementById("content").children[1].style.opacity = "";
    };

    if (viewmode == "list") {
        el.getElementById("media_poster").style.display = "block";
        el.getElementById("media_plot").style.display = "block";
        el.getElementById("media_title").style.display = "none";
        document.getElementById("version_info").style.display = "none";
    }
    else if (viewmode == "banner" || viewmode == "channel") {
        el.getElementById("media_poster").style.display = "none";
        el.getElementById("media_plot").style.display = "none";
        el.getElementById("media_title").style.display = "none";
        document.getElementById("version_info").style.display = "block";
    }
    else {
        el.getElementById("media_poster").style.display = "block";
        el.getElementById("media_plot").style.display = "block";
        el.getElementById("media_title").style.display = "block";
        document.getElementById("version_info").style.display = "none";
    }
    auto_scroll(el.getElementById("media_plot"));
};

function unload_info(obj) {
    var el = document.getElementById('media_info');
    document.getElementById("version_info").style.display = "block";
    el.getElementById("media_poster").style.display = "none";
    el.getElementById("media_plot").style.display = "none";
    el.getElementById("media_title").style.display = "none";
	el.getElementById("media_poster").src = "";
    el.getElementById("media_plot").innerHTML = "";
    el.getElementById("media_title").innerHTML = "";
    document.getElementById("content").style.backgroundImage = ""
    document.getElementById("content").children[0].style.opacity = "";
    document.getElementById("content").children[1].style.opacity = "";
};

function change_category(category) {
    var el = document.getElementById('window_settings');
    el.getElementById("controls_container").scrollTop = 0;
    categories = el.getElementById("controls_container").getElementsByTagName("ul");
    for (var x in categories) {
        if (categories[x].id == "category_" + category) {
            categories[x].style.display = "block";
        }
        else if (categories[x].style) {
            categories[x].style.display = "none";
        };
    };
};

function auto_scroll(element) {
    clearInterval(element.interval);
    element.scrollLeft = 0;
    element.scrollTop = 0;
    if (element.scrollWidth > element.offsetWidth) {
        initialscrollWidth = element.scrollWidth;
        element.innerHTML = element.innerHTML + " | " + element.innerHTML;
        element.interval = setInterval(function () {
            element.scrollLeft += 1;
            if (element.scrollLeft - 1 >= element.scrollWidth - initialscrollWidth) {
                element.scrollLeft = 0;
            };
        }, 80);
    };
    if (element.scrollHeight > element.offsetHeight) {
        initialscrollHeight = element.scrollHeight;
        element.innerHTML = element.innerHTML + "</br>" + element.innerHTML;
        element.interval = setInterval(function () {
            element.scrollTop += 1;
            if (element.scrollTop >= element.scrollHeight - initialscrollHeight) {
                element.scrollTop = 0;
            };
        }, 80);
    };
};

function center_window(el) {
    el.style.top = document.getElementById("window").offsetHeight / 2 - el.offsetHeight / 2 + "px";
};