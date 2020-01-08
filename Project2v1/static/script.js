document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))
    var users = {}

    //const socket = io('http://localhost:5000')
    const messageContainer = document.getElementById('message-container')
    const messageForm = document.getElementById('send-container')
    const messageInput = document.getElementById('message-input')
    const messageUser = document.getElementById('username')

    const name = prompt('What is your name?')


    messageUser.value = name
    messageUser.setAttribute("disabled", true)

    socket.emit('new-user', name)
    appendMessage('You joined')

    socket.on('connect', function(){
        socket.emit('my event', {
            data : 'User Connected!'
        })

        socket.emit('request_user_name', {
            user_name : name
        })
    })

    socket.on('new-user', name => {
      appendMessage(`user ${name} connected...`)
    })

    socket.on('chat-message', data => {
      appendMessage(`${data.user_name}: ${data.message}`)
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

      //appendMessage(`${name}: ${message}`)
      socket.emit('send-chat-message', {
            user_name : name ,
            message : message
        }
      )

      //const user_id = users[socket.id]
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

    socket.on('post_message', function(msg){
        console.log(msg)
        if( typeof msg.user_name !== 'undefined'){
            $('h3').remove()
            const messageElement = document.createElement('div')
            messageElement.innerText = msg.user + " : " + msg
            messageContainer.append(messageElement)
         }
    })

});