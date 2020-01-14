document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))
    var users = {}

    //var room = "Lounge"

    const timestamp = new Date()
    timestamp.getTime()
    const time_stamp = timestamp.toLocaleTimeString()

    const messageContainer = document.getElementById('message-container')
    const messageForm = document.getElementById('send-container')
    const messageInput = document.getElementById('message-input')
    //const name = document.getElementById('users-connected').getAttribute('name')
    const btnLogout = document.getElementById('logout-btn')
    const listName = document.getElementById('list-user-room')
    const room = document.getElementById('room')
    const name = document.getElementById('username').getAttribute("value")


    socket.emit('new-user', name)
    //appendMessage('You joined')


    socket.on('new-user', name => {
      appendMessage(`user ${name}`)
    })


    socket.on('chat-message', data => {

      const p = document.createElement('p');
      const span_username = document.createElement('span');
      const span_timestamp = document.createElement('span');
      const br = document.createElement('br');

        if (data.user_name){

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

      //appendMessage(p)
      messageContainer.append(p);

      //appendMessage(`${data.user_name} says ${data.timestamp} : ${data.message} on ${data.room}`)

    })

    socket.on('user-connected', name => {
      appendMessage(`${name} connected`)
    })

    socket.on('user-disconnected', name => {
      appendMessage(`${name} disconnected`)
    })

    messageForm.addEventListener('submit', e => {
      e.preventDefault()
      const message = messageInput.value

      let user_name = name

      //appendMessage(`${name}: ${message}`)

      socket.emit('send-chat-message', {
            "user_name" : name ,
            "message" : message,
            "timestamp" : time_stamp,
            "room" : room
        }
      )

      messageInput.value = ''
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

    //Room selection
    document.querySelectorAll('users-connected').forEach(p =>{

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

    //logout from chat
    btnLogout.onclick = function(){
        leaveRom(room);
    }

    // leave the room
    function leaveRoom(room){
        socket.emit('leave', {'user_name' : name, 'room': room})
    }

    //join room
    function joinRoom(room){
        console(room)
        socket.emit('join', {'user_name' : name, 'room': room})
        //clear message area
        document.querySelectorAll('#message-container').innerHTML = ''
    }

    //printing system message
    function printSysMsg(msg){
        const p = document.createElement('p')
        p.innerHTML = msg;
        document.querySelector('#message-container').append(p)

    }

    //disconnecting
    socket.on('disconnect', function(){
        socket.broadcast.emit(`user ${name} disconnectedßß`)
    })
});