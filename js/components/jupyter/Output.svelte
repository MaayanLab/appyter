<script>
  import * as Prompt from './Prompt.svelte'
  import * as Markdown from '../Markdown.svelte'
  import * as Ansi from '../Ansi.svelte'
  import * as HTML from '../HTML.svelte'
  import collapse from '../../utils/collapse.js'

  export let index
  export let data
</script>

<div class="output_area">
  <Prompt
    index={index}
    prompt_type="output"
  />
  {#if data}
  <div class="output_subarea">
    {#if data.output_type === 'stream'}
      <div class="output_stream output_{data.name} output_text">
        <Ansi data={collapse(data.text)} />
      </div>
    {:else if data.output_type === 'execute_result'}
      {#if data.data['text/html']}
        <HTML
          classes="output_html rendered_html output_execute_result"
          data={collapse(data.data['text/html'])}
        />
      {:else}
        <div class="output_text output_execute_result">
          <Ansi data={collapse(data.data['text/plain'])} />
        </div>
      {/if}
    {:else if data.output_type === 'display_data'}
      {#if data.data['image/png']}
        <div class="output_png">
          <img
            class="img-fluid"
            src="data:img/png;base64,{collapse(data.data['image/png'])}"
          />
        </div>
      {:else if data.data['text/html']}
        <HTML
          classes="output_html rendered_html output_execute_result"
          data={collapse(data.data['text/html'])}
        />
      {:else if data.data['text/markdown']}
        <div class="output_stream output_{data.name} output_markdown">
          <Markdown data={collapse(data.data['text/markdown'])} />
        </div>
      {:else if data.data['text/plain']}
        <div class="output_stream output_{data.name} output_text">
          <Ansi data={collapse(data.data['text/plain'])} />
        </div>
      {:else if data.data['application/javascript']}
        <HTML data="<script>{collapse(data.data['application/javascript'])}</script>" />
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