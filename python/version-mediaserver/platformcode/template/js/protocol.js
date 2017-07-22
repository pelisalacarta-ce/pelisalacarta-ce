function get_response(data) {
    var response = JSON.parse(data)
    var data = response.data;

    switch (response.action) {
    case "connect":
        document.getElementById("version").innerHTML = data.version;
        document.getElementById("date").innerHTML = data.date;
        session_id = response.id;
        break;

    case "EndItems":
        var item_list = [];

        for (var item in data.itemlist) {
            context_items = [];
            item = data.itemlist[item];
            if (item.thumbnail && item.thumbnail.indexOf("http") != 0) {
                item.thumbnail = domain + "/local/" + encodeURIComponent(btoa(item.thumbnail));
            }
			else if (item.thumbnail & false){
				item.thumbnail = domain + "/proxy/" + encodeURIComponent(btoa(item.thumbnail));
			};
			if (item.fanart && item.fanart.indexOf("http") != 0) {
                item.fanart = domain + "/local/" + encodeURIComponent(btoa(item.fanart));
            }
			else if (item.fanart & false){
				item.fanart = domain + "/proxy/" + encodeURIComponent(btoa(item.fanart));
			};

            if (item.action == "go_back") {
                item.url = "go_back";
            };

            if (item.context.length ) {
                for (var x in item.context) {
                    html_item = replace_list(html.dialog.select.item, {
                        "item_action": "send_request('" + item.context[x].url + "')",
                        "item_title": item.context[x].title
                    });
                    context_items.push(html_item);
                }
                var menu_button = replace_list(html.itemlist.menu, {
                    "menu_items": btoa(context_items.join(""))
                });
                var menu_class = "item_with_menu";
            }
            else {
                var menu_button = "";
                var menu_class = "";
            };

            var replace_dict = {
                "item_class": menu_class,
                "item_url": item.url,
                "item_thumbnail": item.thumbnail,
                "item_fanart": item.fanart,
                "item_title": item.title,
                "item_plot": item.plot,
                "item_menu": menu_button,
				"menu_items": btoa(context_items.join(""))
            };

            if (html.itemlist[data.viewmode]) {
                var html_item = replace_list(html.itemlist[data.viewmode], replace_dict);
            }
            else {
                var html_item = replace_list(html.itemlist.movie, replace_dict);
            }
            item_list.push(html_item);

        };

        document.getElementById("itemlist").innerHTML = item_list.join("");
        set_category(data.category);
        document.getElementById("itemlist").children[0].children[0].focus();
        document.getElementById("itemlist").scrollTop = 0;
		show_images();

        nav_history.newResponse(item_list, data.category);

        //console.debug(nav_history)
        send_data({
            "id": response.id,
            "result": true
        });
        loading.close();
        break;

    case "Refresh":
        nav_history.current -= 1
        send_request(nav_history.states[nav_history.current].url);
        send_data({
            "id": response.id,
            "result": true
        });
        break;

    case "Alert":
        loading.close();
        dialog.ok(response.id, data);
        break;

	case "notification":
        dialog.notification(response.id, data);
        break;

    case "AlertYesNo":
        loading.close()
        dialog.yesno(response.id, data)
        break;

    case "ProgressBG":
        dialog.progress_bg(response.id, data);
        send_data({
            "id": response.id,
            "result": true
        });
        break;

    case "ProgressBGUpdate":
        dialog.progress_bg(response.id, data);
        break;

    case "ProgressBGClose":
        dialog.progress_bg_close();
        send_data({
            "id": response.id,
            "result": true
        });
        break;

    case "Progress":
        loading.close();
        dialog.progress(response.id, data);
        send_data({
            "id": response.id,
            "result": true
        });
        break;

    case "ProgressUpdate":
        dialog.progress_update(response.id, data);
        break;

    case "ProgressClose":
        dialog.progress_close();
        send_data({
            "id": response.id,
            "result": true
        });
        loading.close();
        break;

    case "ProgressIsCanceled":
        send_data({
            "id": response.id,
            "result": document.getElementById("window_progress").getElementById("canceled").checked != ""
        });
        break;

    case "isPlaying":
        send_data({
            "id": response.id,
            "result": document.getElementById("Player-popup").style.display == "block" || document.getElementById("Lista-popup").style.display == "block"
        });
        break;

    case "Keyboard":
        loading.close();
        dialog.keyboard(response.id, data);
        break;

	case "recaptcha":
        loading.close();
        dialog.recaptcha(response.id, data);
        break;
	
	case "recaptcha_select":
        loading.close();
        dialog.recaptcha_select(response.id, data);
        break

    case "List":
        loading.close();
        dialog.select(response.id, data);
        break;

    case "Play":
        send_data({
            "id": response.id,
            "result": true
        });
		
        loading.close();

        if (settings.player_mode == 0) {
            var lista = [];
            for (var player in players) {
                lista.push(replace_list(html.dialog.select.item, {
                    "item_title": players[player],
                    "item_action": "play_mode('" + data.video_url + "','" + data.title + "','" + player + "')"
                }));
            };
            dialog.menu("Elige el Reproductor", btoa(lista.join("")));

        }
        else {
            play_mode(data.video_url, data.title, Object.keys(players)[settings.player_mode - 1]);
        };
		
        break;
		
    case "Update":
        send_request(data.url);
        loading.close();
        break;
		
    case "HideLoading":
        loading.close();
        break;
	
	case "ShowLoading":
        loading.show();
        break;
		
    case "OpenInfo":
        loading.close();
        dialog.info(response.id, data);
        break;

	case "custom_button":
		dialog.custom_button(response.id, data);
		break;

    case "OpenConfig":
        loading.close();
        var itemlist = {};
        default_settings = {};
        settings_controls = [];

        for (var x in data.items) {

            if (!itemlist[data.items[x].category]) {
                itemlist[data.items[x].category] = [];
            };
            if (data.items[x].id) {
                default_settings[data.items[x].id] = data.items[x]["default"];
            }
            if (!data.items[x].color || data.items[x].color == "auto") {
                data.items[x].color = "#FFFFFF";
            };
			if (!data.items[x].enabled && data.items[x].enable) {
                data.items[x].enabled = data.items[x].enable;
            };

            settings_controls.push(data.items[x]);

            switch (data.items[x].type) {
            case "sep":
                itemlist[data.items[x].category].push(replace_list(html.config.sep, {}));
                break;

            case "lsep":
            case "label":
                itemlist[data.items[x].category].push(replace_list(html.config.label, {
                    "item_color": data.items[x].color,
                    "item_label": data.items[x].label
                }));
                break;

            case "number":
            case "text":
                if (data.items[x].hidden) {
                    var type = "password";
                }
                else {
                    var type = "text";
                };
				if (data.items[x].type == 'number') {
					keypress = "if ('0123456789'.indexOf(event.key) == -1 && event.charCode){return false}"
				}
				else {
					keypress = "";
				};
                itemlist[data.items[x].category].push(replace_list(html.config.text, {
                    "item_color": data.items[x].color,
                    "item_label": data.items[x].label,
                    "item_id": data.items[x].id,
                    "item_value": data.items[x].value,
                    "item_type": type,
					"keypress": keypress

                }));
                break;

            case "bool":
                if (data.items[x].value == "true" || data.items[x].value == true) {
                    var value = "checked='checked'";
                }
                else {
                    var value = "";
                };
                itemlist[data.items[x].category].push(replace_list(html.config.bool, {
                    "item_color": data.items[x].color,
                    "item_label": data.items[x].label,
                    "item_id": data.items[x].id,
                    "item_value": value
                }));
                break;

            case "labelenum":
                if (!data.items[x].values) {
                    var values = data.items[x].lvalues.split("|");
                }
                else {
                    var values = data.items[x].values.split("|");
                };

                var options = [];
                for (var y in values) {
                    if (data.items[x].value == values[y]) {
                        options.push("<option selected=selected>" + values[y] + "</option>");
                    }
                    else {
                        options.push("<option>" + values[y] + "</option>");
                    };
                };
                itemlist[data.items[x].category].push(replace_list(html.config.list, {
                    "item_type": "labelenum",
                    "item_color": data.items[x].color,
                    "item_label": data.items[x].label,
                    "item_id": data.items[x].id,
                    "item_values": options
                }));
                break;

            case "list":
                var options = [];
                for (var y in data.items[x].lvalues) {
                    if (data.items[x].value == y) {
                        options.push("<option selected=selected>" + data.items[x].lvalues[y] + "</option>");
                    }
                    else {
                        options.push("<option>" + data.items[x].lvalues[y] + "</option>");
                    };
                };

                itemlist[data.items[x].category].push(replace_list(html.config.list, {
                    "item_type": "enum",
                    "item_color": data.items[x].color,
                    "item_label": data.items[x].label,
                    "item_id": data.items[x].id,
                    "item_values": options
                }));
                break;

            case "enum":
                if (!data.items[x].values) {
                    var values = data.items[x].lvalues.split("|");
                }
                else {
                    var values = data.items[x].values.split("|");
                };

                var options = [];
                for (var y in values) {
                    if (data.items[x].value == y) {
                        options.push("<option selected=selected>" + values[y] + "</option>");
                    }
                    else {
                        options.push("<option>" + values[y] + "</option>");
                    };
                };

                itemlist[data.items[x].category].push(replace_list(html.config.list, {
                    "item_type": "enum",
                    "item_color": data.items[x].color,
                    "item_label": data.items[x].label,
                    "item_id": data.items[x].id,
                    "item_values": options
                }));
                break;
				
            default:
                break;
            };

        };
		
        var categories = [];
        var category_list = [];

        for (var category in itemlist) {
            if (Object.keys(itemlist).length > 1 || category != "undefined") {
                categories.push(replace_list(html.config.category, {
                    "item_label": category,
                    "item_category": category
                }));
            };
            category_list.push(replace_list(html.config.container, {
                "item_id": "category_" + category,
                "item_value": itemlist[category].join("")
            }));

        };
        dialog.config(response.id, data, categories.join(""), category_list.join(""));
        evaluate_controls();
        break;

    default:
        break;
    };
};

function custom_button(data) {
    if (data == null) {
        var controls = document.getElementById("window_settings").getControls();

        for (var x in controls) {
            switch (controls[x].type) {
            case "text":
                controls[x].value = default_settings[controls[x].id];
                break;
            case "password":
                controls[x].value = default_settings[controls[x].id];
                break;
            case "checkbox":
                value = default_settings[controls[x].id];
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
                    controls[x].selectedIndex = default_settings[controls[x].id];
                }
                else if (controls[x].name == "labelenum") {
                    controls[x].value = default_settings[controls[x].id];
                };
                break;
            };
			controls[x].onchange()
        };
    }
    else {
        send_data({
            "id": document.getElementById("window_settings").RequestID,
            "result": "custom_button"
        });
        if (data["close"] == true) {
            dialog.closeall();
        };
    };
};

function info_window(comando) {
    send_data({
        "id": document.getElementById("window_info").RequestID,
        "result": comando
    });
};

function save_config(Guardar) {
    if (Guardar === true) {
        var JsonAjustes = {};
        var controls = document.getElementById("window_settings").getControls();

        for (var x in controls) {
            switch (controls[x].type) {
            case "text":
                JsonAjustes[controls[x].id] = controls[x].value;
                break;
            case "password":
                JsonAjustes[controls[x].id] = controls[x].value;
                break;
            case "checkbox":
                JsonAjustes[controls[x].id] = controls[x].checked.toString();
                break;
            case "select-one":
                if (controls[x].name == "enum") {
                    JsonAjustes[controls[x].id] = controls[x].selectedIndex.toString();
                }
                else if (controls[x].name == "labelenum") {
                    JsonAjustes[controls[x].id] = controls[x].value;
                }
                break;
            }
        }
        send_data({
            "id": document.getElementById("window_settings").RequestID,
            "result": JsonAjustes
        });
    }
    else {
        send_data({
            "id": document.getElementById("window_settings").RequestID,
            "result": false
        });
    };

    loading.show();
};

function evaluate_controls(control_changed) {
    if (typeof control_changed != "undefined") {
        for (var x in settings_controls) {
            if (settings_controls[x].id == control_changed.id) {
                switch (control_changed.type) {
                case "text":
                    settings_controls[x].value = control_changed.value;
                    break;
                case "password":
                    settings_controls[x].value = control_changed.value;
                    break;
                case "checkbox":
                    settings_controls[x].value = control_changed.checked;
                    break;
                case "select-one":
                    if (control_changed.name == "enum") {
                        settings_controls[x].value = control_changed.selectedIndex;
                    }
                    else if (control_changed.name == "labelenum") {
                        settings_controls[x].value = control_changed.value;
                    };
                    break;
                };
                break;
            };
        };
    };

    for (var index in settings_controls) {
        control = get_control_group(index);
        set_visible(document.getElementById("window_settings").getElementById("controls_container").children[control[0]].children[control[1]], evaluate(index, settings_controls[index].visible));
        set_enabled(document.getElementById("window_settings").getElementById("controls_container").children[control[0]].children[control[1]], evaluate(index, settings_controls[index].enabled));
    };
};

function set_visible(element, visible) {
    if (visible) {
        element.style.display = "block";
    }
    else {
        element.style.display = "none";
    };
};

function set_enabled(element, enabled) {
    if (element.children[0].className == "control") {
        element.children[0].children[1].disabled = !enabled;
    };
};

function get_control_group(index) {
    var group = 0;
    var pos = 0;
    var children = document.getElementById("window_settings").getElementById("controls_container").children;
    for (child in children) {
        if (pos + children[child].children.length <= index) {
            group ++;
            pos += children[child].children.length;
        }
        else {
            break;
        };
    };
    return [group, index - pos];
};

function evaluate(index, condition) {
    index = parseInt(index);

    if (typeof condition == "undefined") {
        return true;
    };
    if (typeof condition == "boolean") {
        return condition;
    };

    if (condition.toLocaleLowerCase() == "true") {
        return true;
    }
    else if (condition.toLocaleLowerCase() == "false") {
        return false;
    };

    const regex = /(!?eq|!?gt|!?lt)?\(([^,]+),[\"|']?([^)|'|\"]*)['|\"]?\)[ ]*([+||])?/g;

    while ((m = regex.exec(condition)) !== null) {
        // This is necessary to avoid infinite loops with zero-width matches
        if (m.index === regex.lastIndex) {
            regex.lastIndex++;
        };

        var operator = m[1];
        var id = parseInt(m[2]);
        var value = m[3];
        var next = m[4];

        if (isNaN(id)) {
            return false;
        };

        if (index + id < 0 || index + id >= settings_controls.length) {
            return false;
        }
        else {
            if (settings_controls[index + id].type == "list" || settings_controls[index + id].type == "enum") {
				if (settings_controls[index + id].lvalues){
					control_value = settings_controls[index + id].lvalues[settings_controls[index + id].value];
				}
				else {
					control_value = settings_controls[index + id].values[settings_controls[index + id].value];
				};
            }
            else {
                control_value = settings_controls[index + id].value;
            };
        };

        if (["lt", "!lt", "gt", "!gt"].indexOf(operator) > -1) {
            value = parseInt(value);
            if (isNaN(value)) {
                return false;
            };
        };

        if (["eq", "!eq"].indexOf(operator) > -1) {
			if (typeof(value) == "string") {
				if (!isNaN(parseInt(value))) {
					value = parseInt(value);
				}
				else if (value.toLocaleLowerCase() == "true") {
					value = true;
				}
				else if (value.toLocaleLowerCase() == "false") {
					value = false;
				};
			};
        };

        if (operator == "eq") {
            ok = (control_value == value);
        };
        if (operator == "!eq") {
            ok = !(control_value == value);
        };
        if (operator == "gt") {
            ok = (control_value > value);
        };
        if (operator == "!gt") {
            ok = !(control_value > value);
        };
        if (operator == "lt") {
            ok = (control_value < value);
        };
        if (operator == "!lt") {
            ok = !(control_value < value);
        };

        if (next == "|" && ok == true) {
            break;
        };
        if (next == "+" && ok == false) {
            break;
        };
    };
    return ok;
};