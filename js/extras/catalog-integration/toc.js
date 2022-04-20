import { readable, writable } from 'svelte/store'

/**
 * Constuct a table of contents from a DOM
 *  tree based on header elements.
 */
function toc_store() {
  const { subscribe: subscribeRef, set: setRef } = writable()
  const { subscribe } = readable(undefined, set => {
    let observer
    return subscribeRef(
      ref => {
        if (ref === undefined) return
        observer = new MutationObserver(mutations => {
          // look through mutations and update update toc iff a header element was added/removed
          for (const mutation of mutations) {
            if (mutation.type !== 'childList') continue
            for (const e of [...mutation.addedNodes, ...mutation.removedNodes]) {
              if (e.tagName !== undefined && e.tagName.startsWith('H')) {
                set(
                  [...ref.querySelectorAll('h1,h2,h3,h4,h5,h6')]
                    .map(e => ({
                      h: e.tagName.slice(1),
                      textContent: e.textContent.replace(/ ¶$/, ''),
                      id: e.id,
                    }))
                    .filter(({ id }) => id)
                )
              }
            }
          }
        })
        observer.observe(ref, { childList: true, subtree: true })
      },
      () => {
        if (observer === undefined) return
        observer.disconnect()
      }
    )
  })
  return { subscribe, attach: setRef }
}

const toc = toc_store()
export default toc