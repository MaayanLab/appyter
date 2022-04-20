import { v4 as uuidv4 } from 'uuid'
import io from 'socket.io-client'
const socket = io({
  path: `${window._config.PREFIX}/socket.io/`,
  extraHeaders: { Authorization: uuidv4() },
})
export default socket