import ApplicationJavascript from './ApplicationJavascript.svelte'
import ImagePng from './ImagePng.svelte'
import TextHtml from './TextHtml.svelte'
import TextMarkdown from './TextMarkdown.svelte'
import TextPlain from './TextPlain.svelte'

const output_mimetypes = {
  'application/javascript': ApplicationJavascript,
  'image/png': ImagePng,
  'text/html': TextHtml,
  'text/markdown': TextMarkdown,
  'text/plain': TextPlain,
}
export default output_mimetypes
