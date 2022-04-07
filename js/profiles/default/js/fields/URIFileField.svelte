<script>
  import Lazy from '@/components/Lazy.svelte';

  export let args
</script>

<Lazy
  module={() => import('@/components/fields/DescriptionField.svelte')}
  children
>
  <span style="font-weight: 500">URI Passthrough</span>: This allows you to pass the file through a number of different URI protocols. Supported protocols include: drs (GA4GH), s3, gs, ftp, http, & https
</Lazy>

<Lazy
  module={() => import('@/profiles/biojupies/js/fields/StringField.svelte')}
  props={{
    args: {
      ...args,
      description: 'One of several supported identifiers for accessing your file',
      hint: 'e.g. drs://yourhost.com/yourid...',
      constraint: '^(drs|s3|gs|ftp|http|https)://.+$',
      feedback: 'Supported protocols include: drs (GA4GH), s3, gs, ftp, http, & https',
    }
  }}
/>
