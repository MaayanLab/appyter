"use strict";
(self["webpackChunkappyter_js"] = self["webpackChunkappyter_js"] || []).push([["lib_stores_keycloak_auth_store_js"],{

/***/ "./lib/stores/keycloak_auth_store.js":
/*!*******************************************!*\
  !*** ./lib/stores/keycloak_auth_store.js ***!
  \*******************************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var svelte_store__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/store */ "./node_modules/svelte/src/runtime/store/index.js");
/* harmony import */ var _lib_stores_url_hash_store_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @/lib/stores/url_hash_store.js */ "./lib/stores/url_hash_store.js");
/* harmony import */ var _utils_with_timeout__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @/utils/with_timeout */ "./utils/with_timeout.js");



function keycloak_auth_store() {
  const enabled = window._config.EXTRAS.includes('catalog-integration') && window._config.keycloak !== undefined;
  const {
    subscribe,
    set
  } = (0,svelte_store__WEBPACK_IMPORTED_MODULE_0__.writable)({
    state: enabled ? 'init' : 'error',
    keycloak: {}
  });
  if (enabled) {
    __webpack_require__.e(/*! import() */ "vendors-node_modules_keycloak-js_lib_keycloak_js").then(__webpack_require__.bind(__webpack_require__, /*! keycloak-js */ "./node_modules/keycloak-js/lib/keycloak.js")).then((0,_utils_with_timeout__WEBPACK_IMPORTED_MODULE_2__["default"])(async ({
      default: Keycloak
    }) => {
      const keycloak = new Keycloak(window._config.keycloak.params);
      const keycloakLogout = keycloak.logout;
      Object.assign(keycloak, {
        getValidToken: async () => {
          try {
            await keycloak.updateToken(30);
          } catch (e) {
            console.error(e);
            set({
              state: 'guest',
              keycloak
            });
          }
          return keycloak.token;
        },
        logout: () => {
          keycloakLogout();
          set({
            state: 'guest',
            keycloak
          });
        }
      });
      const authenticated = await keycloak.init({
        ...window._config.keycloak.init,
        redirectUri: window.location.href + (window.location.href.includes('#') ? '' : '#') + (window.location.href.includes('?') ? '' : '?')
      });
      set({
        state: authenticated ? 'auth' : 'guest',
        keycloak
      });
      // cleanup keycloak auth params
      _lib_stores_url_hash_store_js__WEBPACK_IMPORTED_MODULE_1__["default"].update($hash => {
        const params = {
          ...$hash.params
        };
        if ('code' in params) delete params['code'];
        if ('session_state' in params) delete params['session_state'];
        if ('state' in params) delete params['state'];
        return {
          ...$hash,
          params
        };
      });
    }, 5000)).catch(err => {
      console.error(err);
      set({
        state: 'error',
        keycloak: {}
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
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (auth);

/***/ }),

/***/ "./lib/stores/url_hash_store.js":
/*!**************************************!*\
  !*** ./lib/stores/url_hash_store.js ***!
  \**************************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var svelte_store__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/store */ "./node_modules/svelte/src/runtime/store/index.js");

function params_parse(params_encoded) {
  if (params_encoded === '') return {};
  return params_encoded.split('&').map(param_pair => param_pair.split('=').map(decodeURIComponent)).reduce((params, [key, value]) => ({
    ...params,
    [key]: value !== undefined ? value : true
  }), {});
}
function params_stringify(params) {
  return Object.keys(params).filter(param => params[param] !== undefined && params[param] !== '').map(param => params[param] === true ? encodeURIComponent(param) : [param, params[param]].map(encodeURIComponent).join('=')).join('&');
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
  } = {
    ...fragment_parse(fragment_get()),
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
  window.addEventListener('hashchange', () => set({
    ...fragment_parse(fragment_get()),
    initServer
  }));
  return {
    subscribe,
    update,
    set
  };
}
const hash = url_hash_store();
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (hash);

/***/ }),

/***/ "./node_modules/svelte/src/runtime/store/index.js":
/*!********************************************************!*\
  !*** ./node_modules/svelte/src/runtime/store/index.js ***!
  \********************************************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   derived: () => (/* binding */ derived),
/* harmony export */   get: () => (/* reexport safe */ _internal_index_js__WEBPACK_IMPORTED_MODULE_0__.get_store_value),
/* harmony export */   readable: () => (/* binding */ readable),
/* harmony export */   readonly: () => (/* binding */ readonly),
/* harmony export */   writable: () => (/* binding */ writable)
/* harmony export */ });
/* harmony import */ var _internal_index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../internal/index.js */ "./node_modules/svelte/src/runtime/internal/index.js");

const subscriber_queue = [];

/**
 * Creates a `Readable` store that allows reading by subscription.
 *
 * https://svelte.dev/docs/svelte-store#readable
 * @template T
 * @param {T} [value] initial value
 * @param {import('./public.js').StartStopNotifier<T>} [start]
 * @returns {import('./public.js').Readable<T>}
 */
function readable(value, start) {
  return {
    subscribe: writable(value, start).subscribe
  };
}

/**
 * Create a `Writable` store that allows both updating and reading by subscription.
 *
 * https://svelte.dev/docs/svelte-store#writable
 * @template T
 * @param {T} [value] initial value
 * @param {import('./public.js').StartStopNotifier<T>} [start]
 * @returns {import('./public.js').Writable<T>}
 */
function writable(value, start = _internal_index_js__WEBPACK_IMPORTED_MODULE_0__.noop) {
  /** @type {import('./public.js').Unsubscriber} */
  let stop;
  /** @type {Set<import('./private.js').SubscribeInvalidateTuple<T>>} */
  const subscribers = new Set();
  /** @param {T} new_value
   * @returns {void}
   */
  function set(new_value) {
    if ((0,_internal_index_js__WEBPACK_IMPORTED_MODULE_0__.safe_not_equal)(value, new_value)) {
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

  /**
   * @param {import('./public.js').Updater<T>} fn
   * @returns {void}
   */
  function update(fn) {
    set(fn(value));
  }

  /**
   * @param {import('./public.js').Subscriber<T>} run
   * @param {import('./private.js').Invalidator<T>} [invalidate]
   * @returns {import('./public.js').Unsubscriber}
   */
  function subscribe(run, invalidate = _internal_index_js__WEBPACK_IMPORTED_MODULE_0__.noop) {
    /** @type {import('./private.js').SubscribeInvalidateTuple<T>} */
    const subscriber = [run, invalidate];
    subscribers.add(subscriber);
    if (subscribers.size === 1) {
      stop = start(set, update) || _internal_index_js__WEBPACK_IMPORTED_MODULE_0__.noop;
    }
    run(value);
    return () => {
      subscribers.delete(subscriber);
      if (subscribers.size === 0 && stop) {
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

/**
 * Derived value store by synchronizing one or more readable stores and
 * applying an aggregation function over its input values.
 *
 * https://svelte.dev/docs/svelte-store#derived
 * @template {import('./private.js').Stores} S
 * @template T
 * @overload
 * @param {S} stores - input stores
 * @param {(values: import('./private.js').StoresValues<S>, set: (value: T) => void, update: (fn: import('./public.js').Updater<T>) => void) => import('./public.js').Unsubscriber | void} fn - function callback that aggregates the values
 * @param {T} [initial_value] - initial value
 * @returns {import('./public.js').Readable<T>}
 */

/**
 * Derived value store by synchronizing one or more readable stores and
 * applying an aggregation function over its input values.
 *
 * https://svelte.dev/docs/svelte-store#derived
 * @template {import('./private.js').Stores} S
 * @template T
 * @overload
 * @param {S} stores - input stores
 * @param {(values: import('./private.js').StoresValues<S>) => T} fn - function callback that aggregates the values
 * @param {T} [initial_value] - initial value
 * @returns {import('./public.js').Readable<T>}
 */

/**
 * @template {import('./private.js').Stores} S
 * @template T
 * @param {S} stores
 * @param {Function} fn
 * @param {T} [initial_value]
 * @returns {import('./public.js').Readable<T>}
 */
function derived(stores, fn, initial_value) {
  const single = !Array.isArray(stores);
  /** @type {Array<import('./public.js').Readable<any>>} */
  const stores_array = single ? [stores] : stores;
  if (!stores_array.every(Boolean)) {
    throw new Error('derived() expects stores as input, got a falsy value');
  }
  const auto = fn.length < 2;
  return readable(initial_value, (set, update) => {
    let started = false;
    const values = [];
    let pending = 0;
    let cleanup = _internal_index_js__WEBPACK_IMPORTED_MODULE_0__.noop;
    const sync = () => {
      if (pending) {
        return;
      }
      cleanup();
      const result = fn(single ? values[0] : values, set, update);
      if (auto) {
        set(result);
      } else {
        cleanup = (0,_internal_index_js__WEBPACK_IMPORTED_MODULE_0__.is_function)(result) ? result : _internal_index_js__WEBPACK_IMPORTED_MODULE_0__.noop;
      }
    };
    const unsubscribers = stores_array.map((store, i) => (0,_internal_index_js__WEBPACK_IMPORTED_MODULE_0__.subscribe)(store, value => {
      values[i] = value;
      pending &= ~(1 << i);
      if (started) {
        sync();
      }
    }, () => {
      pending |= 1 << i;
    }));
    started = true;
    sync();
    return function stop() {
      (0,_internal_index_js__WEBPACK_IMPORTED_MODULE_0__.run_all)(unsubscribers);
      cleanup();
      // We need to set this to false because callbacks can still happen despite having unsubscribed:
      // Callbacks might already be placed in the queue which doesn't know it should no longer
      // invoke this derived store.
      started = false;
    };
  });
}

/**
 * Takes a store and returns a new one derived from the old one that is readable.
 *
 * https://svelte.dev/docs/svelte-store#readonly
 * @template T
 * @param {import('./public.js').Readable<T>} store  - store to make readonly
 * @returns {import('./public.js').Readable<T>}
 */
function readonly(store) {
  return {
    subscribe: store.subscribe.bind(store)
  };
}


/***/ }),

/***/ "./utils/with_timeout.js":
/*!*******************************!*\
  !*** ./utils/with_timeout.js ***!
  \*******************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ with_timeout)
/* harmony export */ });
function with_timeout(promise, timeout) {
  return (...args) => new Promise((resolve, reject) => {
    let ctx = {
      done: false
    };
    setTimeout(() => {
      if (ctx.done) return;
      ctx.done = true;
      reject('Timeout');
    }, timeout);
    promise(...args).then(value => {
      if (ctx.done) return;
      ctx.done = true;
      resolve(value);
    }).catch(e => {
      if (ctx.done) return;
      ctx.done = true;
      reject(e);
    });
  });
}

/***/ })

}]);
//# sourceMappingURL=lib_stores_keycloak_auth_store_js.js.map