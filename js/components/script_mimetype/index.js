import javascript from './javascript'
import ipywidgets_view from './ipywidgets_view'
import ipywidgets_state from './ipywidgets_state'

const script_mimetypes = {
  'application/javascript': javascript,
  'application/vnd.jupyter.widget-view+json': ipywidgets_view,
  'application/vnd.jupyter.widget-state+json': ipywidgets_state,
}

// These mimetypes can be safely ignored
const ignored_mimetypes = {
}

export { script_mimetypes, ignored_mimetypes }
