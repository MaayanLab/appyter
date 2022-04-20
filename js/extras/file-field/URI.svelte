<script>
import StringField from '@/components/fields/StringField.svelte';

  import Lazy from '@/components/Lazy.svelte';

  export let args
  let stringArgs = {
    ...args,
    name: `${args.name}-string`,
    description: 'One of several supported identifiers for accessing your file',
    hint: 'e.g. drs://yourhost.com/yourid...',
    constraint: '^(drs|s3|gs|ftp|http|https)://.+$',
    feedback: 'Supported protocols include: drs (GA4GH), s3, gs, ftp, http, & https',
  }
  $: args.value = (stringArgs.value || '').replace(/^(.+)\/(.+?)$/g, '$1/$2#$2')
</script>

<Lazy
  module={() => import('@/components/fields/DescriptionField.svelte')}
  children
>
  <span style="font-weight: 500">URI Passthrough</span>: This allows you to pass the file through a number of different URI protocols. Supported protocols include: drs (GA4GH), s3, gs, ftp, http, & https
</Lazy>

<StringField bind:args={stringArgs} />

<input
  type="text"
  class="hidden"
  name={args.name}
  value={args.value}
/>
