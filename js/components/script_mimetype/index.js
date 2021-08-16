import javascript from './javascript'

const script_mimetypes = {
  'application/javascript': javascript,
}

// These mimetypes can be safely ignored
const ignored_mimetypes = {
}

export { script_mimetypes, ignored_mimetypes }
