<script>
  import TextListField from '@/components/fields/TextListField.svelte';
  import ensure_string_list from '@/utils/ensure_string_list'

  export let args
</script>

<TextListField
  args={{
    ...args,
    default: ensure_string_list(args.default).join('\n'),
    value: ensure_string_list(args.value).join('\n')
  }}
/>
