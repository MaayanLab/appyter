<script>
  import * as Output from "./Output.svelte"
  import collapse from '../../utils/collapse.js'

  export let data = []

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
        yield output
      }
    }
    for (const stream in streams) {
      yield streams[stream]
    }
  }
</script>

<div class="output_wrapper">
  <div class="output">
    {#each [...reduce_output_streams(data)] as output}
      <Output data={output} />
    {/each}
  </div>
</div>