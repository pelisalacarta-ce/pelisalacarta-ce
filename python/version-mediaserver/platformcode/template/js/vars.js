var domain = window.location.href.split("/").slice(0, 3).join("/");
var focused_item = null;
var websocket = null;
var session_id = null;
var default_settings = {};
var settings_controls = [];
var connection_retry = true;
var settings = {};
var loading = {};
var dialog = {};
var ajax_running = [];
var keychar = {
    "keyCode": 0,
    "Time": 0,
    "Char": ""
};
var html = {
    "dialog": {
        "select": {}
    },
    "config": {},
    "itemlist": {}
};
var players = {
    "play": "Abrir enlace",
    "vlc_play": "Plugin VLC",
    "flash_play": "Reproductor Flash",
    "html_play": "Video HTML"
};
var nav_history = {
    "newRequest": function (url) {
        if (this.confirmed) {
            if (this.states[this.current].url == url) {
                this.states[this.current].url;
                this.states[this.current].start;
            }
            else {
                this.states[this.current].scroll = document.getElementById("itemlist").scrollTop;
                this.states[this.current].focus = Array.prototype.indexOf.call(document.getElementById("itemlist").children, focused_item.parentNode);
                this.current += 1;
                this.states.splice(this.current, 0, {
                    "start": new Date().getTime(),
                    "url": url
                });
                this.confirmed = false;
            }
        }
        else {
            if (this.current == -1) {
                this.current = 0;
                this.states.push({
                    "start": new Date().getTime(),
                    "url": url
                });
            }
            else {
                this.states[this.current].start = new Date().getTime();
                this.states[this.current].url = url;
            }
        }
    },
    "newResponse": function (data, category) {
        if (!this.confirmed) {
			if (this.states[this.current].focus >= 0) {
                document.getElementById("itemlist").children[this.states[this.current].focus].children[0].focus();
                document.getElementById("itemlist").scrollTop = this.states[this.current].scroll;
            }
            this.states[this.current].end = new Date().getTime();
            this.states[this.current].data = data;
            this.states[this.current].category = category;
            this.confirmed = true;
            if (settings.builtin_history && !this.from_nav) {
                if (this.current > 0) {
                    history.pushState(this.current.toString(), "", "#" + this.states[this.current].url);
                }
                else {
                    history.replaceState(this.current.toString(), "", "#" + this.states[this.current].url);
                }
            }
        }
        else {
            if (this.states[this.current].focus >= 0) {
                document.getElementById("itemlist").children[this.states[this.current].focus].children[0].focus();
                document.getElementById("itemlist").scrollTop = this.states[this.current].scroll;
            }
            this.states[this.current].end = new Date().getTime();
            this.states[this.current].data = data;
            this.states[this.current].category = category;
            this.states = this.states.slice(0, this.current + 1);
        }
		this.from_nav = false;
    },

    "go": function (index) {
        if (!this.confirmed) {
            this.current -= 1;
            this.confirmed = true;
        }
        this.states[this.current].scroll = document.getElementById("itemlist").scrollTop;
        this.states[this.current].focus = Array.prototype.indexOf.call(document.getElementById("itemlist").children, focused_item.parentNode);

        if (this.current + index < 0) {
            this.current = -1;
            this.confirmed = false;
            send_request("");
            return;
        }

        else if (this.current + index >= this.states.lenght) {
            this.current = this.states.lenght - 1;
        }
        else {
            this.current += index;
        }

        if (this.states[this.current].end - this.states[this.current].start > this.cache) {
            document.getElementById("itemlist").innerHTML = this.states[this.current].data.join("");
            set_category(this.states[this.current].category)
            if (this.states[this.current].focus >= 0) {
                document.getElementById("itemlist").children[this.states[this.current].focus].children[0].focus();
            }
            if (this.states[this.current].scroll) {
                document.getElementById("itemlist").scrollTop = this.states[this.current].scroll;
            }
			show_images();
            this.confirmed = true;
        }
        else {
            this.confirmed = false;
			this.from_nav = true;
            send_request(this.states[this.current].url);
        }
    },
    "current": -1,
    "confirmed": false,
	"from_nav": false,
    "states": [],
    "cache": 2000 //Tiempo para determinar si se cargará la cache o se volvera a solicitar el item (el tiempo es el que tarda en responder el servidor)
};