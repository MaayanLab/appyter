(window.webpackJsonp=window.webpackJsonp||[]).push([[6],{313:function(e,t,s){"use strict";s.r(t),s.d(t,"IPYWidgetManager",(function(){return n}));var i=s(315),o=s(431),_=s(430),a=s(320);class n extends o.a{constructor(e){super(),this.el=e,this.__lock={lock:!1,callbacks:[]},this.__models_state={},this.__models_view={},this.create_and_display_views=this.create_and_display_views.bind(this),this.register_view=this.register_view.bind(this),this.register_state=this.register_state.bind(this),window.define("@jupyter-widgets/controls",(function(){return _})),window.define("@jupyter-widgets/base",(function(){return i}))}loadClass(e,t,s){return new Promise((function(e,i){window.require.defined(t)||window.require.config({paths:{[t]:`https://unpkg.com/${t}@${s}/dist/index`}}),window.require([t],e,i)})).then((function(i){return i[e]?i[e]:Promise.reject(`Class ${e} not found in module ${t}@${s}`)}))}async create_and_display_views(){(this.__lock.lock||this.__lock.callbacks.length>0)&&await new Promise((e,t)=>this.__lock.callbacks.push(e)),this.__lock.lock=!0;const e={...this.__models_state,state:{}};for(const t in this.__models_state.state){const s=this.__models_view[t];void 0!==s&&void 0===s.view&&(e.state[t]=this.__models_state.state[t])}if(Object.keys(e.state).length>0){const t=await this.set_state(e);for(const e of t){const t=this.__models_view[e.model_id].el;this.__models_view[e.model_id].view=await this.create_view(e),await this.display_view(this.__models_view[e.model_id].view,{el:t})}}for(this.__lock.lock=!1;this.__lock.callbacks.length>0;)await this.__lock.callbacks.shift()()}async register_view({metadata:e,el:t}){this.__models_view[e.model_id]={metadata:e,el:t},await this.create_and_display_views()}async register_state(e){this.__models_state=e,await this.create_and_display_views()}display_view(e,t){return Promise.resolve(e).then(e=>(a.d.attach(e.pWidget,t.el),e.on("remove",()=>{console.log("View removed",e)}),e))}_get_comm_info(){return Promise.resolve({})}_create_comm(e,t,s,i,o){return Promise.resolve({on_close:()=>{},on_msg:()=>{},close:()=>{}})}}},352:function(e,t){}}]);