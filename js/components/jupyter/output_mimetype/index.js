import ApplicationJavascript from './ApplicationJavascript.svelte'
import ImagePng from './ImagePng.svelte'
import ImageSvgXml from './ImageSvgXml.svelte'
import TextHtml from './TextHtml.svelte'
import TextMarkdown from './TextMarkdown.svelte'
import TextPlain from './TextPlain.svelte'

const output_mimetypes = {
  'application/javascript': ApplicationJavascript,
  'image/png': ImagePng,
  'image/svg+xml': ImageSvgXml,
  'text/html': TextHtml,
  'text/markdown': TextMarkdown,
  'text/plain': TextPlain,
}
export default output_mimetypes
