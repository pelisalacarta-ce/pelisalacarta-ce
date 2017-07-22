function websocket_connect() {
    if (websocket) {
        websocket.close();
    };
    var status = document.getElementById("footer").getElementById("status");
    status.innerHTML = "Conectando...";

    loading.show("Estableciendo conexión...");
    websocket = new WebSocket(websocket_host);
    websocket.onopen = function (evt) {
        loading.show();
        status.innerHTML = "Conectado";
    };

    websocket.onclose = function (evt) {
        status.innerHTML = "Desconectado";
    };

    websocket.onmessage = function (evt) {
        get_response(evt.data);
    };

    websocket.onerror = function (evt) {
        websocket.close();
    };
};

function websocket_send(data, retry) {
    if (!retry) {
        connection_retry = true;
    };
	if (!websocket){
		websocket_connect();
	};
    if (websocket.readyState != 1) {
		if ((websocket.readyState == 2 || websocket.readyState == 3) && connection_retry) {
			websocket_connect();
		};
        setTimeout(websocket_send, 500, data, true);
        return;
    }
    else if (websocket.readyState == 1) {
        data["id"] = session_id;
        websocket.send(JSON.stringify(data));
    };
};

function send_request(url) {
    if (url == "go_back") {
        nav_history.go(-1);
        return;
    };

    nav_history.newRequest(url);

    loading.show();
    var send = {};
    send["request"] = url;
    websocket_send(send);
};

function send_data(dato) {
    var send = {};
    send["data"] = dato;
    websocket_send(send);
};

function ajax_to_dict(url, obj, key) {
    var xhttp = new XMLHttpRequest();
    ajax_running.push(xhttp);
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            eval("obj." + key + " = xhttp.responseText");
            ajax_running.remove(xhttp)
        };
    };
    xhttp.open("GET", url, true);
    xhttp.send();
};