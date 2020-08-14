<script>
  import * as Markdown from './Markdown.svelte'

  export let data
</script>

<div class="output_area">
  <div class="prompt"></div>
  {#if data}
  <div class="output_subarea">
    {#if data.output_type === 'stream'}
      <div class="output_stream output_{data.name} output_text">
        {data.text}
      </div>
    {:else if data.output_type === 'execute_result'}
      <div class="output_html rendered_html output_execute_result">
        {#if data.data['text/html']}
          {@html data.data['text/html']}
        {:else}
          {data.data['text/plain']}
        {/if}
      </div>
    {:else if data.output_type === 'display_data'}
      {#if data.data['image/png']}
        <div class="output_png">
          <img
            class="img-fluid"
            src="data:img/png;base64,{data.data['image/png']}"
          />
        </div>
      {:else if data.data['text/html']}
        <div class="output_html rendered_html output_execute_result">
          {@html data.data['text/html']}
        </div>
      {:else if data.data['text/markdown']}
        <div class="output_stream output_{data.name} output_markdown">
          <Markdown data={data.data['text/markdown']} />
        </div>
      {:else if data.data['text/plain']}
        <div class="output_stream output_{data.name} output_text">
          <pre>{data.data['text/plain']}</pre>
        </div>
      {:else if data.data['application/javascript']}
        {@html '<script>'+data.data['application/javascript']+'</script>'}
      {:else}
        {JSON.stringify(data)}
      {/if}
    {:else if data.output_type === 'error'}
      <div class="output_subarea output_test output_error">
        <pre>
          {data.ename}: {data.evalue}<br />
          {data.traceback}
        </pre>
      </div>
    {:else}
      {JSON.stringify(data)}
    {/if}
  </div>
  {/if}
</div>