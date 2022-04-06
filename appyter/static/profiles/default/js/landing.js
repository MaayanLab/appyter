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

/***/ "./components/Lazy.svelte":
/*!********************************!*\
  !*** ./components/Lazy.svelte ***!
  \********************************/
/***/ (function(module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var svelte_internal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/internal */ "./node_modules/svelte/internal/index.mjs");
/* harmony import */ var svelte__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! svelte */ "./node_modules/svelte/index.mjs");
/* harmony import */ var _components_Loader_svelte__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @/components/Loader.svelte */ "./components/Loader.svelte");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_loader_lib_hot_api_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./node_modules/svelte-loader/lib/hot-api.js */ "./node_modules/svelte-loader/lib/hot-api.js");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_hmr_runtime_proxy_adapter_dom_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js */ "./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js");
/* module decorator */ module = __webpack_require__.hmd(module);
/* components/Lazy.svelte generated by Svelte v3.46.4 */

const {
  console: console_1
} = svelte_internal__WEBPACK_IMPORTED_MODULE_0__.globals;


const file = "components/Lazy.svelte"; // (24:0) {:else}

function create_else_block_1(ctx) {
  let loader;
  let current;
  loader = new _components_Loader_svelte__WEBPACK_IMPORTED_MODULE_2__["default"]({
    $$inline: true
  });
  const block = {
    c: function create() {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_component)(loader.$$.fragment);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.mount_component)(loader, target, anchor);
      current = true;
    },
    p: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    i: function intro(local) {
      if (current) return;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(loader.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(loader.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_component)(loader, detaching);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_else_block_1.name,
    type: "else",
    source: "(24:0) {:else}",
    ctx
  });
  return block;
} // (16:0) {#if component !== undefined}


function create_if_block(ctx) {
  let current_block_type_index;
  let if_block;
  let if_block_anchor;
  let current;
  const if_block_creators = [create_if_block_1, create_else_block];
  const if_blocks = [];

  function select_block_type_1(ctx, dirty) {
    if (
    /*children*/
    ctx[1]) return 0;
    return 1;
  }

  current_block_type_index = select_block_type_1(ctx, -1);
  if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
  const block = {
    c: function create() {
      if_block.c();
      if_block_anchor = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.empty)();
    },
    m: function mount(target, anchor) {
      if_blocks[current_block_type_index].m(target, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, if_block_anchor, anchor);
      current = true;
    },
    p: function update(ctx, dirty) {
      let previous_block_index = current_block_type_index;
      current_block_type_index = select_block_type_1(ctx, dirty);

      if (current_block_type_index === previous_block_index) {
        if_blocks[current_block_type_index].p(ctx, dirty);
      } else {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.group_outros)();
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_blocks[previous_block_index], 1, 1, () => {
          if_blocks[previous_block_index] = null;
        });
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.check_outros)();
        if_block = if_blocks[current_block_type_index];

        if (!if_block) {
          if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
          if_block.c();
        } else {
          if_block.p(ctx, dirty);
        }

        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block, 1);
        if_block.m(if_block_anchor.parentNode, if_block_anchor);
      }
    },
    i: function intro(local) {
      if (current) return;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block);
      current = true;
    },
    o: function outro(local) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_block);
      current = false;
    },
    d: function destroy(detaching) {
      if_blocks[current_block_type_index].d(detaching);
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(if_block_anchor);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block.name,
    type: "if",
    source: "(16:0) {#if component !== undefined}",
    ctx
  });
  return block;
} // (21:2) {:else}


function create_else_block(ctx) {
  let switch_instance;
  let switch_instance_anchor;
  let current;
  const switch_instance_spread_levels = [
  /*props*/
  ctx[0]];
  var switch_value =
  /*component*/
  ctx[2];

  function switch_props(ctx) {
    let switch_instance_props = {};

    for (let i = 0; i < switch_instance_spread_levels.length; i += 1) {
      switch_instance_props = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.assign)(switch_instance_props, switch_instance_spread_levels[i]);
    }

    return {
      props: switch_instance_props,
      $$inline: true
    };
  }

  if (switch_value) {
    switch_instance = new switch_value(switch_props(ctx));
  }

  const block = {
    c: function create() {
      if (switch_instance) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_component)(switch_instance.$$.fragment);
      switch_instance_anchor = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.empty)();
    },
    m: function mount(target, anchor) {
      if (switch_instance) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.mount_component)(switch_instance, target, anchor);
      }

      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, switch_instance_anchor, anchor);
      current = true;
    },
    p: function update(ctx, dirty) {
      const switch_instance_changes = dirty &
      /*props*/
      1 ? (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.get_spread_update)(switch_instance_spread_levels, [(0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.get_spread_object)(
      /*props*/
      ctx[0])]) : {};

      if (switch_value !== (switch_value =
      /*component*/
      ctx[2])) {
        if (switch_instance) {
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.group_outros)();
          const old_component = switch_instance;
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(old_component.$$.fragment, 1, 0, () => {
            (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_component)(old_component, 1);
          });
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.check_outros)();
        }

        if (switch_value) {
          switch_instance = new switch_value(switch_props(ctx));
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_component)(switch_instance.$$.fragment);
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(switch_instance.$$.fragment, 1);
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.mount_component)(switch_instance, switch_instance_anchor.parentNode, switch_instance_anchor);
        } else {
          switch_instance = null;
        }
      } else if (switch_value) {
        switch_instance.$set(switch_instance_changes);
      }
    },
    i: function intro(local) {
      if (current) return;
      if (switch_instance) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(switch_instance.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      if (switch_instance) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(switch_instance.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(switch_instance_anchor);
      if (switch_instance) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_component)(switch_instance, detaching);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_else_block.name,
    type: "else",
    source: "(21:2) {:else}",
    ctx
  });
  return block;
} // (17:2) {#if children}


function create_if_block_1(ctx) {
  let switch_instance;
  let switch_instance_anchor;
  let current;
  const switch_instance_spread_levels = [
  /*props*/
  ctx[0]];
  var switch_value =
  /*component*/
  ctx[2];

  function switch_props(ctx) {
    let switch_instance_props = {
      $$slots: {
        default: [create_default_slot]
      },
      $$scope: {
        ctx
      }
    };

    for (let i = 0; i < switch_instance_spread_levels.length; i += 1) {
      switch_instance_props = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.assign)(switch_instance_props, switch_instance_spread_levels[i]);
    }

    return {
      props: switch_instance_props,
      $$inline: true
    };
  }

  if (switch_value) {
    switch_instance = new switch_value(switch_props(ctx));
  }

  const block = {
    c: function create() {
      if (switch_instance) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_component)(switch_instance.$$.fragment);
      switch_instance_anchor = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.empty)();
    },
    m: function mount(target, anchor) {
      if (switch_instance) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.mount_component)(switch_instance, target, anchor);
      }

      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, switch_instance_anchor, anchor);
      current = true;
    },
    p: function update(ctx, dirty) {
      const switch_instance_changes = dirty &
      /*props*/
      1 ? (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.get_spread_update)(switch_instance_spread_levels, [(0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.get_spread_object)(
      /*props*/
      ctx[0])]) : {};

      if (dirty &
      /*$$scope*/
      32) {
        switch_instance_changes.$$scope = {
          dirty,
          ctx
        };
      }

      if (switch_value !== (switch_value =
      /*component*/
      ctx[2])) {
        if (switch_instance) {
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.group_outros)();
          const old_component = switch_instance;
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(old_component.$$.fragment, 1, 0, () => {
            (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_component)(old_component, 1);
          });
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.check_outros)();
        }

        if (switch_value) {
          switch_instance = new switch_value(switch_props(ctx));
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_component)(switch_instance.$$.fragment);
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(switch_instance.$$.fragment, 1);
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.mount_component)(switch_instance, switch_instance_anchor.parentNode, switch_instance_anchor);
        } else {
          switch_instance = null;
        }
      } else if (switch_value) {
        switch_instance.$set(switch_instance_changes);
      }
    },
    i: function intro(local) {
      if (current) return;
      if (switch_instance) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(switch_instance.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      if (switch_instance) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(switch_instance.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(switch_instance_anchor);
      if (switch_instance) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_component)(switch_instance, detaching);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_1.name,
    type: "if",
    source: "(17:2) {#if children}",
    ctx
  });
  return block;
} // (18:4) <svelte:component this={component} {...props}>


function create_default_slot(ctx) {
  let current;
  const default_slot_template =
  /*#slots*/
  ctx[4].default;
  const default_slot = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_slot)(default_slot_template, ctx,
  /*$$scope*/
  ctx[5], null);
  const block = {
    c: function create() {
      if (default_slot) default_slot.c();
    },
    m: function mount(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }

      current = true;
    },
    p: function update(ctx, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty &
        /*$$scope*/
        32)) {
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.update_slot_base)(default_slot, default_slot_template, ctx,
          /*$$scope*/
          ctx[5], !current ? (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.get_all_dirty_from_scope)(
          /*$$scope*/
          ctx[5]) : (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.get_slot_changes)(default_slot_template,
          /*$$scope*/
          ctx[5], dirty, null), null);
        }
      }
    },
    i: function intro(local) {
      if (current) return;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(default_slot, local);
      current = true;
    },
    o: function outro(local) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(default_slot, local);
      current = false;
    },
    d: function destroy(detaching) {
      if (default_slot) default_slot.d(detaching);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_default_slot.name,
    type: "slot",
    source: "(18:4) <svelte:component this={component} {...props}>",
    ctx
  });
  return block;
}

function create_fragment(ctx) {
  let current_block_type_index;
  let if_block;
  let if_block_anchor;
  let current;
  const if_block_creators = [create_if_block, create_else_block_1];
  const if_blocks = [];

  function select_block_type(ctx, dirty) {
    if (
    /*component*/
    ctx[2] !== undefined) return 0;
    return 1;
  }

  current_block_type_index = select_block_type(ctx, -1);
  if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
  const block = {
    c: function create() {
      if_block.c();
      if_block_anchor = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.empty)();
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      if_blocks[current_block_type_index].m(target, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, if_block_anchor, anchor);
      current = true;
    },
    p: function update(ctx, [dirty]) {
      let previous_block_index = current_block_type_index;
      current_block_type_index = select_block_type(ctx, dirty);

      if (current_block_type_index === previous_block_index) {
        if_blocks[current_block_type_index].p(ctx, dirty);
      } else {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.group_outros)();
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_blocks[previous_block_index], 1, 1, () => {
          if_blocks[previous_block_index] = null;
        });
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.check_outros)();
        if_block = if_blocks[current_block_type_index];

        if (!if_block) {
          if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
          if_block.c();
        } else {
          if_block.p(ctx, dirty);
        }

        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block, 1);
        if_block.m(if_block_anchor.parentNode, if_block_anchor);
      }
    },
    i: function intro(local) {
      if (current) return;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block);
      current = true;
    },
    o: function outro(local) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_block);
      current = false;
    },
    d: function destroy(detaching) {
      if_blocks[current_block_type_index].d(detaching);
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(if_block_anchor);
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
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_slots)('Lazy', slots, ['default']);
  let {
    module
  } = $$props;
  let {
    props = {}
  } = $$props;
  let {
    children = false
  } = $$props;
  let component;
  (0,svelte__WEBPACK_IMPORTED_MODULE_1__.onMount)(() => module().then(({
    default: mod
  }) => $$invalidate(2, component = mod)).catch(e => console.error(e)));
  const writable_props = ['module', 'props', 'children'];
  Object.keys($$props).forEach(key => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1.warn(`<Lazy> was created with unknown prop '${key}'`);
  });

  $$self.$$set = $$props => {
    if ('module' in $$props) $$invalidate(3, module = $$props.module);
    if ('props' in $$props) $$invalidate(0, props = $$props.props);
    if ('children' in $$props) $$invalidate(1, children = $$props.children);
    if ('$$scope' in $$props) $$invalidate(5, $$scope = $$props.$$scope);
  };

  $$self.$capture_state = () => ({
    onMount: svelte__WEBPACK_IMPORTED_MODULE_1__.onMount,
    Loader: _components_Loader_svelte__WEBPACK_IMPORTED_MODULE_2__["default"],
    module,
    props,
    children,
    component
  });

  $$self.$inject_state = $$props => {
    if ('module' in $$props) $$invalidate(3, module = $$props.module);
    if ('props' in $$props) $$invalidate(0, props = $$props.props);
    if ('children' in $$props) $$invalidate(1, children = $$props.children);
    if ('component' in $$props) $$invalidate(2, component = $$props.component);
  };

  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }

  return [props, children, component, module, slots, $$scope];
}

class Lazy extends svelte_internal__WEBPACK_IMPORTED_MODULE_0__.SvelteComponentDev {
  constructor(options) {
    super(options);
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.init)(this, options, instance, create_fragment, svelte_internal__WEBPACK_IMPORTED_MODULE_0__.safe_not_equal, {
      module: 3,
      props: 0,
      children: 1
    });
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterComponent", {
      component: this,
      tagName: "Lazy",
      options,
      id: create_fragment.name
    });
    const {
      ctx
    } = this.$$;
    const props = options.props || {};

    if (
    /*module*/
    ctx[3] === undefined && !('module' in props)) {
      console_1.warn("<Lazy> was created without expected prop 'module'");
    }
  }

  get module() {
    throw new Error("<Lazy>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

  set module(value) {
    throw new Error("<Lazy>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

  get props() {
    throw new Error("<Lazy>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

  set props(value) {
    throw new Error("<Lazy>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

  get children() {
    throw new Error("<Lazy>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

  set children(value) {
    throw new Error("<Lazy>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

}




if (module && module.hot) {}

/* harmony default export */ __webpack_exports__["default"] = (Lazy);

/***/ }),

/***/ "./components/Loader.svelte":
/*!**********************************!*\
  !*** ./components/Loader.svelte ***!
  \**********************************/
/***/ (function(module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var svelte_internal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/internal */ "./node_modules/svelte/internal/index.mjs");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_loader_lib_hot_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./node_modules/svelte-loader/lib/hot-api.js */ "./node_modules/svelte-loader/lib/hot-api.js");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_hmr_runtime_proxy_adapter_dom_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js */ "./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js");
/* module decorator */ module = __webpack_require__.hmd(module);
/* components/Loader.svelte generated by Svelte v3.46.4 */

const file = "components/Loader.svelte";

function create_fragment(ctx) {
  let div4;
  let div0;
  let t0;
  let div1;
  let t1;
  let div2;
  let t2;
  let div3;
  const block = {
    c: function create() {
      div4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      t0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      t1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      t2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div3 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div0, file, 4, 2, 117);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div1, file, 5, 2, 131);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div2, file, 6, 2, 145);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div3, file, 7, 2, 159);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div4, "class", "lds-ellipsis");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div4, file, 3, 0, 88);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div4, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, div0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, t0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, div1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, t1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, div2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, t2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, div3);
    },
    p: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    i: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    o: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div4);
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

function instance($$self, $$props) {
  let {
    $$slots: slots = {},
    $$scope
  } = $$props;
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_slots)('Loader', slots, []);
  const writable_props = [];
  Object.keys($$props).forEach(key => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<Loader> was created with unknown prop '${key}'`);
  });
  return [];
}

class Loader extends svelte_internal__WEBPACK_IMPORTED_MODULE_0__.SvelteComponentDev {
  constructor(options) {
    super(options);
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.init)(this, options, instance, create_fragment, svelte_internal__WEBPACK_IMPORTED_MODULE_0__.safe_not_equal, {});
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterComponent", {
      component: this,
      tagName: "Loader",
      options,
      id: create_fragment.name
    });
  }

}




if (module && module.hot) {}

/* harmony default export */ __webpack_exports__["default"] = (Loader);

/***/ }),

/***/ "./profiles/default/js/landing.svelte":
/*!********************************************!*\
  !*** ./profiles/default/js/landing.svelte ***!
  \********************************************/
/***/ (function(module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var svelte_internal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/internal */ "./node_modules/svelte/internal/index.mjs");
/* harmony import */ var svelte__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! svelte */ "./node_modules/svelte/index.mjs");
/* harmony import */ var _lib_stores_keycloak_auth_store__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @/lib/stores/keycloak_auth_store */ "./lib/stores/keycloak_auth_store.js");
/* harmony import */ var _lib_stores_url_hash_store__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @/lib/stores/url_hash_store */ "./lib/stores/url_hash_store.js");
/* harmony import */ var _components_Lazy_svelte__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @/components/Lazy.svelte */ "./components/Lazy.svelte");
/* harmony import */ var _components_Loader_svelte__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @/components/Loader.svelte */ "./components/Loader.svelte");
/* harmony import */ var _lib_socketio__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @/lib/socketio */ "./lib/socketio.js");
/* harmony import */ var _extras_catalog_integration_pagehit__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @/extras/catalog-integration/pagehit */ "./extras/catalog-integration/pagehit.js");
/* harmony import */ var _extras_catalog_integration_toc__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @/extras/catalog-integration/toc */ "./extras/catalog-integration/toc.js");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_loader_lib_hot_api_js__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./node_modules/svelte-loader/lib/hot-api.js */ "./node_modules/svelte-loader/lib/hot-api.js");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_hmr_runtime_proxy_adapter_dom_js__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js */ "./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js");
/* module decorator */ module = __webpack_require__.hmd(module);
/* profiles/default/js/landing.svelte generated by Svelte v3.46.4 */

const {
  Error: Error_1,
  console: console_1
} = svelte_internal__WEBPACK_IMPORTED_MODULE_0__.globals;








const file = "profiles/default/js/landing.svelte";

function add_css(target) {
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_styles)(target, "svelte-1g0xm7f", "a.header-anchor{text-decoration:none;cursor:pointer}h1{display:block}h1 .header-anchor{display:none}h1:hover .header-anchor{display:inline-block}h2{display:block}h2 .header-anchor{display:none}h2:hover .header-anchor{display:inline-block}h3{display:block}h3 .header-anchor{display:none}h3:hover .header-anchor{display:inline-block}h4{display:block}h4 .header-anchor{display:none}h4:hover .header-anchor{display:inline-block}h5{display:block}h5 .header-anchor{display:none}h5:hover .header-anchor{display:inline-block}h6{display:block}h6 .header-anchor{display:none}h6:hover .header-anchor{display:inline-block}a.prompt-anchor{text-decoration:none;cursor:pointer}.prompt .prompt-anchor{display:inline-block;visibility:hidden}.prompt:hover .prompt-anchor{visibility:visible}.dropdown-menu.svelte-1g0xm7f{z-index:1021}\n/*# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoibGFuZGluZy5zdmVsdGUiLCJzb3VyY2VzIjpbImxhbmRpbmcuc3ZlbHRlIl0sInNvdXJjZXNDb250ZW50IjpbIjxzY3JpcHQ+XG4gIGltcG9ydCB7IHRpY2ssIG9uTW91bnQgfSBmcm9tICdzdmVsdGUnXG4gIGltcG9ydCBhdXRoIGZyb20gJ0AvbGliL3N0b3Jlcy9rZXljbG9ha19hdXRoX3N0b3JlJ1xuICBpbXBvcnQgaGFzaCBmcm9tICdAL2xpYi9zdG9yZXMvdXJsX2hhc2hfc3RvcmUnXG4gIGltcG9ydCBMYXp5IGZyb20gJ0AvY29tcG9uZW50cy9MYXp5LnN2ZWx0ZSdcbiAgaW1wb3J0IExvYWRlciBmcm9tICdAL2NvbXBvbmVudHMvTG9hZGVyLnN2ZWx0ZSdcbiAgaW1wb3J0IHsgc2V0dXBfY2h1bmtpbmcgfSBmcm9tICdAL2xpYi9zb2NrZXRpbydcbiAgaW1wb3J0IHBhZ2VoaXQgZnJvbSAnQC9leHRyYXMvY2F0YWxvZy1pbnRlZ3JhdGlvbi9wYWdlaGl0J1xuICBpbXBvcnQgdG9jIGZyb20gJ0AvZXh0cmFzL2NhdGFsb2ctaW50ZWdyYXRpb24vdG9jJ1xuICBleHBvcnQgbGV0IG5iZG93bmxvYWRcblxuICBjb25zdCBwYXRocyA9IHdpbmRvdy5sb2NhdGlvbi5wYXRobmFtZS5zcGxpdCgnLycpLmZpbHRlcihwID0+IHApXG4gIGNvbnN0IGluc3RhbmNlX2lkID0gcGF0aHNbcGF0aHMubGVuZ3RoIC0gMV1cblxuICBsZXQgbmJcbiAgbGV0IG5vdGVib29rUmVmXG4gIGxldCBsb2NhbF9ydW5fdXJsXG5cbiAgLy8gdGFibGUgb2YgY29udGVudHNcbiAgJDogaWYgKHdpbmRvdy5fY29uZmlnLkVYVFJBUy5pbmRleE9mKCd0b2MnKSAhPT0gLTEpIHRvYy5hdHRhY2gobm90ZWJvb2tSZWYpXG5cbiAgLy8gZHluYW1pYyBub3RlYm9va1xuICBsZXQgc3RhdHVzID0gJ0xvYWRpbmcuLi4nXG4gIGxldCBzdGF0dXNCZyA9ICdwcmltYXJ5J1xuICB2YXIgY3VycmVudF9jb2RlX2NlbGxcblxuICBhc3luYyBmdW5jdGlvbiBzZXR1cF9hc3luY19leGVjKHNvY2tldCkge1xuICAgIHNvY2tldC5vbignY29ubmVjdCcsIGFzeW5jICgpID0+IHtcbiAgICAgIGF3YWl0IHRpY2soKVxuICAgICAgc3RhdHVzID0gYENvbm5lY3RlZCB0byBzZXJ2ZXIsIHJlLWluaXRpYWxpemluZy4uLmBcbiAgICAgIHN0YXR1c0JnID0gJ3dhcm5pbmcnXG4gICAgICBhd2FpdCBpbml0KClcbiAgICB9KVxuICAgIHNvY2tldC5vbigncmVjb25uZWN0JywgYXN5bmMgKCkgPT4ge1xuICAgICAgYXdhaXQgdGljaygpXG4gICAgICBzdGF0dXMgPSBgUmVjb25uZWN0aW5nIHRvIHNlcnZlci4uLmBcbiAgICAgIHN0YXR1c0JnID0gJ3dhcm5pbmcnXG4gICAgfSlcbiAgICBzb2NrZXQub24oJ2Rpc2Nvbm5lY3QnLCBhc3luYyAocmVhc29uKSA9PiB7XG4gICAgICBpZiAocmVhc29uICE9PSAnaW8gY2xpZW50IGRpc2Nvbm5lY3QnKSB7XG4gICAgICAgIGF3YWl0IHRpY2soKVxuICAgICAgICBzdGF0dXMgPSBgRGlzY29ubmVjdGVkIGZyb20gc2VydmVyLi4uYFxuICAgICAgICBzdGF0dXNCZyA9ICdkYW5nZXInXG4gICAgICB9XG4gICAgfSlcbiAgICBzb2NrZXQub24oJ3N0YXR1cycsIGFzeW5jICh2YWx1ZSkgPT4ge1xuICAgICAgYXdhaXQgdGljaygpXG4gICAgICBzdGF0dXMgPSB2YWx1ZVxuICAgICAgc3RhdHVzQmcgPSAncHJpbWFyeSdcbiAgICAgIGlmIChzdGF0dXMgPT09ICdTdWNjZXNzJykge1xuICAgICAgICBjdXJyZW50X2NvZGVfY2VsbCA9IHVuZGVmaW5lZFxuICAgICAgICBpZiAoIXdpbmRvdy5fY29uZmlnLkRFQlVHKSB7XG4gICAgICAgICAgc29ja2V0LmRpc2Nvbm5lY3QoKVxuICAgICAgICB9XG4gICAgICB9XG4gICAgfSlcbiAgICBzb2NrZXQub24oJ2Vycm9yJywgYXN5bmMgKHZhbHVlKSA9PiB7XG4gICAgICBhd2FpdCB0aWNrKClcbiAgICAgIGN1cnJlbnRfY29kZV9jZWxsID0gdW5kZWZpbmVkXG4gICAgICBzdGF0dXMgPSBgRXJyb3I6ICR7dmFsdWV9YFxuICAgICAgc3RhdHVzQmcgPSAnZGFuZ2VyJ1xuICAgIH0pXG4gICAgc29ja2V0Lm9uKCduYicsIGFzeW5jICh2YWx1ZSkgPT4ge1xuICAgICAgYXdhaXQgdGljaygpXG4gICAgICBuYiA9IHsuLi52YWx1ZSwgY2VsbHM6IHZhbHVlLmNlbGxzLm1hcCgoY2VsbCwgaW5kZXgpID0+ICh7IC4uLmNlbGwsIGluZGV4IH0pKSB9XG4gICAgfSlcbiAgICBzb2NrZXQub24oJ3Byb2dyZXNzJywgYXN5bmMgKHZhbHVlKSA9PiB7XG4gICAgICBhd2FpdCB0aWNrKClcbiAgICAgIGN1cnJlbnRfY29kZV9jZWxsID0gdmFsdWVcbiAgICB9KVxuICAgIHNvY2tldC5vbignY2VsbCcsIGFzeW5jICh2YWx1ZV9pbmRleCkgPT4ge1xuICAgICAgbGV0IHZhbHVlID0gdmFsdWVfaW5kZXhbMF1cbiAgICAgIGxldCBjZWxsX2luZGV4ID0gdmFsdWVfaW5kZXhbMV1cbiAgICAgIGF3YWl0IHRpY2soKVxuICAgICAgbmIuY2VsbHNbY2VsbF9pbmRleF0gPSB7Li4ubmIuY2VsbHNbY2VsbF9pbmRleF0sIC4uLnZhbHVlfVxuICAgIH0pXG4gICAgc2V0dXBfY2h1bmtpbmcoc29ja2V0KVxuICB9XG5cbiAgbGV0IGNvbm5lY3RfaW5pdCA9IGZhbHNlXG4gIGFzeW5jIGZ1bmN0aW9uIGNvbm5lY3QoZXhlY3V0ZSkge1xuICAgIGNvbnN0IHsgZGVmYXVsdDogc29ja2V0IH0gPSBhd2FpdCBpbXBvcnQoJ0AvbGliL3NvY2tldCcpXG4gICAgaWYgKCFjb25uZWN0X2luaXQpIHtcbiAgICAgIGNvbm5lY3RfaW5pdCA9IHRydWVcbiAgICAgIC8vIGVuc3VyZSB3ZSdyZSBjb25uZWN0ZWRcbiAgICAgIGF3YWl0IG5ldyBQcm9taXNlKChyZXNvbHZlLCByZWplY3QpID0+IHtcbiAgICAgICAgaWYgKHNvY2tldC5jb25uZWN0ZWQpIHJlc29sdmUoKVxuICAgICAgICBlbHNlIHNvY2tldC5vbignY29ubmVjdCcsIHJlc29sdmUpXG4gICAgICB9KVxuICAgICAgYXdhaXQgc2V0dXBfYXN5bmNfZXhlYyhzb2NrZXQpXG4gICAgfVxuICAgIGNvbnN0IGV2dCA9IGV4ZWN1dGUgPyAnc3VibWl0JyA6ICdqb2luJ1xuICAgIHNvY2tldC5lbWl0KGV2dCwge1xuICAgICAgX2lkOiBpbnN0YW5jZV9pZCxcbiAgICAgIF9hdXRoOiAkYXV0aC5rZXljbG9hay50b2tlbixcbiAgICAgIF9zdG9yYWdlOiAkaGFzaC5zZXJ2ZXIucGFyYW1zLnN0b3JhZ2UsXG4gICAgICBfZXhlY3V0b3I6ICRoYXNoLnNlcnZlci5wYXJhbXMuZXhlY3V0b3IsXG4gICAgfSlcbiAgfVxuXG4gIGFzeW5jIGZ1bmN0aW9uIGluaXQoKSB7XG4gICAgbGV0IHBhZ2VoaXRfdHlwZSA9ICd2aWV3J1xuICAgIHRyeSB7XG4gICAgICAvLyBMb2FkIG5vdGVib29rXG4gICAgICAvLyBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi1VUy9kb2NzL1dlYi9BUEkvUmVxdWVzdC9jYWNoZVxuICAgICAgLy8gbm8tY2FjaGUgaW1wbGllcyBhIGNoZWNrIHdpdGggdGhlIHJlbW90ZSBzZXJ2ZXIgbm8gbWF0dGVyIHdoYXQsIGl0IHN0aWxsIHVzZXMgdGhlIGNhY2hlIGlmIHRoZSByZXNvdXJjZSBoYXNuJ3QgY2hhbmdlZFxuICAgICAgY29uc3QgcmVxID0gYXdhaXQgZmV0Y2goYCR7bmJkb3dubG9hZH0ke3dpbmRvdy5sb2NhdGlvbi5zZWFyY2h9YCwge1xuICAgICAgICAgIGNhY2hlOiAnbm8tY2FjaGUnLFxuICAgICAgICAgIGhlYWRlcnM6IHtcbiAgICAgICAgICAgICdBdXRob3JpemF0aW9uJzogJGF1dGguc3RhdGUgPT09ICdhdXRoJyA/IGBCZWFyZXIgJHskYXV0aC5rZXljbG9hay50b2tlbn1gIDogbnVsbCxcbiAgICAgICAgICB9LFxuICAgICAgICB9KVxuICAgICAgaWYgKHJlcS5zdGF0dXMgPT09IDQwNCkge1xuICAgICAgICB0aHJvdyBuZXcgRXJyb3IoJ05vdGVib29rIG5vdCBmb3VuZCcpXG4gICAgICB9XG4gICAgICBjb25zdCB2YWx1ZSA9IGF3YWl0IHJlcS5qc29uKClcbiAgICAgIGlmICh2YWx1ZS5tZXRhZGF0YS5hcHB5dGVyID09PSB1bmRlZmluZWQpIHtcbiAgICAgICAgY29uc29sZS53YXJuKCdDb252ZXJ0aW5nIGxlZ2FjeSBtZXRhZGF0YScpXG4gICAgICAgIHZhbHVlLm1ldGFkYXRhLmFwcHl0ZXIgPSB7XG4gICAgICAgICAgbmJjb25zdHJ1Y3Q6IHt9LFxuICAgICAgICB9XG4gICAgICAgIGlmICh2YWx1ZS5tZXRhZGF0YS5leGVjdXRpb25faW5mbyAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgdmFsdWUubWV0YWRhdGEuYXBweXRlci5uYmV4ZWN1dGUgPSB7XG4gICAgICAgICAgICBzdGFydGVkOiB2YWx1ZS5tZXRhZGF0YS5leGVjdXRpb25faW5mby5zdGFydGVkLFxuICAgICAgICAgICAgY29tcGxldGVkOiB2YWx1ZS5tZXRhZGF0YS5leGVjdXRpb25faW5mby5jb21wbGV0ZWQsXG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG4gICAgICBpZiAobmIgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICBuYiA9IHsuLi52YWx1ZSwgY2VsbHM6IHZhbHVlLmNlbGxzLm1hcCgoY2VsbCwgaW5kZXgpID0+ICh7IC4uLmNlbGwsIGluZGV4IH0pKSB9XG4gICAgICB9XG5cbiAgICAgIGlmICh2YWx1ZS5tZXRhZGF0YS5hcHB5dGVyLm5iZXhlY3V0ZSA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIC8vIEV4ZWN1dGUgbm90ZWJvb2sgaWYgaXQgaGFzbid0IGFscmVhZHkgYmVlbiBleGVjdXRlZFxuICAgICAgICBhd2FpdCBjb25uZWN0KHRydWUpXG4gICAgICAgIHBhZ2VoaXRfdHlwZSA9ICdleGVjdXRlJ1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgaWYgKHZhbHVlLm1ldGFkYXRhLmFwcHl0ZXIubmJleGVjdXRlLmNvbXBsZXRlZCA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgLy8gTm90ZWJvb2sgc3RhcnRlZCBidXQgaGFzbid0IGNvbXBsZXRlZFxuICAgICAgICAgIGF3YWl0IGNvbm5lY3QoZmFsc2UpXG4gICAgICAgICAgYXdhaXQgdGljaygpXG4gICAgICAgICAgc3RhdHVzID0gJ05vdGVib29rIGlzIGN1cnJlbnRseSBleGVjdXRpbmcsIGpvaW5pbmcgc2Vzc2lvbi4uLidcbiAgICAgICAgICBzdGF0dXNCZyA9ICdwcmltYXJ5J1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGF3YWl0IHRpY2soKVxuICAgICAgICAgIHN0YXR1cyA9IHVuZGVmaW5lZFxuICAgICAgICAgIG5iID0gey4uLnZhbHVlLCBjZWxsczogdmFsdWUuY2VsbHMubWFwKChjZWxsLCBpbmRleCkgPT4gKHsgLi4uY2VsbCwgaW5kZXggfSkpIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0gY2F0Y2ggKGUpIHtcbiAgICAgIGF3YWl0IHRpY2soKVxuICAgICAgc3RhdHVzID0gYCR7ZX1gXG4gICAgICBzdGF0dXNCZyA9ICdkYW5nZXInXG4gICAgfVxuXG4gICAgaWYgKHdpbmRvdy5fY29uZmlnLkVYVFJBUy5pbmRleE9mKCdjYXRhbG9nLWludGVncmF0aW9uJykgIT09IC0xKSB7XG4gICAgICAvLyBzZXR1cCBsb2NhbCBydW4gYXBweXRlciBsaW5rXG4gICAgICB0cnkge1xuICAgICAgICBjb25zdCBzbHVnID0gcGF0aHNbcGF0aHMubGVuZ3RoIC0gMl0gfHwgJydcblxuICAgICAgICBsZXQgYXBweXRlcl92ZXJzaW9uID0gJydcbiAgICAgICAgaWYgKG5iLm1ldGFkYXRhLmFwcHl0ZXIuaW5mbyAhPT0gdW5kZWZpbmVkKSBhcHB5dGVyX3ZlcnNpb24gPSBuYi5tZXRhZGF0YS5hcHB5dGVyLmluZm8udmVyc2lvbiB8fCAnJ1xuXG4gICAgICAgIGxldCBsaWJyYXJ5X3ZlcnNpb24gPSAnJ1xuICAgICAgICBpZiAobmIubWV0YWRhdGEuYXBweXRlci5uYmV4ZWN1dGUgIT09IHVuZGVmaW5lZCkgbGlicmFyeV92ZXJzaW9uID0gbmIubWV0YWRhdGEuYXBweXRlci5uYmV4ZWN1dGUudmVyc2lvbiB8fCAnJ1xuICAgICAgICBlbHNlIGlmIChuYi5tZXRhZGF0YS5hcHB5dGVyLm5iY29uc3RydWN0ICE9PSB1bmRlZmluZWQpIGxpYnJhcnlfdmVyc2lvbiA9IG5iLm1ldGFkYXRhLmFwcHl0ZXIubmJjb25zdHJ1Y3QudmVyc2lvbiB8fCAnJ1xuXG4gICAgICAgIGxvY2FsX3J1bl91cmwgPSBgJHt3aW5kb3cuX2NvbmZpZy5DQVRBTE9HX09SSUdJTn0vIy9ydW5uaW5nLWFwcHl0ZXJzLz9zbHVnPSR7c2x1Z30mYXBweXRlcl92ZXJzaW9uPSR7YXBweXRlcl92ZXJzaW9ufSZsaWJyYXJ5X3ZlcnNpb249JHtsaWJyYXJ5X3ZlcnNpb259JmlkPSR7aW5zdGFuY2VfaWR9YFxuICAgICAgfSBjYXRjaCAoZSkge1xuICAgICAgICBjb25zb2xlLmVycm9yKCdjYXRhbG9nLWludGVncmF0aW9uOiBsb2NhbF9ydW5fdXJsIHNldHVwIGVycm9yJylcbiAgICAgICAgY29uc29sZS5lcnJvcihlKVxuICAgICAgfVxuXG4gICAgICBwYWdlaGl0KHBhZ2VoaXRfdHlwZSlcbiAgICB9XG4gIH1cblxuICBsZXQgc2hvd19jb2RlID0gdW5kZWZpbmVkXG4gICQ6IGlmICgkaGFzaC5wYXJhbXMuc2hvd19jb2RlKSB7XG4gICAgc2hvd19jb2RlID0gSlNPTi5wYXJzZSgkaGFzaC5wYXJhbXMuc2hvd19jb2RlKVxuICB9XG5cbiAgbGV0IHBhdGggPSAkaGFzaC5wYXRoIC8vIGRlZmVyIHNjcm9sbCBoYW5kbGluZyBmb3IgaW5pdFxuICAkOiBpZiAoJGhhc2gucGF0aCAmJiAkaGFzaC5wYXRoICE9PSBwYXRoKSB7IC8vIGRlYm91bmNlIHNjcm9sbCBoYW5kbGluZ1xuICAgIHBhdGggPSAkaGFzaC5wYXRoKycnXG4gICAgY29uc3QgZWwgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChwYXRoKVxuICAgIGlmIChlbCkgZWwuc2Nyb2xsSW50b1ZpZXcoKVxuICB9XG5cbiAgLy8gaW5pdGlhbGl6YXRpb25cbiAgJDogaWYgKCRhdXRoLnN0YXRlICE9PSAnaW5pdCcpIHtcbiAgICBpbml0KClcbiAgICAgIC50aGVuKCgpID0+IHtcbiAgICAgICAgLy8gdHJpZ2dlciBzY3JvbGwgaGFuZGxlclxuICAgICAgICBwYXRoID0gdW5kZWZpbmVkXG4gICAgICB9KVxuICB9XG5cbiAgb25Nb3VudChhc3luYyAoKSA9PiB7XG4gICAgaWYgKHNob3dfY29kZSA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICBzaG93X2NvZGUgPSB3aW5kb3cuX2NvbmZpZy5FWFRSQVMuaW5kZXhPZignaGlkZS1jb2RlJykgPT09IC0xXG4gICAgfVxuICB9KVxuPC9zY3JpcHQ+XG5cbjxzdHlsZT5cbiAgLyogbWFya2Rvd24taXQtYW5jaG9ycyAqL1xuICA6Z2xvYmFsKGEuaGVhZGVyLWFuY2hvcikge1xuICAgIHRleHQtZGVjb3JhdGlvbjogbm9uZTtcbiAgICBjdXJzb3I6IHBvaW50ZXI7XG4gIH1cbiAgOmdsb2JhbChoMSkge1xuICAgIGRpc3BsYXk6IGJsb2NrO1xuICB9XG4gIDpnbG9iYWwoaDEpIDpnbG9iYWwoLmhlYWRlci1hbmNob3IpIHsgXG4gICAgZGlzcGxheTogbm9uZTtcbiAgfVxuICA6Z2xvYmFsKGgxKTpob3ZlciA6Z2xvYmFsKC5oZWFkZXItYW5jaG9yKSB7IFxuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgfVxuICA6Z2xvYmFsKGgyKSB7XG4gICAgZGlzcGxheTogYmxvY2s7XG4gIH1cbiAgOmdsb2JhbChoMikgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbiAgOmdsb2JhbChoMik6aG92ZXIgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgfVxuICA6Z2xvYmFsKGgzKSB7XG4gICAgZGlzcGxheTogYmxvY2s7XG4gIH1cbiAgOmdsb2JhbChoMykgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbiAgOmdsb2JhbChoMyk6aG92ZXIgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgfVxuICA6Z2xvYmFsKGg0KSB7XG4gICAgZGlzcGxheTogYmxvY2s7XG4gIH1cbiAgOmdsb2JhbChoNCkgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbiAgOmdsb2JhbChoNCk6aG92ZXIgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgfVxuICA6Z2xvYmFsKGg1KSB7XG4gICAgZGlzcGxheTogYmxvY2s7XG4gIH1cbiAgOmdsb2JhbChoNSkgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbiAgOmdsb2JhbChoNSk6aG92ZXIgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgfVxuICA6Z2xvYmFsKGg2KSB7XG4gICAgZGlzcGxheTogYmxvY2s7XG4gIH1cbiAgOmdsb2JhbChoNikgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IG5vbmU7XG4gIH1cbiAgOmdsb2JhbChoNik6aG92ZXIgOmdsb2JhbCguaGVhZGVyLWFuY2hvcikge1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgfVxuICAvKiBwcm9tcHQgYW5jaG9ycyAqL1xuICA6Z2xvYmFsKGEucHJvbXB0LWFuY2hvcikge1xuICAgIHRleHQtZGVjb3JhdGlvbjogbm9uZTtcbiAgICBjdXJzb3I6IHBvaW50ZXI7XG4gIH1cbiAgOmdsb2JhbCgucHJvbXB0KSA6Z2xvYmFsKC5wcm9tcHQtYW5jaG9yKSB7IFxuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgICB2aXNpYmlsaXR5OiBoaWRkZW47XG4gIH1cbiAgOmdsb2JhbCgucHJvbXB0KTpob3ZlciA6Z2xvYmFsKC5wcm9tcHQtYW5jaG9yKSB7XG4gICAgdmlzaWJpbGl0eTogdmlzaWJsZTtcbiAgfVxuXG4gIC8qIGVuc3VyZSBtZW51IGFwcGVhcnMgb3ZlciB0b2MgKi9cbiAgLmRyb3Bkb3duLW1lbnUge1xuICAgIHotaW5kZXg6IDEwMjE7XG4gIH1cbjwvc3R5bGU+XG5cbjxkaXYgY2xhc3M9XCJyb3dcIj5cbiAgPGRpdiBjbGFzcz1cImNvbC1zbS0xMiB0ZXh0LWNlbnRlclwiPlxuICAgIDxkaXYgY2xhc3M9XCJkLWlubGluZS1ibG9ja1wiPlxuICAgICAgPGRpdiBjbGFzcz1cImRyb3Bkb3duXCI+XG4gICAgICAgIDxidXR0b24gdHlwZT1cImJ1dHRvblwiIGNsYXNzPVwiYnRuIGJ0bi1wcmltYXJ5IGRyb3Bkb3duLXRvZ2dsZVwiIGRhdGEtdG9nZ2xlPVwiZHJvcGRvd25cIiBhcmlhLWhhc3BvcHVwPVwidHJ1ZVwiIGFyaWEtZXhwYW5kZWQ9XCJmYWxzZVwiPlxuICAgICAgICAgIERvd25sb2FkIE5vdGVib29rXG4gICAgICAgIDwvYnV0dG9uPlxuICAgICAgICA8ZGl2IGNsYXNzPVwiZHJvcGRvd24tbWVudVwiPlxuICAgICAgICAgIDxhXG4gICAgICAgICAgICBjbGFzcz1cImRyb3Bkb3duLWl0ZW1cIlxuICAgICAgICAgICAgaHJlZj17YCR7bmJkb3dubG9hZH0ke3dpbmRvdy5sb2NhdGlvbi5zZWFyY2h9YH1cbiAgICAgICAgICAgIHRpdGxlPVwiVGhlIHN0YW5kYWxvbmUganVweXRlciBub3RlYm9vayBhcyBzaG93blwiXG4gICAgICAgICAgPkp1cHl0ZXIgTm90ZWJvb2sgKC5pcHluYik8L2E+XG4gICAgICAgICAgPGFcbiAgICAgICAgICAgIGNsYXNzPVwiZHJvcGRvd24taXRlbVwiXG4gICAgICAgICAgICBocmVmPXtgLi4vZXhwb3J0LyR7aW5zdGFuY2VfaWR9LyR7d2luZG93LmxvY2F0aW9uLnNlYXJjaCA/IGAke3dpbmRvdy5sb2NhdGlvbi5zZWFyY2h9JmAgOiAnPyd9Zm9ybWF0PWh0bWxgfVxuICAgICAgICAgICAgdGl0bGU9XCJBbiBuYmNvbnZlcnQgSFRNTCBleHBvcnQgb2YgdGhlIG5vdGVib29rIGZvciBlYXN5IHZpZXdpbmcgaW4gYnJvd3NlclwiXG4gICAgICAgICAgPkhUTUwgRXhwb3J0ICguaHRtbCk8L2E+XG4gICAgICAgICAgPGFcbiAgICAgICAgICAgIGNsYXNzPVwiZHJvcGRvd24taXRlbVwiXG4gICAgICAgICAgICBocmVmPXtgLi4vZXhwb3J0LyR7aW5zdGFuY2VfaWR9LyR7d2luZG93LmxvY2F0aW9uLnNlYXJjaCA/IGAke3dpbmRvdy5sb2NhdGlvbi5zZWFyY2h9JmAgOiAnPyd9Zm9ybWF0PXppcGB9XG4gICAgICAgICAgICB0aXRsZT1cIkFuIGFyY2hpdmUgd2l0aCB0aGUgbm90ZWJvb2sgYW5kIGRlcGVuZGVudCBmaWxlcyBmb3IgcnVubmluZyBpdFwiXG4gICAgICAgICAgPk5vdGVib29rIEJ1bmRsZSAoLnppcCk8L2E+XG4gICAgICAgIDwvZGl2PlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gICAgeyNpZiB3aW5kb3cuX2NvbmZpZy5FWFRSQVMuaW5kZXhPZigndG9nZ2xlLWNvZGUnKSAhPT0gLTF9XG4gICAgICA8YnV0dG9uXG4gICAgICAgIHR5cGU9XCJidXR0b25cIiAgXG4gICAgICAgIGNsYXNzPVwiYnRuIGJ0bi1zZWNvbmRhcnkgd2hpdGVcIlxuICAgICAgICBvbjpjbGljaz17KCkgPT4ge1xuICAgICAgICAgICRoYXNoLnBhcmFtcy5zaG93X2NvZGUgPSBKU09OLnN0cmluZ2lmeSghc2hvd19jb2RlKVxuICAgICAgICAgICRoYXNoLnBhdGggPSAnJ1xuICAgICAgICB9fVxuICAgICAgPlxuICAgICAgICBUb2dnbGUgQ29kZVxuICAgICAgPC9idXR0b24+XG4gICAgey9pZn1cbiAgICB7I2lmIHdpbmRvdy5fY29uZmlnLkVYVFJBUy5pbmRleE9mKCdjYXRhbG9nLWludGVncmF0aW9uJykgIT09IC0xfVxuICAgIDxhXG4gICAgICBpZD1cInJ1bi1ub3RlYm9vay1sb2NhbGx5XCJcbiAgICAgIGNsYXNzPVwiYnRuIGJ0bi1wcmltYXJ5XCJcbiAgICAgIHJvbGU9XCJidXR0b25cIlxuICAgICAgY2xhc3M6ZGlzYWJsZWQ9e2xvY2FsX3J1bl91cmwgPT09IHVuZGVmaW5lZH1cbiAgICAgIGhyZWY9e2xvY2FsX3J1bl91cmx9XG4gICAgPlJ1biBMb2NhbGx5PC9hPlxuICAgIHsvaWZ9XG4gIDwvZGl2PlxuICA8ZGl2IGNsYXNzPVwidy0xMDBcIj4mbmJzcDs8L2Rpdj5cbiAgeyNpZiBzdGF0dXN9XG4gICAgPGRpdiBjbGFzcz1cImNvbC1zbS04IG9mZnNldC1zbS0yXCI+XG4gICAgICA8ZGl2IGNsYXNzPVwiYWxlcnQgYWxlcnQte3N0YXR1c0JnfVwiIHJvbGU9XCJhbGVydFwiPlxuICAgICAgICB7c3RhdHVzfVxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gIHsvaWZ9XG4gIDxkaXYgY2xhc3M9XCJ3LTEwMFwiPjwvZGl2PlxuICB7I2lmICR0b2MgIT09IHVuZGVmaW5lZH1cbiAgICA8TGF6eVxuICAgICAgbW9kdWxlPXsoKSA9PiBpbXBvcnQoJ0AvZXh0cmFzL2NhdGFsb2ctaW50ZWdyYXRpb24vVGFibGVPZkNvbnRlbnRzLnN2ZWx0ZScpfVxuICAgICAgcHJvcHM9e3sgdG9jOiAkdG9jIH19XG4gICAgLz5cbiAgey9pZn1cbiAgeyNpZiBzdGF0dXMgPT09ICdMb2FkaW5nLi4uJ31cbiAgICA8ZGl2IGNsYXNzPVwiY29sLXNtLTEyIHRleHQtY2VudGVyXCI+XG4gICAgICA8TG9hZGVyIC8+XG4gICAgPC9kaXY+XG4gIHsvaWZ9XG4gIDxkaXZcbiAgICBiaW5kOnRoaXM9e25vdGVib29rUmVmfVxuICAgIGNsYXNzPVwiY29sLXNtLTEyXCJcbiAgICBjbGFzczpjb2wtbWQtOT17JHRvYyAhPT0gdW5kZWZpbmVkfVxuICAgIGNsYXNzOmNvbC14bC0xMD17JHRvYyAhPT0gdW5kZWZpbmVkfVxuICA+XG4gICAgeyNpZiBuYn1cbiAgICAgIDxMYXp5XG4gICAgICAgIG1vZHVsZT17KCkgPT4gaW1wb3J0KCdAL2NvbXBvbmVudHMvanVweXRlci9Ob3RlYm9vay5zdmVsdGUnKX1cbiAgICAgICAgcHJvcHM9e3tcbiAgICAgICAgICBuYiwgc2hvd19jb2RlLCBjdXJyZW50X2NvZGVfY2VsbFxuICAgICAgICB9fVxuICAgICAgLz5cbiAgICB7L2lmfVxuICA8L2Rpdj5cbjwvZGl2PlxuIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQStNVSxlQUFlLEFBQUUsQ0FBQyxBQUN4QixlQUFlLENBQUUsSUFBSSxDQUNyQixNQUFNLENBQUUsT0FBTyxBQUNqQixDQUFDLEFBQ08sRUFBRSxBQUFFLENBQUMsQUFDWCxPQUFPLENBQUUsS0FBSyxBQUNoQixDQUFDLEFBQ08sRUFBRSxBQUFDLENBQUMsQUFBUSxjQUFjLEFBQUUsQ0FBQyxBQUNuQyxPQUFPLENBQUUsSUFBSSxBQUNmLENBQUMsQUFDTyxFQUFFLEFBQUMsTUFBTSxDQUFDLEFBQVEsY0FBYyxBQUFFLENBQUMsQUFDekMsT0FBTyxDQUFFLFlBQVksQUFDdkIsQ0FBQyxBQUNPLEVBQUUsQUFBRSxDQUFDLEFBQ1gsT0FBTyxDQUFFLEtBQUssQUFDaEIsQ0FBQyxBQUNPLEVBQUUsQUFBQyxDQUFDLEFBQVEsY0FBYyxBQUFFLENBQUMsQUFDbkMsT0FBTyxDQUFFLElBQUksQUFDZixDQUFDLEFBQ08sRUFBRSxBQUFDLE1BQU0sQ0FBQyxBQUFRLGNBQWMsQUFBRSxDQUFDLEFBQ3pDLE9BQU8sQ0FBRSxZQUFZLEFBQ3ZCLENBQUMsQUFDTyxFQUFFLEFBQUUsQ0FBQyxBQUNYLE9BQU8sQ0FBRSxLQUFLLEFBQ2hCLENBQUMsQUFDTyxFQUFFLEFBQUMsQ0FBQyxBQUFRLGNBQWMsQUFBRSxDQUFDLEFBQ25DLE9BQU8sQ0FBRSxJQUFJLEFBQ2YsQ0FBQyxBQUNPLEVBQUUsQUFBQyxNQUFNLENBQUMsQUFBUSxjQUFjLEFBQUUsQ0FBQyxBQUN6QyxPQUFPLENBQUUsWUFBWSxBQUN2QixDQUFDLEFBQ08sRUFBRSxBQUFFLENBQUMsQUFDWCxPQUFPLENBQUUsS0FBSyxBQUNoQixDQUFDLEFBQ08sRUFBRSxBQUFDLENBQUMsQUFBUSxjQUFjLEFBQUUsQ0FBQyxBQUNuQyxPQUFPLENBQUUsSUFBSSxBQUNmLENBQUMsQUFDTyxFQUFFLEFBQUMsTUFBTSxDQUFDLEFBQVEsY0FBYyxBQUFFLENBQUMsQUFDekMsT0FBTyxDQUFFLFlBQVksQUFDdkIsQ0FBQyxBQUNPLEVBQUUsQUFBRSxDQUFDLEFBQ1gsT0FBTyxDQUFFLEtBQUssQUFDaEIsQ0FBQyxBQUNPLEVBQUUsQUFBQyxDQUFDLEFBQVEsY0FBYyxBQUFFLENBQUMsQUFDbkMsT0FBTyxDQUFFLElBQUksQUFDZixDQUFDLEFBQ08sRUFBRSxBQUFDLE1BQU0sQ0FBQyxBQUFRLGNBQWMsQUFBRSxDQUFDLEFBQ3pDLE9BQU8sQ0FBRSxZQUFZLEFBQ3ZCLENBQUMsQUFDTyxFQUFFLEFBQUUsQ0FBQyxBQUNYLE9BQU8sQ0FBRSxLQUFLLEFBQ2hCLENBQUMsQUFDTyxFQUFFLEFBQUMsQ0FBQyxBQUFRLGNBQWMsQUFBRSxDQUFDLEFBQ25DLE9BQU8sQ0FBRSxJQUFJLEFBQ2YsQ0FBQyxBQUNPLEVBQUUsQUFBQyxNQUFNLENBQUMsQUFBUSxjQUFjLEFBQUUsQ0FBQyxBQUN6QyxPQUFPLENBQUUsWUFBWSxBQUN2QixDQUFDLEFBRU8sZUFBZSxBQUFFLENBQUMsQUFDeEIsZUFBZSxDQUFFLElBQUksQ0FDckIsTUFBTSxDQUFFLE9BQU8sQUFDakIsQ0FBQyxBQUNPLE9BQU8sQUFBQyxDQUFDLEFBQVEsY0FBYyxBQUFFLENBQUMsQUFDeEMsT0FBTyxDQUFFLFlBQVksQ0FDckIsVUFBVSxDQUFFLE1BQU0sQUFDcEIsQ0FBQyxBQUNPLE9BQU8sQUFBQyxNQUFNLENBQUMsQUFBUSxjQUFjLEFBQUUsQ0FBQyxBQUM5QyxVQUFVLENBQUUsT0FBTyxBQUNyQixDQUFDLEFBR0QsY0FBYyxlQUFDLENBQUMsQUFDZCxPQUFPLENBQUUsSUFBSSxBQUNmLENBQUMifQ== */");
} // (311:4) {#if window._config.EXTRAS.indexOf('toggle-code') !== -1}


function create_if_block_5(ctx) {
  let button;
  let mounted;
  let dispose;
  const block = {
    c: function create() {
      button = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("button");
      button.textContent = "Toggle Code";
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "type", "button");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "class", "btn btn-secondary white");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(button, file, 311, 6, 9288);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, button, anchor);

      if (!mounted) {
        dispose = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.listen_dev)(button, "click",
        /*click_handler*/
        ctx[13], false, false, false);
        mounted = true;
      }
    },
    p: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(button);
      mounted = false;
      dispose();
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_5.name,
    type: "if",
    source: "(311:4) {#if window._config.EXTRAS.indexOf('toggle-code') !== -1}",
    ctx
  });
  return block;
} // (323:4) {#if window._config.EXTRAS.indexOf('catalog-integration') !== -1}


function create_if_block_4(ctx) {
  let a;
  let t;
  const block = {
    c: function create() {
      a = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("a");
      t = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("Run Locally");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a, "id", "run-notebook-locally");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a, "class", "btn btn-primary");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a, "role", "button");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a, "href",
      /*local_run_url*/
      ctx[4]);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(a, "disabled",
      /*local_run_url*/
      ctx[4] === undefined);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(a, file, 323, 4, 9613);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, a, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(a, t);
    },
    p: function update(ctx, dirty) {
      if (dirty &
      /*local_run_url*/
      16) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a, "href",
        /*local_run_url*/
        ctx[4]);
      }

      if (dirty &
      /*local_run_url, undefined*/
      16) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(a, "disabled",
        /*local_run_url*/
        ctx[4] === undefined);
      }
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(a);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_4.name,
    type: "if",
    source: "(323:4) {#if window._config.EXTRAS.indexOf('catalog-integration') !== -1}",
    ctx
  });
  return block;
} // (334:2) {#if status}


function create_if_block_3(ctx) {
  let div1;
  let div0;
  let t;
  let div0_class_value;
  const block = {
    c: function create() {
      div1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      t = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(
      /*status*/
      ctx[5]);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "class", div0_class_value = "alert alert-" +
      /*statusBg*/
      ctx[6] + " svelte-1g0xm7f");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "role", "alert");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div0, file, 335, 6, 9910);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div1, "class", "col-sm-8 offset-sm-2");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div1, file, 334, 4, 9869);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div1, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, div0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t);
    },
    p: function update(ctx, dirty) {
      if (dirty &
      /*status*/
      32) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_data_dev)(t,
      /*status*/
      ctx[5]);

      if (dirty &
      /*statusBg*/
      64 && div0_class_value !== (div0_class_value = "alert alert-" +
      /*statusBg*/
      ctx[6] + " svelte-1g0xm7f")) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "class", div0_class_value);
      }
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div1);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_3.name,
    type: "if",
    source: "(334:2) {#if status}",
    ctx
  });
  return block;
} // (342:2) {#if $toc !== undefined}


function create_if_block_2(ctx) {
  let lazy;
  let current;
  lazy = new _components_Lazy_svelte__WEBPACK_IMPORTED_MODULE_4__["default"]({
    props: {
      module: func,
      props: {
        toc:
        /*$toc*/
        ctx[9]
      }
    },
    $$inline: true
  });
  const block = {
    c: function create() {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_component)(lazy.$$.fragment);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.mount_component)(lazy, target, anchor);
      current = true;
    },
    p: function update(ctx, dirty) {
      const lazy_changes = {};
      if (dirty &
      /*$toc*/
      512) lazy_changes.props = {
        toc:
        /*$toc*/
        ctx[9]
      };
      lazy.$set(lazy_changes);
    },
    i: function intro(local) {
      if (current) return;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(lazy.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(lazy.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_component)(lazy, detaching);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_2.name,
    type: "if",
    source: "(342:2) {#if $toc !== undefined}",
    ctx
  });
  return block;
} // (348:2) {#if status === 'Loading...'}


function create_if_block_1(ctx) {
  let div;
  let loader;
  let current;
  loader = new _components_Loader_svelte__WEBPACK_IMPORTED_MODULE_5__["default"]({
    $$inline: true
  });
  const block = {
    c: function create() {
      div = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_component)(loader.$$.fragment);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div, "class", "col-sm-12 text-center");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div, file, 348, 4, 10236);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.mount_component)(loader, div, null);
      current = true;
    },
    i: function intro(local) {
      if (current) return;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(loader.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(loader.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_component)(loader);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_1.name,
    type: "if",
    source: "(348:2) {#if status === 'Loading...'}",
    ctx
  });
  return block;
} // (359:4) {#if nb}


function create_if_block(ctx) {
  let lazy;
  let current;
  lazy = new _components_Lazy_svelte__WEBPACK_IMPORTED_MODULE_4__["default"]({
    props: {
      module: func_1,
      props: {
        nb:
        /*nb*/
        ctx[3],
        show_code:
        /*show_code*/
        ctx[8],
        current_code_cell:
        /*current_code_cell*/
        ctx[7]
      }
    },
    $$inline: true
  });
  const block = {
    c: function create() {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.create_component)(lazy.$$.fragment);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.mount_component)(lazy, target, anchor);
      current = true;
    },
    p: function update(ctx, dirty) {
      const lazy_changes = {};
      if (dirty &
      /*nb, show_code, current_code_cell*/
      392) lazy_changes.props = {
        nb:
        /*nb*/
        ctx[3],
        show_code:
        /*show_code*/
        ctx[8],
        current_code_cell:
        /*current_code_cell*/
        ctx[7]
      };
      lazy.$set(lazy_changes);
    },
    i: function intro(local) {
      if (current) return;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(lazy.$$.fragment, local);
      current = true;
    },
    o: function outro(local) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(lazy.$$.fragment, local);
      current = false;
    },
    d: function destroy(detaching) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.destroy_component)(lazy, detaching);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block.name,
    type: "if",
    source: "(359:4) {#if nb}",
    ctx
  });
  return block;
}

function create_fragment(ctx) {
  let div7;
  let div3;
  let div2;
  let div1;
  let button;
  let t1;
  let div0;
  let a0;
  let t2;
  let a0_href_value;
  let t3;
  let a1;
  let t4;
  let a1_href_value;
  let t5;
  let a2;
  let t6;
  let a2_href_value;
  let t7;
  let show_if_1 = window._config.EXTRAS.indexOf('toggle-code') !== -1;
  let t8;
  let show_if = window._config.EXTRAS.indexOf('catalog-integration') !== -1;
  let t9;
  let div4;
  let t11;
  let t12;
  let div5;
  let t13;
  let t14;
  let t15;
  let div6;
  let current;
  let if_block0 = show_if_1 && create_if_block_5(ctx);
  let if_block1 = show_if && create_if_block_4(ctx);
  let if_block2 =
  /*status*/
  ctx[5] && create_if_block_3(ctx);
  let if_block3 =
  /*$toc*/
  ctx[9] !== undefined && create_if_block_2(ctx);
  let if_block4 =
  /*status*/
  ctx[5] === 'Loading...' && create_if_block_1(ctx);
  let if_block5 =
  /*nb*/
  ctx[3] && create_if_block(ctx);
  const block = {
    c: function create() {
      div7 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div3 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      button = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("button");
      button.textContent = "Download Notebook";
      t1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      a0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("a");
      t2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("Jupyter Notebook (.ipynb)");
      t3 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      a1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("a");
      t4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("HTML Export (.html)");
      t5 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      a2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("a");
      t6 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("Notebook Bundle (.zip)");
      t7 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      if (if_block0) if_block0.c();
      t8 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      if (if_block1) if_block1.c();
      t9 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div4.textContent = " ";
      t11 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      if (if_block2) if_block2.c();
      t12 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div5 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      t13 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      if (if_block3) if_block3.c();
      t14 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      if (if_block4) if_block4.c();
      t15 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div6 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      if (if_block5) if_block5.c();
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "type", "button");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "class", "btn btn-primary dropdown-toggle");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "data-toggle", "dropdown");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "aria-haspopup", "true");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "aria-expanded", "false");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(button, file, 288, 8, 8182);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a0, "class", "dropdown-item");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a0, "href", a0_href_value = `${
      /*nbdownload*/
      ctx[0]}${window.location.search}`);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a0, "title", "The standalone jupyter notebook as shown");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(a0, file, 292, 10, 8403);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a1, "class", "dropdown-item");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a1, "href", a1_href_value = `../export/${
      /*instance_id*/
      ctx[10]}/${window.location.search ? `${window.location.search}&` : '?'}format=html`);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a1, "title", "An nbconvert HTML export of the notebook for easy viewing in browser");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(a1, file, 297, 10, 8612);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a2, "class", "dropdown-item");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a2, "href", a2_href_value = `../export/${
      /*instance_id*/
      ctx[10]}/${window.location.search ? `${window.location.search}&` : '?'}format=zip`);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a2, "title", "An archive with the notebook and dependent files for running it");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(a2, file, 302, 10, 8903);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "class", "dropdown-menu svelte-1g0xm7f");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div0, file, 291, 8, 8365);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div1, "class", "dropdown");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div1, file, 287, 6, 8151);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div2, "class", "d-inline-block");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div2, file, 286, 4, 8116);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div3, "class", "col-sm-12 text-center");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div3, file, 285, 2, 8076);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div4, "class", "w-100");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div4, file, 332, 2, 9818);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div5, "class", "w-100");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div5, file, 340, 2, 10011);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div6, "class", "col-sm-12");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(div6, "col-md-9",
      /*$toc*/
      ctx[9] !== undefined);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(div6, "col-xl-10",
      /*$toc*/
      ctx[9] !== undefined);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div6, file, 352, 2, 10310);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div7, "class", "row");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div7, file, 284, 0, 8056);
    },
    l: function claim(nodes) {
      throw new Error_1("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div7, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div3);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, div2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div2, div1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, button);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, t1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, div0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, a0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(a0, t2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t3);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, a1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(a1, t4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t5);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, a2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(a2, t6);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, t7);
      if (if_block0) if_block0.m(div3, null);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, t8);
      if (if_block1) if_block1.m(div3, null);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t9);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t11);
      if (if_block2) if_block2.m(div7, null);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t12);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div5);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t13);
      if (if_block3) if_block3.m(div7, null);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t14);
      if (if_block4) if_block4.m(div7, null);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t15);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div6);
      if (if_block5) if_block5.m(div6, null);
      /*div6_binding*/

      ctx[14](div6);
      current = true;
    },
    p: function update(ctx, [dirty]) {
      if (!current || dirty &
      /*nbdownload*/
      1 && a0_href_value !== (a0_href_value = `${
      /*nbdownload*/
      ctx[0]}${window.location.search}`)) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a0, "href", a0_href_value);
      }

      if (show_if_1) if_block0.p(ctx, dirty);
      if (show_if) if_block1.p(ctx, dirty);

      if (
      /*status*/
      ctx[5]) {
        if (if_block2) {
          if_block2.p(ctx, dirty);
        } else {
          if_block2 = create_if_block_3(ctx);
          if_block2.c();
          if_block2.m(div7, t12);
        }
      } else if (if_block2) {
        if_block2.d(1);
        if_block2 = null;
      }

      if (
      /*$toc*/
      ctx[9] !== undefined) {
        if (if_block3) {
          if_block3.p(ctx, dirty);

          if (dirty &
          /*$toc*/
          512) {
            (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block3, 1);
          }
        } else {
          if_block3 = create_if_block_2(ctx);
          if_block3.c();
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block3, 1);
          if_block3.m(div7, t14);
        }
      } else if (if_block3) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.group_outros)();
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_block3, 1, 1, () => {
          if_block3 = null;
        });
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.check_outros)();
      }

      if (
      /*status*/
      ctx[5] === 'Loading...') {
        if (if_block4) {
          if (dirty &
          /*status*/
          32) {
            (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block4, 1);
          }
        } else {
          if_block4 = create_if_block_1(ctx);
          if_block4.c();
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block4, 1);
          if_block4.m(div7, t15);
        }
      } else if (if_block4) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.group_outros)();
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_block4, 1, 1, () => {
          if_block4 = null;
        });
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.check_outros)();
      }

      if (
      /*nb*/
      ctx[3]) {
        if (if_block5) {
          if_block5.p(ctx, dirty);

          if (dirty &
          /*nb*/
          8) {
            (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block5, 1);
          }
        } else {
          if_block5 = create_if_block(ctx);
          if_block5.c();
          (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block5, 1);
          if_block5.m(div6, null);
        }
      } else if (if_block5) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.group_outros)();
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_block5, 1, 1, () => {
          if_block5 = null;
        });
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.check_outros)();
      }

      if (dirty &
      /*$toc, undefined*/
      512) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(div6, "col-md-9",
        /*$toc*/
        ctx[9] !== undefined);
      }

      if (dirty &
      /*$toc, undefined*/
      512) {
        (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.toggle_class)(div6, "col-xl-10",
        /*$toc*/
        ctx[9] !== undefined);
      }
    },
    i: function intro(local) {
      if (current) return;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block3);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_in)(if_block5);
      current = true;
    },
    o: function outro(local) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_block3);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_block4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.transition_out)(if_block5);
      current = false;
    },
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div7);
      if (if_block0) if_block0.d();
      if (if_block1) if_block1.d();
      if (if_block2) if_block2.d();
      if (if_block3) if_block3.d();
      if (if_block4) if_block4.d();
      if (if_block5) if_block5.d();
      /*div6_binding*/

      ctx[14](null);
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

const func = () => __webpack_require__.e(/*! import() */ "extras_catalog-integration_TableOfContents_svelte").then(__webpack_require__.bind(__webpack_require__, /*! @/extras/catalog-integration/TableOfContents.svelte */ "./extras/catalog-integration/TableOfContents.svelte"));

const func_1 = () => Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_ansi_up_ansi_up_js-node_modules_markdown-it_index_js-node_modules_highli-574955"), __webpack_require__.e("components_jupyter_Notebook_svelte")]).then(__webpack_require__.bind(__webpack_require__, /*! @/components/jupyter/Notebook.svelte */ "./components/jupyter/Notebook.svelte"));

function instance($$self, $$props, $$invalidate) {
  let $auth;
  let $hash;
  let $toc;
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_store)(_lib_stores_keycloak_auth_store__WEBPACK_IMPORTED_MODULE_2__["default"], 'auth');
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.component_subscribe)($$self, _lib_stores_keycloak_auth_store__WEBPACK_IMPORTED_MODULE_2__["default"], $$value => $$invalidate(12, $auth = $$value));
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_store)(_lib_stores_url_hash_store__WEBPACK_IMPORTED_MODULE_3__["default"], 'hash');
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.component_subscribe)($$self, _lib_stores_url_hash_store__WEBPACK_IMPORTED_MODULE_3__["default"], $$value => $$invalidate(2, $hash = $$value));
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_store)(_extras_catalog_integration_toc__WEBPACK_IMPORTED_MODULE_8__["default"], 'toc');
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.component_subscribe)($$self, _extras_catalog_integration_toc__WEBPACK_IMPORTED_MODULE_8__["default"], $$value => $$invalidate(9, $toc = $$value));
  let {
    $$slots: slots = {},
    $$scope
  } = $$props;
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_slots)('Landing', slots, []);
  let {
    nbdownload
  } = $$props;
  const paths = window.location.pathname.split('/').filter(p => p);
  const instance_id = paths[paths.length - 1];
  let nb;
  let notebookRef;
  let local_run_url; // dynamic notebook

  let status = 'Loading...';
  let statusBg = 'primary';
  var current_code_cell;

  async function setup_async_exec(socket) {
    socket.on('connect', async () => {
      await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
      $$invalidate(5, status = `Connected to server, re-initializing...`);
      $$invalidate(6, statusBg = 'warning');
      await init();
    });
    socket.on('reconnect', async () => {
      await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
      $$invalidate(5, status = `Reconnecting to server...`);
      $$invalidate(6, statusBg = 'warning');
    });
    socket.on('disconnect', async reason => {
      if (reason !== 'io client disconnect') {
        await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
        $$invalidate(5, status = `Disconnected from server...`);
        $$invalidate(6, statusBg = 'danger');
      }
    });
    socket.on('status', async value => {
      await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
      $$invalidate(5, status = value);
      $$invalidate(6, statusBg = 'primary');

      if (status === 'Success') {
        $$invalidate(7, current_code_cell = undefined);

        if (!window._config.DEBUG) {
          socket.disconnect();
        }
      }
    });
    socket.on('error', async value => {
      await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
      $$invalidate(7, current_code_cell = undefined);
      $$invalidate(5, status = `Error: ${value}`);
      $$invalidate(6, statusBg = 'danger');
    });
    socket.on('nb', async value => {
      await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
      $$invalidate(3, nb = { ...value,
        cells: value.cells.map((cell, index) => ({ ...cell,
          index
        }))
      });
    });
    socket.on('progress', async value => {
      await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
      $$invalidate(7, current_code_cell = value);
    });
    socket.on('cell', async value_index => {
      let value = value_index[0];
      let cell_index = value_index[1];
      await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
      $$invalidate(3, nb.cells[cell_index] = { ...nb.cells[cell_index],
        ...value
      }, nb);
    });
    (0,_lib_socketio__WEBPACK_IMPORTED_MODULE_6__.setup_chunking)(socket);
  }

  let connect_init = false;

  async function connect(execute) {
    const {
      default: socket
    } = await Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_socket_io-client_build_esm_index_js"), __webpack_require__.e("lib_socket_js")]).then(__webpack_require__.bind(__webpack_require__, /*! @/lib/socket */ "./lib/socket.js"));

    if (!connect_init) {
      connect_init = true; // ensure we're connected

      await new Promise((resolve, reject) => {
        if (socket.connected) resolve();else socket.on('connect', resolve);
      });
      await setup_async_exec(socket);
    }

    const evt = execute ? 'submit' : 'join';
    socket.emit(evt, {
      _id: instance_id,
      _auth: $auth.keycloak.token,
      _storage: $hash.server.params.storage,
      _executor: $hash.server.params.executor
    });
  }

  async function init() {
    let pagehit_type = 'view';

    try {
      // Load notebook
      // https://developer.mozilla.org/en-US/docs/Web/API/Request/cache
      // no-cache implies a check with the remote server no matter what, it still uses the cache if the resource hasn't changed
      const req = await fetch(`${nbdownload}${window.location.search}`, {
        cache: 'no-cache',
        headers: {
          'Authorization': $auth.state === 'auth' ? `Bearer ${$auth.keycloak.token}` : null
        }
      });

      if (req.status === 404) {
        throw new Error('Notebook not found');
      }

      const value = await req.json();

      if (value.metadata.appyter === undefined) {
        console.warn('Converting legacy metadata');
        value.metadata.appyter = {
          nbconstruct: {}
        };

        if (value.metadata.execution_info !== undefined) {
          value.metadata.appyter.nbexecute = {
            started: value.metadata.execution_info.started,
            completed: value.metadata.execution_info.completed
          };
        }
      }

      if (nb === undefined) {
        $$invalidate(3, nb = { ...value,
          cells: value.cells.map((cell, index) => ({ ...cell,
            index
          }))
        });
      }

      if (value.metadata.appyter.nbexecute === undefined) {
        // Execute notebook if it hasn't already been executed
        await connect(true);
        pagehit_type = 'execute';
      } else {
        if (value.metadata.appyter.nbexecute.completed === undefined) {
          // Notebook started but hasn't completed
          await connect(false);
          await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
          $$invalidate(5, status = 'Notebook is currently executing, joining session...');
          $$invalidate(6, statusBg = 'primary');
        } else {
          await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
          $$invalidate(5, status = undefined);
          $$invalidate(3, nb = { ...value,
            cells: value.cells.map((cell, index) => ({ ...cell,
              index
            }))
          });
        }
      }
    } catch (e) {
      await (0,svelte__WEBPACK_IMPORTED_MODULE_1__.tick)();
      $$invalidate(5, status = `${e}`);
      $$invalidate(6, statusBg = 'danger');
    }

    if (window._config.EXTRAS.indexOf('catalog-integration') !== -1) {
      // setup local run appyter link
      try {
        const slug = paths[paths.length - 2] || '';
        let appyter_version = '';
        if (nb.metadata.appyter.info !== undefined) appyter_version = nb.metadata.appyter.info.version || '';
        let library_version = '';
        if (nb.metadata.appyter.nbexecute !== undefined) library_version = nb.metadata.appyter.nbexecute.version || '';else if (nb.metadata.appyter.nbconstruct !== undefined) library_version = nb.metadata.appyter.nbconstruct.version || '';
        $$invalidate(4, local_run_url = `${window._config.CATALOG_ORIGIN}/#/running-appyters/?slug=${slug}&appyter_version=${appyter_version}&library_version=${library_version}&id=${instance_id}`);
      } catch (e) {
        console.error('catalog-integration: local_run_url setup error');
        console.error(e);
      }

      (0,_extras_catalog_integration_pagehit__WEBPACK_IMPORTED_MODULE_7__["default"])(pagehit_type);
    }
  }

  let show_code = undefined;
  let path = $hash.path; // defer scroll handling for init

  (0,svelte__WEBPACK_IMPORTED_MODULE_1__.onMount)(async () => {
    if (show_code === undefined) {
      $$invalidate(8, show_code = window._config.EXTRAS.indexOf('hide-code') === -1);
    }
  });
  const writable_props = ['nbdownload'];
  Object.keys($$props).forEach(key => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console_1.warn(`<Landing> was created with unknown prop '${key}'`);
  });

  const click_handler = () => {
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_store_value)(_lib_stores_url_hash_store__WEBPACK_IMPORTED_MODULE_3__["default"], $hash.params.show_code = JSON.stringify(!show_code), $hash);
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_store_value)(_lib_stores_url_hash_store__WEBPACK_IMPORTED_MODULE_3__["default"], $hash.path = '', $hash);
  };

  function div6_binding($$value) {
    svelte_internal__WEBPACK_IMPORTED_MODULE_0__.binding_callbacks[$$value ? 'unshift' : 'push'](() => {
      notebookRef = $$value;
      $$invalidate(1, notebookRef);
    });
  }

  $$self.$$set = $$props => {
    if ('nbdownload' in $$props) $$invalidate(0, nbdownload = $$props.nbdownload);
  };

  $$self.$capture_state = () => ({
    tick: svelte__WEBPACK_IMPORTED_MODULE_1__.tick,
    onMount: svelte__WEBPACK_IMPORTED_MODULE_1__.onMount,
    auth: _lib_stores_keycloak_auth_store__WEBPACK_IMPORTED_MODULE_2__["default"],
    hash: _lib_stores_url_hash_store__WEBPACK_IMPORTED_MODULE_3__["default"],
    Lazy: _components_Lazy_svelte__WEBPACK_IMPORTED_MODULE_4__["default"],
    Loader: _components_Loader_svelte__WEBPACK_IMPORTED_MODULE_5__["default"],
    setup_chunking: _lib_socketio__WEBPACK_IMPORTED_MODULE_6__.setup_chunking,
    pagehit: _extras_catalog_integration_pagehit__WEBPACK_IMPORTED_MODULE_7__["default"],
    toc: _extras_catalog_integration_toc__WEBPACK_IMPORTED_MODULE_8__["default"],
    nbdownload,
    paths,
    instance_id,
    nb,
    notebookRef,
    local_run_url,
    status,
    statusBg,
    current_code_cell,
    setup_async_exec,
    connect_init,
    connect,
    init,
    show_code,
    path,
    $auth,
    $hash,
    $toc
  });

  $$self.$inject_state = $$props => {
    if ('nbdownload' in $$props) $$invalidate(0, nbdownload = $$props.nbdownload);
    if ('nb' in $$props) $$invalidate(3, nb = $$props.nb);
    if ('notebookRef' in $$props) $$invalidate(1, notebookRef = $$props.notebookRef);
    if ('local_run_url' in $$props) $$invalidate(4, local_run_url = $$props.local_run_url);
    if ('status' in $$props) $$invalidate(5, status = $$props.status);
    if ('statusBg' in $$props) $$invalidate(6, statusBg = $$props.statusBg);
    if ('current_code_cell' in $$props) $$invalidate(7, current_code_cell = $$props.current_code_cell);
    if ('connect_init' in $$props) connect_init = $$props.connect_init;
    if ('show_code' in $$props) $$invalidate(8, show_code = $$props.show_code);
    if ('path' in $$props) $$invalidate(11, path = $$props.path);
  };

  if ($$props && "$$inject" in $$props) {
    $$self.$inject_state($$props.$$inject);
  }

  $$self.$$.update = () => {
    if ($$self.$$.dirty &
    /*notebookRef*/
    2) {
      // table of contents
      $: if (window._config.EXTRAS.indexOf('toc') !== -1) _extras_catalog_integration_toc__WEBPACK_IMPORTED_MODULE_8__["default"].attach(notebookRef);
    }

    if ($$self.$$.dirty &
    /*$hash*/
    4) {
      $: if ($hash.params.show_code) {
        $$invalidate(8, show_code = JSON.parse($hash.params.show_code));
      }
    }

    if ($$self.$$.dirty &
    /*$hash, path*/
    2052) {
      $: if ($hash.path && $hash.path !== path) {
        // debounce scroll handling
        $$invalidate(11, path = $hash.path + '');
        const el = document.getElementById(path);
        if (el) el.scrollIntoView();
      }
    }

    if ($$self.$$.dirty &
    /*$auth*/
    4096) {
      // initialization
      $: if ($auth.state !== 'init') {
        init().then(() => {
          // trigger scroll handler
          $$invalidate(11, path = undefined);
        });
      }
    }
  };

  return [nbdownload, notebookRef, $hash, nb, local_run_url, status, statusBg, current_code_cell, show_code, $toc, instance_id, path, $auth, click_handler, div6_binding];
}

class Landing extends svelte_internal__WEBPACK_IMPORTED_MODULE_0__.SvelteComponentDev {
  constructor(options) {
    super(options);
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.init)(this, options, instance, create_fragment, svelte_internal__WEBPACK_IMPORTED_MODULE_0__.safe_not_equal, {
      nbdownload: 0
    }, add_css);
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterComponent", {
      component: this,
      tagName: "Landing",
      options,
      id: create_fragment.name
    });
    const {
      ctx
    } = this.$$;
    const props = options.props || {};

    if (
    /*nbdownload*/
    ctx[0] === undefined && !('nbdownload' in props)) {
      console_1.warn("<Landing> was created without expected prop 'nbdownload'");
    }
  }

  get nbdownload() {
    throw new Error_1("<Landing>: Props cannot be read directly from the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

  set nbdownload(value) {
    throw new Error_1("<Landing>: Props cannot be set directly on the component instance unless compiling with 'accessors: true' or '<svelte:options accessors/>'");
  }

}




if (module && module.hot) {}

/* harmony default export */ __webpack_exports__["default"] = (Landing);

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

/***/ "./extras/catalog-integration/pagehit.js":
/*!***********************************************!*\
  !*** ./extras/catalog-integration/pagehit.js ***!
  \***********************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": function() { return /* binding */ pagehit; }
/* harmony export */ });
/* harmony import */ var _utils_get_require__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @/utils/get_require */ "./utils/get_require.js");

function pagehit(pagehit_type) {
  if (window._config.EXTRAS.indexOf('catalog-integration') !== -1) {
    if (window._config.pagehit !== undefined) {
      window._config.pagehit(pagehit_type);
    } else {
      console.info(`[catalog-integration:pagehit]: ${pagehit_type}`);
      console.warn('[catalog-integration:pagehit]: attempting deprecated requirejs resolution');
      (0,_utils_get_require__WEBPACK_IMPORTED_MODULE_0__["default"])(window, 'pagehit').then(catalog_pagehit => {
        console.warn('[catalog-integration:pagehit]: deprecated requirejs pagehit');
        catalog_pagehit(pagehit_type);
      }).catch(e => {});
    }
  }
}

/***/ }),

/***/ "./extras/catalog-integration/toc.js":
/*!*******************************************!*\
  !*** ./extras/catalog-integration/toc.js ***!
  \*******************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var svelte_store__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/store */ "./node_modules/svelte/store/index.mjs");

/**
 * Constuct a table of contents from a DOM
 *  tree based on header elements.
 */

function toc_store() {
  const {
    subscribe: subscribeRef,
    set: setRef
  } = (0,svelte_store__WEBPACK_IMPORTED_MODULE_0__.writable)();
  const {
    subscribe
  } = (0,svelte_store__WEBPACK_IMPORTED_MODULE_0__.readable)(undefined, set => {
    let observer;
    return subscribeRef(ref => {
      if (ref === undefined) return;
      observer = new MutationObserver(mutations => {
        // look through mutations and update update toc iff a header element was added/removed
        for (const mutation of mutations) {
          if (mutation.type !== 'childList') continue;

          for (const e of [...mutation.addedNodes, ...mutation.removedNodes]) {
            if (e.tagName !== undefined && e.tagName.startsWith('H')) {
              set([...ref.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(e => ({
                h: e.tagName.slice(1),
                textContent: e.textContent.replace(/ ¶$/, ''),
                id: e.id
              })).filter(({
                id
              }) => id));
            }
          }
        }
      });
      observer.observe(ref, {
        childList: true,
        subtree: true
      });
    }, () => {
      if (observer === undefined) return;
      observer.disconnect();
    });
  });
  return {
    subscribe,
    attach: setRef
  };
}

const toc = toc_store();
/* harmony default export */ __webpack_exports__["default"] = (toc);

/***/ }),

/***/ "./lib/socketio.js":
/*!*************************!*\
  !*** ./lib/socketio.js ***!
  \*************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "setup_chunking": function() { return /* binding */ setup_chunking; }
/* harmony export */ });
function setup_chunking(socket) {
  let chunks = {};
  socket.on('chunked', ({
    id,
    event,
    chunk,
    total,
    data
  }) => {
    console.debug(`${id}: Received chunked packet ${chunk + 1} / ${total}`);

    if (chunks[id] === undefined) {
      chunks[id] = {};
    }

    chunks[id][chunk] = data;

    if (Object.keys(chunks[id]).length == total) {
      console.debug(`${id}: Collecting chunks`);
      let chunked = '';

      for (let n = 0; n < total; n++) {
        chunked += chunks[id][n];
        delete chunks[id][n];
      } // TODO: verify hash


      try {
        let data = JSON.parse(chunked);
        console.debug(`${id}: Emitting event ${event}`);

        for (const k in socket._callbacks['$' + event] || {}) {
          socket._callbacks['$' + event][k](data);
        }
      } catch (e) {
        console.error(e);
      }
    }
  });
}

/***/ }),

/***/ "./lib/stores/keycloak_auth_store.js":
/*!*******************************************!*\
  !*** ./lib/stores/keycloak_auth_store.js ***!
  \*******************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var svelte_store__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/store */ "./node_modules/svelte/store/index.mjs");
/* harmony import */ var _lib_stores_url_hash_store_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @/lib/stores/url_hash_store.js */ "./lib/stores/url_hash_store.js");



function keycloak_auth_store() {
  const {
    subscribe,
    set
  } = (0,svelte_store__WEBPACK_IMPORTED_MODULE_0__.writable)({
    state: 'init',
    keycloak: {}
  });

  if (window._config.EXTRAS.indexOf('catalog-integration') !== -1 && window._config.keycloak !== undefined) {
    __webpack_require__.e(/*! import() */ "vendors-node_modules_keycloak-js_dist_keycloak_mjs").then(__webpack_require__.bind(__webpack_require__, /*! keycloak-js */ "./node_modules/keycloak-js/dist/keycloak.mjs")).then(async ({
      default: Keycloak
    }) => {
      const keycloak = new Keycloak(window._config.keycloak.params);
      const authenticated = await keycloak.init({ ...window._config.keycloak.init,
        redirectUri: window.location.href + (window.location.href.includes('#') ? '' : '#') + (window.location.href.includes('?') ? '' : '?')
      });

      keycloak.onTokenExpired = () => {
        console.debug('refreshing expired token...');
        keycloak.updateToken().success(() => {
          set({
            state: 'auth',
            keycloak
          });
        }).error(e => {
          set({
            state: 'error',
            keycloak
          });
        });
      };

      set({
        state: authenticated ? 'auth' : 'guest',
        keycloak: { ...keycloak,
          logout: () => {
            keycloak.logout();
            set({
              state: 'guest',
              keycloak
            });
          }
        }
      }); // cleanup keycloak auth params

      _lib_stores_url_hash_store_js__WEBPACK_IMPORTED_MODULE_1__["default"].update($hash => {
        const params = { ...$hash.params
        };
        if ('code' in params) delete params['code'];
        if ('session_state' in params) delete params['session_state'];
        if ('state' in params) delete params['state'];
        return { ...$hash,
          params
        };
      });
    }).catch(err => {
      console.error(err);
      set({
        state: 'error',
        keycloak
      });
    });
  }

  return {
    subscribe
  };
}

const auth = keycloak_auth_store();
auth.subscribe(auth => {
  if (auth.state === 'auth' && document.cookie.match(/^(.*;)?\s*authorization\s*=\s*[^;]+(.*)?$/) === null) {
    document.cookie = `authorization=${auth.keycloak.token}; expires=${new Date(auth.keycloak.tokenParsed.exp * 1000).toUTCString()}; secure`;
  }
});
/* harmony default export */ __webpack_exports__["default"] = (auth);

/***/ }),

/***/ "./lib/stores/url_hash_store.js":
/*!**************************************!*\
  !*** ./lib/stores/url_hash_store.js ***!
  \**************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var svelte_store__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/store */ "./node_modules/svelte/store/index.mjs");


function params_parse(params_encoded) {
  if (params_encoded === '') return {};
  return params_encoded.split('&').map(param_pair => param_pair.split('=').map(decodeURIComponent)).reduce((params, [key, value]) => ({ ...params,
    [key]: value
  }), {});
}

function params_stringify(params) {
  return Object.keys(params).filter(param => params[param] !== undefined && params[param] !== '').map(param => [param, params[param]].map(encodeURIComponent).join('=')).join('&');
}

function fragment_parse(hash_encoded) {
  // if (!hash_encoded.startsWith('/')) hash_encoded = `/${hash_encoded}`
  const q = hash_encoded.indexOf('?');

  if (q === -1) {
    return {
      path: hash_encoded,
      params: {}
    };
  } else {
    const [path, params_encoded] = [hash_encoded.slice(0, q), hash_encoded.slice(q + 1)];
    const params = params_parse(params_encoded);
    return {
      path,
      params
    };
  }
}

function hash_stringify({
  path,
  params
}) {
  const params_encoded = params_stringify(params);

  if (params_encoded === '') {
    return path;
  } else {
    return `${path}?${params_encoded}`;
  }
}

function fragment_get() {
  return (window.location.hash || '#').slice(1);
}

function server_get() {
  return `${window.location.pathname}${window.location.search}`;
}

function url_hash_store() {
  const {
    path: initPath,
    params: initParams,
    server: initServer
  } = { ...fragment_parse(fragment_get()),
    server: fragment_parse(server_get())
  };
  const {
    subscribe,
    update,
    set
  } = (0,svelte_store__WEBPACK_IMPORTED_MODULE_0__.writable)({
    path: initPath,
    params: initParams,
    server: initServer
  });
  let lastPath = initPath;
  subscribe(({
    path,
    params,
    server
  }) => {
    const newHash = hash_stringify({
      path,
      params
    });

    if (path !== lastPath) {
      // add changes to path to history
      window.location.hash = newHash;
      lastPath = path;
    } else {
      // don't add changes to params to history, but modify the hash url
      const url = `${window.location.origin}${window.location.pathname}${window.location.search}`;
      history.replaceState(undefined, undefined, newHash !== '' ? `${url}#${newHash}` : url);
    }
  });
  window.addEventListener('hashchange', () => set({ ...fragment_parse(fragment_get()),
    initServer
  }));
  return {
    subscribe,
    update,
    set
  };
}

const hash = url_hash_store();
/* harmony default export */ __webpack_exports__["default"] = (hash);

/***/ }),

/***/ "./lib/webpack_public_path.js":
/*!************************************!*\
  !*** ./lib/webpack_public_path.js ***!
  \************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
__webpack_require__.p = `${window._config.STATIC}/`;

/***/ }),

/***/ "./node_modules/svelte/index.mjs":
/*!***************************************!*\
  !*** ./node_modules/svelte/index.mjs ***!
  \***************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SvelteComponent": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.SvelteComponentDev; },
/* harmony export */   "SvelteComponentTyped": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.SvelteComponentTyped; },
/* harmony export */   "afterUpdate": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.afterUpdate; },
/* harmony export */   "beforeUpdate": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.beforeUpdate; },
/* harmony export */   "createEventDispatcher": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.createEventDispatcher; },
/* harmony export */   "getAllContexts": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.getAllContexts; },
/* harmony export */   "getContext": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.getContext; },
/* harmony export */   "hasContext": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.hasContext; },
/* harmony export */   "onDestroy": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.onDestroy; },
/* harmony export */   "onMount": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.onMount; },
/* harmony export */   "setContext": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.setContext; },
/* harmony export */   "tick": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.tick; }
/* harmony export */ });
/* harmony import */ var _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./internal/index.mjs */ "./node_modules/svelte/internal/index.mjs");


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

/***/ "./node_modules/svelte/store/index.mjs":
/*!*********************************************!*\
  !*** ./node_modules/svelte/store/index.mjs ***!
  \*********************************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "derived": function() { return /* binding */ derived; },
/* harmony export */   "get": function() { return /* reexport safe */ _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.get_store_value; },
/* harmony export */   "readable": function() { return /* binding */ readable; },
/* harmony export */   "writable": function() { return /* binding */ writable; }
/* harmony export */ });
/* harmony import */ var _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../internal/index.mjs */ "./node_modules/svelte/internal/index.mjs");


const subscriber_queue = [];
/**
 * Creates a `Readable` store that allows reading by subscription.
 * @param value initial value
 * @param {StartStopNotifier}start start and stop notifications for subscriptions
 */

function readable(value, start) {
  return {
    subscribe: writable(value, start).subscribe
  };
}
/**
 * Create a `Writable` store that allows both updating and reading by subscription.
 * @param {*=}value initial value
 * @param {StartStopNotifier=}start start and stop notifications for subscriptions
 */


function writable(value, start = _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.noop) {
  let stop;
  const subscribers = new Set();

  function set(new_value) {
    if ((0,_internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.safe_not_equal)(value, new_value)) {
      value = new_value;

      if (stop) {
        // store is ready
        const run_queue = !subscriber_queue.length;

        for (const subscriber of subscribers) {
          subscriber[1]();
          subscriber_queue.push(subscriber, value);
        }

        if (run_queue) {
          for (let i = 0; i < subscriber_queue.length; i += 2) {
            subscriber_queue[i][0](subscriber_queue[i + 1]);
          }

          subscriber_queue.length = 0;
        }
      }
    }
  }

  function update(fn) {
    set(fn(value));
  }

  function subscribe(run, invalidate = _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.noop) {
    const subscriber = [run, invalidate];
    subscribers.add(subscriber);

    if (subscribers.size === 1) {
      stop = start(set) || _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.noop;
    }

    run(value);
    return () => {
      subscribers.delete(subscriber);

      if (subscribers.size === 0) {
        stop();
        stop = null;
      }
    };
  }

  return {
    set,
    update,
    subscribe
  };
}

function derived(stores, fn, initial_value) {
  const single = !Array.isArray(stores);
  const stores_array = single ? [stores] : stores;
  const auto = fn.length < 2;
  return readable(initial_value, set => {
    let inited = false;
    const values = [];
    let pending = 0;
    let cleanup = _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.noop;

    const sync = () => {
      if (pending) {
        return;
      }

      cleanup();
      const result = fn(single ? values[0] : values, set);

      if (auto) {
        set(result);
      } else {
        cleanup = (0,_internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.is_function)(result) ? result : _internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.noop;
      }
    };

    const unsubscribers = stores_array.map((store, i) => (0,_internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.subscribe)(store, value => {
      values[i] = value;
      pending &= ~(1 << i);

      if (inited) {
        sync();
      }
    }, () => {
      pending |= 1 << i;
    }));
    inited = true;
    sync();
    return function stop() {
      (0,_internal_index_mjs__WEBPACK_IMPORTED_MODULE_0__.run_all)(unsubscribers);
      cleanup();
    };
  });
}



/***/ }),

/***/ "./utils/get_require.js":
/*!******************************!*\
  !*** ./utils/get_require.js ***!
  \******************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": function() { return /* binding */ get_require; }
/* harmony export */ });
function get_require(window, required) {
  if (Array.isArray(required)) {
    return new Promise((resolve, reject) => window.require(required, (...args) => resolve(args), reject));
  } else {
    return new Promise((resolve, reject) => window.require([required], resolve, reject));
  }
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
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/amd options */
/******/ 	!function() {
/******/ 		__webpack_require__.amdO = {};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	!function() {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = function(module) {
/******/ 			var getter = module && module.__esModule ?
/******/ 				function() { return module['default']; } :
/******/ 				function() { return module; };
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	}();
/******/ 	
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
/******/ 	/* webpack/runtime/ensure chunk */
/******/ 	!function() {
/******/ 		__webpack_require__.f = {};
/******/ 		// This file contains only the entry chunk.
/******/ 		// The chunk loading function for additional chunks
/******/ 		__webpack_require__.e = function(chunkId) {
/******/ 			return Promise.all(Object.keys(__webpack_require__.f).reduce(function(promises, key) {
/******/ 				__webpack_require__.f[key](chunkId, promises);
/******/ 				return promises;
/******/ 			}, []));
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/get javascript chunk filename */
/******/ 	!function() {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.u = function(chunkId) {
/******/ 			// return url for filenames based on template
/******/ 			return "profiles/default/js/chunks/" + chunkId + ".js";
/******/ 		};
/******/ 	}();
/******/ 	
/******/ 	/* webpack/runtime/get mini-css chunk filename */
/******/ 	!function() {
/******/ 		// This function allow to reference async chunks
/******/ 		__webpack_require__.miniCssF = function(chunkId) {
/******/ 			// return url for filenames based on template
/******/ 			return undefined;
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
/******/ 	/* webpack/runtime/load script */
/******/ 	!function() {
/******/ 		var inProgress = {};
/******/ 		var dataWebpackPrefix = "appyter-js:";
/******/ 		// loadScript function to load a script via script tag
/******/ 		__webpack_require__.l = function(url, done, key, chunkId) {
/******/ 			if(inProgress[url]) { inProgress[url].push(done); return; }
/******/ 			var script, needAttach;
/******/ 			if(key !== undefined) {
/******/ 				var scripts = document.getElementsByTagName("script");
/******/ 				for(var i = 0; i < scripts.length; i++) {
/******/ 					var s = scripts[i];
/******/ 					if(s.getAttribute("src") == url || s.getAttribute("data-webpack") == dataWebpackPrefix + key) { script = s; break; }
/******/ 				}
/******/ 			}
/******/ 			if(!script) {
/******/ 				needAttach = true;
/******/ 				script = document.createElement('script');
/******/ 		
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.setAttribute("data-webpack", dataWebpackPrefix + key);
/******/ 				script.src = url;
/******/ 			}
/******/ 			inProgress[url] = [done];
/******/ 			var onScriptComplete = function(prev, event) {
/******/ 				// avoid mem leaks in IE.
/******/ 				script.onerror = script.onload = null;
/******/ 				clearTimeout(timeout);
/******/ 				var doneFns = inProgress[url];
/******/ 				delete inProgress[url];
/******/ 				script.parentNode && script.parentNode.removeChild(script);
/******/ 				doneFns && doneFns.forEach(function(fn) { return fn(event); });
/******/ 				if(prev) return prev(event);
/******/ 			}
/******/ 			;
/******/ 			var timeout = setTimeout(onScriptComplete.bind(null, undefined, { type: 'timeout', target: script }), 120000);
/******/ 			script.onerror = onScriptComplete.bind(null, script.onerror);
/******/ 			script.onload = onScriptComplete.bind(null, script.onload);
/******/ 			needAttach && document.head.appendChild(script);
/******/ 		};
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
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	!function() {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"profiles/default/js/landing": 0
/******/ 		};
/******/ 		
/******/ 		__webpack_require__.f.j = function(chunkId, promises) {
/******/ 				// JSONP chunk loading for javascript
/******/ 				var installedChunkData = __webpack_require__.o(installedChunks, chunkId) ? installedChunks[chunkId] : undefined;
/******/ 				if(installedChunkData !== 0) { // 0 means "already installed".
/******/ 		
/******/ 					// a Promise means "currently loading".
/******/ 					if(installedChunkData) {
/******/ 						promises.push(installedChunkData[2]);
/******/ 					} else {
/******/ 						if(true) { // all chunks have JS
/******/ 							// setup Promise in chunk cache
/******/ 							var promise = new Promise(function(resolve, reject) { installedChunkData = installedChunks[chunkId] = [resolve, reject]; });
/******/ 							promises.push(installedChunkData[2] = promise);
/******/ 		
/******/ 							// start chunk loading
/******/ 							var url = __webpack_require__.p + __webpack_require__.u(chunkId);
/******/ 							// create error before stack unwound to get useful stacktrace later
/******/ 							var error = new Error();
/******/ 							var loadingEnded = function(event) {
/******/ 								if(__webpack_require__.o(installedChunks, chunkId)) {
/******/ 									installedChunkData = installedChunks[chunkId];
/******/ 									if(installedChunkData !== 0) installedChunks[chunkId] = undefined;
/******/ 									if(installedChunkData) {
/******/ 										var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 										var realSrc = event && event.target && event.target.src;
/******/ 										error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 										error.name = 'ChunkLoadError';
/******/ 										error.type = errorType;
/******/ 										error.request = realSrc;
/******/ 										installedChunkData[1](error);
/******/ 									}
/******/ 								}
/******/ 							};
/******/ 							__webpack_require__.l(url, loadingEnded, "chunk-" + chunkId, chunkId);
/******/ 						} else installedChunks[chunkId] = 0;
/******/ 					}
/******/ 				}
/******/ 		};
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		// no on chunks loaded
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = function(parentChunkLoadingFunction, data) {
/******/ 			var chunkIds = data[0];
/******/ 			var moreModules = data[1];
/******/ 			var runtime = data[2];
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some(function(id) { return installedChunks[id] !== 0; })) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 		
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkappyter_js"] = self["webpackChunkappyter_js"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	}();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	__webpack_require__("./lib/webpack_public_path.js");
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./profiles/default/js/landing.svelte");
/******/ 	
/******/ 	return __webpack_exports__;
/******/ })()
;
});
//# sourceMappingURL=landing.js.map