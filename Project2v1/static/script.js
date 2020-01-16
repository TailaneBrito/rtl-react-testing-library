document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))
    var users = {}
    //var io = require(socket)(app);

    //let room

    const timestamp = new Date()
    timestamp.getTime()
    const time_stamp = timestamp.toLocaleTimeString()

    const messageContainer = document.getElementById('message-container')
    const messageForm = document.getElementById('send-container')
    const messageInput = document.getElementById('message-input')
    const btnLogout = document.getElementById('btnLogout')
    const listName = document.getElementById('list-user-room')
    const room = document.getElementById('room').getAttribute("value")
    const name = document.getElementById('username').getAttribute("value")
    const btnSend = document.getElementById('send-button')
    const p = document.getElementById('room').getAttribute('value')
    const selectRoom = document.getElementById('select-room')

    const room_name = room

    socket.on('connection', function(socket){
        console.log(`entrou aqui`)

        localStorage.setItem(name, room, socket)

        //handling new socket connection
        users.append(socket)

        //joins the user to a room
        joinRoom(room)

        setSessionItem(name, room)

        /*
        socket.emit('join', function(roomName, nickname, callback){
            console.log(`join`)
            socket.join(roomName)
            socket.nickname = nickname

            const messages = []
            callback(messages)
        })
        */

        //event handlers for each user
        socket.on('disconnect', function(){
            const idx = users.indexOf(socket)
            users.splice(idx, 1)
        })

        socket.on('nickname', function(nickname){
            socket.nickname = nickname
        })

        socket.on('message', data=>{
            //add the message process here
            //const roomName = Object.keys(io.sockets.adapter.sids[socket.id])[1]

            console.log(` message script.js`)

            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br');
        })

        socket.on('error', function(msg){
            printSysMsg(msg)
        })
    })

    //go to application.py and grab new-user func
    socket.emit('new-user', name)


    socket.on('test-chat-message', data => {
        console.log(`test-chat-message`)

        const p = document.createElement('p')
        const span_username = document.createElement('span')
        const span_timestamp = document.createElement('span')
        const br = document.createElement('br')

        if (data.user_name){
          console.log(`chat-message ${data.user_name}`)
          p.setAttribute("class", "my-msg");
          span_username.setAttribute("class", "my-username");
          span_username.innerText = data.user_name;

          span_timestamp.setAttribute("class", "timestamp");
          span_timestamp.innerText = data.timestamp;

          p.innerHTML = span_username.innerText +
                        br.outerHTML + data.message
                        + br.innerText + br.outerHTML +
                        span_timestamp.innerText + br.innerText + br.outerHTML +data.room
        }else{
          printSysMsg(data.message)
        }
      messageContainer.append(p);

    })

    //Room selection
    document.querySelectorAll('select-room').forEach(p =>{

        p.onclick = () => {
            let newRoom = p.innerHTML;
            //user wants to joy the same as the actual room?
            if (newRoom == room) {
                msg = `You are already in ${room} room.`
                //printSysMsg(msg);
                appendMessage(msg)

            }else{
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom
            }
        }
    })

    socket.on('new-user', name => {
      appendMessage(`user ${name}`)
    })


    socket.on('chat-message', data => {
      console.log(`chat-message`)
      const p = document.createElement('p');
      const span_username = document.createElement('span');
      const span_timestamp = document.createElement('span');
      const br = document.createElement('br');

        if (data.user_name){
          console.log(`chat-message ${data.user_name}`)
          p.setAttribute("class", "my-msg");
          span_username.setAttribute("class", "my-username");
          span_username.innerText = data.user_name;

          span_timestamp.setAttribute("class", "timestamp");
          span_timestamp.innerText = data.timestamp;

          p.innerHTML = span_username.innerText +
                        br.outerHTML + data.message
                        + br.innerText + br.outerHTML +
                        span_timestamp.innerText + br.innerText + br.outerHTML +data.room
        }else{
          printSysMsg(data.message)
        }
      messageContainer.append(p);
    })

    // receive from application.py the name of connected user
    socket.on('user-connected', name => {
      appendMessage(`${name} connected`)
    })

    // receive from application.py the name of connected user
    socket.on('user-disconnected', name => {
      appendMessage(`${name} disconnected`)
    })

    messageForm.addEventListener('submit', e => {
      e.preventDefault()
      const message = messageInput.value
      let user_name = name

      socket.emit('send-chat-message', {
            "user_name" : name ,
            "message" : message,
            "timestamp" : time_stamp,
            "room" : room
        }
      )

      messageInput.value = ''
      return false
    })

    socket.on('leave-room', data => {
        console.log(`on leave-room`)

        //in case the user wants to switch rooms
        if(socket.room)
            socket.leave(socket.room)
        socket.room = data.room

        leaveRoom(data.room)
    })

    function appendMessage(message) {
      const messageElement = document.createElement('div')
      messageElement.innerText = message
      messageContainer.append(messageElement)
    }


    socket.on('my response', function(msg){
        console.log(msg)

        if( typeof msg.user_name !== 'undefined'){
            $('h3').remove()
            const messageElement = document.createElement('div')
            messageElement.innerText = msg.user + " : " + msg
            messageContainer.append(messageElement)
         }
    })

    //logout from chat active Leave function
    btnLogout.onclick = function(){
        leaveRoom(room_name)
        //closes the tab after clicking the leave room button
        window.close();
    }

    //btnSend.onclick = function(data){
    //function myFunction(data){
   //btnSend.addEventListener('click', function(data){
   btnSend.onclick = () => {
        //verify if the user is at the room it joined and emit the message only for those who
        //are at the same room.
        socket.send({"message": messageInput.value,
                    "user_name": username, "room": room})

     /*
        if (newRoom == room) {
                msg = `You are already in ${room} room.`
                console.log(msg )
                //printSysMsg(msg);
                //appendMessage(msg)
                socket.emit('message', data)

      const p = document.createElement('p')
      const span_username = document.createElement('span')
      const span_timestamp = document.createElement('span')
      const br = document.createElement('br')
      const newRoom = p.value

      console.log(` nova sala ${newRoom}`)

        if (data.user_name){
            console.log(`user name abaixo`)
            console.log(data.user_name)

          //user wants to joy the same as the actual room?


              p.setAttribute("class", "my-msg");
              span_username.setAttribute("class", "my-username");
              span_username.innerText = data.user_name;

              span_timestamp.setAttribute("class", "timestamp");
              span_timestamp.innerText = data.timestamp;

              p.innerHTML = span_username.innerText +
                            br.outerHTML + data.message
                            + br.innerText + br.outerHTML +
                            span_timestamp.innerText + br.innerText + br.outerHTML +data.room

            }else{
                console.log(`else`)
                leaveRoom(room)
                joinRoom(newRoom)
                room = newRoom
            }
        }else{
          printSysMsg(data.message)
        }
      messageContainer.append(p);
      */
    }

    // leave the room
    function leaveRoom(room){
        console.log(`leaveRoom func calling leave`)
        //sends to the server a request for the user to leave the room
        socket.emit('leave', {'user_name' : name, 'room': room_name})
    }

    //join room
    function joinRoom(room){
        console.log(`joinRoom`)
        socket.emit('join', {'user_name' : name, 'room': room})
        //clear message area
       // document.querySelectorAll('#message-container').innerHTML = ''
        messageForm.innerHTML = ''
    }

    //printing system message
    function printSysMsg(msg){
        const p = document.createElement('p')
        p.innerHTML = msg;
        messageContainer.append(p)

        //socket.emit('send-chat-message', { "message": "redirecting"})
    }

    function broadcastMemberJoined(roomName, nickname) {
    // send them out
        io.sockets.in(roomName).emit('newMember', nickname);
    }


    //LocalStorage

    function setSessionItem(name, value) {
        var mySession;
        try {
            mySession = JSON.parse(localStorage.getItem('mySession'));
        } catch (e) {
            console.log(e);
            mySession = {};
        }

        mySession[name] = value;

        mySession = JSON.stringify(mySession);

        localStorage.setItem('mySession', mySession);
    }

    function getSessionItem(name) {
        var mySession = localStorage.getItem('mySession');
        if (mySession) {
            try {
                mySession = JSON.stringify(mySession);
                return mySession[name];
            } catch (e) {
                console.log(e);
            }
        }
    }

    function restoreSession(data) {
        for (var x in data) {
            //use saved data to set values as needed
            console.log(x, data[x]);
        }
    }



    window.addEventListener('load', function(e) {
        var mySession = localStorage.getItem('mySession');
        if (mySession) {
            try {
                mySession = JSON.parse(localStorage.getItem('mySession'));
            } catch (e) {
                console.log(e);
                mySession = {};
            }
            restoreSession(mySession);
        } else {
            localStorage.setItem('mySession', '{}');
        }

        setSessionItem('foo', Date.now()); //should change each time

        if (!mySession.bar) {
            setSessionItem('bar', Date.now()); //should not change on refresh
        }
    }, false);
});