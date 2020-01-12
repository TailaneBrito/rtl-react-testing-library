document.addEventListener('DOMContentLoaded', () => {


    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))

    const messageUserLogged = document.getElementById('username')
    const  messageUserSession = document.getElementById('user_logged')

    // inputting user_name
    const name = prompt('What is your name?')

    messageUserLogged.value = name
    messageUserSession.value  = name
    messageUserSession.setAttribute("value", name)
    messageUserLogged.setAttribute("disabled", true)

    var users = new Object()
    var users = {}

    users.name = name
    console.log(users.name)

    socket.on('connect', function() {
      // adding user entrees
      socket.emit('get-user', {
            "user_name" :  users.name
            })
    })


    function appendUser(user){
        users.push(name)
        return users
    }


    function appendMessage(message) {
      const messageElement = document.createElement('div')
      messageElement.innerText = message
      messageContainer.append(messageElement)
    }


    socket.on('my response', function(msg){
        console.log(msg)
    })

});