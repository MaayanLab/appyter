import MarkdownIt from 'markdown-it'
import MarkdownItAnchor from 'markdown-it-anchor'
import slugify from '@/utils/slugify'

import hljs from 'highlight.js/lib/core'
import hljs_python from 'highlight.js/lib/languages/python'
import hljs_markdown from 'highlight.js/lib/languages/markdown'
import hljs_bash from 'highlight.js/lib/languages/bash'
hljs.registerLanguage('python', hljs_python)
hljs.registerLanguage('markdown', hljs_markdown)
hljs.registerLanguage('bash', hljs_bash)

const slugs = {}
function uniqueSlug (slug) {
  let uniq = slug
  let i = 1

  while (Object.prototype.hasOwnProperty.call(slugs, uniq)) {
    uniq = `${slug}-${i}`
    i += 1
  }
  slugs[uniq] = true
  return uniq
}

const md = new MarkdownIt({
  html: true,
  highlight: function (code, language) {
    if (language && hljs.getLanguage(language)) {
      try {
        return hljs.highlight(code, { language }).value
      } catch (__) {}
    }
    return ''
  }
}).use(MarkdownItAnchor, {
  permalink: MarkdownItAnchor.permalink.linkInsideHeader({
    symbol: `¶`,
    placement: 'after',
  }),
  slugify: label => uniqueSlug(slugify(label)),
})

export default md
