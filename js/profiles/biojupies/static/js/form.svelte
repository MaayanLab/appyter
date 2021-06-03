<script>
  import SSRField from '@/components/app/SSRField.svelte'
  import SectionField from './fields/SectionField.svelte'
  import Loader from '@/components/Loader.svelte'
  export let extras
  export let debug
  export let fields = []

  let submitting = false
  let error
  let orphaned_fields
  $: orphaned_fields = fields.filter(field => field.type !== 'section' && !field.args.section)

  async function onSubmit(evt) {
    try {
      submitting = true
      const formData = new FormData(evt.target)
      const res = await fetch(window.location.href, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
        },
        body: formData,
      })
      if (res.status === 406) {
        const { error: _error } = await res.json()
        error = _error
      } else {
        const { session_id } = await res.json()
        error = undefined
        window.location.href = `${window.location.href.replace(/\/$/, '')}/${session_id}/`
      }
    } catch (e) {
      error = e.toString()
    } finally {
      submitting = false
    }
  }
</script>

<form
  method="POST"
  enctype="multipart/form-data"
  action="#"
  on:submit|preventDefault={onSubmit}
>
  {#if orphaned_fields.length > 0}
    <SectionField
      field="SectionField"
      args={{
        name: '_primary',
        section: null,
        title: 'Customize Your Notebook',
        subtitle: 'Customize your notebook',
      }}
      fields={orphaned_fields}
    />
  {/if}
  {#each fields.filter(field => field.type === 'section') as field}
    {#if field.field === 'SectionField'}
      <SSRField
        field={field.field}
        args={field.args}
        fields={fields.filter(_field => _field.args.section === field.args.name)}
      />
    {/if}
  {/each}
  <div class="row">
    <div class="col-sm-12">
      &nbsp;
    </div>
    {#if error !== undefined}
    <div class="col-sm-12 alert alert-danger">
      {error}
    </div>
    {/if}
    <div class="col-sm-12 text-center">
      {#if submitting}
        <Loader />
      {:else}
        <input
          class="btn navigate white border-custom bg-blue nodecoration"
          type="submit"
          value="Submit"
        />
      {/if}
    </div>
  </div>
</form>
