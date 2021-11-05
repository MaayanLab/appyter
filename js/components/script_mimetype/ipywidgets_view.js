import get_require from '@/utils/get_require'

async function ensure_view(manager, { widgetViewObject, el }) {
  const model_id = widgetViewObject.model_id;
  if (manager.__views === undefined) manager.__views = {}
  if (model_id in manager.__views) {
    const view = manager.__views[model_id]
    await manager.display_view(view, el.previousElementSibling)
  } else {
    if (manager.__models === undefined) manager.__models = []
    const model = manager.__models.find(item => item.model_id == model_id)
    if (model === undefined) {
      if (manager.__views_queued === undefined) manager.__views_queued = {}
      manager.__views_queued[model_id] = () => ensure_view(manager, { widgetViewObject, el })
    } else {
      const prev = el.previousElementSibling;
      if (
        prev &&
        prev.tagName === 'img' &&
        prev.classList.contains('jupyter-widget')
      ) {
        el.parentElement.removeChild(prev);
      }
      const widgetTag = document.createElement('div');
      widgetTag.className = 'widget-subarea';
      el.parentElement.insertBefore(widgetTag, el);
      const view = await manager.create_view(model);
      manager.__views[model_id] = view;
      await manager.display_view(view, widgetTag);
      if (manager.__views_queued !== undefined && model_id in manager.__views_queued) {
        delete manager.__views_queued[model_id]
      }
    }
  }
}

export default async function ipyidgets_view(el) {
  const manager = await get_require(window, '@appyter/ipywidgets-manager')
  const widgetViewObject = JSON.parse(el.innerHTML);
  await ensure_view(manager, { widgetViewObject, el })
}
