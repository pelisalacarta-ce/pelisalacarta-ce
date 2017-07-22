loading.close = function () {
    var el = document.getElementById("window_loading");
    if (el.style.display == "block") {
        el.style.display = "none";
        document.getElementById("window_overlay").style.display = "none";
        if (focused_item) {
            focused_item.focus();
        }
        else if (document.getElementById("itemlist").children.length) {
            document.getElementById("itemlist").children[0].children[0].focus();
        };
    };
};

loading.show = function (message) {
    if (!message) {
        message = "Cargando...";
    };
    var el = document.getElementById("window_loading");
    el.getElementById("loading_message").innerHTML = message;
    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";
    el.getElementById("loading_message").focus();
    center_window(el);
};

dialog.closeall = function () {
    document.getElementById('window_overlay').style.display = 'none';
    document.getElementById("window_loading").style.display = "none";
    document.getElementById("window_select").style.display = "none";
    document.getElementById("window_settings").style.display = "none";
    document.getElementById("window_settings").style.display = "none";
    document.getElementById("window_player").style.display = "none";
    document.getElementById("window_player").getElementById("media_content").innerHTML = '';
    document.getElementById("window_ok").style.display = "none";
    document.getElementById("window_yesno").style.display = "none";
    document.getElementById("window_input").style.display = "none";
	document.getElementById("window_recaptcha").style.display = "none";
    document.getElementById("window_progress").style.display = "none";
    document.getElementById("window_info").style.display = "none";
    if (focused_item) {
        focused_item.focus();
    }
    else if (document.getElementById("itemlist").children.length) {
        document.getElementById("itemlist").children[0].children[0].focus();
    };
};

dialog.menu = function (title, list) {
    dialog.closeall();
    if (list) {
        var el = document.getElementById("window_select")
        el.getElementById("window_heading").innerHTML = title;
        el.getElementById("control_list").innerHTML = atob(list);
        el.style.display = "block";
        document.getElementById("window_overlay").style.display = "block";
        el.getElementById("control_list").children[0].children[0].focus();
        center_window(el);
    };
};

dialog.select = function (id, data) {
    dialog.closeall();
    var el = document.getElementById("window_select");

    el.getElementById("window_heading").innerHTML = data.title;
    el.RequestID = id;
    var lista = [];
    for (var x in data.list) {
        lista.push(replace_list(html.dialog.select.item, {
            "item_title": data.list[x],
            "item_action": "send_data({'id':'" + id + "', 'result':" + x + "})"
        }));
    };
    el.getElementById("control_list").innerHTML = lista.join("");
    el.style.display = "block";
    document.getElementById("window_overlay").style.display = "block";

    el.getElementById("control_list").children[0].children[0].focus();
    center_window(el);
};

dialog.player = function (title, player) {
    dialog.closeall();
    var el = document.getElementById("window_player");
    el.getElementById("window_heading").innerHTML = title;
    el.getElementById("media_content").innerHTML = player;
    el.style.display = "block";
    document.getElementById("window_overlay").style.display = "block";
    el.children[0].focus();
    center_window(el);
};

dialog.ok = function (id, data) {
    dialog.closeall();
    var el = document.getElementById("window_ok");
    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";
    el.RequestID = id;
    el.getElementById("window_message").innerHTML = data.text.replace(new RegExp("\n", 'g'), "<br/>");
    el.getElementById("window_heading").innerHTML = data.title;
    el.getElementById("window_footer").children[0].focus();
    center_window(el);
};

dialog.yesno = function (id, data) {
    dialog.closeall();
    var el = document.getElementById("window_yesno");
    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";
    el.RequestID = id;
    el.getElementById("window_message").innerHTML = data.text.replace(new RegExp("\n", 'g'), "<br/>");
    el.getElementById("window_heading").innerHTML = data.title;
    el.getElementById("window_footer").children[0].focus();
    center_window(el);
};

dialog.notification = function (id, data) {
    var el = document.getElementById("window_notification");
    el.style.display = "block";
	if (!data.icon){data.icon = 0}
	el.getElementById("window_heading").innerHTML = data.title;
	el.getElementById("window_message").innerHTML = data.text;
	el.getElementById("window_icon").className = "window_icon" + data.icon;

	
	
	auto_scroll(el.getElementById("window_message"))
	setTimeout(function(){ el.style.display = "none"; }, data.time);
};

dialog.keyboard = function (id, data) {
    dialog.closeall();
    var el = document.getElementById("window_input");

    if (data.title === "") {
        data.title = "Teclado";
    };
    if (data.password == true) {
        el.getElementById("window_value").type = "password";
    }
    else {
        el.getElementById("window_value").type = "text";
    };

    el.RequestID = id;
    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";
    el.getElementById("window_value").value = data.text;
    el.getElementById("window_heading").innerHTML = data.title;
    el.getElementById("window_value").focus();
    center_window(el);
};

dialog.recaptcha = function (id, data) {
    dialog.closeall();
    var el = document.getElementById("window_recaptcha");

    if (data.title === "") {
        data.title = "Introduce el texto de la imagen";
    };

    el.RequestID = id;
    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";
	el.getElementById("window_image").style.backgroundImage = "url(" + data.image + ")";
    el.getElementById("window_heading").innerHTML = data.title;
	el.getElementById("window_message").innerHTML = data.message;

	for (var x in [0,1,2,3,4,5,6,7,8]) {
		el.getElementById("window_image").children[x].className = "";
	}
	el.getElementById("window_footer").children[0].focus();
    center_window(el);
};

dialog.recaptcha_select = function (id, data) {
    var el = document.getElementById("window_recaptcha");
	console.log(data.selected)
	console.log(data.unselected)
	for (var x in data.selected) {
		el.getElementById("window_image").children[data.selected[x]].className = "selected";
	}
	for (var x in data.unselected) {
		el.getElementById("window_image").children[data.unselected[x]].className = "";
	}
  
};

dialog.progress_bg = function (id, data) {
    var el = document.getElementById("window_background_progress");
    el.style.display = "block";
    el.RequestID = id;
    el.getElementById("window_message").innerHTML = data.text.replace(new RegExp("\n", 'g'), "<br/>");
    el.getElementById("window_heading").innerHTML = data.title;
    el.getElementById("progressbar").style.width = data.percent + "%";
};

dialog.progress_bg_close = function () {
    document.getElementById("window_background_progress").style.display = "none";
};

dialog.progress = function (id, data) {
    var el = document.getElementById("window_progress");
    if (id != el.RequestID) {
        dialog.closeall();
    };
    el.RequestID = id;
    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";
    el.getElementById("window_message").innerHTML = data.text.replace(new RegExp("\n", 'g'), "<br/>");
    el.getElementById("window_heading").innerHTML = data.title;
    el.getElementById("canceled").checked = "";
    el.getElementById("progress").style.width = data.percent + "%";
    el.getElementById("window_footer").children[0].focus;
    center_window(el);
};

dialog.progress_update = function (id, data) {
    var el = document.getElementById("window_progress");
    el.getElementById("window_message").innerHTML = data.text.replace(new RegExp("\n", 'g'), "<br/>");
    if (el.getElementById("canceled").checked != "") {
        el.getElementById("window_heading").innerHTML = data.title + " " + data.percent + "% - Cancelando...";
    }
    else {
        el.getElementById("window_heading").innerHTML = data.title + " " + data.percent + "%";
    };
    el.getElementById("progress").style.width = data.percent + "%";
};

dialog.progress_close = function () {
    dialog.closeall();
};

dialog.custom_button = function(id, data) {
    var el = document.getElementById("window_settings");
	el.RequestID = id;
	if (data.return_value.label){
		el.getElementById("custom_button").innerHTML = data.return_value.label
	};
	var controls = document.getElementById("window_settings").getControls();
	for (var x in controls) {
		switch (controls[x].type) {
		case "text":
			controls[x].value = data.values[controls[x].id];
			break;
		case "password":
			controls[x].value = data.values[controls[x].id];
			break;
		case "checkbox":
			value = data.values[controls[x].id];
			if (value == true) {
				value = "checked";
			}
			else {
				value = "";
			};
			controls[x].checked = value;
			break;
		case "select-one":
			if (controls[x].name == "enum") {
				controls[x].selectedIndex = data.values[controls[x].id];
			}
			else if (controls[x].name == "labelenum") {
				controls[x].value = data.values[controls[x].id];
			};
			break;
		};
		controls[x].onchange()
	};
};

dialog.config = function (id, data, Secciones, Lista) {
    dialog.closeall();
    var el = document.getElementById("window_settings");

    el.RequestID = id;
    el.getElementById("controls_container").innerHTML = Lista;
    el.getElementById("window_heading").innerHTML = data.title;
    if (data.custom_button != null) {
		if  (!data.custom_button.visible) {
			el.getElementById("custom_button").style.display = "none" 
		}
		else {
			el.getElementById("custom_button").style.display = "inline";
			el.getElementById("custom_button").innerHTML = data.custom_button.label;
			el.getElementById("custom_button").onclick = function () {
				custom_button(data.custom_button);
			};
		};
    }
    else {
		el.getElementById("custom_button").style.display = "inline";
        el.getElementById("custom_button").innerHTML = "Por defecto";
        el.getElementById("custom_button").onclick = function () {
            custom_button(null);
        };
    };

    if (Secciones != "") {
        el.getElementById("category_container").innerHTML = Secciones;
        el.getElementById("category_container").style.display = "block";
        el.getElementById("category_General").style.display = "block";

    }
    else {
        el.getElementById("category_container").style.display = "none";
        el.getElementById("category_undefined").style.display = "block";

    };

    el.getElementById("window_footer").style.display = "block";
    el.getElementById("window_footer_local").style.display = "none";
    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";
    if (Secciones != "") {
        el.getElementById("category_container").children[0].focus();
        el.getElementById("category_General").scrollTop = 0;
    }
    else {
        el.getElementById("window_footer").children[0].focus();
        el.getElementById("category_undefined").scrollTop = 0;
    };
    center_window(el);
};

dialog.settings = function () {
    dialog.closeall();
    var el = document.getElementById("window_settings");
    el.getElementById("window_heading").innerHTML = "Ajustes";
    var controls = [];

	controls.push(replace_list(html.config.label, {
        "item_color": "#FFFFFF",
        "item_label": "Navegación:"
    }));

	if (settings.builtin_history) {
        var value = "checked=checked";
    }
    else {
        var value = "";
    };

    controls.push(replace_list(html.config.bool, {
        "item_color": "#FFFFFF",
        "item_label": "Usar navegación del explorador",
        "item_id": "builtin_history",
        "item_value": value
    }));
	
    controls.push(replace_list(html.config.label, {
        "item_color": "#FFFFFF",
        "item_label": "Visualización:"
    }));

    if (settings.show_fanart) {
        var value = "checked=checked";
    }
    else {
        var value = "";
    };

    controls.push(replace_list(html.config.bool, {
        "item_color": "#FFFFFF",
        "item_label": "Mostrar Fanarts",
        "item_id": "show_fanart",
        "item_value": value
    }));

    controls.push(replace_list(html.config.label, {
        "item_color": "#FFFFFF",
        "item_label": "Reproducción:"
    }));

    var options = ["<option>Preguntar</option>", "<option>Indirecto</option>", "<option>Directo</option>"];
    options[settings.play_mode] = options[settings.play_mode].replace("<option>", "<option selected=selected>");
    controls.push(replace_list(html.config.list, {
        "item_type": "enum",
        "item_color": "#FFFFFF",
        "item_label": "Método de reproduccion:",
        "item_id": "play_mode",
        "item_values": options.join("")
    }));

    options = ["<option>Preguntar</option>"];
    for (var player in players) {
        options.push("<option>" + players[player] + "</option>");
    };
    options[settings.player_mode] = options[settings.player_mode].replace("<option>", "<option selected=selected>");
    controls.push(replace_list(html.config.list, {
        "item_type": "enum",
        "item_color": "#FFFFFF",
        "item_label": "Reproductor:",
        "item_id": "player_mode",
        "item_values": options.join("")
    }));

    el.getElementById("controls_container").innerHTML = replace_list(html.config.container, {
        "item_id": "category_all",
        "item_value": controls.join("").replace(/evaluate_controls\(this\)/g, '')
    });
    el.getElementById("category_container").style.display = "none";
    el.getElementById("category_all").style.display = "block";
    el.getElementById("window_footer").style.display = "none";
    el.getElementById("window_footer_local").style.display = "block";
    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";
    el.children[0].focus();
    center_window(el);
};

dialog.info = function (id, data) {
    dialog.closeall();
    var el = document.getElementById("window_info");

    el.RequestID = id;
    el.getElementById("window_heading").innerHTML = data.title;
    el.getElementById("info_fanart").src = data.fanart;
    el.getElementById("info_poster").src = data.thumbnail;

    if (data.buttons) {
        el.getElementById("window_footer").style.display = "block";
        el.getElementById("page_info").innerHTML = data.count;

        if (data.previous) {
            el.getElementById("previous").onclick = function () {
                info_window('previous');
            };
            el.getElementById("previous").className = "control_button";
			el.getElementById("previous").disabled = false;
        }
        else {
            el.getElementById("previous").onclick = "";
            el.getElementById("previous").className = "control_button disabled";
			el.getElementById("previous").disabled = true;
        };

        if (data.next) {
            el.getElementById("next").onclick = function () {
                info_window('next');
            };
            el.getElementById("next").className = "control_button";
			el.getElementById("next").disabled = false;
        }
        else {
            el.getElementById("next").onclick = "";
            el.getElementById("next").className = "control_button disabled";
			el.getElementById("next").disabled = true;
        };
    }
    else {
        el.getElementById("window_footer").style.display = "none";
    };

    el.getElementById("line1_head").innerHTML = data["lines"][0]["title"];
    el.getElementById("line2_head").innerHTML = data["lines"][1]["title"];
    el.getElementById("line3_head").innerHTML = data["lines"][2]["title"];
    el.getElementById("line4_head").innerHTML = data["lines"][3]["title"];
    el.getElementById("line5_head").innerHTML = data["lines"][4]["title"];
    el.getElementById("line6_head").innerHTML = data["lines"][5]["title"];
    el.getElementById("line7_head").innerHTML = data["lines"][6]["title"];
    el.getElementById("line8_head").innerHTML = data["lines"][7]["title"];

    el.getElementById("line1").innerHTML = data["lines"][0]["text"];
    el.getElementById("line2").innerHTML = data["lines"][1]["text"];
    el.getElementById("line3").innerHTML = data["lines"][2]["text"];
    el.getElementById("line4").innerHTML = data["lines"][3]["text"];
    el.getElementById("line5").innerHTML = data["lines"][4]["text"];
    el.getElementById("line6").innerHTML = data["lines"][5]["text"];
    el.getElementById("line7").innerHTML = data["lines"][6]["text"];
    el.getElementById("line8").innerHTML = data["lines"][7]["text"];

    if (el.style.display == "block") {
        update = true;
    }
    else {
        update = false;
    };

    document.getElementById("window_overlay").style.display = "block";
    el.style.display = "block";

    auto_scroll(el.getElementById("line1"));
    auto_scroll(el.getElementById("line2"));
    auto_scroll(el.getElementById("line3"));
    auto_scroll(el.getElementById("line4"));
    auto_scroll(el.getElementById("line5"));
    auto_scroll(el.getElementById("line6"));
    auto_scroll(el.getElementById("line7"));
    auto_scroll(el.getElementById("line8"));

    if (data["buttons"]) {
        if (!update) {
            el.getElementById("window_footer").children[3].focus();
        };
    }
    else {
        el.children[0].focus();
    };

    center_window(el);
};