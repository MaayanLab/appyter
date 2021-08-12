import ApplicationJavascript from './ApplicationJavascript.svelte'
import ImagePng from './ImagePng.svelte'
import ImageSvgXml from './ImageSvgXml.svelte'
import TextHtml from './TextHtml.svelte'
import TextMarkdown from './TextMarkdown.svelte'
import TextPlain from './TextPlain.svelte'

// NOTE: ordering matters, most 'preferred' mimetypes should appear first.
const output_mimetypes = {
  'image/svg+xml': ImageSvgXml,
  'image/png': ImagePng,
  'text/html': TextHtml,
  'application/javascript': ApplicationJavascript,
  'text/markdown': TextMarkdown,
  'text/plain': TextPlain,
}

// These mimetypes can be safely ignored
const ignored_mimetypes = {
  'application/vnd.bokehjs_load.v0+json': true,
  'application/vnd.bokehjs_exec.v0+json': true,
}

export { output_mimetypes, ignored_mimetypes }
