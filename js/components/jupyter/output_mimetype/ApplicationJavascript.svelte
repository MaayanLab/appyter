<script>
  import HTML from '@/components/HTML.svelte'
  import collapse from '@/utils/collapse.js'
  export let data
</script>

<HTML classes="output_javascript" data="<script>{collapse(data)}</script>" />
