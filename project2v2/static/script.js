document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))

    const name = prompt('Wat is your name?')
    $("input.username").attr("value", name);
    $("input.username").attr("disabled", true);

    const users = {}


    socket.on('connect', function() {

        socket.emit('my event', {
            data: 'User Connected ' + name
        })

        var form = $('form').on('submit', function(e) {
            e.preventDefault()

            let user_name = $( 'input.username' ).val()
            let user_input = $( 'input.message' ).val()


            socket.emit('my event', {
                user_name : user_name,
                message : user_input
            })

            $('input.message').val('').focus()

        })
    })

    socket.on('new-user', function(name){
       console.log(name)
       users[socket.id] = name
       socket.broadcast.emit('user-connected', name)
    })

    socket.on('my response', function(msg){
        console.log(msg)
        if( typeof msg.user_name !== 'undefined') {
            $('h3').remove()
            $('div.message_holder').append('<div><b style="color:#000">'+msg.user_name+
            '</b>'+": "+msg.message+'</div>')
        }
    })

    socket.on('user-connected', name => {
      appendMessage(`${name} connected`)
    })

    socket.on('user-disconnected', name => {
      appendMessage(`${name} disconnected`)
    })

    function appendMessage(message) {
      const messageElement = document.createElement('div')
      messageElement.innerText = message
      messageContainer.append(messageElement)
      //$('div.message_holder').append(messageElement)
    }


    /**

    const messageContainer = document.getElementById('message-container')
    const messageForm = document.getElementById('send-container')
    const messageInput = document.getElementById('message-input')

    const name = prompt('What is your name?')
    appendMessage('you joined')

    socket.emit('new-user', name)

    socket.on('chat-message', data => {
      appendMessage(`${data.name}: ${data.message}`)
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
      appendMessage(`You: ${message}`)
      socket.emit('send-chat-message', message)
      messageInput.value = ''
    })

    function appendMessage(message) {
      const messageElement = document.createElement('div')
      messageElement.innerText = message
      messageContainer.append(messageElement)
    }
    **/
});