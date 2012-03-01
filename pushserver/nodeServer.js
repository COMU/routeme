var app = require('express').createServer()
var io = require('socket.io').listen(app);

app.listen(8090);

var clients = {};
   
// routing
app.get('/message', function (req, res) {
    console.log(req.query['user']);
    clients[req.query['user']].emit('message', req.query['data']);
    res.send("Hello World!");
});

// usernames which are currently connected to the chat

io.sockets.on('connection', function (socket) {
    socket.on('adduser', function(data){
        console.log(data);
        clients[data] = socket;
    });
 
    socket.on('newMessage', function(data){
	console.log("Message to :" + data);
	clients[data].emit('message', "data");
    });
   
    socket.on('disconnect', function(){
        //TODO remove sid from hashtable
    });

});
