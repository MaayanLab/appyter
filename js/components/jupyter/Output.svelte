<script>
  import { onMount, tick } from 'svelte'
  import * as Markdown from './Markdown.svelte'
  import * as Ansi from './Ansi.svelte'
  import collapse from '../../utils/collapse.js'

  export let data
  export let ref

  let evaled = {}
  function eval_once(src) {
    if (evaled[src] === undefined) {
      evaled[src] = true
      eval(src)
    }
  }

  $: {
    if (ref) {
      const target = ref.getAttribute('data-target')
      if (target === 'application/json') {
        const src = collapse(data.data[target])
        ref.innerHTML = '<script>' + src + '\<\/script>'
        eval_once(src)
      } else if (target === 'text/html') {
        ref.innerHTML = collapse(data.data[target])
        ref.querySelectorAll('script').forEach((el) => {
          const src = el.innerHTML
          eval_once(src)
        })
      } else {
        console.error('Unrecognized type')
      }
    }
  }
</script>

<div class="output_area">
  <div class="prompt"></div>
  {#if data}
  <div class="output_subarea">
    {#if data.output_type === 'stream'}
      <div class="output_stream output_{data.name} output_text">
        <Ansi data={collapse(data.text)} />
      </div>
    {:else if data.output_type === 'execute_result'}
      <div class="output_html rendered_html output_execute_result">
        {#if data.data['text/html']}
          <div bind:this={ref} data-target="text/html"></div>
        {:else}
          <Ansi data={collapse(data.data['text/plain'])} />
        {/if}
      </div>
    {:else if data.output_type === 'display_data'}
      {#if data.data['image/png']}
        <div class="output_png">
          <img
            class="img-fluid"
            src="data:img/png;base64,{collapse(data.data['image/png'])}"
          />
        </div>
      {:else if data.data['text/html']}
        <div class="output_html rendered_html output_execute_result">
          <div bind:this={ref} data-target="text/html"></div>
        </div>
      {:else if data.data['text/markdown']}
        <div class="output_stream output_{data.name} output_markdown">
          <Markdown data={collapse(data.data['text/markdown'])} />
        </div>
      {:else if data.data['text/plain']}
        <div class="output_stream output_{data.name} output_text">
          <Ansi data={collapse(data.data['text/plain'])} />
        </div>
      {:else if data.data['application/javascript']}
        <div bind:this={ref} data-target="application/javascript"></div>
      {:else}
        {JSON.stringify(data)}
      {/if}
    {:else if data.output_type === 'error'}
      <div class="output_subarea output_test output_error">
        {#if data.traceback !== undefined}
          <Ansi data="{collapse(data.traceback, '\n')}" />
        {:else}
          <Ansi data="{data.ename}: {data.evalue}" />
        {/if}
      </div>
    {:else}
      {JSON.stringify(data)}
    {/if}
  </div>
  {/if}
</div>