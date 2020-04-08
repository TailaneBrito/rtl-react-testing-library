// set starting value of user_name = none
if (!localStorage.getItem('username')){
    localStorage.setItem('username', 'undefined');
    localStorage.setItem('status', 'loggedOut')
    }

document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))

    //const  messageUserSession = document.getElementById('user_logged')
    const  messageUserLogged = document.getElementById('username')
    const  btnConnect = document.getElementById('send-button')
    const  formConnect = document.getElementById('user-login')
    const  selectRoomName = document.getElementById('room_name')
    const  btnLogout = document.getElementById('logout-btn')

    // inputting user_name
     //const user_name = prompt('What is your name?')

     var ask = true;
     while (ask){
        var user_name = prompt('What is your name?')

        if (user_name !== ''){
            document.querySelector("#username").innerHTML = username;
            localStorage.setItem('username', user_name);
            ask = false;
            break;
        }
     }

    messageUserLogged.outerHTML = localStorage.getItem('username')
    localStorage.setItem('username', name)

    messageUserLogged.value = name
    messageUserSession.value  = name

    //setting a name for h1
    document.querySelector("#username").innerHTML = localStorage.getItem('username');
    messageUserSession.setAttribute("value", name)
    messageUserLogged.setAttribute("disabled", true)

    var users = new Object()
    var users = {}

    var channel = {}

    // add users to user dict
    users.name = name
    print(users.name)
    users.room = selectRoomName.value

    //add the user to the storage
    document.querySelector('username').innerHTML = localStorage.getItem('user_name');
    console.log(localStorage.setItem('user_name'))

    socket.on('my response', function(msg){
        console.log(msg)
    })

    btnConnect.onclick = function(){
        get_user()
    }

    function get_user_input(){
        var ask = true;
        while (ask){
            var user_name = prompt('What is your name?')

            if (user_name !== ''){
                //document.querySelector("#username").innerHTML = username;
                localStorage.setItem('username', user_name);
                ask = false;
                break;
            }
         }
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