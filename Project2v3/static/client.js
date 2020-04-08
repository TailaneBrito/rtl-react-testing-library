document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect((location.protocol + '//' + document.domain + ':' + location.port))
    var users = {}

    const name = prompt('What is your name?')
    $("input.username").attr("value", name);
    $("input.username").attr("disabled", true);

    socket.on('connect', function(){
      socket.emit('send_message', {
          //users[socket.id] = name
          data : 'user connected'
        })
    })

    var form = $( 'form' ).on( 'submit', function(e){
      e.preventDefault()
      let user_name = name
      let user_message = $( 'input.message' ).val()

      socket.emit('send_message', {user : user_name, msg : user_message})

      $( 'input.message-input' ).val( ' ' ).focus()

      //capture message
      socket.on('post_message', function(msg){
        if( typeof msg.user_name !== 'undefined' ){
          $( 'h1' ).remove()
          $( 'div.msg-wrapper' ).append( '<div class="msgbbl"><b> ' +msg.user + '</b> ' +msg.msg +'</div>')
        }
        console.log(msg)
      })
    })
});