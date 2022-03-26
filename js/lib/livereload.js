export default async function livereload(window) {
  const { default: socket } = await import('@/lib/socket')
  let first_connect = true
  socket.on('connect', () => {
    if (first_connect) {
      console.debug('connected')
      first_connect = false
    } else {
      console.debug('reconnect')
      window.location.reload()
    }
  })
  socket.on('livereload', (data) => {
    console.debug('livereload')
    window.location.reload()
  })
}
