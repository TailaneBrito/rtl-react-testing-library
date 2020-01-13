document.addEventListener('DOMContentLoaded', () => {


    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))

    const  messageUserLogged = document.getElementById('username')
    const  messageUserSession = document.getElementById('user_logged')
    const  btnConnect = document.getElementById('send-button')
    const  formConnect = document.getElementById('user-login')
    const  selectRoomName = document.getElementById('room_name')

    // inputting user_name
    const name = prompt('What is your name?')

    messageUserLogged.value = name
    messageUserSession.value  = name
    messageUserSession.setAttribute("value", name)
    messageUserLogged.setAttribute("disabled", true)

    var users = new Object()
    var users = {}
    var channel = {}

    // add users to user dict
    users.name = name
    users.channel = selectRoomName.value
    //console.log(room)

    // add channel and users to channel dict
    //channel.name = messageChannel.value
    //channel.user = users.name

    console.log(users.name)

    /*
    socket.on('connect', function() {
      // adding user entrees
      socket.emit('get-user', {
            "user_name" :  users.name
            })
    })
    */

    socket.on('my response', function(msg){
        console.log(msg)
    })

    //console.log(room)

    //Room selection
    document.querySelectorAll('.select-room').forEach(p =>{

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

    btnConnect.onclick = function(){
        get_user_room();
    }

    function get_user_room(){
        var room = selectRoomName.value

        json = {user_name : users.name ,
                room : room
        }
        console.log(room)
        socket.emit('get-user', json)

        console.log(room)
    }

    /* logout from chat
    document.querySelector("#logout-btn").onclick() => {
        leaveRom(room);
    }
    */
    // leave the room
    function leaveRoom(room){
        socket.emit('leave', {'user_name' : user_name, 'room': room})
    }

    //join room
    function joinRoom(room){
        socket.emit('join', {'user_name' : user_name, 'room': room})
        //clear message area
        document.querySelectorAll('message-container').innerHTML = ''
    }

    //printing system message
    function printSysMsg(msg){
        const p = document.createElement('p')
        p.innerHTML = msg;
        document.querySelector('#message-container').append(p)

    }


});