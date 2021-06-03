<script>
  import Output from '@/components/jupyter/Output.svelte'
  import Loader from '@/components/Loader.svelte'
  import Prompt from '@/components/jupyter/Prompt.svelte'
  import collapse from '@/utils/collapse.js'
  import hash from '@/utils/hash.js'

  export let data = []
  export let index
  export let loading

  function *reduce_output_streams(outputs) {
    let streams = {}
    for (const output of outputs) {
      if (output.output_type === 'stream') {
        if (streams[output.name] === undefined) {
          const output_text = collapse(output.text, '\n')
          streams[output.name] = {...output, text: output_text}
        } else {
          const output_text = collapse(output.text, '\n')
          if (output_text.startsWith('\r')) streams[output.name].text = output_text
          else streams[output.name].text += output_text
        }
      } else {
        yield {...output, hash: hash(output)}
      }
    }
    for (const stream in streams) {
      streams[stream].text = streams[stream].text.replace(/^\r/, '').replace(/(\r?\n)+$/, '')
      if (streams[stream].text) {
        yield {...streams[stream], hash: hash(streams[stream])}
      }
    }
  }
</script>

<div class="output_wrapper">
  <div class="output">
    {#if index === loading}
      <div class="output_area">
        <Prompt
          index="{index}-loader"
          prompt_type="output"
        />
        <div class="output_subarea">
          <Loader />
        </div>
      </div>
    {/if}
    {#each [...reduce_output_streams(data)] as output, output_index (output.hash)}
      <div class="output_area">
        <Prompt
          index="{index}-{output_index}"
          prompt_type="output"
        />
        <div class="output_subarea">
          <Output data={output} />
        </div>
      </div>
    {/each}
  </div>
</div>
