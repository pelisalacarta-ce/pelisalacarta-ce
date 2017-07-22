window.onkeydown = function (e) {
    if (e.keyCode == 27) {
        dialog.closeall()
    }

    if (e.target.tagName == "BODY") {
        body_events(e);
    };
    if (document.getElementById("window_loading").contains(e.target)) {
        window_loading_events(e);
    };
    if (document.getElementById("window_settings").contains(e.target)) {
        window_settings_events(e);
    };
    if (document.getElementById("window_select").contains(e.target)) {
        window_select_events(e);
    };
    if (document.getElementById("window_ok").contains(e.target)) {
        window_generic_events(e);
    };
    if (document.getElementById("window_yesno").contains(e.target)) {
        window_generic_events(e);
    };
	if (document.getElementById("window_recaptcha").contains(e.target)) {
        window_recaptcha_events(e);
    };
    if (document.getElementById("window_progress").contains(e.target)) {
        window_generic_events(e);
    };
    if (document.getElementById("window_info").contains(e.target)) {
        window_generic_events(e);
    }
    if (document.getElementById("window_input").contains(e.target)) {
        window_input_events(e);
    };
    if (document.getElementById("itemlist").contains(e.target)) {
        itemlist_events(e);
    };
};

function itemlist_events(e) {
    var el = document.getElementById('itemlist');

    switch (e.keyCode) {
    case 96:
    case 97:
    case 98:
    case 99:
    case 100:
    case 101:
    case 102:
    case 103:
    case 104:
    case 105:
        numeric_search(e.keyCode);
        break;

    case 93: //Menu
        e.preventDefault();
        if (e.target.parentNode.children.length == 2) {
            e.target.parentNode.children[1].onclick.apply(e.target.parentNode.children[1]);
            focused_item = e.target.parentNode.children[1];
        };
        break;

    case 8: //BACK
        e.preventDefault();
        if (nav_history.current > 0) {
            send_request("go_back");
        };
        break;

    case 37: //LEFT
        e.preventDefault();
        var index = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);
		if (index > 0){
			e.target.parentNode.children[index - 1].focus();
		};
        break;

    case 38: //UP
        e.preventDefault();
        var index = Array.prototype.indexOf.call(el.children, e.target.parentNode);
        if (index == 0) {
            index = el.children.length;
        };
        el.children[index - 1].children[0].focus();
        break;

    case 39: //RIGHT
        e.preventDefault();
        var index = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);
        if (index < e.target.parentNode.children.length - 1){
			e.target.parentNode.children[index + 1].focus();
		};
        break;

    case 40: //DOWN
        e.preventDefault();
        var index = Array.prototype.indexOf.call(el.children, e.target.parentNode);
        if (index + 1 == el.children.length) {
            index = -1;
        };
        el.children[index + 1].children[0].focus();
        break;
    };
};

function window_loading_events(e) {
    switch (e.keyCode) {
    case 8: //BACK
        loading.close();
        connection_retry = false;
        e.preventDefault();
        break;
    };
};

function body_events(e) {
    switch (e.keyCode) {
    case 8: //BACK
        e.preventDefault();
        break;

    case 37: //LEFT
    case 38: //UP
    case 39: //RIGHT
    case 40: //DOWN
        e.preventDefault();
        document.getElementById("itemlist").children[0].children[0].focus();
        break;
    };
};

function window_generic_events(e) {
    var el = (document.getElementById("window_ok").contains(e.target) ? document.getElementById("window_ok") : el);
    var el = (document.getElementById("window_yesno").contains(e.target) ? document.getElementById("window_yesno") : el);
    var el = (document.getElementById("window_progress").contains(e.target) ? document.getElementById("window_progress") : el);
    var el = (document.getElementById("window_info").contains(e.target) ? document.getElementById("window_info") : el);

    switch (e.keyCode) {
    case 8: //BACK
        e.preventDefault();
        dialog.closeall();
        break;

    case 38: //UP
        e.preventDefault();
        if (el.getElementById("window_footer").contains(e.target)) {
            el.children[0].focus();
        };
        break;

    case 37: //LEFT
        e.preventDefault();

        if (el.getElementById("window_footer").contains(e.target)) {
            var index = Array.prototype.indexOf.call(el.getElementById("window_footer").children, e.target) -1;
			while (index >= 0 && el.getElementById("window_footer").children[index].disabled){
				index --;
			};
			if (index >=0){
				el.getElementById("window_footer").children[index].focus();
			};
        };
        break;

    case 39: //RIGHT
        e.preventDefault();
        if (el.getElementById("window_footer").contains(e.target)) {
            var index = Array.prototype.indexOf.call(el.getElementById("window_footer").children, e.target) +1;
			while (index < el.getElementById("window_footer").children.length && el.getElementById("window_footer").children[index].disabled){
				index ++;
			};
			if (index < el.getElementById("window_footer").children.length){
				el.getElementById("window_footer").children[index].focus();
			};
        };
        break;

    case 40: //DOWN
        e.preventDefault();
        if (e.target.parentNode == el) {
            el.getElementById("window_footer").children[0].focus();
        };
        break;
    };
};

function window_recaptcha_events(e) {
    var el = document.getElementById("window_recaptcha");

    switch (e.keyCode) {
    case 8: //BACK
        e.preventDefault();
        dialog.closeall();
        break;

    case 38: //UP
        e.preventDefault();
        if (el.getElementById("window_footer").contains(e.target)) {
            el.getElementById("window_image").children[el.getElementById("window_image").children.length -1].focus();
        }
		
		else {
			var index = Array.prototype.indexOf.call(el.getElementById("window_image").children, e.target) -3;
			if (index >-1) {
				el.getElementById("window_image").children[index].focus();
			}
			else {
				el.children[0].focus();
			};
		};
        break;

    case 37: //LEFT
        e.preventDefault();

        if (el.getElementById("window_footer").contains(e.target)) {
            var index = Array.prototype.indexOf.call(el.getElementById("window_footer").children, e.target) -1;
			while (index >= 0 && el.getElementById("window_footer").children[index].disabled){
				index --;
			};
			if (index >=0){
				el.getElementById("window_footer").children[index].focus();
			};
        } else if (e.target.parentNode == el.getElementById("window_image")) {
			var index = Array.prototype.indexOf.call(el.getElementById("window_image").children, e.target) -1;
			if ([-1,2,5].indexOf(index) == -1) {
				el.getElementById("window_image").children[index].focus();
			};
		};
        break;

    case 39: //RIGHT
        e.preventDefault();
        if (el.getElementById("window_footer").contains(e.target)) {
            var index = Array.prototype.indexOf.call(el.getElementById("window_footer").children, e.target) +1;
			while (index < el.getElementById("window_footer").children.length && el.getElementById("window_footer").children[index].disabled){
				index ++;
			};
			if (index < el.getElementById("window_footer").children.length){
				el.getElementById("window_footer").children[index].focus();
			};
        } else if (e.target.parentNode == el.getElementById("window_image")) {
			var index = Array.prototype.indexOf.call(el.getElementById("window_image").children, e.target) +1;
			if ([3,6,9].indexOf(index) == -1) {
				el.getElementById("window_image").children[index].focus();
			};
		};
        break;

    case 40: //DOWN
        e.preventDefault();
        if (e.target.parentNode == el) {
            el.getElementById("window_image").children[0].focus();
        }
		else if (e.target.parentNode == el.getElementById("window_image")) {
			var index = Array.prototype.indexOf.call(el.getElementById("window_image").children, e.target) +3;
			if (index < el.getElementById("window_image").children.length) {
				el.getElementById("window_image").children[index].focus();
			}
			else {
				el.getElementById("window_footer").children[0].focus();
			};
		};
        break;
    };
};

function window_select_events(e) {
    var el = document.getElementById('window_select');

    switch (e.keyCode) {
    case 8: //BACK
        e.preventDefault();
        dialog.closeall();
        break;

    case 38: //UP
        e.preventDefault();
        var index = Array.prototype.indexOf.call(el.getElementById("control_list").children, e.target.parentNode);
        if (index != 0) {
            el.getElementById("control_list").children[index - 1].children[0].focus();
        }
        else {
            el.children[0].focus();
        };
        break;

    case 40: //DOWN
        e.preventDefault();
        if (e.target.parentNode == el) {
            el.getElementById("control_list").children[0].children[0].focus();
        }
        else {
            var index = Array.prototype.indexOf.call(el.getElementById("control_list").children, e.target.parentNode);
            el.getElementById("control_list").children[index + 1].children[0].focus();
        };
        break;
    };
};

function window_settings_events(e) {
    el = document.getElementById('window_settings');

    switch (e.keyCode) {
    case 8: //BACK
        if ((e.target.tagName != "INPUT" || (e.target.type != "text" && e.target.type != "password")) && e.target.tagName != "SELECT") {
            e.preventDefault();
            dialog.closeall();
        };
        break;

    case 38: //UP
        e.preventDefault();
        if (e.target.parentNode == el) {
            return;
        };
        if (el.getElementById("category_container").contains(e.target)) {
            el.children[0].focus();
            return;

        }
        else if (el.getElementById("window_footer").contains(e.target) || el.getElementById("window_footer_local").contains(e.target)) {
            var index = null;
            var group = null;

        }
        else if (el.getElementById("controls_container").contains(e.target)) {
            var group = Array.prototype.indexOf.call(el.getElementById("controls_container").children, e.target.parentNode.parentNode.parentNode);
            var index = Array.prototype.indexOf.call(el.getElementById("controls_container").children[group].children, e.target.parentNode.parentNode) - 1;
        };

        if (group == null) {
            for (group = 0; group < el.getElementById("category_container").children.length; group++) {
                if (el.getElementById("category_container").children[group].style.display != "none") {
                    break;
                };
            };
        };

        if (index == null) {
            index = el.getElementById("controls_container").children[group].children.length - 1;
        };

        while (index >= 0 &&
            (el.getElementById("controls_container").children[group].children[index].children[0].className != "control" ||
                el.getElementById("controls_container").children[group].children[index].children[0].children[1].disabled ||
                el.getElementById("controls_container").children[group].children[index].style.display == "none")) {

            index--;
        };

        if (index >= 0) {
            el.getElementById("controls_container").children[group].children[index].children[0].children[1].focus();
        }
        else {
            if (el.getElementById("category_container").style.display == "none") {
                el.children[0].focus();
            }
            else {
                el.getElementById("category_container").children[0].focus();
            };
        };
        break;

    case 37: //LEFT
        if ((e.target.tagName != "INPUT" || (e.target.type != "text" && e.target.type != "password")) && e.target.tagName != "SELECT") {
            e.preventDefault();
            if (el.getElementById("category_container").contains(e.target)) {
                var index = Array.prototype.indexOf.call(el.getElementById("category_container").children, e.target);
                el.getElementById("category_container").children[index - 1].focus();
            }
            else if (el.getElementById("window_footer").contains(e.target)) {
                var index = Array.prototype.indexOf.call(el.getElementById("window_footer").children, e.target);
                el.getElementById("window_footer").children[index - 1].focus();
            }
            else if (el.getElementById("window_footer_local").contains(e.target)) {
                var index = Array.prototype.indexOf.call(el.getElementById("window_footer_local").children, e.target);
                el.getElementById("window_footer_local").children[index - 1].focus();
            };
        };
        break;

    case 39: //RIGHT
        if ((e.target.tagName != "INPUT" || (e.target.type != "text" && e.target.type != "password")) && e.target.tagName != "SELECT") {
            e.preventDefault();
            if (el.getElementById("category_container").contains(e.target)) {
                var index = Array.prototype.indexOf.call(el.getElementById("category_container").children, e.target);
                el.getElementById("category_container").children[index + 1].focus();
            }
            else if (el.getElementById("window_footer").contains(e.target)) {
                var index = Array.prototype.indexOf.call(el.getElementById("window_footer").children, e.target);
                el.getElementById("window_footer").children[index + 1].focus();
            }
            else if (el.getElementById("window_footer_local").contains(e.target)) {
                var index = Array.prototype.indexOf.call(el.getElementById("window_footer_local").children, e.target);
                el.getElementById("window_footer_local").children[index + 1].focus();
            };
        };
        break;

    case 40: //DOWN
        e.preventDefault();
        if (e.target.parentNode == el) {
            if (el.getElementById("category_container").style.display == "none") {
                var index = 0;
                var group = null;
            }
            else {
                el.getElementById("category_container").children[0].focus();
            };
        }
        else if (el.getElementById("category_container").contains(e.target)) {
            var index = 0;
            var group = null;

        }
        else if (el.getElementById("controls_container").contains(e.target)) {
            var group = Array.prototype.indexOf.call(el.getElementById("controls_container").children, e.target.parentNode.parentNode.parentNode);
            var index = Array.prototype.indexOf.call(el.getElementById("controls_container").children[group].children, e.target.parentNode.parentNode) + 1;
        };

        if (group == null) {
            for (group = 0; group < el.getElementById("category_container").children.length; group++) {
                if (el.getElementById("category_container").children[group].style.display != "none") {
                    break;
                };
            };
        };

        while (index < el.getElementById("controls_container").children[group].children.length &&
            (el.getElementById("controls_container").children[group].children[index].children[0].className != "control" ||
                el.getElementById("controls_container").children[group].children[index].children[0].children[1].disabled ||
                el.getElementById("controls_container").children[group].children[index].style.display == "none")) {

            index++;
        };

        if (index < el.getElementById("controls_container").children[group].children.length) {
            el.getElementById("controls_container").children[group].children[index].children[0].children[1].focus();
        }
        else {
            el.getElementById("window_footer").children[0].focus();
            el.getElementById("window_footer_local").children[0].focus();
        };
        break;
    };
};

function window_input_events(e) {
    el = document.getElementById("window_input");

    switch (e.keyCode) {
    case 8: //BACK
        if (e.target.tagName != "INPUT") {
            e.preventDefault();
            dialog.closeall();
        };
        break;

    case 38: //UP
        e.preventDefault();
        if (el.getElementById("window_footer").contains(e.target)) {
            el.getElementById("control_input").children[0].focus();
        }
        if (el.getElementById("control_input").contains(e.target)) {
            el.children[0].focus();
        };
        break;

    case 37: //LEFT
        if (el.getElementById("window_footer").contains(e.target)) {
            var index = Array.prototype.indexOf.call(el.getElementById("window_footer").children, e.target);
            el.getElementById("window_footer").children[index - 1].focus();
            e.preventDefault();
        };
        break;

    case 39: //RIGHT
        if (el.getElementById("window_footer").contains(e.target)) {
            var index = Array.prototype.indexOf.call(el.getElementById("window_footer").children, e.target);
            el.getElementById("window_footer").children[index + 1].focus();
            e.preventDefault();
        };
        break;

    case 40: //DOWN
        e.preventDefault();
        if (e.target.parentNode == el) {
            el.getElementById("control_input").children[0].focus();
        };
        if (el.getElementById("control_input").contains(e.target)) {
            el.getElementById("window_footer").children[0].focus();
        };
        break;
    };
};

function numeric_search(keyCode) {
    switch (keyCode) {
    case 96:
        keychar["keyCode"] = keyCode;
        keychar["Char"] = "0";
        break;

    case 97:
        keychar["keyCode"] = keyCode;
        keychar["Char"] = "1";
        break;

    case 98:
        if (keychar["keyCode"] == keyCode) {
            switch (keychar["Char"]) {
            case "a":
                keychar["Char"] = "b";
                break;
            case "b":
                keychar["Char"] = "c";
                break;
            case "c":
                keychar["Char"] = "2";
                break;
            case "2":
                keychar["Char"] = "a";
                break;
            };
        }
        else {
            keychar["keyCode"] = keyCode;
            keychar["Char"] = "a";
        };
        break;

    case 99:
        if (keychar["keyCode"] == keyCode) {
            switch (keychar["Char"]) {
            case "d":
                keychar["Char"] = "e";
                break;
            case "e":
                keychar["Char"] = "f";
                break;
            case "f":
                keychar["Char"] = "3";
                break;
            case "3":
                keychar["Char"] = "d";
                break;
            };
        }
        else {
            keychar["keyCode"] = keyCode;
            keychar["Char"] = "d";
        };
        break;

    case 100:
        if (keychar["keyCode"] == keyCode) {
            switch (keychar["Char"]) {
            case "g":
                keychar["Char"] = "h";
                break;
            case "h":
                keychar["Char"] = "i";
                break;
            case "i":
                keychar["Char"] = "4";
                break;
            case "4":
                keychar["Char"] = "g";
                break;
            };
        }
        else {
            keychar["keyCode"] = keyCode;
            keychar["Char"] = "g";
        };
        break;

    case 101:
        if (keychar["keyCode"] == keyCode) {
            switch (keychar["Char"]) {
            case "j":
                keychar["Char"] = "k";
                break;
            case "k":
                keychar["Char"] = "l";
                break;
            case "l":
                keychar["Char"] = "5";
                break;
            case "5":
                keychar["Char"] = "j";
                break;
            };
        }
        else {
            keychar["keyCode"] = keyCode;
            keychar["Char"] = "j";
        };
        break;

    case 102:
        if (keychar["keyCode"] == keyCode) {
            switch (keychar["Char"]) {
            case "m":
                keychar["Char"] = "n";
                break;
            case "n":
                keychar["Char"] = "o";
                break;
            case "o":
                keychar["Char"] = "6";
                break;
            case "6":
                keychar["Char"] = "m";
                break;
            };
        }
        else {
            keychar["keyCode"] = keyCode;
            keychar["Char"] = "m";
        };
        break;

    case 103:
        if (keychar["keyCode"] == keyCode) {
            switch (keychar["Char"]) {
            case "p":
                keychar["Char"] = "q";
                break;
            case "q":
                keychar["Char"] = "r";
                break;
            case "r":
                keychar["Char"] = "s";
                break;
            case "s":
                keychar["Char"] = "7";
                break;
            case "7":
                keychar["Char"] = "p";
                break;
            };
        }
        else {
            keychar["keyCode"] = keyCode;
            keychar["Char"] = "p";
        };
        break;

    case 104:
        if (keychar["keyCode"] == keyCode) {
            switch (keychar["Char"]) {
            case "t":
                keychar["Char"] = "u";
                break;
            case "u":
                keychar["Char"] = "u";
                break;
            case "v":
                keychar["Char"] = "8";
                break;
            case "8":
                keychar["Char"] = "t";
                break;
            };
        }
        else {
            keychar["keyCode"] = keyCode;
            keychar["Char"] = "t";
        };
        break;

    case 105:
        if (keychar["keyCode"] == keyCode) {
            switch (keychar["Char"]) {
            case "x":
                keychar["Char"] = "y";
                break;
            case "y":
                keychar["Char"] = "z";
                break;
            case "z":
                keychar["Char"] = "w";
                break;
            case "w":
                keychar["Char"] = "9";
                break;
            case "9":
                keychar["Char"] = "x";
                break;
            };
        }
        else {
            keychar["keyCode"] = keyCode;
            keychar["Char"] = "x";
        };
        break;
    };

    var el = document.getElementById('itemlist');

    for (x = 0; x < el.children.length; x++) {
        if (el.children[x].children[0].children[2].innerHTML.toLowerCase().indexOf(keychar["Char"]) === 0) {
            el.children[x].children[0].focus();
            break;
        };
        if (el.children[x].children[0].children[0].innerHTML.toLowerCase().indexOf(keychar["Char"]) === 0) {
            el.children[x].children[0].focus();
            break;
        };
    };
};

document.onkeypress = function (e) {
    if ((e || window.event).keyCode === 32) {
        if (media_player.paused) {
            media_player.play();
        }
        else {
            media_player.pause();
        };
    };
};

document.ondblclick = function () {
    if (media_player.requestFullscreen) {
        media_player.requestFullscreen();
    }
    else if (media_player.mozRequestFullScreen) {
        media_player.mozRequestFullScreen();
    }
    else if (media_player.webkitRequestFullscreen) {
        media_player.webkitRequestFullscreen();
    };
};