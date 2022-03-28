import io from 'socket.io-client'
const socket = io({ path: window._config.PREFIX + '/socket.io/' })
export default socket