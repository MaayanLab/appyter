(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else {
		var a = factory();
		for(var i in a) (typeof exports === 'object' ? exports : root)[i] = a[i];
	}
})(self, function() {
return /******/ (function() { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./node_modules/svelte-hmr/runtime/hot-api.js":
/*!****************************************************!*\
  !*** ./node_modules/svelte-hmr/runtime/hot-api.js ***!
  \****************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "makeApplyHmr": function() { return /* binding */ makeApplyHmr; }
/* harmony export */ });
/* harmony import */ var _proxy_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./proxy.js */ "./node_modules/svelte-hmr/runtime/proxy.js");
/* eslint-env browser */

const logPrefix = '[HMR:Svelte]'; // eslint-disable-next-line no-console

const log = (...args) => console.log(logPrefix, ...args);

const domReload = () => {
  // eslint-disable-next-line no-undef
  const win = typeof window !== 'undefined' && window;

  if (win && win.location && win.location.reload) {
    log('Reload');
    win.location.reload();
  } else {
    log('Full reload required');
  }
};

const replaceCss = (previousId, newId) => {
  if (typeof document === 'undefined') return false;
  if (!previousId) return false;
  if (!newId) return false; // svelte-xxx-style => svelte-xxx

  const previousClass = previousId.slice(0, -6);
  const newClass = newId.slice(0, -6); // eslint-disable-next-line no-undef

  document.querySelectorAll('.' + previousClass).forEach(el => {
    el.classList.remove(previousClass);
    el.classList.add(newClass);
  });
  return true;
};

const removeStylesheet = cssId => {
  if (cssId == null) return;
  if (typeof document === 'undefined') return; // eslint-disable-next-line no-undef

  const el = document.getElementById(cssId);
  if (el) el.remove();
  return;
};

const defaultArgs = {
  reload: domReload
};
const makeApplyHmr = transformArgs => args => {
  const allArgs = transformArgs({ ...defaultArgs,
    ...args
  });
  return applyHmr(allArgs);
};
let needsReload = false;

function applyHmr(args) {
  const {
    id,
    cssId,
    nonCssHash,
    reload = domReload,
    // normalized hot API (must conform to rollup-plugin-hot)
    hot,
    hotOptions,
    Component,
    acceptable,
    // some types of components are impossible to HMR correctly
    preserveLocalState,
    ProxyAdapter,
    emitCss
  } = args;
  const existing = hot.data && hot.data.record;
  const canAccept = acceptable && (!existing || existing.current.canAccept);
  const r = existing || (0,_proxy_js__WEBPACK_IMPORTED_MODULE_0__.createProxy)({
    Adapter: ProxyAdapter,
    id,
    Component,
    hotOptions,
    canAccept,
    preserveLocalState
  });
  const cssOnly = hotOptions.injectCss && existing && nonCssHash && existing.current.nonCssHash === nonCssHash;
  r.update({
    Component,
    hotOptions,
    canAccept,
    nonCssHash,
    cssId,
    previousCssId: r.current.cssId,
    cssOnly,
    preserveLocalState
  });
  hot.dispose(data => {
    // handle previous fatal errors
    if (needsReload || (0,_proxy_js__WEBPACK_IMPORTED_MODULE_0__.hasFatalError)()) {
      if (hotOptions && hotOptions.noReload) {
        log('Full reload required');
      } else {
        reload();
      }
    } // 2020-09-21 Snowpack master doesn't pass data as arg to dispose handler


    data = data || hot.data;
    data.record = r;

    if (!emitCss && cssId && r.current.cssId !== cssId) {
      if (hotOptions.cssEjectDelay) {
        setTimeout(() => removeStylesheet(cssId), hotOptions.cssEjectDelay);
      } else {
        removeStylesheet(cssId);
      }
    }
  });

  if (canAccept) {
    hot.accept(async arg => {
      const {
        bubbled
      } = arg || {}; // NOTE Snowpack registers accept handlers only once, so we can NOT rely
      // on the surrounding scope variables -- they're not the last version!

      const {
        cssId: newCssId,
        previousCssId
      } = r.current;
      const cssChanged = newCssId !== previousCssId; // ensure old style sheet has been removed by now

      if (!emitCss && cssChanged) removeStylesheet(previousCssId); // guard: css only change

      if ( // NOTE bubbled is provided only by rollup-plugin-hot, and we
      // can't safely assume a CSS only change without it... this means we
      // can't support CSS only injection with Nollup or Webpack currently
      bubbled === false && // WARNING check false, not falsy!
      r.current.cssOnly && (!cssChanged || replaceCss(previousCssId, newCssId))) {
        return;
      }

      const success = await r.reload();

      if ((0,_proxy_js__WEBPACK_IMPORTED_MODULE_0__.hasFatalError)() || !success && !hotOptions.optimistic) {
        needsReload = true;
      }
    });
  } // well, endgame... we won't be able to render next updates, even successful,
  // if we don't have proxies in svelte's tree
  //
  // since we won't return the proxy and the app will expect a svelte component,
  // it's gonna crash... so it's best to report the real cause
  //
  // full reload required
  //


  const proxyOk = r && r.proxy;

  if (!proxyOk) {
    throw new Error(`Failed to create HMR proxy for Svelte component ${id}`);
  }

  return r.proxy;
}

/***/ }),

/***/ "./node_modules/svelte-hmr/runtime/index.js":
/*!**************************************************!*\
  !*** ./node_modules/svelte-hmr/runtime/index.js ***!
  \**************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "makeApplyHmr": function() { return /* reexport safe */ _hot_api_js__WEBPACK_IMPORTED_MODULE_0__.makeApplyHmr; }
/* harmony export */ });
/* harmony import */ var _hot_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./hot-api.js */ "./node_modules/svelte-hmr/runtime/hot-api.js");


/***/ }),

/***/ "./node_modules/svelte-hmr/runtime/overlay.js":
/*!****************************************************!*\
  !*** ./node_modules/svelte-hmr/runtime/overlay.js ***!
  \****************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* eslint-env browser */
const removeElement = el => el && el.parentNode && el.parentNode.removeChild(el);

const ErrorOverlay = () => {
  let errors = [];
  let compileError = null;
  const errorsTitle = 'Failed to init component';
  const compileErrorTitle = 'Failed to compile';
  const style = {
    section: `
      position: fixed;
      top: 0;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 32px;
      background: rgba(0, 0, 0, .85);
      font-family: Menlo, Consolas, monospace;
      font-size: large;
      color: rgb(232, 232, 232);
      overflow: auto;
      z-index: 2147483647;
    `,
    h1: `
      margin-top: 0;
      color: #E36049;
      font-size: large;
      font-weight: normal;
    `,
    h2: `
      margin: 32px 0 0;
      font-size: large;
      font-weight: normal;
    `,
    pre: ``
  };

  const createOverlay = () => {
    const h1 = document.createElement('h1');
    h1.style = style.h1;
    const section = document.createElement('section');
    section.appendChild(h1);
    section.style = style.section;
    const body = document.createElement('div');
    section.appendChild(body);
    return {
      h1,
      el: section,
      body
    };
  };

  const setTitle = title => {
    overlay.h1.textContent = title;
  };

  const show = () => {
    const {
      el
    } = overlay;

    if (!el.parentNode) {
      const target = document.body;
      target.appendChild(overlay.el);
    }
  };

  const hide = () => {
    const {
      el
    } = overlay;

    if (el.parentNode) {
      overlay.el.remove();
    }
  };

  const update = () => {
    if (compileError) {
      overlay.body.innerHTML = '';
      setTitle(compileErrorTitle);
      const errorEl = renderError(compileError);
      overlay.body.appendChild(errorEl);
      show();
    } else if (errors.length > 0) {
      overlay.body.innerHTML = '';
      setTitle(errorsTitle);
      errors.forEach(({
        title,
        message
      }) => {
        const errorEl = renderError(message, title);
        overlay.body.appendChild(errorEl);
      });
      show();
    } else {
      hide();
    }
  };

  const renderError = (message, title) => {
    const div = document.createElement('div');

    if (title) {
      const h2 = document.createElement('h2');
      h2.textContent = title;
      h2.style = style.h2;
      div.appendChild(h2);
    }

    const pre = document.createElement('pre');
    pre.textContent = message;
    div.appendChild(pre);
    return div;
  };

  const addError = (error, title) => {
    const message = error && error.stack || error;
    errors.push({
      title,
      message
    });
    update();
  };

  const clearErrors = () => {
    errors.forEach(({
      element
    }) => {
      removeElement(element);
    });
    errors = [];
    update();
  };

  const setCompileError = message => {
    compileError = message;
    update();
  };

  const overlay = createOverlay();
  return {
    addError,
    clearErrors,
    setCompileError
  };
};

/* harmony default export */ __webpack_exports__["default"] = (ErrorOverlay);

/***/ }),

/***/ "./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js":
/*!**************************************************************!*\
  !*** ./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js ***!
  \**************************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "adapter": function() { return /* binding */ adapter; }
/* harmony export */ });
/* harmony import */ var svelte_internal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/internal */ "./node_modules/svelte/internal/index.mjs");
/* harmony import */ var _overlay_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./overlay.js */ "./node_modules/svelte-hmr/runtime/overlay.js");
/* global window, document */
 // NOTE from 3.38.3 (or so), insert was carrying the hydration logic, that must
// be used because DOM elements are reused more (and so insertion points are not
// necessarily added in order); then in 3.40 the logic was moved to
// insert_hydration, which is the one we must use for HMR

const svelteInsert = svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_hydration || svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert;

if (!svelteInsert) {
  throw new Error('failed to find insert_hydration and insert in svelte/internal');
}



const removeElement = el => el && el.parentNode && el.parentNode.removeChild(el);

const adapter = class ProxyAdapterDom {
  constructor(instance) {
    this.instance = instance;
    this.insertionPoint = null;
    this.afterMount = this.afterMount.bind(this);
    this.rerender = this.rerender.bind(this);
    this._noOverlay = !!instance.hotOptions.noOverlay;
  } // NOTE overlay is only created before being actually shown to help test
  // runner (it won't have to account for error overlay when running assertions
  // about the contents of the rendered page)


  static getErrorOverlay(noCreate = false) {
    if (!noCreate && !this.errorOverlay) {
      this.errorOverlay = (0,_overlay_js__WEBPACK_IMPORTED_MODULE_1__["default"])();
    }

    return this.errorOverlay;
  } // TODO this is probably unused now: remove in next breaking release


  static renderCompileError(message) {
    const noCreate = !message;
    const overlay = this.getErrorOverlay(noCreate);
    if (!overlay) return;
    overlay.setCompileError(message);
  }

  dispose() {
    // Component is being destroyed, detaching is not optional in Svelte3's
    // component API, so we can dispose of the insertion point in every case.
    if (this.insertionPoint) {
      removeElement(this.insertionPoint);
      this.insertionPoint = null;
    }

    this.clearError();
  } // NOTE afterMount CAN be called multiple times (e.g. keyed list)


  afterMount(target, anchor) {
    const {
      instance: {
        debugName
      }
    } = this;

    if (!this.insertionPoint) {
      this.insertionPoint = document.createComment(debugName);
    }

    svelteInsert(target, this.insertionPoint, anchor);
  }

  rerender() {
    this.clearError();
    const {
      instance: {
        refreshComponent
      },
      insertionPoint
    } = this;

    if (!insertionPoint) {
      throw new Error('Cannot rerender: missing insertion point');
    }

    refreshComponent(insertionPoint.parentNode, insertionPoint);
  }

  renderError(err) {
    if (this._noOverlay) return;
    const {
      instance: {
        debugName
      }
    } = this;
    const title = debugName || err.moduleName || 'Error';
    this.constructor.getErrorOverlay().addError(err, title);
  }

  clearError() {
    if (this._noOverlay) return;
    const overlay = this.constructor.getErrorOverlay(true);
    if (!overlay) return;
    overlay.clearErrors();
  }

}; // TODO this is probably unused now: remove in next breaking release

if (typeof window !== 'undefined') {
  window.__SVELTE_HMR_ADAPTER = adapter;
} // mitigate situation with Snowpack remote source pulling latest of runtime,
// but using previous version of the Node code transform in the plugin
// see: https://github.com/rixo/svelte-hmr/issues/27


/* harmony default export */ __webpack_exports__["default"] = (adapter);

/***/ }),

/***/ "./node_modules/svelte-hmr/runtime/proxy.js":
/*!**************************************************!*\
  !*** ./node_modules/svelte-hmr/runtime/proxy.js ***!
  \**************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createProxy": function() { return /* binding */ createProxy; },
/* harmony export */   "hasFatalError": function() { return /* binding */ hasFatalError; }
/* harmony export */ });
/* harmony import */ var _svelte_hooks_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./svelte-hooks.js */ "./node_modules/svelte-hmr/runtime/svelte-hooks.js");
/* eslint-env browser */

/**
 * The HMR proxy is a component-like object whose task is to sit in the
 * component tree in place of the proxied component, and rerender each
 * successive versions of said component.
 */

const handledMethods = ['constructor', '$destroy'];
const forwardedMethods = ['$set', '$on'];

const logError = (msg, err) => {
  // eslint-disable-next-line no-console
  console.error('[HMR][Svelte]', msg);

  if (err) {
    // NOTE avoid too much wrapping around user errors
    // eslint-disable-next-line no-console
    console.error(err);
  }
};

const posixify = file => file.replace(/[/\\]/g, '/');

const getBaseName = id => id.split('/').pop().split('.').slice(0, -1).join('.');

const capitalize = str => str[0].toUpperCase() + str.slice(1);

const getFriendlyName = id => capitalize(getBaseName(posixify(id)));

const getDebugName = id => `<${getFriendlyName(id)}>`;

const relayCalls = (getTarget, names, dest = {}) => {
  for (const key of names) {
    dest[key] = function (...args) {
      const target = getTarget();

      if (!target) {
        return;
      }

      return target[key] && target[key].call(this, ...args);
    };
  }

  return dest;
};

const isInternal = key => key !== '$$' && key.substr(0, 2) === '$$'; // This is intented as a somewhat generic / prospective fix to the situation
// that arised with the introduction of $$set in Svelte 3.24.1 -- trying to
// avoid giving full knowledge (like its name) of this implementation detail
// to the proxy. The $$set method can be present or not on the component, and
// its presence impacts the behaviour (but with HMR it will be tested if it is
// present _on the proxy_). So the idea here is to expose exactly the same $$
// props as the current version of the component and, for those that are
// functions, proxy the calls to the current component.


const relayInternalMethods = (proxy, cmp) => {
  // delete any previously added $$ prop
  Object.keys(proxy).filter(isInternal).forEach(key => {
    delete proxy[key];
  }); // guard: no component

  if (!cmp) return; // proxy current $$ props to the actual component

  Object.keys(cmp).filter(isInternal).forEach(key => {
    Object.defineProperty(proxy, key, {
      configurable: true,

      get() {
        const value = cmp[key];
        if (typeof value !== 'function') return value;
        return value && function (...args) {
          return value.apply(this, args);
        };
      }

    });
  });
};

const copyComponentProperties = (proxy, cmp, previous) => {
  //proxy custom methods
  const props = Object.getOwnPropertyNames(Object.getPrototypeOf(cmp));

  if (previous) {
    previous.forEach(prop => {
      delete proxy[prop];
    });
  }

  return props.filter(prop => {
    if (!handledMethods.includes(prop) && !forwardedMethods.includes(prop)) {
      Object.defineProperty(proxy, prop, {
        configurable: true,

        get() {
          return cmp[prop];
        },

        set(value) {
          // we're changing it on the real component first to see what it
          // gives... if it throws an error, we want to throw the same error in
          // order to most closely follow non-hmr behaviour.
          cmp[prop] = value;
        }

      });
      return true;
    }
  });
}; // everything in the constructor!
//
// so we don't polute the component class with new members
//


class ProxyComponent {
  constructor({
    Adapter,
    id,
    debugName,
    current,
    // { Component, hotOptions: { preserveLocalState, ... } }
    register
  }, options // { target, anchor, ... }
  ) {
    let cmp;
    let disposed = false;
    let lastError = null;

    const setComponent = _cmp => {
      cmp = _cmp;
      relayInternalMethods(this, cmp);
    };

    const getComponent = () => cmp;

    const destroyComponent = () => {
      // destroyComponent is tolerant (don't crash on no cmp) because it
      // is possible that reload/rerender is called after a previous
      // createComponent has failed (hence we have a proxy, but no cmp)
      if (cmp) {
        cmp.$destroy();
        setComponent(null);
      }
    };

    const refreshComponent = (target, anchor, conservativeDestroy) => {
      if (lastError) {
        lastError = null;
        adapter.rerender();
      } else {
        try {
          const replaceOptions = {
            target,
            anchor,
            preserveLocalState: current.preserveLocalState
          };

          if (conservativeDestroy) {
            replaceOptions.conservativeDestroy = true;
          }

          setComponent(cmp.$replace(current.Component, replaceOptions));
        } catch (err) {
          setError(err, target, anchor);

          if (!current.hotOptions.optimistic || // non acceptable components (that is components that have to defer
          // to their parent for rerender -- e.g. accessors, named exports)
          // are most tricky, and they havent been considered when most of the
          // code has been written... as a result, they are especially tricky
          // to deal with, it's better to consider any error with them to be
          // fatal to avoid odities
          !current.canAccept || err && err.hmrFatal) {
            throw err;
          } else {
            // const errString = String((err && err.stack) || err)
            logError(`Error during component init: ${debugName}`, err);
          }
        }
      }
    };

    const setError = err => {
      lastError = err;
      adapter.renderError(err);
    };

    const instance = {
      hotOptions: current.hotOptions,
      proxy: this,
      id,
      debugName,
      refreshComponent
    };
    const adapter = new Adapter(instance);
    const {
      afterMount,
      rerender
    } = adapter; // $destroy is not called when a child component is disposed, so we
    // need to hook from fragment.

    const onDestroy = () => {
      // NOTE do NOT call $destroy on the cmp from here; the cmp is already
      //   dead, this would not work
      if (!disposed) {
        disposed = true;
        adapter.dispose();
        unregister();
      }
    }; // ---- register proxy instance ----


    const unregister = register(rerender); // ---- augmented methods ----

    this.$destroy = () => {
      destroyComponent();
      onDestroy();
    }; // ---- forwarded methods ----


    relayCalls(getComponent, forwardedMethods, this); // ---- create & mount target component instance ---

    try {
      let lastProperties;

      const _cmp = (0,_svelte_hooks_js__WEBPACK_IMPORTED_MODULE_0__.createProxiedComponent)(current.Component, options, {
        onDestroy,
        onMount: afterMount,
        onInstance: comp => {
          // WARNING the proxy MUST use the same $$ object as its component
          // instance, because a lot of wiring happens during component
          // initialisation... lots of references to $$ and $$.fragment have
          // already been distributed around when the component constructor
          // returns, before we have a chance to wrap them (and so we can't
          // wrap them no more, because existing references would become
          // invalid)
          this.$$ = comp.$$;
          lastProperties = copyComponentProperties(this, comp, lastProperties);
        }
      });

      setComponent(_cmp);
    } catch (err) {
      const {
        target,
        anchor
      } = options;
      setError(err, target, anchor);
      throw err;
    }
  }

} // TODO we should probably delete statics that were added on the previous
// iteration, to avoid the case where something removed in the code would
// remain available, and HMR would produce a different result than non-HMR --
// namely, we'd expect a crash if a static method is still used somewhere but
// removed from the code, and HMR would hide that until next reload


const copyStatics = (component, proxy) => {
  //forward static properties and methods
  for (const key in component) {
    proxy[key] = component[key];
  }
};

const globalListeners = {};

const onGlobal = (event, fn) => {
  event = event.toLowerCase();
  if (!globalListeners[event]) globalListeners[event] = [];
  globalListeners[event].push(fn);
};

const fireGlobal = (event, ...args) => {
  const listeners = globalListeners[event];
  if (!listeners) return;

  for (const fn of listeners) {
    fn(...args);
  }
};

const fireBeforeUpdate = () => fireGlobal('beforeupdate');

const fireAfterUpdate = () => fireGlobal('afterupdate');

if (typeof window !== 'undefined') {
  window.__SVELTE_HMR = {
    on: onGlobal
  };
  window.dispatchEvent(new CustomEvent('svelte-hmr:ready'));
}

let fatalError = false;
const hasFatalError = () => fatalError;
/**
 * Creates a HMR proxy and its associated `reload` function that pushes a new
 * version to all existing instances of the component.
 */

function createProxy({
  Adapter,
  id,
  Component,
  hotOptions,
  canAccept,
  preserveLocalState
}) {
  const debugName = getDebugName(id);
  const instances = []; // current object will be updated, proxy instances will keep a ref

  const current = {
    Component,
    hotOptions,
    canAccept,
    preserveLocalState
  };
  const name = `Proxy${debugName}`; // this trick gives the dynamic name Proxy<MyComponent> to the concrete
  // proxy class... unfortunately, this doesn't shows in dev tools, but
  // it stills allow to inspect cmp.constructor.name to confirm an instance
  // is a proxy

  const proxy = {
    [name]: class extends ProxyComponent {
      constructor(options) {
        try {
          super({
            Adapter,
            id,
            debugName,
            current,
            register: rerender => {
              instances.push(rerender);

              const unregister = () => {
                const i = instances.indexOf(rerender);
                instances.splice(i, 1);
              };

              return unregister;
            }
          }, options);
        } catch (err) {
          // If we fail to create a proxy instance, any instance, that means
          // that we won't be able to fix this instance when it is updated.
          // Recovering to normal state will be impossible. HMR's dead.
          //
          // Fatal error will trigger a full reload on next update (reloading
          // right now is kinda pointless since buggy code still exists).
          //
          // NOTE Only report first error to avoid too much polution -- following
          // errors are probably caused by the first one, or they will show up
          // in turn when the first one is fixed ¯\_(ツ)_/¯
          //
          if (!fatalError) {
            fatalError = true;
            logError(`Unrecoverable error in ${debugName}: next update will trigger a ` + `full reload`);
          }

          throw err;
        }
      }

    }
  }[name]; // initialize static members

  copyStatics(current.Component, proxy);

  const update = newState => Object.assign(current, newState); // reload all existing instances of this component


  const reload = () => {
    fireBeforeUpdate(); // copy statics before doing anything because a static prop/method
    // could be used somewhere in the create/render call

    copyStatics(current.Component, proxy);
    const errors = [];
    instances.forEach(rerender => {
      try {
        rerender();
      } catch (err) {
        logError(`Failed to rerender ${debugName}`, err);
        errors.push(err);
      }
    });

    if (errors.length > 0) {
      return false;
    }

    fireAfterUpdate();
    return true;
  };

  const hasFatalError = () => fatalError;

  return {
    id,
    proxy,
    update,
    reload,
    hasFatalError,
    current
  };
}

/***/ }),

/***/ "./node_modules/svelte-hmr/runtime/svelte-hooks.js":
/*!*********************************************************!*\
  !*** ./node_modules/svelte-hmr/runtime/svelte-hooks.js ***!
  \*********************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createProxiedComponent": function() { return /* binding */ createProxiedComponent; }
/* harmony export */ });
/* harmony import */ var svelte_internal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/internal */ "./node_modules/svelte/internal/index.mjs");
/**
 * Emulates forthcoming HMR hooks in Svelte.
 *
 * All references to private component state ($$) are now isolated in this
 * module.
 */


const captureState = cmp => {
  // sanity check: propper behaviour here is to crash noisily so that
  // user knows that they're looking at something broken
  if (!cmp) {
    throw new Error('Missing component');
  }

  if (!cmp.$$) {
    throw new Error('Invalid component');
  }

  const {
    $$: {
      callbacks,
      bound,
      ctx
    }
  } = cmp;
  const state = cmp.$capture_state(); // capturing current value of props (or we'll recreate the component with the
  // initial prop values, that may have changed -- and would not be reflected in
  // options.props)

  const props = Object.assign({}, cmp.$$.props);
  Object.keys(cmp.$$.props).forEach(prop => {
    props[prop] = ctx[props[prop]];
  });
  return {
    ctx,
    callbacks,
    bound,
    state,
    props
  };
}; // restoreState
//
// It is too late to restore context at this point because component instance
// function has already been called (and so context has already been read).
// Instead, we rely on setting current_component to the same value it has when
// the component was first rendered -- which fix support for context, and is
// also generally more respectful of normal operation.
//


const restoreState = (cmp, restore) => {
  if (!restore) {
    return;
  }

  const {
    callbacks,
    bound
  } = restore;

  if (callbacks) {
    cmp.$$.callbacks = callbacks;
  }

  if (bound) {
    cmp.$$.bound = bound;
  } // props, props.$$slots are restored at component creation (works
  // better -- well, at all actually)

};

const get_current_component_safe = () => {
  // NOTE relying on dynamic bindings (current_component) makes us dependent on
  // bundler config (and apparently it does not work in demo-svelte-nollup)
  try {
    // unfortunately, unlike current_component, get_current_component() can
    // crash in the normal path (when there is really no parent)
    return (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.get_current_component)();
  } catch (err) {
    // ... so we need to consider that this error means that there is no parent
    //
    // that makes us tightly coupled to the error message but, at least, we
    // won't mute an unexpected error, which is quite a horrible thing to do
    if (err.message === 'Function called outside component initialization') {
      // who knows...
      return svelte_internal__WEBPACK_IMPORTED_MODULE_0__.current_component;
    } else {
      throw err;
    }
  }
};

const createProxiedComponent = (Component, initialOptions, {
  onInstance,
  onMount,
  onDestroy
}) => {
  let cmp;
  let last;
  let options = initialOptions;

  const isCurrent = _cmp => cmp === _cmp;

  const assignOptions = (target, anchor, restore, preserveLocalState) => {
    const props = Object.assign({}, options.props); // Filtering props to avoid "unexpected prop" warning
    // NOTE this is based on props present in initial options, but it should
    //      always works, because props that are passed from the parent can't
    //      change without a code change to the parent itself -- hence, the
    //      child component will be fully recreated, and initial options should
    //      always represent props that are currnetly passed by the parent

    if (options.props && restore.props) {
      for (const prop of Object.keys(options.props)) {
        if (restore.props.hasOwnProperty(prop)) {
          props[prop] = restore.props[prop];
        }
      }
    }

    if (preserveLocalState && restore.state) {
      if (Array.isArray(preserveLocalState)) {
        // form ['a', 'b'] => preserve only 'a' and 'b'
        props.$$inject = {};

        for (const key of preserveLocalState) {
          props.$$inject[key] = restore.state[key];
        }
      } else {
        props.$$inject = restore.state;
      }
    } else {
      delete props.$$inject;
    }

    options = Object.assign({}, initialOptions, {
      target,
      anchor,
      props,
      hydrate: false
    });
  };

  const instrument = targetCmp => {
    const createComponent = (Component, restore, previousCmp) => {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_current_component)(parentComponent || previousCmp);
      const comp = new Component(options);
      restoreState(comp, restore);
      instrument(comp);
      return comp;
    }; // `conservative: true` means we want to be sure that the new component has
    // actually been successfuly created before destroying the old instance.
    // This could be useful for preventing runtime errors in component init to
    // bring down the whole HMR. Unfortunately the implementation bellow is
    // broken (FIXME), but that remains an interesting target for when HMR hooks
    // will actually land in Svelte itself.
    //
    // The goal would be to render an error inplace in case of error, to avoid
    // losing the navigation stack (especially annoying in native, that is not
    // based on URL navigation, so we lose the current page on each error).
    //


    targetCmp.$replace = (Component, {
      target = options.target,
      anchor = options.anchor,
      preserveLocalState,
      conservative = false
    }) => {
      const restore = captureState(targetCmp);
      assignOptions(target, anchor, restore, preserveLocalState);
      const previous = cmp;

      if (conservative) {
        try {
          const next = createComponent(Component, restore, previous); // prevents on_destroy from firing on non-final cmp instance

          cmp = null;
          previous.$destroy();
          cmp = next;
        } catch (err) {
          cmp = previous;
          throw err;
        }
      } else {
        // prevents on_destroy from firing on non-final cmp instance
        cmp = null;

        if (previous) {
          // previous can be null if last constructor has crashed
          previous.$destroy();
        }

        cmp = createComponent(Component, restore, last);
        last = cmp;
      }

      return cmp;
    }; // NOTE onMount must provide target & anchor (for us to be able to determinate
    // 			actual DOM insertion point)
    //
    // 			And also, to support keyed list, it needs to be called each time the
    // 			component is moved (same as $$.fragment.m)


    if (onMount) {
      const m = targetCmp.$$.fragment.m;

      targetCmp.$$.fragment.m = (...args) => {
        const result = m(...args);
        onMount(...args);
        return result;
      };
    } // NOTE onDestroy must be called even if the call doesn't pass through the
    //      component's $destroy method (that we can hook onto by ourselves, since
    //      it's public API) -- this happens a lot in svelte's internals, that
    //      manipulates cmp.$$.fragment directly, often binding to fragment.d,
    //      for example


    if (onDestroy) {
      targetCmp.$$.on_destroy.push(() => {
        if (isCurrent(targetCmp)) {
          onDestroy();
        }
      });
    }

    if (onInstance) {
      onInstance(targetCmp);
    } // Svelte 3 creates and mount components from their constructor if
    // options.target is present.
    //
    // This means that at this point, the component's `fragment.c` and,
    // most notably, `fragment.m` will already have been called _from inside
    // createComponent_. That is: before we have a chance to hook on it.
    //
    // Proxy's constructor
    //   -> createComponent
    //     -> component constructor
    //       -> component.$$.fragment.c(...) (or l, if hydrate:true)
    //       -> component.$$.fragment.m(...)
    //
    //   -> you are here <-
    //


    if (onMount) {
      const {
        target,
        anchor
      } = options;

      if (target) {
        onMount(target, anchor);
      }
    }
  };

  const parentComponent = get_current_component_safe();
  cmp = new Component(options);
  instrument(cmp);
  return cmp;
};

/***/ }),

/***/ "./profiles/biojupies/js/fields/TextListField.svelte":
/*!***********************************************************!*\
  !*** ./profiles/biojupies/js/fields/TextListField.svelte ***!
  \***********************************************************/
/***/ (function(module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var svelte_internal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/internal */ "./node_modules/svelte/internal/index.mjs");
/* harmony import */ var _utils_ensure_list__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @/utils/ensure_list */ "./utils/ensure_list.js");
/* harmony import */ var _utils_re_full__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @/utils/re_full */ "./utils/re_full.js");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_loader_lib_hot_api_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./node_modules/svelte-loader/lib/hot-api.js */ "./node_modules/svelte-loader/lib/hot-api.js");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_hmr_runtime_proxy_adapter_dom_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js */ "./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js");
/* module decorator */ module = __webpack_require__.hmd(module);
/* profiles/biojupies/js/fields/TextListField.svelte generated by Svelte v3.46.4 */

const {
  Object: Object_1
} = svelte_internal__WEBPACK_IMPORTED_MODULE_0__.globals;


const file = "profiles/biojupies/js/fields/TextListField.svelte";

function get_each_context(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[6] = list[i];
  return child_ctx;
}

function get_each_context_1(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[9] = list[i];
  return child_ctx;
} // (29:16) {#if args.description}


function create_if_block_2(ctx) {
  let sup;
  let i;
  let sup_title_value;
  const block = {
    c: function create() {
      sup = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("sup");
      i = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("i");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(i, "class", "far fa-question-circle");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(i, file, 28, 92, 770);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(sup, "data-toggle", "tooltip");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(sup, "title", sup_title_value =
      /*args*/
      ctx[0].description);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(sup, file, 28, 38, 716);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, sup, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(sup, i);
    },
    p: function update(ctx, dirty) {
      if (dirty &
      /*args*/
      1 && sup_title_value !== (sup_title_value =
      /*args*/
      ctx[0].description)) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(sup, "title", sup_title_value);
      }
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(sup);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_2.name,
    type: "if",
    source: "(29:16) {#if args.description}",
    ctx
  });
  return block;
} // (43:6) {#each invalid as el}


function create_each_block_1(ctx) {
  let t0;
  let t1_value =
  /*el*/
  ctx[9].index + "";
  let t1;
  let t2;
  let t3_value =
  /*el*/
  ctx[9].value + "";
  let t3;
  let t4;
  let br;
  const block = {
    c: function create() {
      t0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("Line ");
      t1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(t1_value);
      t2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(": ");
      t3 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(t3_value);
      t4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(" contains unsupported characters");
      br = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("br");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(br, file, 43, 67, 1288);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, t0, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, t1, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, t2, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, t3, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, t4, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, br, anchor);
    },
    p: function update(ctx, dirty) {
      if (dirty &
      /*invalid*/
      4 && t1_value !== (t1_value =
      /*el*/
      ctx[9].index + "")) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_data_dev)(t1, t1_value);
      if (dirty &
      /*invalid*/
      4 && t3_value !== (t3_value =
      /*el*/
      ctx[9].value + "")) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_data_dev)(t3, t3_value);
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(t0);
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(t1);
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(t2);
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(t3);
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(t4);
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(br);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_each_block_1.name,
    type: "each",
    source: "(43:6) {#each invalid as el}",
    ctx
  });
  return block;
} // (48:4) {#if args.examples && Object.keys(args.examples).length > 0}


function create_if_block(ctx) {
  let div1;
  let span;
  let t0;
  let show_if = Object.keys(
  /*args*/
  ctx[0].examples).length > 1;
  let t1;
  let t2;
  let div0;
  let if_block = show_if && create_if_block_1(ctx);
  let each_value = Object.keys(
  /*args*/
  ctx[0].examples);
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_each_argument)(each_value);
  let each_blocks = [];

  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
  }

  const block = {
    c: function create() {
      div1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      span = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("span");
      t0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("Try example");
      if (if_block) if_block.c();
      t1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(":");
      t2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");

      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }

      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(span, "class", "d-table-cell mr-1 my-1 p-1 text-right");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_style)(span, "white-space", "nowrap");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(span, file, 49, 8, 1474);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "class", "d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div0, file, 52, 8, 1651);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div1, "class", "d-table-row");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div1, file, 48, 6, 1440);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div1, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, span);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(span, t0);
      if (if_block) if_block.m(span, null);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(span, t1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, t2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, div0);

      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].m(div0, null);
      }
    },
    p: function update(ctx, dirty) {
      if (dirty &
      /*args*/
      1) show_if = Object.keys(
      /*args*/
      ctx[0].examples).length > 1;

      if (show_if) {
        if (if_block) {} else {
          if_block = create_if_block_1(ctx);
          if_block.c();
          if_block.m(span, t1);
        }
      } else if (if_block) {
        if_block.d(1);
        if_block = null;
      }

      if (dirty &
      /*value, args, Object*/
      3) {
        each_value = Object.keys(
        /*args*/
        ctx[0].examples);
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_each_argument)(each_value);
        let i;

        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context(ctx, each_value, i);

          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(div0, null);
          }
        }

        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }

        each_blocks.length = each_value.length;
      }
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div1);
      if (if_block) if_block.d();
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_each)(each_blocks, detaching);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block.name,
    type: "if",
    source: "(48:4) {#if args.examples && Object.keys(args.examples).length > 0}",
    ctx
  });
  return block;
} // (51:21) {#if Object.keys(args.examples).length > 1}


function create_if_block_1(ctx) {
  let t;
  const block = {
    c: function create() {
      t = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("s");
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, t, anchor);
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(t);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_1.name,
    type: "if",
    source: "(51:21) {#if Object.keys(args.examples).length > 1}",
    ctx
  });
  return block;
} // (54:10) {#each Object.keys(args.examples) as example_name}


function create_each_block(ctx) {
  let span;
  let button;
  let t0_value =
  /*example_name*/
  ctx[6] + "";
  let t0;
  let t1;
  let mounted;
  let dispose;

  function click_handler() {
    return (
      /*click_handler*/
      ctx[5](
      /*example_name*/
      ctx[6])
    );
  }

  const block = {
    c: function create() {
      span = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("span");
      button = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("button");
      t0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(t0_value);
      t1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "type", "button");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "class", "text-btn");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(button, file, 55, 14, 1894);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(span, "class", "text-sm m-1 p-1");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_style)(span, "white-space", "nowrap");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(span, file, 54, 12, 1820);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, span, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(span, button);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(button, t0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(span, t1);

      if (!mounted) {
        dispose = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.listen_dev)(button, "click", click_handler, false, false, false);
        mounted = true;
      }
    },
    p: function update(new_ctx, dirty) {
      ctx = new_ctx;
      if (dirty &
      /*args*/
      1 && t0_value !== (t0_value =
      /*example_name*/
      ctx[6] + "")) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_data_dev)(t0, t0_value);
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(span);
      mounted = false;
      dispose();
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_each_block.name,
    type: "each",
    source: "(54:10) {#each Object.keys(args.examples) as example_name}",
    ctx
  });
  return block;
}

function create_fragment(ctx) {
  let div3;
  let div0;
  let t0_value =
  /*args*/
  ctx[0].label + "";
  let t0;
  let t1;
  let t2;
  let div2;
  let textarea;
  let textarea_name_value;
  let textarea_placeholder_value;
  let textarea_rows_value;
  let textarea_cols_value;
  let t3;
  let div1;
  let t4;
  let t5_value =
  /*args*/
  ctx[0].constraint + "";
  let t5;
  let t6;
  let t7;
  let show_if =
  /*args*/
  ctx[0].examples && Object.keys(
  /*args*/
  ctx[0].examples).length > 0;
  let mounted;
  let dispose;
  let if_block0 =
  /*args*/
  ctx[0].description && create_if_block_2(ctx);
  let each_value_1 =
  /*invalid*/
  ctx[2];
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_each_argument)(each_value_1);
  let each_blocks = [];

  for (let i = 0; i < each_value_1.length; i += 1) {
    each_blocks[i] = create_each_block_1(get_each_context_1(ctx, each_value_1, i));
  }

  let if_block1 = show_if && create_if_block(ctx);
  const block = {
    c: function create() {
      div3 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      t0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(t0_value);
      if (if_block0) if_block0.c();
      t1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(":");
      t2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      textarea = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("textarea");
      t3 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");

      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }

      t4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("\n      Each line should match `");
      t5 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(t5_value);
      t6 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("`");
      t7 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      if (if_block1) if_block1.c();
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "class", "col-lg-3 bold text-lg-right my-auto");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div0, file, 27, 2, 628);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "name", textarea_name_value =
      /*args*/
      ctx[0].name);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "placeholder", textarea_placeholder_value =
      /*args*/
      ctx[0].hint);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "rows", textarea_rows_value =
      /*args*/
      ctx[0].rows);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "cols", textarea_cols_value =
      /*args*/
      ctx[0].cols);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "class", "form-control nodecoration tiny");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(textarea, "is-valid",
      /*invalid*/
      ctx[2].length === 0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(textarea, "is-invalid",
      /*invalid*/
      ctx[2].length !== 0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(textarea, file, 31, 4, 872);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div1, "class", "invalid-feedback");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div1, file, 41, 4, 1162);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div2, "class", "col-lg-6 pt-2 pt-lg-0");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div2, file, 30, 2, 832);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div3, "class", "row px-4 px-lg-3 pb-4");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div3, file, 26, 0, 590);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div3, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, div0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t0);
      if (if_block0) if_block0.m(div0, null);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, t2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, div2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div2, textarea);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_input_value)(textarea,
      /*value*/
      ctx[1]);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div2, t3);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div2, div1);

      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].m(div1, null);
      }

      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, t4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, t5);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, t6);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div2, t7);
      if (if_block1) if_block1.m(div2, null);

      if (!mounted) {
        dispose = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.listen_dev)(textarea, "input",
        /*textarea_input_handler*/
        ctx[4]);
        mounted = true;
      }
    },
    p: function update(ctx, [dirty]) {
      if (dirty &
      /*args*/
      1 && t0_value !== (t0_value =
      /*args*/
      ctx[0].label + "")) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_data_dev)(t0, t0_value);

      if (
      /*args*/
      ctx[0].description) {
        if (if_block0) {
          if_block0.p(ctx, dirty);
        } else {
          if_block0 = create_if_block_2(ctx);
          if_block0.c();
          if_block0.m(div0, t1);
        }
      } else if (if_block0) {
        if_block0.d(1);
        if_block0 = null;
      }

      if (dirty &
      /*args*/
      1 && textarea_name_value !== (textarea_name_value =
      /*args*/
      ctx[0].name)) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "name", textarea_name_value);
      }

      if (dirty &
      /*args*/
      1 && textarea_placeholder_value !== (textarea_placeholder_value =
      /*args*/
      ctx[0].hint)) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "placeholder", textarea_placeholder_value);
      }

      if (dirty &
      /*args*/
      1 && textarea_rows_value !== (textarea_rows_value =
      /*args*/
      ctx[0].rows)) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "rows", textarea_rows_value);
      }

      if (dirty &
      /*args*/
      1 && textarea_cols_value !== (textarea_cols_value =
      /*args*/
      ctx[0].cols)) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(textarea, "cols", textarea_cols_value);
      }

      if (dirty &
      /*value*/
      2) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_input_value)(textarea,
        /*value*/
        ctx[1]);
      }

      if (dirty &
      /*invalid*/
      4) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(textarea, "is-valid",
        /*invalid*/
        ctx[2].length === 0);
      }

      if (dirty &
      /*invalid*/
      4) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(textarea, "is-invalid",
        /*invalid*/
        ctx[2].length !== 0);
      }

      if (dirty &
      /*invalid*/
      4) {
        each_value_1 =
        /*invalid*/
        ctx[2];
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_each_argument)(each_value_1);
        let i;

        for (i = 0; i < each_value_1.length; i += 1) {
          const child_ctx = get_each_context_1(ctx, each_value_1, i);

          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block_1(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(div1, t4);
          }
        }

        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }

        each_blocks.length = each_value_1.length;
      }

      if (dirty &
      /*args*/
      1 && t5_value !== (t5_value =
      /*args*/
      ctx[0].constraint + "")) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_data_dev)(t5, t5_value);
      if (dirty &
      /*args*/
      1) show_if =
      /*args*/
      ctx[0].examples && Object.keys(
      /*args*/
      ctx[0].examples).length > 0;

      if (show_if) {
        if (if_block1) {
          if_block1.p(ctx, dirty);
        } else {
          if_block1 = create_if_block(ctx);
          if_block1.c();
          if_block1.m(div2, null);
        }
      } else if (if_block1) {
        if_block1.d(1);
        if_block1 = null;
      }
    },
    i: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    o: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div3);
      if (if_block0) if_block0.d();
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_each)(each_blocks, detaching);
      if (if_block1) if_block1.d();
      mounted = false;
      dispose();
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_fragment.name,
    type: "component",
    source: "",
    ctx
  });
  return block;
}

function instance($$self, $$props, $$invalidate) {
  let {
    $$slots: slots = {},
    $$scope
  } = $$props;
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_slots)('TextListField', slots, []);
  let {
    args
  } = $$props;
  let value;
  let constraint;
  let invalid = [];
  const writable_props = ['args'];
  Object_1.keys($$props).forEach(key => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<TextListField> was created with unknown prop '${key}'`);
  });

  function textarea_input_handler() {
    value = this.value;
    $$invalidate(1, value), $$invalidate(0, args);
  }

  const click_handler = example_name => $$invalidate(1, value = args.examples[example_name].join('\n'));

  $$self.$$set = $$props => {
    if ('args' in $$props) $$invalidate(0, args = $$props.args);
  };

  $$self.$capture_state = () => ({
    ensure_list: _utils_ensure_list__WEBPACK_IMPORTED_MODULE_1__["default"],
    re_full: _utils_re_full__WEBPACK_IMPORTED_MODULE_2__["default"],
    args,
    value,
    constraint,
    invalid
  });

  $$self.$inject_state = $$props => {
    if ('args' in $$props) $$invalidate(0, args = $$props.args);
    if ('value' in $$props) $$invalidate(1, value = $$props.value);
    if ('constraint' in $$props) $$invalidate(3, constraint = $$props.constraint);
    if ('invalid' in $$props) $$invalidate(2, invalid = $$props.invalid);
  };

  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }

  $$self.$$.update = () => {
    if ($$self.$$.dirty &
    /*args, value*/
    3) {
      $: if (args !== undefined && value === undefined) {
        $$invalidate(1, value = (0,_utils_ensure_list__WEBPACK_IMPORTED_MODULE_1__["default"])(args.default).join('\n'));
      }
    }

    if ($$self.$$.dirty &
    /*args*/
    1) {
      $: if (args !== undefined) {
        $$invalidate(3, constraint = (0,_utils_re_full__WEBPACK_IMPORTED_MODULE_2__["default"])(args.constraint));
      }
    }

    if ($$self.$$.dirty &
    /*value, constraint*/
    10) {
      $: if (value !== undefined && constraint !== undefined) {
        $$invalidate(2, invalid = value.replace(/\n+$/g, '').split('\n').filter(v => constraint.exec(v) === null).map((value, index) => ({
          value,
          index
        })));
      }
    }
  };

  return [args, value, invalid, constraint, textarea_input_handler, click_handler];
}

class TextListField extends svelte_internal__WEBPACK_IMPORTED_MODULE_0__.SvelteComponentDev {
  constructor(options) {
    super(options);
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.init)(this, options, instance, create_fragment, svelte_internal__WEBPACK_IMPORTED_MODULE_0__.safe_not_equal, {
      args: 0
    });
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterComponent", {
      component: this,
      tagName: "TextListField",
      options,
      id: create_fragment.name
    });
    const {
      ctx
    } = this.$$;
    const props = options.props || {};

    if (
    /*args*/
    ctx[0] === undefined && !('args' in props)) {
      console.warn("<TextListField> was created without expected prop 'args'");
    }
  }

  get args() {
    throw new Error("<TextListField>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

  set args(value) {
    throw new Error("<TextListField>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

}




if (module && module.hot) {}

/* harmony default export */ __webpack_exports__["default"] = (TextListField);

/***/ }),

/***/ "./node_modules/svelte-loader/lib/hot-api.js":
/*!***************************************************!*\
  !*** ./node_modules/svelte-loader/lib/hot-api.js ***!
  \***************************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "applyHmr": function() { return /* binding */ applyHmr; }
/* harmony export */ });
/* harmony import */ var svelte_hmr_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte-hmr/runtime */ "./node_modules/svelte-hmr/runtime/index.js");
 // eslint-disable-next-line no-undef

const g = typeof window !== 'undefined' ? window : __webpack_require__.g;
const globalKey = typeof Symbol !== 'undefined' ? Symbol('SVELTE_LOADER_HOT') : '__SVELTE_LOADER_HOT';

if (!g[globalKey]) {
  // do updating refs counting to know when a full update has been applied
  let updatingCount = 0;

  const notifyStart = () => {
    updatingCount++;
  };

  const notifyError = reload => err => {
    const errString = err && err.stack || err; // eslint-disable-next-line no-console

    console.error('[HMR] Failed to accept update (nollup compat mode)', errString);
    reload();
    notifyEnd();
  };

  const notifyEnd = () => {
    updatingCount--;

    if (updatingCount === 0) {
      // NOTE this message is important for timing in tests
      // eslint-disable-next-line no-console
      console.log('[HMR:Svelte] Up to date');
    }
  };

  g[globalKey] = {
    hotStates: {},
    notifyStart,
    notifyError,
    notifyEnd
  };
}

const runAcceptHandlers = acceptHandlers => {
  const queue = [...acceptHandlers];

  const next = () => {
    const cur = queue.shift();

    if (cur) {
      return cur(null).then(next);
    } else {
      return Promise.resolve(null);
    }
  };

  return next();
};

const applyHmr = (0,svelte_hmr_runtime__WEBPACK_IMPORTED_MODULE_0__.makeApplyHmr)(args => {
  const {
    notifyStart,
    notifyError,
    notifyEnd
  } = g[globalKey];
  const {
    m,
    reload
  } = args;
  let acceptHandlers = m.hot.data && m.hot.data.acceptHandlers || [];
  let nextAcceptHandlers = [];
  m.hot.dispose(data => {
    data.acceptHandlers = nextAcceptHandlers;
  });

  const dispose = (...args) => m.hot.dispose(...args);

  const accept = handler => {
    if (nextAcceptHandlers.length === 0) {
      m.hot.accept();
    }

    nextAcceptHandlers.push(handler);
  };

  const check = status => {
    if (status === 'ready') {
      notifyStart();
    } else if (status === 'idle') {
      runAcceptHandlers(acceptHandlers).then(notifyEnd).catch(notifyError(reload));
    }
  };

  m.hot.addStatusHandler(check);
  m.hot.dispose(() => {
    m.hot.removeStatusHandler(check);
  });
  const hot = {
    data: m.hot.data,
    dispose,
    accept
  };
  return { ...args,
    hot
  };
});

/***/ }),

/***/ "./lib/webpack_public_path.js":
/*!************************************!*\
  !*** ./lib/webpack_public_path.js ***!
  \************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
__webpack_require__.p = `${window._config.STATIC}/`;

/***/ }),

/***/ "./node_modules/svelte/internal/index.mjs":
/*!************************************************!*\
  !*** ./node_modules/svelte/internal/index.mjs ***!
  \************************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HtmlTag": function() { return /* binding */ HtmlTag; },
/* harmony export */   "HtmlTagHydration": function() { return /* binding */ HtmlTagHydration; },
/* harmony export */   "SvelteComponent": function() { return /* binding */ SvelteComponent; },
/* harmony export */   "SvelteComponentDev": function() { return /* binding */ SvelteComponentDev; },
/* harmony export */   "SvelteComponentTyped": function() { return /* binding */ SvelteComponentTyped; },
/* harmony export */   "SvelteElement": function() { return /* binding */ SvelteElement; },
/* harmony export */   "action_destroyer": function() { return /* binding */ action_destroyer; },
/* harmony export */   "add_attribute": function() { return /* binding */ add_attribute; },
/* harmony export */   "add_classes": function() { return /* binding */ add_classes; },
/* harmony export */   "add_flush_callback": function() { return /* binding */ add_flush_callback; },
/* harmony export */   "add_location": function() { return /* binding */ add_location; },
/* harmony export */   "add_render_callback": function() { return /* binding */ add_render_callback; },
/* harmony export */   "add_resize_listener": function() { return /* binding */ add_resize_listener; },
/* harmony export */   "add_styles": function() { return /* binding */ add_styles; },
/* harmony export */   "add_transform": function() { return /* binding */ add_transform; },
/* harmony export */   "afterUpdate": function() { return /* binding */ afterUpdate; },
/* harmony export */   "append": function() { return /* binding */ append; },
/* harmony export */   "append_dev": function() { return /* binding */ append_dev; },
/* harmony export */   "append_empty_stylesheet": function() { return /* binding */ append_empty_stylesheet; },
/* harmony export */   "append_hydration": function() { return /* binding */ append_hydration; },
/* harmony export */   "append_hydration_dev": function() { return /* binding */ append_hydration_dev; },
/* harmony export */   "append_styles": function() { return /* binding */ append_styles; },
/* harmony export */   "assign": function() { return /* binding */ assign; },
/* harmony export */   "attr": function() { return /* binding */ attr; },
/* harmony export */   "attr_dev": function() { return /* binding */ attr_dev; },
/* harmony export */   "attribute_to_object": function() { return /* binding */ attribute_to_object; },
/* harmony export */   "beforeUpdate": function() { return /* binding */ beforeUpdate; },
/* harmony export */   "bind": function() { return /* binding */ bind; },
/* harmony export */   "binding_callbacks": function() { return /* binding */ binding_callbacks; },
/* harmony export */   "blank_object": function() { return /* binding */ blank_object; },
/* harmony export */   "bubble": function() { return /* binding */ bubble; },
/* harmony export */   "check_outros": function() { return /* binding */ check_outros; },
/* harmony export */   "children": function() { return /* binding */ children; },
/* harmony export */   "claim_component": function() { return /* binding */ claim_component; },
/* harmony export */   "claim_element": function() { return /* binding */ claim_element; },
/* harmony export */   "claim_html_tag": function() { return /* binding */ claim_html_tag; },
/* harmony export */   "claim_space": function() { return /* binding */ claim_space; },
/* harmony export */   "claim_svg_element": function() { return /* binding */ claim_svg_element; },
/* harmony export */   "claim_text": function() { return /* binding */ claim_text; },
/* harmony export */   "clear_loops": function() { return /* binding */ clear_loops; },
/* harmony export */   "component_subscribe": function() { return /* binding */ component_subscribe; },
/* harmony export */   "compute_rest_props": function() { return /* binding */ compute_rest_props; },
/* harmony export */   "compute_slots": function() { return /* binding */ compute_slots; },
/* harmony export */   "createEventDispatcher": function() { return /* binding */ createEventDispatcher; },
/* harmony export */   "create_animation": function() { return /* binding */ create_animation; },
/* harmony export */   "create_bidirectional_transition": function() { return /* binding */ create_bidirectional_transition; },
/* harmony export */   "create_component": function() { return /* binding */ create_component; },
/* harmony export */   "create_in_transition": function() { return /* binding */ create_in_transition; },
/* harmony export */   "create_out_transition": function() { return /* binding */ create_out_transition; },
/* harmony export */   "create_slot": function() { return /* binding */ create_slot; },
/* harmony export */   "create_ssr_component": function() { return /* binding */ create_ssr_component; },
/* harmony export */   "current_component": function() { return /* binding */ current_component; },
/* harmony export */   "custom_event": function() { return /* binding */ custom_event; },
/* harmony export */   "dataset_dev": function() { return /* binding */ dataset_dev; },
/* harmony export */   "debug": function() { return /* binding */ debug; },
/* harmony export */   "destroy_block": function() { return /* binding */ destroy_block; },
/* harmony export */   "destroy_component": function() { return /* binding */ destroy_component; },
/* harmony export */   "destroy_each": function() { return /* binding */ destroy_each; },
/* harmony export */   "detach": function() { return /* binding */ detach; },
/* harmony export */   "detach_after_dev": function() { return /* binding */ detach_after_dev; },
/* harmony export */   "detach_before_dev": function() { return /* binding */ detach_before_dev; },
/* harmony export */   "detach_between_dev": function() { return /* binding */ detach_between_dev; },
/* harmony export */   "detach_dev": function() { return /* binding */ detach_dev; },
/* harmony export */   "dirty_components": function() { return /* binding */ dirty_components; },
/* harmony export */   "dispatch_dev": function() { return /* binding */ dispatch_dev; },
/* harmony export */   "each": function() { return /* binding */ each; },
/* harmony export */   "element": function() { return /* binding */ element; },
/* harmony export */   "element_is": function() { return /* binding */ element_is; },
/* harmony export */   "empty": function() { return /* binding */ empty; },
/* harmony export */   "end_hydrating": function() { return /* binding */ end_hydrating; },
/* harmony export */   "escape": function() { return /* binding */ escape; },
/* harmony export */   "escape_attribute_value": function() { return /* binding */ escape_attribute_value; },
/* harmony export */   "escape_object": function() { return /* binding */ escape_object; },
/* harmony export */   "escaped": function() { return /* binding */ escaped; },
/* harmony export */   "exclude_internal_props": function() { return /* binding */ exclude_internal_props; },
/* harmony export */   "fix_and_destroy_block": function() { return /* binding */ fix_and_destroy_block; },
/* harmony export */   "fix_and_outro_and_destroy_block": function() { return /* binding */ fix_and_outro_and_destroy_block; },
/* harmony export */   "fix_position": function() { return /* binding */ fix_position; },
/* harmony export */   "flush": function() { return /* binding */ flush; },
/* harmony export */   "getAllContexts": function() { return /* binding */ getAllContexts; },
/* harmony export */   "getContext": function() { return /* binding */ getContext; },
/* harmony export */   "get_all_dirty_from_scope": function() { return /* binding */ get_all_dirty_from_scope; },
/* harmony export */   "get_binding_group_value": function() { return /* binding */ get_binding_group_value; },
/* harmony export */   "get_current_component": function() { return /* binding */ get_current_component; },
/* harmony export */   "get_custom_elements_slots": function() { return /* binding */ get_custom_elements_slots; },
/* harmony export */   "get_root_for_style": function() { return /* binding */ get_root_for_style; },
/* harmony export */   "get_slot_changes": function() { return /* binding */ get_slot_changes; },
/* harmony export */   "get_spread_object": function() { return /* binding */ get_spread_object; },
/* harmony export */   "get_spread_update": function() { return /* binding */ get_spread_update; },
/* harmony export */   "get_store_value": function() { return /* binding */ get_store_value; },
/* harmony export */   "globals": function() { return /* binding */ globals; },
/* harmony export */   "group_outros": function() { return /* binding */ group_outros; },
/* harmony export */   "handle_promise": function() { return /* binding */ handle_promise; },
/* harmony export */   "hasContext": function() { return /* binding */ hasContext; },
/* harmony export */   "has_prop": function() { return /* binding */ has_prop; },
/* harmony export */   "identity": function() { return /* binding */ identity; },
/* harmony export */   "init": function() { return /* binding */ init; },
/* harmony export */   "insert": function() { return /* binding */ insert; },
/* harmony export */   "insert_dev": function() { return /* binding */ insert_dev; },
/* harmony export */   "insert_hydration": function() { return /* binding */ insert_hydration; },
/* harmony export */   "insert_hydration_dev": function() { return /* binding */ insert_hydration_dev; },
/* harmony export */   "intros": function() { return /* binding */ intros; },
/* harmony export */   "invalid_attribute_name_character": function() { return /* binding */ invalid_attribute_name_character; },
/* harmony export */   "is_client": function() { return /* binding */ is_client; },
/* harmony export */   "is_crossorigin": function() { return /* binding */ is_crossorigin; },
/* harmony export */   "is_empty": function() { return /* binding */ is_empty; },
/* harmony export */   "is_function": function() { return /* binding */ is_function; },
/* harmony export */   "is_promise": function() { return /* binding */ is_promise; },
/* harmony export */   "listen": function() { return /* binding */ listen; },
/* harmony export */   "listen_dev": function() { return /* binding */ listen_dev; },
/* harmony export */   "loop": function() { return /* binding */ loop; },
/* harmony export */   "loop_guard": function() { return /* binding */ loop_guard; },
/* harmony export */   "merge_ssr_styles": function() { return /* binding */ merge_ssr_styles; },
/* harmony export */   "missing_component": function() { return /* binding */ missing_component; },
/* harmony export */   "mount_component": function() { return /* binding */ mount_component; },
/* harmony export */   "noop": function() { return /* binding */ noop; },
/* harmony export */   "not_equal": function() { return /* binding */ not_equal; },
/* harmony export */   "now": function() { return /* binding */ now; },
/* harmony export */   "null_to_empty": function() { return /* binding */ null_to_empty; },
/* harmony export */   "object_without_properties": function() { return /* binding */ object_without_properties; },
/* harmony export */   "onDestroy": function() { return /* binding */ onDestroy; },
/* harmony export */   "onMount": function() { return /* binding */ onMount; },
/* harmony export */   "once": function() { return /* binding */ once; },
/* harmony export */   "outro_and_destroy_block": function() { return /* binding */ outro_and_destroy_block; },
/* harmony export */   "prevent_default": function() { return /* binding */ prevent_default; },
/* harmony export */   "prop_dev": function() { return /* binding */ prop_dev; },
/* harmony export */   "query_selector_all": function() { return /* binding */ query_selector_all; },
/* harmony export */   "raf": function() { return /* binding */ raf; },
/* harmony export */   "run": function() { return /* binding */ run; },
/* harmony export */   "run_all": function() { return /* binding */ run_all; },
/* harmony export */   "safe_not_equal": function() { return /* binding */ safe_not_equal; },
/* harmony export */   "schedule_update": function() { return /* binding */ schedule_update; },
/* harmony export */   "select_multiple_value": function() { return /* binding */ select_multiple_value; },
/* harmony export */   "select_option": function() { return /* binding */ select_option; },
/* harmony export */   "select_options": function() { return /* binding */ select_options; },
/* harmony export */   "select_value": function() { return /* binding */ select_value; },
/* harmony export */   "self": function() { return /* binding */ self; },
/* harmony export */   "setContext": function() { return /* binding */ setContext; },
/* harmony export */   "set_attributes": function() { return /* binding */ set_attributes; },
/* harmony export */   "set_current_component": function() { return /* binding */ set_current_component; },
/* harmony export */   "set_custom_element_data": function() { return /* binding */ set_custom_element_data; },
/* harmony export */   "set_data": function() { return /* binding */ set_data; },
/* harmony export */   "set_data_dev": function() { return /* binding */ set_data_dev; },
/* harmony export */   "set_input_type": function() { return /* binding */ set_input_type; },
/* harmony export */   "set_input_value": function() { return /* binding */ set_input_value; },
/* harmony export */   "set_now": function() { return /* binding */ set_now; },
/* harmony export */   "set_raf": function() { return /* binding */ set_raf; },
/* harmony export */   "set_store_value": function() { return /* binding */ set_store_value; },
/* harmony export */   "set_style": function() { return /* binding */ set_style; },
/* harmony export */   "set_svg_attributes": function() { return /* binding */ set_svg_attributes; },
/* harmony export */   "space": function() { return /* binding */ space; },
/* harmony export */   "spread": function() { return /* binding */ spread; },
/* harmony export */   "src_url_equal": function() { return /* binding */ src_url_equal; },
/* harmony export */   "start_hydrating": function() { return /* binding */ start_hydrating; },
/* harmony export */   "stop_propagation": function() { return /* binding */ stop_propagation; },
/* harmony export */   "subscribe": function() { return /* binding */ subscribe; },
/* harmony export */   "svg_element": function() { return /* binding */ svg_element; },
/* harmony export */   "text": function() { return /* binding */ text; },
/* harmony export */   "tick": function() { return /* binding */ tick; },
/* harmony export */   "time_ranges_to_array": function() { return /* binding */ time_ranges_to_array; },
/* harmony export */   "to_number": function() { return /* binding */ to_number; },
/* harmony export */   "toggle_class": function() { return /* binding */ toggle_class; },
/* harmony export */   "transition_in": function() { return /* binding */ transition_in; },
/* harmony export */   "transition_out": function() { return /* binding */ transition_out; },
/* harmony export */   "trusted": function() { return /* binding */ trusted; },
/* harmony export */   "update_await_block_branch": function() { return /* binding */ update_await_block_branch; },
/* harmony export */   "update_keyed_each": function() { return /* binding */ update_keyed_each; },
/* harmony export */   "update_slot": function() { return /* binding */ update_slot; },
/* harmony export */   "update_slot_base": function() { return /* binding */ update_slot_base; },
/* harmony export */   "validate_component": function() { return /* binding */ validate_component; },
/* harmony export */   "validate_each_argument": function() { return /* binding */ validate_each_argument; },
/* harmony export */   "validate_each_keys": function() { return /* binding */ validate_each_keys; },
/* harmony export */   "validate_slots": function() { return /* binding */ validate_slots; },
/* harmony export */   "validate_store": function() { return /* binding */ validate_store; },
/* harmony export */   "xlink_attr": function() { return /* binding */ xlink_attr; }
/* harmony export */ });
function noop() {}

const identity = x => x;

function assign(tar, src) {
  // @ts-ignore
  for (const k in src) tar[k] = src[k];

  return tar;
}

function is_promise(value) {
  return value && typeof value === 'object' && typeof value.then === 'function';
}

function add_location(element, file, line, column, char) {
  element.__svelte_meta = {
    loc: {
      file,
      line,
      column,
      char
    }
  };
}

function run(fn) {
  return fn();
}

function blank_object() {
  return Object.create(null);
}

function run_all(fns) {
  fns.forEach(run);
}

function is_function(thing) {
  return typeof thing === 'function';
}

function safe_not_equal(a, b) {
  return a != a ? b == b : a !== b || a && typeof a === 'object' || typeof a === 'function';
}

let src_url_equal_anchor;

function src_url_equal(element_src, url) {
  if (!src_url_equal_anchor) {
    src_url_equal_anchor = document.createElement('a');
  }

  src_url_equal_anchor.href = url;
  return element_src === src_url_equal_anchor.href;
}

function not_equal(a, b) {
  return a != a ? b == b : a !== b;
}

function is_empty(obj) {
  return Object.keys(obj).length === 0;
}

function validate_store(store, name) {
  if (store != null && typeof store.subscribe !== 'function') {
    throw new Error(`'${name}' is not a store with a 'subscribe' method`);
  }
}

function subscribe(store, ...callbacks) {
  if (store == null) {
    return noop;
  }

  const unsub = store.subscribe(...callbacks);
  return unsub.unsubscribe ? () => unsub.unsubscribe() : unsub;
}

function get_store_value(store) {
  let value;
  subscribe(store, _ => value = _)();
  return value;
}

function component_subscribe(component, store, callback) {
  component.$$.on_destroy.push(subscribe(store, callback));
}

function create_slot(definition, ctx, $$scope, fn) {
  if (definition) {
    const slot_ctx = get_slot_context(definition, ctx, $$scope, fn);
    return definition[0](slot_ctx);
  }
}

function get_slot_context(definition, ctx, $$scope, fn) {
  return definition[1] && fn ? assign($$scope.ctx.slice(), definition[1](fn(ctx))) : $$scope.ctx;
}

function get_slot_changes(definition, $$scope, dirty, fn) {
  if (definition[2] && fn) {
    const lets = definition[2](fn(dirty));

    if ($$scope.dirty === undefined) {
      return lets;
    }

    if (typeof lets === 'object') {
      const merged = [];
      const len = Math.max($$scope.dirty.length, lets.length);

      for (let i = 0; i < len; i += 1) {
        merged[i] = $$scope.dirty[i] | lets[i];
      }

      return merged;
    }

    return $$scope.dirty | lets;
  }

  return $$scope.dirty;
}

function update_slot_base(slot, slot_definition, ctx, $$scope, slot_changes, get_slot_context_fn) {
  if (slot_changes) {
    const slot_context = get_slot_context(slot_definition, ctx, $$scope, get_slot_context_fn);
    slot.p(slot_context, slot_changes);
  }
}

function update_slot(slot, slot_definition, ctx, $$scope, dirty, get_slot_changes_fn, get_slot_context_fn) {
  const slot_changes = get_slot_changes(slot_definition, $$scope, dirty, get_slot_changes_fn);
  update_slot_base(slot, slot_definition, ctx, $$scope, slot_changes, get_slot_context_fn);
}

function get_all_dirty_from_scope($$scope) {
  if ($$scope.ctx.length > 32) {
    const dirty = [];
    const length = $$scope.ctx.length / 32;

    for (let i = 0; i < length; i++) {
      dirty[i] = -1;
    }

    return dirty;
  }

  return -1;
}

function exclude_internal_props(props) {
  const result = {};

  for (const k in props) if (k[0] !== '$') result[k] = props[k];

  return result;
}

function compute_rest_props(props, keys) {
  const rest = {};
  keys = new Set(keys);

  for (const k in props) if (!keys.has(k) && k[0] !== '$') rest[k] = props[k];

  return rest;
}

function compute_slots(slots) {
  const result = {};

  for (const key in slots) {
    result[key] = true;
  }

  return result;
}

function once(fn) {
  let ran = false;
  return function (...args) {
    if (ran) return;
    ran = true;
    fn.call(this, ...args);
  };
}

function null_to_empty(value) {
  return value == null ? '' : value;
}

function set_store_value(store, ret, value) {
  store.set(value);
  return ret;
}

const has_prop = (obj, prop) => Object.prototype.hasOwnProperty.call(obj, prop);

function action_destroyer(action_result) {
  return action_result && is_function(action_result.destroy) ? action_result.destroy : noop;
}

const is_client = typeof window !== 'undefined';
let now = is_client ? () => window.performance.now() : () => Date.now();
let raf = is_client ? cb => requestAnimationFrame(cb) : noop; // used internally for testing

function set_now(fn) {
  now = fn;
}

function set_raf(fn) {
  raf = fn;
}

const tasks = new Set();

function run_tasks(now) {
  tasks.forEach(task => {
    if (!task.c(now)) {
      tasks.delete(task);
      task.f();
    }
  });
  if (tasks.size !== 0) raf(run_tasks);
}
/**
 * For testing purposes only!
 */


function clear_loops() {
  tasks.clear();
}
/**
 * Creates a new task that runs on each raf frame
 * until it returns a falsy value or is aborted
 */


function loop(callback) {
  let task;
  if (tasks.size === 0) raf(run_tasks);
  return {
    promise: new Promise(fulfill => {
      tasks.add(task = {
        c: callback,
        f: fulfill
      });
    }),

    abort() {
      tasks.delete(task);
    }

  };
} // Track which nodes are claimed during hydration. Unclaimed nodes can then be removed from the DOM
// at the end of hydration without touching the remaining nodes.


let is_hydrating = false;

function start_hydrating() {
  is_hydrating = true;
}

function end_hydrating() {
  is_hydrating = false;
}

function upper_bound(low, high, key, value) {
  // Return first index of value larger than input value in the range [low, high)
  while (low < high) {
    const mid = low + (high - low >> 1);

    if (key(mid) <= value) {
      low = mid + 1;
    } else {
      high = mid;
    }
  }

  return low;
}

function init_hydrate(target) {
  if (target.hydrate_init) return;
  target.hydrate_init = true; // We know that all children have claim_order values since the unclaimed have been detached if target is not <head>

  let children = target.childNodes; // If target is <head>, there may be children without claim_order

  if (target.nodeName === 'HEAD') {
    const myChildren = [];

    for (let i = 0; i < children.length; i++) {
      const node = children[i];

      if (node.claim_order !== undefined) {
        myChildren.push(node);
      }
    }

    children = myChildren;
  }
  /*
  * Reorder claimed children optimally.
  * We can reorder claimed children optimally by finding the longest subsequence of
  * nodes that are already claimed in order and only moving the rest. The longest
  * subsequence subsequence of nodes that are claimed in order can be found by
  * computing the longest increasing subsequence of .claim_order values.
  *
  * This algorithm is optimal in generating the least amount of reorder operations
  * possible.
  *
  * Proof:
  * We know that, given a set of reordering operations, the nodes that do not move
  * always form an increasing subsequence, since they do not move among each other
  * meaning that they must be already ordered among each other. Thus, the maximal
  * set of nodes that do not move form a longest increasing subsequence.
  */
  // Compute longest increasing subsequence
  // m: subsequence length j => index k of smallest value that ends an increasing subsequence of length j


  const m = new Int32Array(children.length + 1); // Predecessor indices + 1

  const p = new Int32Array(children.length);
  m[0] = -1;
  let longest = 0;

  for (let i = 0; i < children.length; i++) {
    const current = children[i].claim_order; // Find the largest subsequence length such that it ends in a value less than our current value
    // upper_bound returns first greater value, so we subtract one
    // with fast path for when we are on the current longest subsequence

    const seqLen = (longest > 0 && children[m[longest]].claim_order <= current ? longest + 1 : upper_bound(1, longest, idx => children[m[idx]].claim_order, current)) - 1;
    p[i] = m[seqLen] + 1;
    const newLen = seqLen + 1; // We can guarantee that current is the smallest value. Otherwise, we would have generated a longer sequence.

    m[newLen] = i;
    longest = Math.max(newLen, longest);
  } // The longest increasing subsequence of nodes (initially reversed)


  const lis = []; // The rest of the nodes, nodes that will be moved

  const toMove = [];
  let last = children.length - 1;

  for (let cur = m[longest] + 1; cur != 0; cur = p[cur - 1]) {
    lis.push(children[cur - 1]);

    for (; last >= cur; last--) {
      toMove.push(children[last]);
    }

    last--;
  }

  for (; last >= 0; last--) {
    toMove.push(children[last]);
  }

  lis.reverse(); // We sort the nodes being moved to guarantee that their insertion order matches the claim order

  toMove.sort((a, b) => a.claim_order - b.claim_order); // Finally, we move the nodes

  for (let i = 0, j = 0; i < toMove.length; i++) {
    while (j < lis.length && toMove[i].claim_order >= lis[j].claim_order) {
      j++;
    }

    const anchor = j < lis.length ? lis[j] : null;
    target.insertBefore(toMove[i], anchor);
  }
}

function append(target, node) {
  target.appendChild(node);
}

function append_styles(target, style_sheet_id, styles) {
  const append_styles_to = get_root_for_style(target);

  if (!append_styles_to.getElementById(style_sheet_id)) {
    const style = element('style');
    style.id = style_sheet_id;
    style.textContent = styles;
    append_stylesheet(append_styles_to, style);
  }
}

function get_root_for_style(node) {
  if (!node) return document;
  const root = node.getRootNode ? node.getRootNode() : node.ownerDocument;

  if (root && root.host) {
    return root;
  }

  return node.ownerDocument;
}

function append_empty_stylesheet(node) {
  const style_element = element('style');
  append_stylesheet(get_root_for_style(node), style_element);
  return style_element.sheet;
}

function append_stylesheet(node, style) {
  append(node.head || node, style);
}

function append_hydration(target, node) {
  if (is_hydrating) {
    init_hydrate(target);

    if (target.actual_end_child === undefined || target.actual_end_child !== null && target.actual_end_child.parentElement !== target) {
      target.actual_end_child = target.firstChild;
    } // Skip nodes of undefined ordering


    while (target.actual_end_child !== null && target.actual_end_child.claim_order === undefined) {
      target.actual_end_child = target.actual_end_child.nextSibling;
    }

    if (node !== target.actual_end_child) {
      // We only insert if the ordering of this node should be modified or the parent node is not target
      if (node.claim_order !== undefined || node.parentNode !== target) {
        target.insertBefore(node, target.actual_end_child);
      }
    } else {
      target.actual_end_child = node.nextSibling;
    }
  } else if (node.parentNode !== target || node.nextSibling !== null) {
    target.appendChild(node);
  }
}

function insert(target, node, anchor) {
  target.insertBefore(node, anchor || null);
}

function insert_hydration(target, node, anchor) {
  if (is_hydrating && !anchor) {
    append_hydration(target, node);
  } else if (node.parentNode !== target || node.nextSibling != anchor) {
    target.insertBefore(node, anchor || null);
  }
}

function detach(node) {
  node.parentNode.removeChild(node);
}

function destroy_each(iterations, detaching) {
  for (let i = 0; i < iterations.length; i += 1) {
    if (iterations[i]) iterations[i].d(detaching);
  }
}

function element(name) {
  return document.createElement(name);
}

function element_is(name, is) {
  return document.createElement(name, {
    is
  });
}

function object_without_properties(obj, exclude) {
  const target = {};

  for (const k in obj) {
    if (has_prop(obj, k) // @ts-ignore
    && exclude.indexOf(k) === -1) {
      // @ts-ignore
      target[k] = obj[k];
    }
  }

  return target;
}

function svg_element(name) {
  return document.createElementNS('http://www.w3.org/2000/svg', name);
}

function text(data) {
  return document.createTextNode(data);
}

function space() {
  return text(' ');
}

function empty() {
  return text('');
}

function listen(node, event, handler, options) {
  node.addEventListener(event, handler, options);
  return () => node.removeEventListener(event, handler, options);
}

function prevent_default(fn) {
  return function (event) {
    event.preventDefault(); // @ts-ignore

    return fn.call(this, event);
  };
}

function stop_propagation(fn) {
  return function (event) {
    event.stopPropagation(); // @ts-ignore

    return fn.call(this, event);
  };
}

function self(fn) {
  return function (event) {
    // @ts-ignore
    if (event.target === this) fn.call(this, event);
  };
}

function trusted(fn) {
  return function (event) {
    // @ts-ignore
    if (event.isTrusted) fn.call(this, event);
  };
}

function attr(node, attribute, value) {
  if (value == null) node.removeAttribute(attribute);else if (node.getAttribute(attribute) !== value) node.setAttribute(attribute, value);
}

function set_attributes(node, attributes) {
  // @ts-ignore
  const descriptors = Object.getOwnPropertyDescriptors(node.__proto__);

  for (const key in attributes) {
    if (attributes[key] == null) {
      node.removeAttribute(key);
    } else if (key === 'style') {
      node.style.cssText = attributes[key];
    } else if (key === '__value') {
      node.value = node[key] = attributes[key];
    } else if (descriptors[key] && descriptors[key].set) {
      node[key] = attributes[key];
    } else {
      attr(node, key, attributes[key]);
    }
  }
}

function set_svg_attributes(node, attributes) {
  for (const key in attributes) {
    attr(node, key, attributes[key]);
  }
}

function set_custom_element_data(node, prop, value) {
  if (prop in node) {
    node[prop] = typeof node[prop] === 'boolean' && value === '' ? true : value;
  } else {
    attr(node, prop, value);
  }
}

function xlink_attr(node, attribute, value) {
  node.setAttributeNS('http://www.w3.org/1999/xlink', attribute, value);
}

function get_binding_group_value(group, __value, checked) {
  const value = new Set();

  for (let i = 0; i < group.length; i += 1) {
    if (group[i].checked) value.add(group[i].__value);
  }

  if (!checked) {
    value.delete(__value);
  }

  return Array.from(value);
}

function to_number(value) {
  return value === '' ? null : +value;
}

function time_ranges_to_array(ranges) {
  const array = [];

  for (let i = 0; i < ranges.length; i += 1) {
    array.push({
      start: ranges.start(i),
      end: ranges.end(i)
    });
  }

  return array;
}

function children(element) {
  return Array.from(element.childNodes);
}

function init_claim_info(nodes) {
  if (nodes.claim_info === undefined) {
    nodes.claim_info = {
      last_index: 0,
      total_claimed: 0
    };
  }
}

function claim_node(nodes, predicate, processNode, createNode, dontUpdateLastIndex = false) {
  // Try to find nodes in an order such that we lengthen the longest increasing subsequence
  init_claim_info(nodes);

  const resultNode = (() => {
    // We first try to find an element after the previous one
    for (let i = nodes.claim_info.last_index; i < nodes.length; i++) {
      const node = nodes[i];

      if (predicate(node)) {
        const replacement = processNode(node);

        if (replacement === undefined) {
          nodes.splice(i, 1);
        } else {
          nodes[i] = replacement;
        }

        if (!dontUpdateLastIndex) {
          nodes.claim_info.last_index = i;
        }

        return node;
      }
    } // Otherwise, we try to find one before
    // We iterate in reverse so that we don't go too far back


    for (let i = nodes.claim_info.last_index - 1; i >= 0; i--) {
      const node = nodes[i];

      if (predicate(node)) {
        const replacement = processNode(node);

        if (replacement === undefined) {
          nodes.splice(i, 1);
        } else {
          nodes[i] = replacement;
        }

        if (!dontUpdateLastIndex) {
          nodes.claim_info.last_index = i;
        } else if (replacement === undefined) {
          // Since we spliced before the last_index, we decrease it
          nodes.claim_info.last_index--;
        }

        return node;
      }
    } // If we can't find any matching node, we create a new one


    return createNode();
  })();

  resultNode.claim_order = nodes.claim_info.total_claimed;
  nodes.claim_info.total_claimed += 1;
  return resultNode;
}

function claim_element_base(nodes, name, attributes, create_element) {
  return claim_node(nodes, node => node.nodeName === name, node => {
    const remove = [];

    for (let j = 0; j < node.attributes.length; j++) {
      const attribute = node.attributes[j];

      if (!attributes[attribute.name]) {
        remove.push(attribute.name);
      }
    }

    remove.forEach(v => node.removeAttribute(v));
    return undefined;
  }, () => create_element(name));
}

function claim_element(nodes, name, attributes) {
  return claim_element_base(nodes, name, attributes, element);
}

function claim_svg_element(nodes, name, attributes) {
  return claim_element_base(nodes, name, attributes, svg_element);
}

function claim_text(nodes, data) {
  return claim_node(nodes, node => node.nodeType === 3, node => {
    const dataStr = '' + data;

    if (node.data.startsWith(dataStr)) {
      if (node.data.length !== dataStr.length) {
        return node.splitText(dataStr.length);
      }
    } else {
      node.data = dataStr;
    }
  }, () => text(data), true // Text nodes should not update last index since it is likely not worth it to eliminate an increasing subsequence of actual elements
  );
}

function claim_space(nodes) {
  return claim_text(nodes, ' ');
}

function find_comment(nodes, text, start) {
  for (let i = start; i < nodes.length; i += 1) {
    const node = nodes[i];

    if (node.nodeType === 8
    /* comment node */
    && node.textContent.trim() === text) {
      return i;
    }
  }

  return nodes.length;
}

function claim_html_tag(nodes) {
  // find html opening tag
  const start_index = find_comment(nodes, 'HTML_TAG_START', 0);
  const end_index = find_comment(nodes, 'HTML_TAG_END', start_index);

  if (start_index === end_index) {
    return new HtmlTagHydration();
  }

  init_claim_info(nodes);
  const html_tag_nodes = nodes.splice(start_index, end_index - start_index + 1);
  detach(html_tag_nodes[0]);
  detach(html_tag_nodes[html_tag_nodes.length - 1]);
  const claimed_nodes = html_tag_nodes.slice(1, html_tag_nodes.length - 1);

  for (const n of claimed_nodes) {
    n.claim_order = nodes.claim_info.total_claimed;
    nodes.claim_info.total_claimed += 1;
  }

  return new HtmlTagHydration(claimed_nodes);
}

function set_data(text, data) {
  data = '' + data;
  if (text.wholeText !== data) text.data = data;
}

function set_input_value(input, value) {
  input.value = value == null ? '' : value;
}

function set_input_type(input, type) {
  try {
    input.type = type;
  } catch (e) {// do nothing
  }
}

function set_style(node, key, value, important) {
  if (value === null) {
    node.style.removeProperty(key);
  } else {
    node.style.setProperty(key, value, important ? 'important' : '');
  }
}

function select_option(select, value) {
  for (let i = 0; i < select.options.length; i += 1) {
    const option = select.options[i];

    if (option.__value === value) {
      option.selected = true;
      return;
    }
  }

  select.selectedIndex = -1; // no option should be selected
}

function select_options(select, value) {
  for (let i = 0; i < select.options.length; i += 1) {
    const option = select.options[i];
    option.selected = ~value.indexOf(option.__value);
  }
}

function select_value(select) {
  const selected_option = select.querySelector(':checked') || select.options[0];
  return selected_option && selected_option.__value;
}

function select_multiple_value(select) {
  return [].map.call(select.querySelectorAll(':checked'), option => option.__value);
} // unfortunately this can't be a constant as that wouldn't be tree-shakeable
// so we cache the result instead


let crossorigin;

function is_crossorigin() {
  if (crossorigin === undefined) {
    crossorigin = false;

    try {
      if (typeof window !== 'undefined' && window.parent) {
        void window.parent.document;
      }
    } catch (error) {
      crossorigin = true;
    }
  }

  return crossorigin;
}

function add_resize_listener(node, fn) {
  const computed_style = getComputedStyle(node);

  if (computed_style.position === 'static') {
    node.style.position = 'relative';
  }

  const iframe = element('iframe');
  iframe.setAttribute('style', 'display: block; position: absolute; top: 0; left: 0; width: 100%; height: 100%; ' + 'overflow: hidden; border: 0; opacity: 0; pointer-events: none; z-index: -1;');
  iframe.setAttribute('aria-hidden', 'true');
  iframe.tabIndex = -1;
  const crossorigin = is_crossorigin();
  let unsubscribe;

  if (crossorigin) {
    iframe.src = "data:text/html,<script>onresize=function(){parent.postMessage(0,'*')}</script>";
    unsubscribe = listen(window, 'message', event => {
      if (event.source === iframe.contentWindow) fn();
    });
  } else {
    iframe.src = 'about:blank';

    iframe.onload = () => {
      unsubscribe = listen(iframe.contentWindow, 'resize', fn);
    };
  }

  append(node, iframe);
  return () => {
    if (crossorigin) {
      unsubscribe();
    } else if (unsubscribe && iframe.contentWindow) {
      unsubscribe();
    }

    detach(iframe);
  };
}

function toggle_class(element, name, toggle) {
  element.classList[toggle ? 'add' : 'remove'](name);
}

function custom_event(type, detail, bubbles = false) {
  const e = document.createEvent('CustomEvent');
  e.initCustomEvent(type, bubbles, false, detail);
  return e;
}

function query_selector_all(selector, parent = document.body) {
  return Array.from(parent.querySelectorAll(selector));
}

class HtmlTag {
  constructor() {
    this.e = this.n = null;
  }

  c(html) {
    this.h(html);
  }

  m(html, target, anchor = null) {
    if (!this.e) {
      this.e = element(target.nodeName);
      this.t = target;
      this.c(html);
    }

    this.i(anchor);
  }

  h(html) {
    this.e.innerHTML = html;
    this.n = Array.from(this.e.childNodes);
  }

  i(anchor) {
    for (let i = 0; i < this.n.length; i += 1) {
      insert(this.t, this.n[i], anchor);
    }
  }

  p(html) {
    this.d();
    this.h(html);
    this.i(this.a);
  }

  d() {
    this.n.forEach(detach);
  }

}

class HtmlTagHydration extends HtmlTag {
  constructor(claimed_nodes) {
    super();
    this.e = this.n = null;
    this.l = claimed_nodes;
  }

  c(html) {
    if (this.l) {
      this.n = this.l;
    } else {
      super.c(html);
    }
  }

  i(anchor) {
    for (let i = 0; i < this.n.length; i += 1) {
      insert_hydration(this.t, this.n[i], anchor);
    }
  }

}

function attribute_to_object(attributes) {
  const result = {};

  for (const attribute of attributes) {
    result[attribute.name] = attribute.value;
  }

  return result;
}

function get_custom_elements_slots(element) {
  const result = {};
  element.childNodes.forEach(node => {
    result[node.slot || 'default'] = true;
  });
  return result;
} // we need to store the information for multiple documents because a Svelte application could also contain iframes
// https://github.com/sveltejs/svelte/issues/3624


const managed_styles = new Map();
let active = 0; // https://github.com/darkskyapp/string-hash/blob/master/index.js

function hash(str) {
  let hash = 5381;
  let i = str.length;

  while (i--) hash = (hash << 5) - hash ^ str.charCodeAt(i);

  return hash >>> 0;
}

function create_style_information(doc, node) {
  const info = {
    stylesheet: append_empty_stylesheet(node),
    rules: {}
  };
  managed_styles.set(doc, info);
  return info;
}

function create_rule(node, a, b, duration, delay, ease, fn, uid = 0) {
  const step = 16.666 / duration;
  let keyframes = '{\n';

  for (let p = 0; p <= 1; p += step) {
    const t = a + (b - a) * ease(p);
    keyframes += p * 100 + `%{${fn(t, 1 - t)}}\n`;
  }

  const rule = keyframes + `100% {${fn(b, 1 - b)}}\n}`;
  const name = `__svelte_${hash(rule)}_${uid}`;
  const doc = get_root_for_style(node);
  const {
    stylesheet,
    rules
  } = managed_styles.get(doc) || create_style_information(doc, node);

  if (!rules[name]) {
    rules[name] = true;
    stylesheet.insertRule(`@keyframes ${name} ${rule}`, stylesheet.cssRules.length);
  }

  const animation = node.style.animation || '';
  node.style.animation = `${animation ? `${animation}, ` : ''}${name} ${duration}ms linear ${delay}ms 1 both`;
  active += 1;
  return name;
}

function delete_rule(node, name) {
  const previous = (node.style.animation || '').split(', ');
  const next = previous.filter(name ? anim => anim.indexOf(name) < 0 // remove specific animation
  : anim => anim.indexOf('__svelte') === -1 // remove all Svelte animations
  );
  const deleted = previous.length - next.length;

  if (deleted) {
    node.style.animation = next.join(', ');
    active -= deleted;
    if (!active) clear_rules();
  }
}

function clear_rules() {
  raf(() => {
    if (active) return;
    managed_styles.forEach(info => {
      const {
        stylesheet
      } = info;
      let i = stylesheet.cssRules.length;

      while (i--) stylesheet.deleteRule(i);

      info.rules = {};
    });
    managed_styles.clear();
  });
}

function create_animation(node, from, fn, params) {
  if (!from) return noop;
  const to = node.getBoundingClientRect();
  if (from.left === to.left && from.right === to.right && from.top === to.top && from.bottom === to.bottom) return noop;
  const {
    delay = 0,
    duration = 300,
    easing = identity,
    // @ts-ignore todo: should this be separated from destructuring? Or start/end added to public api and documentation?
    start: start_time = now() + delay,
    // @ts-ignore todo:
    end = start_time + duration,
    tick = noop,
    css
  } = fn(node, {
    from,
    to
  }, params);
  let running = true;
  let started = false;
  let name;

  function start() {
    if (css) {
      name = create_rule(node, 0, 1, duration, delay, easing, css);
    }

    if (!delay) {
      started = true;
    }
  }

  function stop() {
    if (css) delete_rule(node, name);
    running = false;
  }

  loop(now => {
    if (!started && now >= start_time) {
      started = true;
    }

    if (started && now >= end) {
      tick(1, 0);
      stop();
    }

    if (!running) {
      return false;
    }

    if (started) {
      const p = now - start_time;
      const t = 0 + 1 * easing(p / duration);
      tick(t, 1 - t);
    }

    return true;
  });
  start();
  tick(0, 1);
  return stop;
}

function fix_position(node) {
  const style = getComputedStyle(node);

  if (style.position !== 'absolute' && style.position !== 'fixed') {
    const {
      width,
      height
    } = style;
    const a = node.getBoundingClientRect();
    node.style.position = 'absolute';
    node.style.width = width;
    node.style.height = height;
    add_transform(node, a);
  }
}

function add_transform(node, a) {
  const b = node.getBoundingClientRect();

  if (a.left !== b.left || a.top !== b.top) {
    const style = getComputedStyle(node);
    const transform = style.transform === 'none' ? '' : style.transform;
    node.style.transform = `${transform} translate(${a.left - b.left}px, ${a.top - b.top}px)`;
  }
}

let current_component;

function set_current_component(component) {
  current_component = component;
}

function get_current_component() {
  if (!current_component) throw new Error('Function called outside component initialization');
  return current_component;
}

function beforeUpdate(fn) {
  get_current_component().$$.before_update.push(fn);
}

function onMount(fn) {
  get_current_component().$$.on_mount.push(fn);
}

function afterUpdate(fn) {
  get_current_component().$$.after_update.push(fn);
}

function onDestroy(fn) {
  get_current_component().$$.on_destroy.push(fn);
}

function createEventDispatcher() {
  const component = get_current_component();
  return (type, detail) => {
    const callbacks = component.$$.callbacks[type];

    if (callbacks) {
      // TODO are there situations where events could be dispatched
      // in a server (non-DOM) environment?
      const event = custom_event(type, detail);
      callbacks.slice().forEach(fn => {
        fn.call(component, event);
      });
    }
  };
}

function setContext(key, context) {
  get_current_component().$$.context.set(key, context);
}

function getContext(key) {
  return get_current_component().$$.context.get(key);
}

function getAllContexts() {
  return get_current_component().$$.context;
}

function hasContext(key) {
  return get_current_component().$$.context.has(key);
} // TODO figure out if we still want to support
// shorthand events, or if we want to implement
// a real bubbling mechanism


function bubble(component, event) {
  const callbacks = component.$$.callbacks[event.type];

  if (callbacks) {
    // @ts-ignore
    callbacks.slice().forEach(fn => fn.call(this, event));
  }
}

const dirty_components = [];
const intros = {
  enabled: false
};
const binding_callbacks = [];
const render_callbacks = [];
const flush_callbacks = [];
const resolved_promise = Promise.resolve();
let update_scheduled = false;

function schedule_update() {
  if (!update_scheduled) {
    update_scheduled = true;
    resolved_promise.then(flush);
  }
}

function tick() {
  schedule_update();
  return resolved_promise;
}

function add_render_callback(fn) {
  render_callbacks.push(fn);
}

function add_flush_callback(fn) {
  flush_callbacks.push(fn);
} // flush() calls callbacks in this order:
// 1. All beforeUpdate callbacks, in order: parents before children
// 2. All bind:this callbacks, in reverse order: children before parents.
// 3. All afterUpdate callbacks, in order: parents before children. EXCEPT
//    for afterUpdates called during the initial onMount, which are called in
//    reverse order: children before parents.
// Since callbacks might update component values, which could trigger another
// call to flush(), the following steps guard against this:
// 1. During beforeUpdate, any updated components will be added to the
//    dirty_components array and will cause a reentrant call to flush(). Because
//    the flush index is kept outside the function, the reentrant call will pick
//    up where the earlier call left off and go through all dirty components. The
//    current_component value is saved and restored so that the reentrant call will
//    not interfere with the "parent" flush() call.
// 2. bind:this callbacks cannot trigger new flush() calls.
// 3. During afterUpdate, any updated components will NOT have their afterUpdate
//    callback called a second time; the seen_callbacks set, outside the flush()
//    function, guarantees this behavior.


const seen_callbacks = new Set();
let flushidx = 0; // Do *not* move this inside the flush() function

function flush() {
  const saved_component = current_component;

  do {
    // first, call beforeUpdate functions
    // and update components
    while (flushidx < dirty_components.length) {
      const component = dirty_components[flushidx];
      flushidx++;
      set_current_component(component);
      update(component.$$);
    }

    set_current_component(null);
    dirty_components.length = 0;
    flushidx = 0;

    while (binding_callbacks.length) binding_callbacks.pop()(); // then, once components are updated, call
    // afterUpdate functions. This may cause
    // subsequent updates...


    for (let i = 0; i < render_callbacks.length; i += 1) {
      const callback = render_callbacks[i];

      if (!seen_callbacks.has(callback)) {
        // ...so guard against infinite loops
        seen_callbacks.add(callback);
        callback();
      }
    }

    render_callbacks.length = 0;
  } while (dirty_components.length);

  while (flush_callbacks.length) {
    flush_callbacks.pop()();
  }

  update_scheduled = false;
  seen_callbacks.clear();
  set_current_component(saved_component);
}

function update($$) {
  if ($$.fragment !== null) {
    $$.update();
    run_all($$.before_update);
    const dirty = $$.dirty;
    $$.dirty = [-1];
    $$.fragment && $$.fragment.p($$.ctx, dirty);
    $$.after_update.forEach(add_render_callback);
  }
}

let promise;

function wait() {
  if (!promise) {
    promise = Promise.resolve();
    promise.then(() => {
      promise = null;
    });
  }

  return promise;
}

function dispatch(node, direction, kind) {
  node.dispatchEvent(custom_event(`${direction ? 'intro' : 'outro'}${kind}`));
}

const outroing = new Set();
let outros;

function group_outros() {
  outros = {
    r: 0,
    c: [],
    p: outros // parent group

  };
}

function check_outros() {
  if (!outros.r) {
    run_all(outros.c);
  }

  outros = outros.p;
}

function transition_in(block, local) {
  if (block && block.i) {
    outroing.delete(block);
    block.i(local);
  }
}

function transition_out(block, local, detach, callback) {
  if (block && block.o) {
    if (outroing.has(block)) return;
    outroing.add(block);
    outros.c.push(() => {
      outroing.delete(block);

      if (callback) {
        if (detach) block.d(1);
        callback();
      }
    });
    block.o(local);
  }
}

const null_transition = {
  duration: 0
};

function create_in_transition(node, fn, params) {
  let config = fn(node, params);
  let running = false;
  let animation_name;
  let task;
  let uid = 0;

  function cleanup() {
    if (animation_name) delete_rule(node, animation_name);
  }

  function go() {
    const {
      delay = 0,
      duration = 300,
      easing = identity,
      tick = noop,
      css
    } = config || null_transition;
    if (css) animation_name = create_rule(node, 0, 1, duration, delay, easing, css, uid++);
    tick(0, 1);
    const start_time = now() + delay;
    const end_time = start_time + duration;
    if (task) task.abort();
    running = true;
    add_render_callback(() => dispatch(node, true, 'start'));
    task = loop(now => {
      if (running) {
        if (now >= end_time) {
          tick(1, 0);
          dispatch(node, true, 'end');
          cleanup();
          return running = false;
        }

        if (now >= start_time) {
          const t = easing((now - start_time) / duration);
          tick(t, 1 - t);
        }
      }

      return running;
    });
  }

  let started = false;
  return {
    start() {
      if (started) return;
      started = true;
      delete_rule(node);

      if (is_function(config)) {
        config = config();
        wait().then(go);
      } else {
        go();
      }
    },

    invalidate() {
      started = false;
    },

    end() {
      if (running) {
        cleanup();
        running = false;
      }
    }

  };
}

function create_out_transition(node, fn, params) {
  let config = fn(node, params);
  let running = true;
  let animation_name;
  const group = outros;
  group.r += 1;

  function go() {
    const {
      delay = 0,
      duration = 300,
      easing = identity,
      tick = noop,
      css
    } = config || null_transition;
    if (css) animation_name = create_rule(node, 1, 0, duration, delay, easing, css);
    const start_time = now() + delay;
    const end_time = start_time + duration;
    add_render_callback(() => dispatch(node, false, 'start'));
    loop(now => {
      if (running) {
        if (now >= end_time) {
          tick(0, 1);
          dispatch(node, false, 'end');

          if (! --group.r) {
            // this will result in `end()` being called,
            // so we don't need to clean up here
            run_all(group.c);
          }

          return false;
        }

        if (now >= start_time) {
          const t = easing((now - start_time) / duration);
          tick(1 - t, t);
        }
      }

      return running;
    });
  }

  if (is_function(config)) {
    wait().then(() => {
      // @ts-ignore
      config = config();
      go();
    });
  } else {
    go();
  }

  return {
    end(reset) {
      if (reset && config.tick) {
        config.tick(1, 0);
      }

      if (running) {
        if (animation_name) delete_rule(node, animation_name);
        running = false;
      }
    }

  };
}

function create_bidirectional_transition(node, fn, params, intro) {
  let config = fn(node, params);
  let t = intro ? 0 : 1;
  let running_program = null;
  let pending_program = null;
  let animation_name = null;

  function clear_animation() {
    if (animation_name) delete_rule(node, animation_name);
  }

  function init(program, duration) {
    const d = program.b - t;
    duration *= Math.abs(d);
    return {
      a: t,
      b: program.b,
      d,
      duration,
      start: program.start,
      end: program.start + duration,
      group: program.group
    };
  }

  function go(b) {
    const {
      delay = 0,
      duration = 300,
      easing = identity,
      tick = noop,
      css
    } = config || null_transition;
    const program = {
      start: now() + delay,
      b
    };

    if (!b) {
      // @ts-ignore todo: improve typings
      program.group = outros;
      outros.r += 1;
    }

    if (running_program || pending_program) {
      pending_program = program;
    } else {
      // if this is an intro, and there's a delay, we need to do
      // an initial tick and/or apply CSS animation immediately
      if (css) {
        clear_animation();
        animation_name = create_rule(node, t, b, duration, delay, easing, css);
      }

      if (b) tick(0, 1);
      running_program = init(program, duration);
      add_render_callback(() => dispatch(node, b, 'start'));
      loop(now => {
        if (pending_program && now > pending_program.start) {
          running_program = init(pending_program, duration);
          pending_program = null;
          dispatch(node, running_program.b, 'start');

          if (css) {
            clear_animation();
            animation_name = create_rule(node, t, running_program.b, running_program.duration, 0, easing, config.css);
          }
        }

        if (running_program) {
          if (now >= running_program.end) {
            tick(t = running_program.b, 1 - t);
            dispatch(node, running_program.b, 'end');

            if (!pending_program) {
              // we're done
              if (running_program.b) {
                // intro — we can tidy up immediately
                clear_animation();
              } else {
                // outro — needs to be coordinated
                if (! --running_program.group.r) run_all(running_program.group.c);
              }
            }

            running_program = null;
          } else if (now >= running_program.start) {
            const p = now - running_program.start;
            t = running_program.a + running_program.d * easing(p / running_program.duration);
            tick(t, 1 - t);
          }
        }

        return !!(running_program || pending_program);
      });
    }
  }

  return {
    run(b) {
      if (is_function(config)) {
        wait().then(() => {
          // @ts-ignore
          config = config();
          go(b);
        });
      } else {
        go(b);
      }
    },

    end() {
      clear_animation();
      running_program = pending_program = null;
    }

  };
}

function handle_promise(promise, info) {
  const token = info.token = {};

  function update(type, index, key, value) {
    if (info.token !== token) return;
    info.resolved = value;
    let child_ctx = info.ctx;

    if (key !== undefined) {
      child_ctx = child_ctx.slice();
      child_ctx[key] = value;
    }

    const block = type && (info.current = type)(child_ctx);
    let needs_flush = false;

    if (info.block) {
      if (info.blocks) {
        info.blocks.forEach((block, i) => {
          if (i !== index && block) {
            group_outros();
            transition_out(block, 1, 1, () => {
              if (info.blocks[i] === block) {
                info.blocks[i] = null;
              }
            });
            check_outros();
          }
        });
      } else {
        info.block.d(1);
      }

      block.c();
      transition_in(block, 1);
      block.m(info.mount(), info.anchor);
      needs_flush = true;
    }

    info.block = block;
    if (info.blocks) info.blocks[index] = block;

    if (needs_flush) {
      flush();
    }
  }

  if (is_promise(promise)) {
    const current_component = get_current_component();
    promise.then(value => {
      set_current_component(current_component);
      update(info.then, 1, info.value, value);
      set_current_component(null);
    }, error => {
      set_current_component(current_component);
      update(info.catch, 2, info.error, error);
      set_current_component(null);

      if (!info.hasCatch) {
        throw error;
      }
    }); // if we previously had a then/catch block, destroy it

    if (info.current !== info.pending) {
      update(info.pending, 0);
      return true;
    }
  } else {
    if (info.current !== info.then) {
      update(info.then, 1, info.value, promise);
      return true;
    }

    info.resolved = promise;
  }
}

function update_await_block_branch(info, ctx, dirty) {
  const child_ctx = ctx.slice();
  const {
    resolved
  } = info;

  if (info.current === info.then) {
    child_ctx[info.value] = resolved;
  }

  if (info.current === info.catch) {
    child_ctx[info.error] = resolved;
  }

  info.block.p(child_ctx, dirty);
}

const globals = typeof window !== 'undefined' ? window : typeof globalThis !== 'undefined' ? globalThis : global;

function destroy_block(block, lookup) {
  block.d(1);
  lookup.delete(block.key);
}

function outro_and_destroy_block(block, lookup) {
  transition_out(block, 1, 1, () => {
    lookup.delete(block.key);
  });
}

function fix_and_destroy_block(block, lookup) {
  block.f();
  destroy_block(block, lookup);
}

function fix_and_outro_and_destroy_block(block, lookup) {
  block.f();
  outro_and_destroy_block(block, lookup);
}

function update_keyed_each(old_blocks, dirty, get_key, dynamic, ctx, list, lookup, node, destroy, create_each_block, next, get_context) {
  let o = old_blocks.length;
  let n = list.length;
  let i = o;
  const old_indexes = {};

  while (i--) old_indexes[old_blocks[i].key] = i;

  const new_blocks = [];
  const new_lookup = new Map();
  const deltas = new Map();
  i = n;

  while (i--) {
    const child_ctx = get_context(ctx, list, i);
    const key = get_key(child_ctx);
    let block = lookup.get(key);

    if (!block) {
      block = create_each_block(key, child_ctx);
      block.c();
    } else if (dynamic) {
      block.p(child_ctx, dirty);
    }

    new_lookup.set(key, new_blocks[i] = block);
    if (key in old_indexes) deltas.set(key, Math.abs(i - old_indexes[key]));
  }

  const will_move = new Set();
  const did_move = new Set();

  function insert(block) {
    transition_in(block, 1);
    block.m(node, next);
    lookup.set(block.key, block);
    next = block.first;
    n--;
  }

  while (o && n) {
    const new_block = new_blocks[n - 1];
    const old_block = old_blocks[o - 1];
    const new_key = new_block.key;
    const old_key = old_block.key;

    if (new_block === old_block) {
      // do nothing
      next = new_block.first;
      o--;
      n--;
    } else if (!new_lookup.has(old_key)) {
      // remove old block
      destroy(old_block, lookup);
      o--;
    } else if (!lookup.has(new_key) || will_move.has(new_key)) {
      insert(new_block);
    } else if (did_move.has(old_key)) {
      o--;
    } else if (deltas.get(new_key) > deltas.get(old_key)) {
      did_move.add(new_key);
      insert(new_block);
    } else {
      will_move.add(old_key);
      o--;
    }
  }

  while (o--) {
    const old_block = old_blocks[o];
    if (!new_lookup.has(old_block.key)) destroy(old_block, lookup);
  }

  while (n) insert(new_blocks[n - 1]);

  return new_blocks;
}

function validate_each_keys(ctx, list, get_context, get_key) {
  const keys = new Set();

  for (let i = 0; i < list.length; i++) {
    const key = get_key(get_context(ctx, list, i));

    if (keys.has(key)) {
      throw new Error('Cannot have duplicate keys in a keyed each');
    }

    keys.add(key);
  }
}

function get_spread_update(levels, updates) {
  const update = {};
  const to_null_out = {};
  const accounted_for = {
    $$scope: 1
  };
  let i = levels.length;

  while (i--) {
    const o = levels[i];
    const n = updates[i];

    if (n) {
      for (const key in o) {
        if (!(key in n)) to_null_out[key] = 1;
      }

      for (const key in n) {
        if (!accounted_for[key]) {
          update[key] = n[key];
          accounted_for[key] = 1;
        }
      }

      levels[i] = n;
    } else {
      for (const key in o) {
        accounted_for[key] = 1;
      }
    }
  }

  for (const key in to_null_out) {
    if (!(key in update)) update[key] = undefined;
  }

  return update;
}

function get_spread_object(spread_props) {
  return typeof spread_props === 'object' && spread_props !== null ? spread_props : {};
} // source: https://html.spec.whatwg.org/multipage/indices.html


const boolean_attributes = new Set(['allowfullscreen', 'allowpaymentrequest', 'async', 'autofocus', 'autoplay', 'checked', 'controls', 'default', 'defer', 'disabled', 'formnovalidate', 'hidden', 'ismap', 'loop', 'multiple', 'muted', 'nomodule', 'novalidate', 'open', 'playsinline', 'readonly', 'required', 'reversed', 'selected']);
const invalid_attribute_name_character = /[\s'">/=\u{FDD0}-\u{FDEF}\u{FFFE}\u{FFFF}\u{1FFFE}\u{1FFFF}\u{2FFFE}\u{2FFFF}\u{3FFFE}\u{3FFFF}\u{4FFFE}\u{4FFFF}\u{5FFFE}\u{5FFFF}\u{6FFFE}\u{6FFFF}\u{7FFFE}\u{7FFFF}\u{8FFFE}\u{8FFFF}\u{9FFFE}\u{9FFFF}\u{AFFFE}\u{AFFFF}\u{BFFFE}\u{BFFFF}\u{CFFFE}\u{CFFFF}\u{DFFFE}\u{DFFFF}\u{EFFFE}\u{EFFFF}\u{FFFFE}\u{FFFFF}\u{10FFFE}\u{10FFFF}]/u; // https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
// https://infra.spec.whatwg.org/#noncharacter

function spread(args, attrs_to_add) {
  const attributes = Object.assign({}, ...args);

  if (attrs_to_add) {
    const classes_to_add = attrs_to_add.classes;
    const styles_to_add = attrs_to_add.styles;

    if (classes_to_add) {
      if (attributes.class == null) {
        attributes.class = classes_to_add;
      } else {
        attributes.class += ' ' + classes_to_add;
      }
    }

    if (styles_to_add) {
      if (attributes.style == null) {
        attributes.style = style_object_to_string(styles_to_add);
      } else {
        attributes.style = style_object_to_string(merge_ssr_styles(attributes.style, styles_to_add));
      }
    }
  }

  let str = '';
  Object.keys(attributes).forEach(name => {
    if (invalid_attribute_name_character.test(name)) return;
    const value = attributes[name];
    if (value === true) str += ' ' + name;else if (boolean_attributes.has(name.toLowerCase())) {
      if (value) str += ' ' + name;
    } else if (value != null) {
      str += ` ${name}="${value}"`;
    }
  });
  return str;
}

function merge_ssr_styles(style_attribute, style_directive) {
  const style_object = {};

  for (const individual_style of style_attribute.split(';')) {
    const colon_index = individual_style.indexOf(':');
    const name = individual_style.slice(0, colon_index).trim();
    const value = individual_style.slice(colon_index + 1).trim();
    if (!name) continue;
    style_object[name] = value;
  }

  for (const name in style_directive) {
    const value = style_directive[name];

    if (value) {
      style_object[name] = value;
    } else {
      delete style_object[name];
    }
  }

  return style_object;
}

const escaped = {
  '"': '&quot;',
  "'": '&#39;',
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;'
};

function escape(html) {
  return String(html).replace(/["'&<>]/g, match => escaped[match]);
}

function escape_attribute_value(value) {
  return typeof value === 'string' ? escape(value) : value;
}

function escape_object(obj) {
  const result = {};

  for (const key in obj) {
    result[key] = escape_attribute_value(obj[key]);
  }

  return result;
}

function each(items, fn) {
  let str = '';

  for (let i = 0; i < items.length; i += 1) {
    str += fn(items[i], i);
  }

  return str;
}

const missing_component = {
  $$render: () => ''
};

function validate_component(component, name) {
  if (!component || !component.$$render) {
    if (name === 'svelte:component') name += ' this={...}';
    throw new Error(`<${name}> is not a valid SSR component. You may need to review your build config to ensure that dependencies are compiled, rather than imported as pre-compiled modules`);
  }

  return component;
}

function debug(file, line, column, values) {
  console.log(`{@debug} ${file ? file + ' ' : ''}(${line}:${column})`); // eslint-disable-line no-console

  console.log(values); // eslint-disable-line no-console

  return '';
}

let on_destroy;

function create_ssr_component(fn) {
  function $$render(result, props, bindings, slots, context) {
    const parent_component = current_component;
    const $$ = {
      on_destroy,
      context: new Map(context || (parent_component ? parent_component.$$.context : [])),
      // these will be immediately discarded
      on_mount: [],
      before_update: [],
      after_update: [],
      callbacks: blank_object()
    };
    set_current_component({
      $$
    });
    const html = fn(result, props, bindings, slots);
    set_current_component(parent_component);
    return html;
  }

  return {
    render: (props = {}, {
      $$slots = {},
      context = new Map()
    } = {}) => {
      on_destroy = [];
      const result = {
        title: '',
        head: '',
        css: new Set()
      };
      const html = $$render(result, props, {}, $$slots, context);
      run_all(on_destroy);
      return {
        html,
        css: {
          code: Array.from(result.css).map(css => css.code).join('\n'),
          map: null // TODO

        },
        head: result.title + result.head
      };
    },
    $$render
  };
}

function add_attribute(name, value, boolean) {
  if (value == null || boolean && !value) return '';
  return ` ${name}${value === true && boolean_attributes.has(name) ? '' : `=${typeof value === 'string' ? JSON.stringify(escape(value)) : `"${value}"`}`}`;
}

function add_classes(classes) {
  return classes ? ` class="${classes}"` : '';
}

function style_object_to_string(style_object) {
  return Object.keys(style_object).filter(key => style_object[key]).map(key => `${key}: ${style_object[key]};`).join(' ');
}

function add_styles(style_object) {
  const styles = style_object_to_string(style_object);
  return styles ? ` style="${styles}"` : '';
}

function bind(component, name, callback) {
  const index = component.$$.props[name];

  if (index !== undefined) {
    component.$$.bound[index] = callback;
    callback(component.$$.ctx[index]);
  }
}

function create_component(block) {
  block && block.c();
}

function claim_component(block, parent_nodes) {
  block && block.l(parent_nodes);
}

function mount_component(component, target, anchor, customElement) {
  const {
    fragment,
    on_mount,
    on_destroy,
    after_update
  } = component.$$;
  fragment && fragment.m(target, anchor);

  if (!customElement) {
    // onMount happens before the initial afterUpdate
    add_render_callback(() => {
      const new_on_destroy = on_mount.map(run).filter(is_function);

      if (on_destroy) {
        on_destroy.push(...new_on_destroy);
      } else {
        // Edge case - component was destroyed immediately,
        // most likely as a result of a binding initialising
        run_all(new_on_destroy);
      }

      component.$$.on_mount = [];
    });
  }

  after_update.forEach(add_render_callback);
}

function destroy_component(component, detaching) {
  const $$ = component.$$;

  if ($$.fragment !== null) {
    run_all($$.on_destroy);
    $$.fragment && $$.fragment.d(detaching); // TODO null out other refs, including component.$$ (but need to
    // preserve final state?)

    $$.on_destroy = $$.fragment = null;
    $$.ctx = [];
  }
}

function make_dirty(component, i) {
  if (component.$$.dirty[0] === -1) {
    dirty_components.push(component);
    schedule_update();
    component.$$.dirty.fill(0);
  }

  component.$$.dirty[i / 31 | 0] |= 1 << i % 31;
}

function init(component, options, instance, create_fragment, not_equal, props, append_styles, dirty = [-1]) {
  const parent_component = current_component;
  set_current_component(component);
  const $$ = component.$$ = {
    fragment: null,
    ctx: null,
    // state
    props,
    update: noop,
    not_equal,
    bound: blank_object(),
    // lifecycle
    on_mount: [],
    on_destroy: [],
    on_disconnect: [],
    before_update: [],
    after_update: [],
    context: new Map(options.context || (parent_component ? parent_component.$$.context : [])),
    // everything else
    callbacks: blank_object(),
    dirty,
    skip_bound: false,
    root: options.target || parent_component.$$.root
  };
  append_styles && append_styles($$.root);
  let ready = false;
  $$.ctx = instance ? instance(component, options.props || {}, (i, ret, ...rest) => {
    const value = rest.length ? rest[0] : ret;

    if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
      if (!$$.skip_bound && $$.bound[i]) $$.bound[i](value);
      if (ready) make_dirty(component, i);
    }

    return ret;
  }) : [];
  $$.update();
  ready = true;
  run_all($$.before_update); // `false` as a special case of no DOM component

  $$.fragment = create_fragment ? create_fragment($$.ctx) : false;

  if (options.target) {
    if (options.hydrate) {
      start_hydrating();
      const nodes = children(options.target); // eslint-disable-next-line @typescript-eslint/no-non-null-assertion

      $$.fragment && $$.fragment.l(nodes);
      nodes.forEach(detach);
    } else {
      // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
      $$.fragment && $$.fragment.c();
    }

    if (options.intro) transition_in(component.$$.fragment);
    mount_component(component, options.target, options.anchor, options.customElement);
    end_hydrating();
    flush();
  }

  set_current_component(parent_component);
}

let SvelteElement;

if (typeof HTMLElement === 'function') {
  SvelteElement = class extends HTMLElement {
    constructor() {
      super();
      this.attachShadow({
        mode: 'open'
      });
    }

    connectedCallback() {
      const {
        on_mount
      } = this.$$;
      this.$$.on_disconnect = on_mount.map(run).filter(is_function); // @ts-ignore todo: improve typings

      for (const key in this.$$.slotted) {
        // @ts-ignore todo: improve typings
        this.appendChild(this.$$.slotted[key]);
      }
    }

    attributeChangedCallback(attr, _oldValue, newValue) {
      this[attr] = newValue;
    }

    disconnectedCallback() {
      run_all(this.$$.on_disconnect);
    }

    $destroy() {
      destroy_component(this, 1);
      this.$destroy = noop;
    }

    $on(type, callback) {
      // TODO should this delegate to addEventListener?
      const callbacks = this.$$.callbacks[type] || (this.$$.callbacks[type] = []);
      callbacks.push(callback);
      return () => {
        const index = callbacks.indexOf(callback);
        if (index !== -1) callbacks.splice(index, 1);
      };
    }

    $set($$props) {
      if (this.$$set && !is_empty($$props)) {
        this.$$.skip_bound = true;
        this.$$set($$props);
        this.$$.skip_bound = false;
      }
    }

  };
}
/**
 * Base class for Svelte components. Used when dev=false.
 */


class SvelteComponent {
  $destroy() {
    destroy_component(this, 1);
    this.$destroy = noop;
  }

  $on(type, callback) {
    const callbacks = this.$$.callbacks[type] || (this.$$.callbacks[type] = []);
    callbacks.push(callback);
    return () => {
      const index = callbacks.indexOf(callback);
      if (index !== -1) callbacks.splice(index, 1);
    };
  }

  $set($$props) {
    if (this.$$set && !is_empty($$props)) {
      this.$$.skip_bound = true;
      this.$$set($$props);
      this.$$.skip_bound = false;
    }
  }

}

function dispatch_dev(type, detail) {
  document.dispatchEvent(custom_event(type, Object.assign({
    version: '3.46.4'
  }, detail), true));
}

function append_dev(target, node) {
  dispatch_dev('SvelteDOMInsert', {
    target,
    node
  });
  append(target, node);
}

function append_hydration_dev(target, node) {
  dispatch_dev('SvelteDOMInsert', {
    target,
    node
  });
  append_hydration(target, node);
}

function insert_dev(target, node, anchor) {
  dispatch_dev('SvelteDOMInsert', {
    target,
    node,
    anchor
  });
  insert(target, node, anchor);
}

function insert_hydration_dev(target, node, anchor) {
  dispatch_dev('SvelteDOMInsert', {
    target,
    node,
    anchor
  });
  insert_hydration(target, node, anchor);
}

function detach_dev(node) {
  dispatch_dev('SvelteDOMRemove', {
    node
  });
  detach(node);
}

function detach_between_dev(before, after) {
  while (before.nextSibling && before.nextSibling !== after) {
    detach_dev(before.nextSibling);
  }
}

function detach_before_dev(after) {
  while (after.previousSibling) {
    detach_dev(after.previousSibling);
  }
}

function detach_after_dev(before) {
  while (before.nextSibling) {
    detach_dev(before.nextSibling);
  }
}

function listen_dev(node, event, handler, options, has_prevent_default, has_stop_propagation) {
  const modifiers = options === true ? ['capture'] : options ? Array.from(Object.keys(options)) : [];
  if (has_prevent_default) modifiers.push('preventDefault');
  if (has_stop_propagation) modifiers.push('stopPropagation');
  dispatch_dev('SvelteDOMAddEventListener', {
    node,
    event,
    handler,
    modifiers
  });
  const dispose = listen(node, event, handler, options);
  return () => {
    dispatch_dev('SvelteDOMRemoveEventListener', {
      node,
      event,
      handler,
      modifiers
    });
    dispose();
  };
}

function attr_dev(node, attribute, value) {
  attr(node, attribute, value);
  if (value == null) dispatch_dev('SvelteDOMRemoveAttribute', {
    node,
    attribute
  });else dispatch_dev('SvelteDOMSetAttribute', {
    node,
    attribute,
    value
  });
}

function prop_dev(node, property, value) {
  node[property] = value;
  dispatch_dev('SvelteDOMSetProperty', {
    node,
    property,
    value
  });
}

function dataset_dev(node, property, value) {
  node.dataset[property] = value;
  dispatch_dev('SvelteDOMSetDataset', {
    node,
    property,
    value
  });
}

function set_data_dev(text, data) {
  data = '' + data;
  if (text.wholeText === data) return;
  dispatch_dev('SvelteDOMSetData', {
    node: text,
    data
  });
  text.data = data;
}

function validate_each_argument(arg) {
  if (typeof arg !== 'string' && !(arg && typeof arg === 'object' && 'length' in arg)) {
    let msg = '{#each} only iterates over array-like objects.';

    if (typeof Symbol === 'function' && arg && Symbol.iterator in arg) {
      msg += ' You can use a spread to convert this iterable into an array.';
    }

    throw new Error(msg);
  }
}

function validate_slots(name, slot, keys) {
  for (const slot_key of Object.keys(slot)) {
    if (!~keys.indexOf(slot_key)) {
      console.warn(`<${name}> received an unexpected slot "${slot_key}".`);
    }
  }
}
/**
 * Base class for Svelte components with some minor dev-enhancements. Used when dev=true.
 */


class SvelteComponentDev extends SvelteComponent {
  constructor(options) {
    if (!options || !options.target && !options.$$inline) {
      throw new Error("'target' is a required option");
    }

    super();
  }

  $destroy() {
    super.$destroy();

    this.$destroy = () => {
      console.warn('Component was already destroyed'); // eslint-disable-line no-console
    };
  }

  $capture_state() {}

  $inject_state() {}

}
/**
 * Base class to create strongly typed Svelte components.
 * This only exists for typing purposes and should be used in `.d.ts` files.
 *
 * ### Example:
 *
 * You have component library on npm called `component-library`, from which
 * you export a component called `MyComponent`. For Svelte+TypeScript users,
 * you want to provide typings. Therefore you create a `index.d.ts`:
 * ```ts
 * import { SvelteComponentTyped } from "svelte";
 * export class MyComponent extends SvelteComponentTyped<{foo: string}> {}
 * ```
 * Typing this makes it possible for IDEs like VS Code with the Svelte extension
 * to provide intellisense and to use the component like this in a Svelte file
 * with TypeScript:
 * ```svelte
 * <script lang="ts">
 * 	import { MyComponent } from "component-library";
 * </script>
 * <MyComponent foo={'bar'} />
 * ```
 *
 * #### Why not make this part of `SvelteComponent(Dev)`?
 * Because
 * ```ts
 * class ASubclassOfSvelteComponent extends SvelteComponent<{foo: string}> {}
 * const component: typeof SvelteComponent = ASubclassOfSvelteComponent;
 * ```
 * will throw a type error, so we need to separate the more strictly typed class.
 */


class SvelteComponentTyped extends SvelteComponentDev {
  constructor(options) {
    super(options);
  }

}

function loop_guard(timeout) {
  const start = Date.now();
  return () => {
    if (Date.now() - start > timeout) {
      throw new Error('Infinite loop detected');
    }
  };
}



/***/ }),

/***/ "./utils/ensure_list.js":
/*!******************************!*\
  !*** ./utils/ensure_list.js ***!
  \******************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": function() { return /* binding */ ensure_list; }
/* harmony export */ });
function ensure_list(L) {
  if (typeof L === 'object' && Array.isArray(L)) {
    return L;
  } else {
    return [L];
  }
}

/***/ }),

/***/ "./utils/re_full.js":
/*!**************************!*\
  !*** ./utils/re_full.js ***!
  \**************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": function() { return /* binding */ re_full; }
/* harmony export */ });
function re_full(expr, flags) {
  if (/^\^/.exec(expr) === null) expr = `^${expr}`;
  if (/\$$/.exec(expr) === null) expr = `${expr}$`;
  return new RegExp(expr, flags);
}

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			id: moduleId,
/******/ 			loaded: false,
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	!function() {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = function(exports, definition) {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	!function() {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/harmony module decorator */
/******/ 	!function() {
/******/ 		__webpack_require__.hmd = function(module) {
/******/ 			module = Object.create(module);
/******/ 			if (!module.children) module.children = [];
/******/ 			Object.defineProperty(module, 'exports', {
/******/ 				enumerable: true,
/******/ 				set: function() {
/******/ 					throw new Error('ES Modules may not assign module.exports or exports.*, Use ESM export syntax, instead: ' + module.id);
/******/ 				}
/******/ 			});
/******/ 			return module;
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	!function() {
/******/ 		__webpack_require__.o = function(obj, prop) { return Object.prototype.hasOwnProperty.call(obj, prop); }
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	!function() {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = function(exports) {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/publicPath */
/******/ 	!function() {
/******/ 		__webpack_require__.p = "";
/******/ 	}();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	__webpack_require__("./lib/webpack_public_path.js");
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./profiles/biojupies/js/fields/TextListField.svelte");
/******/ 	
/******/ 	return __webpack_exports__;
/******/ })()
;
});
//# sourceMappingURL=TextListField.js.map