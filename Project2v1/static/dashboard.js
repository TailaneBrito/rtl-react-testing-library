document.addEventListener('DOMContentLoaded', () => {


    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))

    // username
    const  messageUserLogged = document.getElementById('username')
    const  messageUserSession = document.getElementById('user_logged')
    const  btnConnect = document.getElementById('send-button')
    const  formConnect = document.getElementById('user-login')
    const  selectRoomName = document.getElementById('room_name')
    const  btnLogout = document.getElementById('logout-btn')

    // inputting user_name
    const name = prompt('What is your name?')
    messageUserLogged.value = name
    messageUserSession.value  = name

    //setting attibutes to div user_logged
    messageUserSession.setAttribute("value", name)
    messageUserLogged.setAttribute("disabled", true)

    var users = new Object()
    var users = {}

    var channel = {}

    // add users to user dict
    users.name = name
    print(users.name)
    users.room = selectRoomName.value


    socket.on('my response', function(msg){
        console.log(msg)
    })

    btnConnect.onclick = function(){
        get_user();
    }

    function get_user(){
        //var room = selectRoomName.value
        localStorage.setItem('user_room') = selectRoomName.value
        var room = localStorage.getItem('user_room');
        var name = localStorage.getItem('user_name');

        let newRoom = room

        if(newRoom == room){
            msg = `You are already in ${room} room.`
            socket.emit('my response', msg)
        }else{
            leaveRoom(room);
            joinRoom(newRoom);
            room = newRoom
        }


        json = {user_name : name ,
                room : localStorage.getItem('user_room')
        }

        // go to application.py get-user
        socket.emit('get-user', json)
        console.log(`room ${room}`)
        console.log(`name ${name}`)
    }

    //adds the information from user to the users list
    socket.on('get-user-info', function(json){
        users.name = json.name,
        users.room = json.room,
        users.sid = json.sid
    })

    //logout from chat
    btnLogout.onclick = function(room){
        leaveRoom(room);
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





});