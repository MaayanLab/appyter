<script>
  import * as MarkdownIt from 'markdown-it'
  import * as MarkdownItAnchor from 'markdown-it-anchor'
  import * as hljs from 'highlight.js'
  import slugify from '../../utils/slugify'

  export let data
  let rendered

  const md = new MarkdownIt({
    highlight: function (str, lang) {
      if (lang && hljs.getLanguage(lang)) {
        try {
          return hljs.highlight(lang, str).value
        } catch (__) {}
      }
      return ''
    }
  }).use(MarkdownItAnchor, {
    slugify,
    permalink: true,
  })
  $: rendered = md.render(data)
</script>

{@html rendered}
