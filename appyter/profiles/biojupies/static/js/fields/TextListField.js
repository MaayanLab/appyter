!function(t,e){if("object"==typeof exports&&"object"==typeof module)module.exports=e();else if("function"==typeof define&&define.amd)define([],e);else{var n=e();for(var c in n)("object"==typeof exports?exports:t)[c]=n[c]}}(window,(function(){return function(t){var e={};function n(c){if(e[c])return e[c].exports;var o=e[c]={i:c,l:!1,exports:{}};return t[c].call(o.exports,o,o.exports,n),o.l=!0,o.exports}return n.m=t,n.c=e,n.d=function(t,e,c){n.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:c})},n.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},n.t=function(t,e){if(1&e&&(t=n(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var c=Object.create(null);if(n.r(c),Object.defineProperty(c,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var o in t)n.d(c,o,function(e){return t[e]}.bind(null,o));return c},n.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return n.d(e,"a",e),e},n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},n.p="/static/",n(n.s=282)}({0:function(t,e,n){"use strict";function c(){}n.d(e,"a",(function(){return L})),n.d(e,"b",(function(){return bt})),n.d(e,"c",(function(){return j})),n.d(e,"d",(function(){return o})),n.d(e,"e",(function(){return k})),n.d(e,"f",(function(){return F})),n.d(e,"g",(function(){return tt})),n.d(e,"h",(function(){return st})),n.d(e,"i",(function(){return d})),n.d(e,"j",(function(){return dt})),n.d(e,"k",(function(){return m})),n.d(e,"l",(function(){return O})),n.d(e,"m",(function(){return g})),n.d(e,"n",(function(){return x})),n.d(e,"o",(function(){return N})),n.d(e,"p",(function(){return ut})),n.d(e,"q",(function(){return it})),n.d(e,"r",(function(){return ct})),n.d(e,"s",(function(){return Z})),n.d(e,"t",(function(){return at})),n.d(e,"u",(function(){return h})),n.d(e,"v",(function(){return v})),n.d(e,"w",(function(){return ft})),n.d(e,"x",(function(){return c})),n.d(e,"y",(function(){return A})),n.d(e,"z",(function(){return ot})),n.d(e,"A",(function(){return w})),n.d(e,"B",(function(){return u})),n.d(e,"C",(function(){return s})),n.d(e,"D",(function(){return P})),n.d(e,"E",(function(){return E})),n.d(e,"F",(function(){return I})),n.d(e,"G",(function(){return M})),n.d(e,"H",(function(){return y})),n.d(e,"I",(function(){return $})),n.d(e,"J",(function(){return K})),n.d(e,"K",(function(){return _})),n.d(e,"L",(function(){return S})),n.d(e,"M",(function(){return et})),n.d(e,"N",(function(){return nt})),n.d(e,"O",(function(){return rt})),n.d(e,"P",(function(){return p}));function o(t,e){for(const n in e)t[n]=e[n];return t}function r(t){return t()}function i(){return Object.create(null)}function u(t){t.forEach(r)}function l(t){return"function"==typeof t}function s(t,e){return t!=t?e==e:t!==e||t&&"object"==typeof t||"function"==typeof t}function f(t){return 0===Object.keys(t).length}function d(t,e,n,c){if(t){const o=a(t,e,n,c);return t[0](o)}}function a(t,e,n,c){return t[1]&&c?o(n.ctx.slice(),t[1](c(e))):n.ctx}function b(t,e,n,c){if(t[2]&&c){const o=t[2](c(n));if(void 0===e.dirty)return o;if("object"==typeof o){const t=[],n=Math.max(e.dirty.length,o.length);for(let c=0;c<n;c+=1)t[c]=e.dirty[c]|o[c];return t}return e.dirty|o}return e.dirty}function p(t,e,n,c,o,r,i){const u=b(e,c,o,r);if(u){const o=a(e,n,c,i);t.p(o,u)}}new Set;function j(t,e){t.appendChild(e)}function h(t,e,n){t.insertBefore(e,n||null)}function O(t){t.parentNode.removeChild(t)}function m(t,e){for(let n=0;n<t.length;n+=1)t[n]&&t[n].d(e)}function g(t){return document.createElement(t)}function $(t){return document.createTextNode(t)}function y(){return $(" ")}function x(){return $("")}function v(t,e,n,c){return t.addEventListener(e,n,c),()=>t.removeEventListener(e,n,c)}function w(t){return function(e){return e.preventDefault(),t.call(this,e)}}function k(t,e,n){null==n?t.removeAttribute(e):t.getAttribute(e)!==n&&t.setAttribute(e,n)}function _(t){return""===t?null:+t}function E(t,e){e=""+e,t.wholeText!==e&&(t.data=e)}function I(t,e){t.value=null==e?"":e}function M(t,e,n,c){t.style.setProperty(e,n,c?"important":"")}function S(t,e,n){t.classList[n?"add":"remove"](e)}class L{constructor(t=null){this.a=t,this.e=this.n=null}m(t,e,n=null){this.e||(this.e=g(e.nodeName),this.t=e,this.h(t)),this.i(n)}h(t){this.e.innerHTML=t,this.n=Array.from(this.e.childNodes)}i(t){for(let e=0;e<this.n.length;e+=1)h(this.t,this.n[e],t)}p(t){this.d(),this.h(t),this.i(this.a)}d(){this.n.forEach(O)}}new Set;let T;function C(t){T=t}function H(){if(!T)throw new Error("Function called outside component initialization");return T}function A(t){H().$$.on_mount.push(t)}function P(t,e){H().$$.context.set(t,e)}function N(t){return H().$$.context.get(t)}const q=[],F=[],G=[],z=[],B=Promise.resolve();let D=!1;function J(){D||(D=!0,B.then(V))}function K(){return J(),B}function R(t){G.push(t)}let Q=!1;const U=new Set;function V(){if(!Q){Q=!0;do{for(let t=0;t<q.length;t+=1){const e=q[t];C(e),W(e.$$)}for(C(null),q.length=0;F.length;)F.pop()();for(let t=0;t<G.length;t+=1){const e=G[t];U.has(e)||(U.add(e),e())}G.length=0}while(q.length);for(;z.length;)z.pop()();D=!1,Q=!1,U.clear()}}function W(t){if(null!==t.fragment){t.update(),u(t.before_update);const e=t.dirty;t.dirty=[-1],t.fragment&&t.fragment.p(t.ctx,e),t.after_update.forEach(R)}}const X=new Set;let Y;function Z(){Y={r:0,c:[],p:Y}}function tt(){Y.r||u(Y.c),Y=Y.p}function et(t,e){t&&t.i&&(X.delete(t),t.i(e))}function nt(t,e,n,c){if(t&&t.o){if(X.has(t))return;X.add(t),Y.c.push(()=>{X.delete(t),c&&(n&&t.d(1),c())}),t.o(e)}}const ct="undefined"!=typeof window?window:"undefined"!=typeof globalThis?globalThis:global;function ot(t,e){nt(t,1,1,()=>{e.delete(t.key)})}function rt(t,e,n,c,o,r,i,u,l,s,f,d){let a=t.length,b=r.length,p=a;const j={};for(;p--;)j[t[p].key]=p;const h=[],O=new Map,m=new Map;for(p=b;p--;){const t=d(o,r,p),u=n(t);let l=i.get(u);l?c&&l.p(t,e):(l=s(u,t),l.c()),O.set(u,h[p]=l),u in j&&m.set(u,Math.abs(p-j[u]))}const g=new Set,$=new Set;function y(t){et(t,1),t.m(u,f),i.set(t.key,t),f=t.first,b--}for(;a&&b;){const e=h[b-1],n=t[a-1],c=e.key,o=n.key;e===n?(f=e.first,a--,b--):O.has(o)?!i.has(c)||g.has(c)?y(e):$.has(o)?a--:m.get(c)>m.get(o)?($.add(c),y(e)):(g.add(o),a--):(l(n,i),a--)}for(;a--;){const e=t[a];O.has(e.key)||l(e,i)}for(;b;)y(h[b-1]);return h}function it(t,e){const n={},c={},o={$$scope:1};let r=t.length;for(;r--;){const i=t[r],u=e[r];if(u){for(const t in i)t in u||(c[t]=1);for(const t in u)o[t]||(n[t]=u[t],o[t]=1);t[r]=u}else for(const t in i)o[t]=1}for(const t in c)t in n||(n[t]=void 0);return n}function ut(t){return"object"==typeof t&&null!==t?t:{}}new Set(["allowfullscreen","allowpaymentrequest","async","autofocus","autoplay","checked","controls","default","defer","disabled","formnovalidate","hidden","ismap","loop","multiple","muted","nomodule","novalidate","open","playsinline","readonly","required","reversed","selected"]);let lt;function st(t){t&&t.c()}function ft(t,e,n,c){const{fragment:o,on_mount:i,on_destroy:s,after_update:f}=t.$$;o&&o.m(e,n),c||R(()=>{const e=i.map(r).filter(l);s?s.push(...e):u(e),t.$$.on_mount=[]}),f.forEach(R)}function dt(t,e){const n=t.$$;null!==n.fragment&&(u(n.on_destroy),n.fragment&&n.fragment.d(e),n.on_destroy=n.fragment=null,n.ctx=[])}function at(t,e,n,o,r,l,s=[-1]){const f=T;C(t);const d=t.$$={fragment:null,ctx:null,props:l,update:c,not_equal:r,bound:i(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(f?f.$$.context:e.context||[]),callbacks:i(),dirty:s,skip_bound:!1};let a=!1;if(d.ctx=n?n(t,e.props||{},(e,n,...c)=>{const o=c.length?c[0]:n;return d.ctx&&r(d.ctx[e],d.ctx[e]=o)&&(!d.skip_bound&&d.bound[e]&&d.bound[e](o),a&&function(t,e){-1===t.$$.dirty[0]&&(q.push(t),J(),t.$$.dirty.fill(0)),t.$$.dirty[e/31|0]|=1<<e%31}(t,e)),n}):[],d.update(),a=!0,u(d.before_update),d.fragment=!!o&&o(d.ctx),e.target){if(e.hydrate){const t=function(t){return Array.from(t.childNodes)}(e.target);d.fragment&&d.fragment.l(t),t.forEach(O)}else d.fragment&&d.fragment.c();e.intro&&et(t.$$.fragment),ft(t,e.target,e.anchor,e.customElement),V()}C(f)}"function"==typeof HTMLElement&&(lt=class extends HTMLElement{constructor(){super(),this.attachShadow({mode:"open"})}connectedCallback(){const{on_mount:t}=this.$$;this.$$.on_disconnect=t.map(r).filter(l);for(const t in this.$$.slotted)this.appendChild(this.$$.slotted[t])}attributeChangedCallback(t,e,n){this[t]=n}disconnectedCallback(){u(this.$$.on_disconnect)}$destroy(){dt(this,1),this.$destroy=c}$on(t,e){const n=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return n.push(e),()=>{const t=n.indexOf(e);-1!==t&&n.splice(t,1)}}$set(t){this.$$set&&!f(t)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}});class bt{$destroy(){dt(this,1),this.$destroy=c}$on(t,e){const n=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return n.push(e),()=>{const t=n.indexOf(e);-1!==t&&n.splice(t,1)}}$set(t){this.$$set&&!f(t)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}},10:function(t,e,n){"use strict";function c(t){return"object"==typeof t&&Array.isArray(t)?t:[t]}n.d(e,"a",(function(){return c}))},282:function(t,e,n){t.exports=n(283)},283:function(t,e,n){"use strict";n.r(e);var c=n(0),o=n(10),r=n(7);function i(t,e,n){const c=t.slice();return c[6]=e[n],c}function u(t,e,n){const c=t.slice();return c[9]=e[n],c}function l(t){let e,n,o;return{c(){e=Object(c.m)("sup"),n=Object(c.m)("i"),Object(c.e)(n,"class","far fa-question-circle"),Object(c.e)(e,"data-toggle","tooltip"),Object(c.e)(e,"title",o=t[0].description)},m(t,o){Object(c.u)(t,e,o),Object(c.c)(e,n)},p(t,n){1&n&&o!==(o=t[0].description)&&Object(c.e)(e,"title",o)},d(t){t&&Object(c.l)(e)}}}function s(t){let e,n,o,r,i,u,l=t[9].index+"",s=t[9].value+"";return{c(){e=Object(c.I)("Line "),n=Object(c.I)(l),o=Object(c.I)(": "),r=Object(c.I)(s),i=Object(c.I)(" contains unsupported characters"),u=Object(c.m)("br")},m(t,l){Object(c.u)(t,e,l),Object(c.u)(t,n,l),Object(c.u)(t,o,l),Object(c.u)(t,r,l),Object(c.u)(t,i,l),Object(c.u)(t,u,l)},p(t,e){4&e&&l!==(l=t[9].index+"")&&Object(c.E)(n,l),4&e&&s!==(s=t[9].value+"")&&Object(c.E)(r,s)},d(t){t&&Object(c.l)(e),t&&Object(c.l)(n),t&&Object(c.l)(o),t&&Object(c.l)(r),t&&Object(c.l)(i),t&&Object(c.l)(u)}}}function f(t){let e,n,o,r,u,l,s=Object.keys(t[0].examples).length>1,f=s&&d(t),b=Object.keys(t[0].examples),p=[];for(let e=0;e<b.length;e+=1)p[e]=a(i(t,b,e));return{c(){e=Object(c.m)("div"),n=Object(c.m)("span"),o=Object(c.I)("Try example"),f&&f.c(),r=Object(c.I)(":"),u=Object(c.H)(),l=Object(c.m)("div");for(let t=0;t<p.length;t+=1)p[t].c();Object(c.e)(n,"class","d-table-cell mr-1 my-1 p-1 text-right"),Object(c.G)(n,"white-space","nowrap"),Object(c.e)(l,"class","d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center"),Object(c.e)(e,"class","d-table-row")},m(t,i){Object(c.u)(t,e,i),Object(c.c)(e,n),Object(c.c)(n,o),f&&f.m(n,null),Object(c.c)(n,r),Object(c.c)(e,u),Object(c.c)(e,l);for(let t=0;t<p.length;t+=1)p[t].m(l,null)},p(t,e){if(1&e&&(s=Object.keys(t[0].examples).length>1),s?f||(f=d(t),f.c(),f.m(n,r)):f&&(f.d(1),f=null),3&e){let n;for(b=Object.keys(t[0].examples),n=0;n<b.length;n+=1){const c=i(t,b,n);p[n]?p[n].p(c,e):(p[n]=a(c),p[n].c(),p[n].m(l,null))}for(;n<p.length;n+=1)p[n].d(1);p.length=b.length}},d(t){t&&Object(c.l)(e),f&&f.d(),Object(c.k)(p,t)}}}function d(t){let e;return{c(){e=Object(c.I)("s")},m(t,n){Object(c.u)(t,e,n)},d(t){t&&Object(c.l)(e)}}}function a(t){let e,n,o,r,i,u,l=t[6]+"";function s(){return t[5](t[6])}return{c(){e=Object(c.m)("span"),n=Object(c.m)("a"),o=Object(c.I)(l),r=Object(c.H)(),Object(c.e)(n,"href","javascript:"),Object(c.e)(e,"class","text-sm m-1 p-1"),Object(c.G)(e,"white-space","nowrap")},m(t,l){Object(c.u)(t,e,l),Object(c.c)(e,n),Object(c.c)(n,o),Object(c.c)(e,r),i||(u=Object(c.v)(n,"click",s),i=!0)},p(e,n){t=e,1&n&&l!==(l=t[6]+"")&&Object(c.E)(o,l)},d(t){t&&Object(c.l)(e),i=!1,u()}}}function b(t){let e,n,o,r,i,d,a,b,p,j,h,O,m,g,$,y,x,v,w,k=t[0].label+"",_=t[0].constraint+"",E=t[0].examples&&Object.keys(t[0].examples).length>0,I=t[0].description&&l(t),M=t[2],S=[];for(let e=0;e<M.length;e+=1)S[e]=s(u(t,M,e));let L=E&&f(t);return{c(){e=Object(c.m)("div"),n=Object(c.m)("div"),o=Object(c.I)(k),I&&I.c(),r=Object(c.I)(":"),i=Object(c.H)(),d=Object(c.m)("div"),a=Object(c.m)("textarea"),O=Object(c.H)(),m=Object(c.m)("div");for(let t=0;t<S.length;t+=1)S[t].c();g=Object(c.I)("\n      Each line should match `"),$=Object(c.I)(_),y=Object(c.I)("`"),x=Object(c.H)(),L&&L.c(),Object(c.e)(n,"class","col-lg-3 bold text-lg-right my-auto"),Object(c.e)(a,"name",b=t[0].name),Object(c.e)(a,"placeholder",p=t[0].hint),Object(c.e)(a,"rows",j=t[0].rows),Object(c.e)(a,"cols",h=t[0].cols),Object(c.e)(a,"class","form-control nodecoration tiny"),Object(c.L)(a,"is-valid",0===t[2].length),Object(c.L)(a,"is-invalid",0!==t[2].length),Object(c.e)(m,"class","invalid-feedback"),Object(c.e)(d,"class","col-lg-6 pt-2 pt-lg-0"),Object(c.e)(e,"class","row px-4 px-lg-3 pb-4")},m(u,l){Object(c.u)(u,e,l),Object(c.c)(e,n),Object(c.c)(n,o),I&&I.m(n,null),Object(c.c)(n,r),Object(c.c)(e,i),Object(c.c)(e,d),Object(c.c)(d,a),Object(c.F)(a,t[1]),Object(c.c)(d,O),Object(c.c)(d,m);for(let t=0;t<S.length;t+=1)S[t].m(m,null);Object(c.c)(m,g),Object(c.c)(m,$),Object(c.c)(m,y),Object(c.c)(d,x),L&&L.m(d,null),v||(w=Object(c.v)(a,"input",t[4]),v=!0)},p(t,[e]){if(1&e&&k!==(k=t[0].label+"")&&Object(c.E)(o,k),t[0].description?I?I.p(t,e):(I=l(t),I.c(),I.m(n,r)):I&&(I.d(1),I=null),1&e&&b!==(b=t[0].name)&&Object(c.e)(a,"name",b),1&e&&p!==(p=t[0].hint)&&Object(c.e)(a,"placeholder",p),1&e&&j!==(j=t[0].rows)&&Object(c.e)(a,"rows",j),1&e&&h!==(h=t[0].cols)&&Object(c.e)(a,"cols",h),2&e&&Object(c.F)(a,t[1]),4&e&&Object(c.L)(a,"is-valid",0===t[2].length),4&e&&Object(c.L)(a,"is-invalid",0!==t[2].length),4&e){let n;for(M=t[2],n=0;n<M.length;n+=1){const c=u(t,M,n);S[n]?S[n].p(c,e):(S[n]=s(c),S[n].c(),S[n].m(m,g))}for(;n<S.length;n+=1)S[n].d(1);S.length=M.length}1&e&&_!==(_=t[0].constraint+"")&&Object(c.E)($,_),1&e&&(E=t[0].examples&&Object.keys(t[0].examples).length>0),E?L?L.p(t,e):(L=f(t),L.c(),L.m(d,null)):L&&(L.d(1),L=null)},i:c.x,o:c.x,d(t){t&&Object(c.l)(e),I&&I.d(),Object(c.k)(S,t),L&&L.d(),v=!1,w()}}}function p(t,e,n){let c,i,{args:u}=e,l=[];return t.$$set=t=>{"args"in t&&n(0,u=t.args)},t.$$.update=()=>{3&t.$$.dirty&&void 0!==u&&void 0===c&&n(1,c=Object(o.a)(u.default).join("\n")),1&t.$$.dirty&&void 0!==u&&n(3,i=Object(r.a)(u.constraint)),10&t.$$.dirty&&void 0!==c&&void 0!==i&&n(2,l=c.replace(/\n+$/g,"").split("\n").filter(t=>null===i.exec(t)).map((t,e)=>({value:t,index:e})))},[u,c,l,i,function(){c=this.value,n(1,c),n(0,u)},t=>n(1,c=u.examples[t].join("\n"))]}class j extends c.b{constructor(t){super(),Object(c.t)(this,t,p,b,c.C,{args:0})}}e.default=j},7:function(t,e,n){"use strict";function c(t,e){return null===/^\^/.exec(t)&&(t="^"+t),null===/\$$/.exec(t)&&(t+="$"),new RegExp(t,e)}n.d(e,"a",(function(){return c}))}})}));