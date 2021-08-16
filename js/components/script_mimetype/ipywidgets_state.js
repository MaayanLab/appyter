import get_require from '@/utils/get_require'

export default async function ipywidgets_state(el) {
  const manager = await get_require(window, '@appyter/ipywidgets-manager')
  manager.__models = await manager.set_state(JSON.parse(el.innerHTML))
  if (manager.__views_queued !== undefined) {
    for (const view of Object.keys(manager.__views_queued)) {
      await manager.__views_queued[view]()
    }
  }
}
