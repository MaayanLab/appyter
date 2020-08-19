<script>
  import * as MarkdownIt from 'markdown-it'
  import * as hljs from 'highlight.js'

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
  })
  $: rendered = md.render(data)
</script>

{@html rendered}
