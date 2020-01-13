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

    socket.on('my response', function(msg){
        console.log(msg)
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


});