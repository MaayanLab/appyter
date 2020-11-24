export function setup_chunking(socket) {
  let chunks = {}
  socket.on('chunked', ({ id, event, chunk, total, data }) => {
    console.debug(`${id}: Received chunked packet ${chunk+1} / ${total}`)
    if (chunks[id] === undefined) {
      chunks[id] = {}
    }
    chunks[id][chunk] = data
    if (Object.keys(chunks[id]).length == total) {
      console.debug(`${id}: Collecting chunks`)
      let chunked = ''
      for (let n = 0; n < total; n++) {
        chunked += chunks[id][n]
        delete chunks[id][n]
      }
      // TODO: verify hash
      try {
        let data = JSON.parse(chunked)
        console.debug(`${id}: Emitting event ${event}`)
        for (const k in socket._callbacks['$'+event] || {}) {
          socket._callbacks['$' + event][k](data)
        }
      } catch (e) {
        console.error(e)
      }
    }
  })
}