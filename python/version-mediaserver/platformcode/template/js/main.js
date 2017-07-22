HTMLElement.prototype.getElementById = function(id) {
    if (this.querySelector("#" + id)) {
        return this.querySelector("#" + id);
    };

    for (var x = 0; x < this.children.length; x++) {
        if (this.children[x].id == id) {
            return this.children[x];
        };
    };

    for (var x = 0; x < this.children.length; x++) {
        result = this.children[x].getElementById(id);
        if (result != null) {
            return result;
        };
    };
    return null;
};

HTMLElement.prototype.getControls = function() {
    return [].concat(Array.prototype.slice.call(this.getElementsByTagName("input")), Array.prototype.slice.call(this.getElementsByTagName("select")));
};

window.onload = function() {
    var url = (window.location.href.split("#")[1] ? window.location.href.split("#")[1] : "");
    dispose();
    loading.show("Cargando pagina...");
    ajax_running.remove = function(val) {
        if (this.indexOf(val) > -1) {
            this.splice(this.indexOf(val), 1);
        };
        if (!this.length && !websocket) {
            send_request(url);
        };
    };
    load_settings();
    dowload_files();
};

window.onpopstate = function(e) {
    if (e.state) {
        nav_history.go(e.state - nav_history.current);
    };
};

window.onresize = function() {
    dispose();
};

window.getCookie = function(name) {
    var match = document.cookie.match(new RegExp(name + '=([^;]+)'));
    if (match) return match[1];
};

function load_settings() {
    settings["play_mode"] = (window.getCookie("play_mode") ? parseInt(window.getCookie("play_mode")) : 0);
    settings["player_mode"] = (window.getCookie("player_mode") ? parseInt(window.getCookie("player_mode")) : 0);
    settings["show_fanart"] = (window.getCookie("show_fanart") == "false" ? false : true);
	settings["builtin_history"] = (window.getCookie("builtin_history") == "true" ? true : false);
};

function save_settings() {
    var controls = document.getElementById("window_settings").getControls();
    for (var x in controls) {
        switch (controls[x].type) {
            case "text":
            case "password":
                save_setting(controls[x].id, controls[x].value);
                break;
            case "checkbox":
                save_setting(controls[x].id, controls[x].checked);
                break;
            case "select-one":
                save_setting(controls[x].id, controls[x].selectedIndex);
                break;
        };
    };
    load_settings();
};

function save_setting(id, value) {
    document.cookie = id + "=" + value + '; expires=Fri, 31 Dec 9999 23:59:59 GMT';
};

function dowload_files() {
    ajax_to_dict("/media/html/player_vlc.html", html, "vlc_player");
    ajax_to_dict("/media/html/player_html.html", html, "html_player");
    ajax_to_dict("/media/html/player_flash.html", html, "flash_player");

    ajax_to_dict("/media/html/itemlist_banner.html", html, "itemlist.banner");
    ajax_to_dict("/media/html/itemlist_channel.html", html, "itemlist.channel");
    ajax_to_dict("/media/html/itemlist_movie.html", html, "itemlist.movie");
    ajax_to_dict("/media/html/itemlist_list.html", html, "itemlist.list");
    ajax_to_dict("/media/html/itemlist_menu.html", html, "itemlist.menu");

    ajax_to_dict("/media/html/select_item.html", html, "dialog.select.item");

    ajax_to_dict("/media/html/config_label.html", html, "config.label");
    ajax_to_dict("/media/html/config_sep.html", html, "config.sep");
    ajax_to_dict("/media/html/config_text.html", html, "config.text");
    ajax_to_dict("/media/html/config_bool.html", html, "config.bool");
    ajax_to_dict("/media/html/config_list.html", html, "config.list");

    ajax_to_dict("/media/html/config_category.html", html, "config.category");
    ajax_to_dict("/media/html/config_container.html", html, "config.container");
};