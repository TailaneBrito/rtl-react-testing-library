const io = require('socket.io')(5000)
//const io = require('socket.io')(location.protocol + '//' + document.domain + ':' + location.port)

const users = {}

io.on('connection', socket => {

  socket.emit('news', {hello: 'world'})

  socket.on('My other event', data => {
    console.log(data)
  })


  socket.on('new-user', name => {
    // user id equal to the socket id
    users[socket.id] = name
    socket.broadcast.emit('user-connected', name)
  })

  socket.on('send-chat-message', message => {
    socket.broadcast.emit('chat-message', { message: message, name: users[socket.id] })
  })

  socket.on('disconnect', () => {
    socket.broadcast.emit('user-disconnected', users[socket.id])
    delete users[socket.id]
  })
})