import get_require from '@/utils/get_require'
import Error from '@/components/app/Error'

export default async function svelte_component_mounter(window) {
  const observer = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      mutation.addedNodes.forEach(node => {
        if (node.classList && node.classList.contains('svelte')) svelte_component_mount_from_dom(window, node)
      })
    })
  })
  observer.observe(document, { subtree: true, childList: true })
  document.querySelectorAll('.svelte').forEach(node => svelte_component_mount_from_dom(window, node))
}


function svelte_component_mount_from_dom(window, target) {
  target.childNodes.forEach(childNode => {
    if (childNode.nodeName === 'SCRIPT' && childNode.getAttribute('type') === 'application/json') {
      svelte_component_mount(window, target, childNode)
        .catch((e) => {
          console.error(e)
          const errorComponent = new Error({ target, props: { error: e.toString() } })
        })
        .finally(() => {
          target.classList.remove('loading')
        })
      return
    }
  })
}

async function svelte_component_mount(window, target, propsNode) {
  const { js_url, ...props } = JSON.parse(propsNode.textContent)
  const { default: Component } = await get_require(window, js_url)
  const currentChildren = [...target.children]
  const component = new Component({ target, props })
  for (const child of currentChildren) child.remove()
}
