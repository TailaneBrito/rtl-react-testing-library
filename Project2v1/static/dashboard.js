document.addEventListener('DOMContentLoaded', () => {


    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))

    const messageUserLogged = document.getElementById('username')
    const  messageUserSession = document.getElementById('user_logged')
    const  messageChannel = document.getElementById('channel')

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

    // add channel and users to channel dict
    channel.name = messageChannel.value
    channel.user = users.name

    console.log(users.name)

    socket.on('connect', function() {
      // adding user entrees
      socket.emit('get-user', {
            "user_name" :  users.name
            })

      socket.emit('get-channel', {
            "channel" : channel.name,
            "user" : channel.user
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