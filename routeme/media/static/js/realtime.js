onopen = function() { alert("connected"); };

onmessage = function (data) {
    alert(data.unread);
};

onclose = function() { alert("disconnected"); };

alert(window.location.hostname);

socket = new io.Socket(window.location.hostname, {
            port:"8888",
            resource:"socket/",
            transports:['websocket', 'flashsocket','xhr-multipart', 'xhr-polling']
            }
     );

socket.on('connect', onopen);
socket.on('message', onmessage);
socket.on('disconnect', onclose);
socket.connect();

