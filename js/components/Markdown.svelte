<script>
  import * as MarkdownIt from 'markdown-it'
  import * as MarkdownItAnchor from 'markdown-it-anchor'
  import * as hljs from 'highlight.js'
  import slugify from '../utils/slugify'

  export let data
  let rendered

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
    permalink: true,
    slugify,
  })
  $: rendered = md.render(data)
</script>

{@html rendered}
