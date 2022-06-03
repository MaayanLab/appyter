<script>
  import Lazy from '@/components/Lazy.svelte';
  import StringField from '@/components/fields/StringField.svelte';
  import TextListField from '@/components/fields/TextListField.svelte';
  import ensure_string_list from '@/utils/ensure_string_list'

  export let args
  let {name: _, ...stringArgs} = {
    ...args,
    description: 'One of several supported identifiers for accessing your file',
    hint: 'e.g. drs://yourhost.com/yourid...',
    constraint: '^(drs|s3|gs|ftp|http|https)://.+$',
    feedback: 'Supported protocols include: drs (GA4GH), s3, gs, ftp, http, & https',
  }
  $: args.value = ensure_string_list(stringArgs.value).map(value => value.replace(/^(.+)\/(.+?)$/g, '$1/$2#$2')).join('\n')
</script>

<Lazy
  module={() => import('@/components/fields/DescriptionField.svelte')}
  children
>
  <span style="font-weight: 500">URI Passthrough</span>: This allows you to pass the file through a number of different URI protocols. Supported protocols include: drs (GA4GH), s3, gs, ftp, http, & https
</Lazy>

{#if args.multiple}
  <TextListField bind:args={stringArgs} />
{:else}
  <StringField bind:args={stringArgs} />
{/if}

<textarea
  type="text"
  class="hidden"
  name={args.name}
  value={args.value}
/>
