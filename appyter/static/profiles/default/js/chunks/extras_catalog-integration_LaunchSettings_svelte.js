"use strict";
(self["webpackChunkappyter_js"] = self["webpackChunkappyter_js"] || []).push([["extras_catalog-integration_LaunchSettings_svelte"],{

/***/ "./extras/catalog-integration/LaunchSettings.svelte":
/*!**********************************************************!*\
  !*** ./extras/catalog-integration/LaunchSettings.svelte ***!
  \**********************************************************/
/***/ (function(module, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var svelte_internal__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! svelte/internal */ "./node_modules/svelte/internal/index.mjs");
/* harmony import */ var _lib_stores_keycloak_auth_store__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @/lib/stores/keycloak_auth_store */ "./lib/stores/keycloak_auth_store.js");
/* harmony import */ var _components_Loader_svelte__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @/components/Loader.svelte */ "./components/Loader.svelte");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_loader_lib_hot_api_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./node_modules/svelte-loader/lib/hot-api.js */ "./node_modules/svelte-loader/lib/hot-api.js");
/* harmony import */ var _home_u8sand_Programs_work_active_appyter_js_node_modules_svelte_hmr_runtime_proxy_adapter_dom_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js */ "./node_modules/svelte-hmr/runtime/proxy-adapter-dom.js");
/* module decorator */ module = __webpack_require__.hmd(module);
/* extras/catalog-integration/LaunchSettings.svelte generated by Svelte v3.46.4 */



const file = "extras/catalog-integration/LaunchSettings.svelte"; // (48:6) {:else}

function create_else_block(ctx) {
  let div1;
  let div0;
  let current_block_type_index;
  let if_block;
  let current;
  const if_block_creators = [create_if_block_1, create_if_block_2, create_else_block_1];
  const if_blocks = [];

  function select_block_type_1(ctx, dirty) {
    if (
    /*$auth*/
    ctx[0].state === 'init') return 0;
    if (
    /*$auth*/
    ctx[0].state === 'error') return 1;
    return 2;
  }

  current_block_type_index = select_block_type_1(ctx, -1);
  if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
  const block = {
    c: function create() {
      div1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      if_block.c();
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "class", "row px-4 px-lg-3 pb-4 justify-content-center");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div0, file, 49, 10, 2255);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div1, "class", "pt-3");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div1, file, 48, 8, 2226);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div1, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, div0);
      if_blocks[current_block_type_index].m(div0, null);
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
        if_block.m(div0, null);
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
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div1);
      if_blocks[current_block_type_index].d();
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_else_block.name,
    type: "else",
    source: "(48:6) {:else}",
    ctx
  });
  return block;
} // (20:6) {#if $auth.state === 'auth'}


function create_if_block(ctx) {
  let div7;
  let div1;
  let div0;
  let t0;
  let t1_value =
  /*$auth*/
  ctx[0].keycloak.tokenParsed.email + "";
  let t1;
  let t2;
  let button;
  let t4;
  let t5;
  let div4;
  let div2;
  let t6;
  let sup;
  let i;
  let t7;
  let div3;
  let select;
  let option0;
  let option1;
  let t10;
  let div6;
  let div5;
  let a;
  let t12;
  let mounted;
  let dispose;
  const block = {
    c: function create() {
      div7 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      t0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("Logged in as ");
      t1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(t1_value);
      t2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(", ");
      button = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("button");
      button.textContent = "click here";
      t4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(" to logout.");
      t5 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      t6 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)("Execution Profile:\n              ");
      sup = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("sup");
      i = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("i");
      t7 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div3 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      select = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("select");
      option0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("option");
      option0.textContent = "Execute in appyter catalog";
      option1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("option");
      option1.textContent = "Execute in CAVATICA";
      t10 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div6 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div5 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      a = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("a");
      a.textContent = "Click here";
      t12 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(" to configure additional integrations.");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "type", "button");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "class", "text-btn");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(button, file, 23, 63, 1057);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "class", "col col-lg-9 px-lg-3 my-auto px-4 text-center");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div0, file, 22, 12, 934);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div1, "class", "row px-4 px-lg-3 pb-4 justify-content-center");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div1, file, 21, 10, 863);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(i, "class", "far fa-question-circle");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(i, file, 29, 80, 1417);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(sup, "data-toggle", "tooltip");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(sup, "title", "How the appyter should execute");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(sup, file, 29, 14, 1351);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div2, "class", "col-lg-3 bold text-lg-right my-auto");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div2, file, 27, 12, 1254);
      option0.selected = true;
      option0.__value = "default";
      option0.value = option0.__value;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(option0, file, 36, 16, 1695);
      option1.__value = "cavatica";
      option1.value = option1.__value;
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(option1, file, 37, 16, 1780);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(select, "name", "_executor");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(select, "class", "form-control nodecoration tiny bg-white px-2 py-1 mb-0");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(select, file, 32, 14, 1543);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div3, "class", "col-lg-6 pt-2 pt-lg-0");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div3, file, 31, 12, 1493);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div4, "class", "row px-3 pb-3");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div4, file, 26, 10, 1214);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(a, "href", "/#/account/integrations");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(a, file, 43, 14, 2066);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div5, "class", "col col-lg-9 px-lg-3 my-auto px-4 text-center alert alert-info");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div5, file, 42, 12, 1975);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div6, "class", "row px-4 px-lg-3 pb-4 justify-content-center");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div6, file, 41, 10, 1904);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div7, "class", "pt-3");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div7, file, 20, 8, 834);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div7, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div1, div0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, button);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, t4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t5);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, div2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div2, t6);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div2, sup);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(sup, i);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, t7);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, div3);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, select);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(select, option0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(select, option1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t10);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div6);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div6, div5);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div5, a);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div5, t12);

      if (!mounted) {
        dispose = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.listen_dev)(button, "click",
        /*click_handler*/
        ctx[1], false, false, false);
        mounted = true;
      }
    },
    p: function update(ctx, dirty) {
      if (dirty &
      /*$auth*/
      1 && t1_value !== (t1_value =
      /*$auth*/
      ctx[0].keycloak.tokenParsed.email + "")) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.set_data_dev)(t1, t1_value);
    },
    i: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    o: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div7);
      mounted = false;
      dispose();
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block.name,
    type: "if",
    source: "(20:6) {#if $auth.state === 'auth'}",
    ctx
  });
  return block;
} // (57:12) {:else}


function create_else_block_1(ctx) {
  let div;
  let button;
  let t1;
  let mounted;
  let dispose;
  const block = {
    c: function create() {
      div = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      button = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("button");
      button.textContent = "Login";
      t1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.text)(" to configure launch settings.");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "type", "button");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(button, "class", "text-btn");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(button, file, 58, 16, 2755);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div, "class", "col col-lg-9 px-lg-3 my-auto px-4 text-center alert alert-info");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div, file, 57, 14, 2662);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div, button);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div, t1);

      if (!mounted) {
        dispose = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.listen_dev)(button, "click",
        /*click_handler_1*/
        ctx[2], false, false, false);
        mounted = true;
      }
    },
    p: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    i: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    o: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div);
      mounted = false;
      dispose();
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_else_block_1.name,
    type: "else",
    source: "(57:12) {:else}",
    ctx
  });
  return block;
} // (53:46) 


function create_if_block_2(ctx) {
  let div;
  const block = {
    c: function create() {
      div = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div.textContent = "Unable to access authentication at this time, please try again later.";
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div, "class", "col col-lg-9 px-lg-3 my-auto px-4 text-center alert alert-warning");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div, file, 53, 14, 2441);
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div, anchor);
    },
    p: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    i: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    o: svelte_internal__WEBPACK_IMPORTED_MODULE_0__.noop,
    d: function destroy(detaching) {
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div);
    }
  };
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterBlock", {
    block,
    id: create_if_block_2.name,
    type: "if",
    source: "(53:46) ",
    ctx
  });
  return block;
} // (51:12) {#if $auth.state === 'init'}


function create_if_block_1(ctx) {
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
    id: create_if_block_1.name,
    type: "if",
    source: "(51:12) {#if $auth.state === 'init'}",
    ctx
  });
  return block;
}

function create_fragment(ctx) {
  let div8;
  let div7;
  let div5;
  let div4;
  let div0;
  let i;
  let t0;
  let div3;
  let div1;
  let t2;
  let div2;
  let t4;
  let div6;
  let current_block_type_index;
  let if_block;
  let current;
  const if_block_creators = [create_if_block, create_else_block];
  const if_blocks = [];

  function select_block_type(ctx, dirty) {
    if (
    /*$auth*/
    ctx[0].state === 'auth') return 0;
    return 1;
  }

  current_block_type_index = select_block_type(ctx, -1);
  if_block = if_blocks[current_block_type_index] = if_block_creators[current_block_type_index](ctx);
  const block = {
    c: function create() {
      div8 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div7 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div5 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      i = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("i");
      t0 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div3 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div1 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div1.textContent = "User Launch Settings";
      t2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div2 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      div2.textContent = "Configure how the appyter launches";
      t4 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.space)();
      div6 = (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.element)("div");
      if_block.c();
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(i, "class", "fas fa-cogs fa-2x");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(i, file, 10, 10, 410);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div0, "class", "d-table-cell align-middle card-icon px-3 py-3 text-center");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div0, file, 9, 8, 328);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div1, "class", "very-small regular pb-2 pr-5");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div1, file, 13, 10, 515);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div2, "class", "tiny light text-muted");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div2, file, 14, 10, 594);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div3, "class", "d-table-cell align-middle");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div3, file, 12, 8, 465);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div4, "class", "d-table w-100 py-2 px-2 py-md-0 px-md-0");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div4, file, 8, 6, 266);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div5, "class", "mt-3 mb-0 w-100 border-custom rounded bg-lightgrey");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div5, "data-toggle", "collapse");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div5, file, 7, 4, 172);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div6, "class", "border-grey mx-2 border-top-0 rounded-bottom tiny collapse show");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div6, file, 18, 4, 713);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div7, "class", "col-sm-12");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div7, file, 6, 2, 144);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.attr_dev)(div8, "class", "row");
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.add_location)(div8, file, 5, 0, 124);
    },
    l: function claim(nodes) {
      throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    },
    m: function mount(target, anchor) {
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.insert_dev)(target, div8, anchor);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div8, div7);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div5);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div5, div4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, div0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div0, i);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, t0);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div4, div3);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, div1);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, t2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div3, div2);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, t4);
      (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.append_dev)(div7, div6);
      if_blocks[current_block_type_index].m(div6, null);
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
        if_block.m(div6, null);
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
      if (detaching) (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.detach_dev)(div8);
      if_blocks[current_block_type_index].d();
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
  let $auth;
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_store)(_lib_stores_keycloak_auth_store__WEBPACK_IMPORTED_MODULE_1__["default"], 'auth');
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.component_subscribe)($$self, _lib_stores_keycloak_auth_store__WEBPACK_IMPORTED_MODULE_1__["default"], $$value => $$invalidate(0, $auth = $$value));
  let {
    $$slots: slots = {},
    $$scope
  } = $$props;
  (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.validate_slots)('LaunchSettings', slots, []);
  const writable_props = [];
  Object.keys($$props).forEach(key => {
    if (!~writable_props.indexOf(key) && key.slice(0, 2) !== '$$' && key !== 'slot') console.warn(`<LaunchSettings> was created with unknown prop '${key}'`);
  });

  const click_handler = () => $auth.keycloak.logout();

  const click_handler_1 = () => $auth.keycloak.login();

  $$self.$capture_state = () => ({
    auth: _lib_stores_keycloak_auth_store__WEBPACK_IMPORTED_MODULE_1__["default"],
    Loader: _components_Loader_svelte__WEBPACK_IMPORTED_MODULE_2__["default"],
    $auth
  });

  return [$auth, click_handler, click_handler_1];
}

class LaunchSettings extends svelte_internal__WEBPACK_IMPORTED_MODULE_0__.SvelteComponentDev {
  constructor(options) {
    super(options);
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.init)(this, options, instance, create_fragment, svelte_internal__WEBPACK_IMPORTED_MODULE_0__.safe_not_equal, {});
    (0,svelte_internal__WEBPACK_IMPORTED_MODULE_0__.dispatch_dev)("SvelteRegisterComponent", {
      component: this,
      tagName: "LaunchSettings",
      options,
      id: create_fragment.name
    });
  }

}




if (module && module.hot) {}

/* harmony default export */ __webpack_exports__["default"] = (LaunchSettings);

/***/ })

}]);
//# sourceMappingURL=extras_catalog-integration_LaunchSettings_svelte.js.map