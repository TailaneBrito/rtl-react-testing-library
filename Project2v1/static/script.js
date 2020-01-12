document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))
    var users = {}


    const messageContainer = document.getElementById('message-container')
    const messageForm = document.getElementById('send-container')
    const messageInput = document.getElementById('message-input')
    const messageUser = document.getElementById('username').getAttribute('value')
    const name = document.getElementById('users-connected').getAttribute('name')

    //const name = messageUser

    //const name = prompt('What is your name?')
    //messageUser.value = messageUser
    //messageUser.setAttribute("disabled", true)

    socket.emit('new-user', name)
    appendMessage('You joined')

    socket.on('connect', function() {

        socket.emit('my event', {
            data : 'User connected'
        })
    })
    /*
    socket.on('connect', function(){
        //adding users to the dictionary as soon as they connect
        socket.emit('my event', {
            data : 'User Connected!'
        })
    })
    */

    socket.on('new-user', name => {
      appendMessage(`user ${name}`)
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

      // getting the user name and sending it
      let user_name = name
      //socket.emit('res_user_name', user_name)

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

    function appendUsers(name){

        users.push({
            user_key : 'key',
            user_name : name
        })
    }

    // LOAD PAGE FUNCTION
    function loadlink(){
        $('users-connected').load('script.js',function () {
            $(this).unwrap();
        });
    }

    loadlink(); // This will run on page load

    setInterval(function(){
        loadlink() // this will run after every 5 seconds
    }, 5000);


});