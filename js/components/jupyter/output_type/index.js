import OutputDisplayData from './OutputDisplayData.svelte'
import OutputError from './OutputError.svelte'
import OutputExecuteResult from './OutputExecuteResult.svelte'
import OutputStream from './OutputStream.svelte'

const output_types = {
  display_data: OutputDisplayData,
  error: OutputError,
  execute_result: OutputExecuteResult,
  stream: OutputStream,
}
export default output_types
