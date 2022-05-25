<script>
  import TabField from '@/components/fields/TabField.svelte'
  import Lazy from '@/components/Lazy.svelte'

  export let args

  let tabArgs = {
    name: `${args.name}-type`,
    label: args.label,
    description: args.description,
    value: 'Upload',
    choices: [
      'Upload',
      window._config.EXTRAS.includes('catalog-integration') && 'Locate',
      'Passthrough'
    ].filter(choice => choice !== false),
  }
</script>

<TabField bind:args={tabArgs} let:tab={tab}>
  {#if tab === 'Upload'}
    <Lazy
      module={() => import('@/extras/file-field/Upload.svelte')}
      props={{
        args: {
          ...args,
          label: 'Choose file',
        }
      }}
    />
  {:else if window._config.EXTRAS.includes('catalog-integration') && tab === 'Locate'}
    <Lazy
      module={() => import('@/extras/catalog-integration/LocateFileField.svelte')}
      props={{ args }}
    />
  {:else if tab === 'Passthrough'}
    <Lazy
      module={() => import('@/extras/file-field/URI.svelte')}
      props={{
        args: {
          name: args.name,
          label: 'Uniform Resource Identifier',
          description: 'One of several supported identifiers for accessing your file',
          examples: Object.keys(args.examples || {}).reduce((agg, example) => (example.indexOf('://') !== -1) ? { ...agg, [example]: args.examples[example] } : agg, {}),
        },
      }}
    />
  {/if}
</TabField>
