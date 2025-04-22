let evaled = {}
function try_eval_once(src) {
  if (evaled[src] === undefined) {
    evaled[src] = true
    try {
      (new Function(src))()
    } catch (e) {
      const error_data = {
        type: 'javascript-cell',
        error: e.toString(),
      }
      report_error(error_data)
    }
  }
}

export default async function JavascriptHandler(el) {
  try_eval_once(el.innerHTML)
}
