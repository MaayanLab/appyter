!function(t,e){if("object"==typeof exports&&"object"==typeof module)module.exports=e();else if("function"==typeof define&&define.amd)define([],e);else{var n=e();for(var o in n)("object"==typeof exports?exports:t)[o]=n[o]}}(self,(function(){return function(){"use strict";var t={d:function(e,n){for(var o in n)t.o(n,o)&&!t.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:n[o]})},o:function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},r:function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},p:""},e={};return t.p=`${window._config.STATIC}/`,function(){function n(){}function o(t){return t()}function l(){return Object.create(null)}function r(t){t.forEach(o)}function s(t){return"function"==typeof t}function c(t,e){return t!=t?e==e:t!==e||t&&"object"==typeof t||"function"==typeof t}function i(t){return 0===Object.keys(t).length}t.r(e),t.d(e,{default:function(){return K}}),new Set;let a,u=!1;function d(t,e){t.appendChild(e)}function f(t,e,n){t.insertBefore(e,n||null)}function p(t){t.parentNode.removeChild(t)}function m(t){return document.createElement(t)}function h(t){return document.createTextNode(t)}function $(){return h(" ")}function g(t,e,n,o){return t.addEventListener(e,n,o),()=>t.removeEventListener(e,n,o)}function y(t,e,n){null==n?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}function b(t,e){e=""+e,t.wholeText!==e&&(t.data=e)}function x(t,e){t.value=null==e?"":e}function v(t,e,n,o){null===n?t.style.removeProperty(e):t.style.setProperty(e,n,o?"important":"")}function w(t,e,n){t.classList[n?"add":"remove"](e)}function _(t){a=t}new Map;const k=[],j=[],O=[],S=[],E=Promise.resolve();let T=!1;function A(t){O.push(t)}const C=new Set;let P=0;function M(){const t=a;do{for(;P<k.length;){const t=k[P];P++,_(t),L(t.$$)}for(_(null),k.length=0,P=0;j.length;)j.pop()();for(let t=0;t<O.length;t+=1){const e=O[t];C.has(e)||(C.add(e),e())}O.length=0}while(k.length);for(;S.length;)S.pop()();T=!1,C.clear(),_(t)}function L(t){if(null!==t.fragment){t.update(),r(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(A)}}const q=new Set;let N;function H(t,e){const n=t.$$;null!==n.fragment&&(r(n.on_destroy),n.fragment&&n.fragment.d(e),n.on_destroy=n.fragment=null,n.ctx=[])}function B(t,e,c,i,d,f,m,h=[-1]){const $=a;_(t);const g=t.$$={fragment:null,ctx:null,props:f,update:n,not_equal:d,bound:l(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(e.context||($?$.$$.context:[])),callbacks:l(),dirty:h,skip_bound:!1,root:e.target||$.$$.root};m&&m(g.root);let y=!1;if(g.ctx=c?c(t,e.props||{},((e,n,...o)=>{const l=o.length?o[0]:n;return g.ctx&&d(g.ctx[e],g.ctx[e]=l)&&(!g.skip_bound&&g.bound[e]&&g.bound[e](l),y&&function(t,e){-1===t.$$.dirty[0]&&(k.push(t),T||(T=!0,E.then(M)),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}(t,e)),n})):[],g.update(),y=!0,r(g.before_update),g.fragment=!!i&&i(g.ctx),e.target){if(e.hydrate){u=!0;const t=(v=e.target,Array.from(v.childNodes));g.fragment&&g.fragment.l(t),t.forEach(p)}else g.fragment&&g.fragment.c();e.intro&&((b=t.$$.fragment)&&b.i&&(q.delete(b),b.i(x))),function(t,e,n,l){const{fragment:c,on_mount:i,on_destroy:a,after_update:u}=t.$$;c&&c.m(e,n),l||A((()=>{const e=i.map(o).filter(s);a?a.push(...e):r(e),t.$$.on_mount=[]})),u.forEach(A)}(t,e.target,e.anchor,e.customElement),u=!1,M()}var b,x,v;_($)}"undefined"!=typeof window?window:"undefined"!=typeof globalThis?globalThis:global,new Set(["allowfullscreen","allowpaymentrequest","async","autofocus","autoplay","checked","controls","default","defer","disabled","formnovalidate","hidden","ismap","loop","multiple","muted","nomodule","novalidate","open","playsinline","readonly","required","reversed","selected"]),"function"==typeof HTMLElement&&(N=class extends HTMLElement{constructor(){super(),this.attachShadow({mode:"open"})}connectedCallback(){const{on_mount:t}=this.$$;this.$$.on_disconnect=t.map(o).filter(s);for(const t in this.$$.slotted)this.appendChild(this.$$.slotted[t])}attributeChangedCallback(t,e,n){this[t]=n}disconnectedCallback(){r(this.$$.on_disconnect)}$destroy(){H(this,1),this.$destroy=n}$on(t,e){const n=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return n.push(e),()=>{const t=n.indexOf(e);-1!==t&&n.splice(t,1)}}$set(t){this.$$set&&!i(t)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}});function I(t,e,n){const o=t.slice();return o[6]=e[n],o}function R(t){let e,n,o;return{c(){e=m("sup"),n=m("i"),y(n,"class","far fa-question-circle"),y(e,"data-toggle","tooltip"),y(e,"title",o=t[0].description)},m(t,o){f(t,e,o),d(e,n)},p(t,n){1&n&&o!==(o=t[0].description)&&y(e,"title",o)},d(t){t&&p(e)}}}function z(t){let e,n,o,l,r,s,c=Object.keys(t[0].examples).length>1,i=c&&D(),a=Object.keys(t[0].examples),u=[];for(let e=0;e<a.length;e+=1)u[e]=F(I(t,a,e));return{c(){e=m("div"),n=m("span"),o=h("Try example"),i&&i.c(),l=h(":"),r=$(),s=m("div");for(let t=0;t<u.length;t+=1)u[t].c();y(n,"class","d-table-cell mr-1 my-1 p-1 text-right"),v(n,"white-space","nowrap"),y(s,"class","d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center"),y(e,"class","d-table-row")},m(t,c){f(t,e,c),d(e,n),d(n,o),i&&i.m(n,null),d(n,l),d(e,r),d(e,s);for(let t=0;t<u.length;t+=1)u[t].m(s,null)},p(t,e){if(1&e&&(c=Object.keys(t[0].examples).length>1),c?i||(i=D(),i.c(),i.m(n,l)):i&&(i.d(1),i=null),3&e){let n;for(a=Object.keys(t[0].examples),n=0;n<a.length;n+=1){const o=I(t,a,n);u[n]?u[n].p(o,e):(u[n]=F(o),u[n].c(),u[n].m(s,null))}for(;n<u.length;n+=1)u[n].d(1);u.length=a.length}},d(t){t&&p(e),i&&i.d(),function(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}(u,t)}}}function D(t){let e;return{c(){e=h("s")},m(t,n){f(t,e,n)},d(t){t&&p(e)}}}function F(t){let e,n,o,l,r,s,c=(Array.isArray(t[0].examples)?t[0].examples[t[6]]:t[6])+"";function i(){return t[5](t[6])}return{c(){e=m("span"),n=m("button"),o=h(c),l=$(),y(n,"type","button"),y(n,"class","text-btn"),y(e,"class","text-sm m-1 p-1"),v(e,"white-space","nowrap")},m(t,c){f(t,e,c),d(e,n),d(n,o),d(e,l),r||(s=g(n,"click",i),r=!0)},p(e,n){t=e,1&n&&c!==(c=(Array.isArray(t[0].examples)?t[0].examples[t[6]]:t[6])+"")&&b(o,c)},d(t){t&&p(e),r=!1,s()}}}function G(t){let e,o,l,r,s,c,i,a,u,v,_,k,j,O,S,E,T,A,C,P=t[0].label+"",M=t[0].constraint+"",L=t[0].examples&&Object.keys(t[0].examples).length>0,q=t[0].description&&R(t),N=L&&z(t);return{c(){e=m("div"),o=m("div"),l=h(P),q&&q.c(),r=h(":"),s=$(),c=m("div"),i=m("textarea"),k=$(),j=m("div"),O=h("String contains unsupported characters (should match `"),S=h(M),E=h("`)."),T=$(),N&&N.c(),y(o,"class","col-lg-3 bold text-lg-right my-auto"),y(i,"name",a=t[0].name),y(i,"placeholder",u=t[0].hint),y(i,"rows",v=t[0].rows),y(i,"cols",_=t[0].cols),y(i,"class","form-control nodecoration tiny"),w(i,"is-valid",t[2]),w(i,"is-invalid",!t[2]),y(j,"class","invalid-feedback"),y(c,"class","col-lg-6 pt-2 pt-lg-0"),y(e,"class","row px-4 px-lg-3 pb-4")},m(n,a){f(n,e,a),d(e,o),d(o,l),q&&q.m(o,null),d(o,r),d(e,s),d(e,c),d(c,i),x(i,t[1]),d(c,k),d(c,j),d(j,O),d(j,S),d(j,E),d(c,T),N&&N.m(c,null),A||(C=g(i,"input",t[4]),A=!0)},p(t,[e]){1&e&&P!==(P=t[0].label+"")&&b(l,P),t[0].description?q?q.p(t,e):(q=R(t),q.c(),q.m(o,r)):q&&(q.d(1),q=null),1&e&&a!==(a=t[0].name)&&y(i,"name",a),1&e&&u!==(u=t[0].hint)&&y(i,"placeholder",u),1&e&&v!==(v=t[0].rows)&&y(i,"rows",v),1&e&&_!==(_=t[0].cols)&&y(i,"cols",_),2&e&&x(i,t[1]),4&e&&w(i,"is-valid",t[2]),4&e&&w(i,"is-invalid",!t[2]),1&e&&M!==(M=t[0].constraint+"")&&b(S,M),1&e&&(L=t[0].examples&&Object.keys(t[0].examples).length>0),L?N?N.p(t,e):(N=z(t),N.c(),N.m(c,null)):N&&(N.d(1),N=null)},i:n,o:n,d(t){t&&p(e),q&&q.d(),N&&N.d(),A=!1,C()}}}function J(t,e,n){let o,l,{args:r}=e,s=!0;return t.$$set=t=>{"args"in t&&n(0,r=t.args)},t.$$.update=()=>{var e;3&t.$$.dirty&&void 0!==r&&void 0===o&&n(1,o=r.default),1&t.$$.dirty&&void 0!==r&&n(3,(e=r.constraint,"s",null===/^\^/.exec(e)&&(e=`^${e}`),null===/\$$/.exec(e)&&(e=`${e}$`),l=new RegExp(e,"s"))),10&t.$$.dirty&&void 0!==o&&void 0!==l&&n(2,s=null!==l.exec(o))},[r,o,s,l,function(){o=this.value,n(1,o),n(0,r)},t=>n(1,o=r.examples[t])]}var K=class extends class{$destroy(){H(this,1),this.$destroy=n}$on(t,e){const n=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return n.push(e),()=>{const t=n.indexOf(e);-1!==t&&n.splice(t,1)}}$set(t){this.$$set&&!i(t)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}{constructor(t){super(),B(this,t,J,G,c,{args:0})}}}(),e}()}));