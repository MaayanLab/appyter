"use strict";(self.webpackChunkappyter_js=self.webpackChunkappyter_js||[]).push([[977],{7977:function(e,t,n){n.r(t);var r=n(8826),a=n(7909),l=n(7003);function s(e){(0,r.qOq)(e,"svelte-7t3aq4",".progress.svelte-7t3aq4{height:25px;width:100%;background-color:grey}.progress-bar.svelte-7t3aq4{height:100%;background-color:blue}.progress-bar.bg-success.svelte-7t3aq4{height:100%;background-color:green}")}function o(e,t,n){const r=e.slice();return r[11]=t[n],r}function i(e,t,n){const r=e.slice();return r[11]=t[n],r}function c(e){let t,n,a,l;return{c(){t=(0,r.bGB)("sup"),n=(0,r.bGB)("i"),l=(0,r.DhX)(),(0,r.Ljt)(n,"class","far fa-question-circle"),(0,r.Ljt)(t,"data-toggle","tooltip"),(0,r.Ljt)(t,"title",a=e[0].description)},m(e,a){(0,r.$Tr)(e,t,a),(0,r.R3I)(t,n),(0,r.$Tr)(e,l,a)},p(e,n){1&n&&a!==(a=e[0].description)&&(0,r.Ljt)(t,"title",a)},d(e){e&&(0,r.ogt)(t),e&&(0,r.ogt)(l)}}}function u(e){let t,n,a,l,s,o,i,c="error"===e[2].bg&&d(e),u="warning"===e[2].bg&&g(e);return{c(){t=(0,r.bGB)("div"),n=(0,r.bGB)("div"),a=(0,r.bGB)("div"),o=(0,r.DhX)(),c&&c.c(),i=(0,r.DhX)(),u&&u.c(),(0,r.Ljt)(a,"class",l="progress-bar bg-"+e[2].bg+" svelte-7t3aq4"),(0,r.Ljt)(a,"role","progressbar"),(0,r.Ljt)(a,"aria-valuemin","0"),(0,r.Ljt)(a,"aria-valuemax","100"),(0,r.Ljt)(a,"aria-valuenow",s=e[2].progress),(0,r.czc)(a,"width",e[2].progress+"%"),(0,r.VHj)(a,"progress-bar-striped",e[2].striped),(0,r.VHj)(a,"progress-bar-animated",e[2].animated),(0,r.Ljt)(n,"class","progress bg-light svelte-7t3aq4")},m(e,l){(0,r.$Tr)(e,t,l),(0,r.R3I)(t,n),(0,r.R3I)(n,a),(0,r.R3I)(t,o),c&&c.m(t,null),(0,r.R3I)(t,i),u&&u.m(t,null)},p(e,n){4&n&&l!==(l="progress-bar bg-"+e[2].bg+" svelte-7t3aq4")&&(0,r.Ljt)(a,"class",l),4&n&&s!==(s=e[2].progress)&&(0,r.Ljt)(a,"aria-valuenow",s),4&n&&(0,r.czc)(a,"width",e[2].progress+"%"),4&n&&(0,r.VHj)(a,"progress-bar-striped",e[2].striped),4&n&&(0,r.VHj)(a,"progress-bar-animated",e[2].animated),"error"===e[2].bg?c?c.p(e,n):(c=d(e),c.c(),c.m(t,i)):c&&(c.d(1),c=null),"warning"===e[2].bg?u?u.p(e,n):(u=g(e),u.c(),u.m(t,null)):u&&(u.d(1),u=null)},d(e){e&&(0,r.ogt)(t),c&&c.d(),u&&u.d()}}}function d(e){let t,n,a,l=e[2].error&&p(e),s=e[2].url&&f(e);return{c(){t=(0,r.bGB)("div"),n=(0,r.fLW)("Error loading file"),l&&l.c(),a=(0,r.DhX)(),s&&s.c(),(0,r.Ljt)(t,"class","alert alert-danger")},m(e,o){(0,r.$Tr)(e,t,o),(0,r.R3I)(t,n),l&&l.m(t,null),(0,r.R3I)(t,a),s&&s.m(t,null)},p(e,n){e[2].error?l?l.p(e,n):(l=p(e),l.c(),l.m(t,a)):l&&(l.d(1),l=null),e[2].url?s?s.p(e,n):(s=f(e),s.c(),s.m(t,null)):s&&(s.d(1),s=null)},d(e){e&&(0,r.ogt)(t),l&&l.d(),s&&s.d()}}}function p(e){let t,n,a=e[2].error+"";return{c(){t=(0,r.fLW)(": "),n=(0,r.fLW)(a)},m(e,a){(0,r.$Tr)(e,t,a),(0,r.$Tr)(e,n,a)},p(e,t){4&t&&a!==(a=e[2].error+"")&&(0,r.rTO)(n,a)},d(e){e&&(0,r.ogt)(t),e&&(0,r.ogt)(n)}}}function f(e){let t,n,a,l,s=e[2].url+"";return{c(){t=(0,r.fLW)("from "),n=(0,r.bGB)("a"),a=(0,r.fLW)(s),(0,r.Ljt)(n,"href",l=e[2].url),(0,r.Ljt)(n,"target","_blank")},m(e,l){(0,r.$Tr)(e,t,l),(0,r.$Tr)(e,n,l),(0,r.R3I)(n,a)},p(e,t){4&t&&s!==(s=e[2].url+"")&&(0,r.rTO)(a,s),4&t&&l!==(l=e[2].url)&&(0,r.Ljt)(n,"href",l)},d(e){e&&(0,r.ogt)(t),e&&(0,r.ogt)(n)}}}function g(e){let t,n,a,l,s,o,i,c,u,d,p=e[2].url+"",f=e[2].error&&m(e);return{c(){t=(0,r.bGB)("div"),n=(0,r.fLW)("Error loading file"),f&&f.c(),a=(0,r.bGB)("br"),l=(0,r.DhX)(),s=(0,r.bGB)("b"),s.textContent="It may require user engagement",o=(0,r.fLW)(", please visit\n            "),i=(0,r.bGB)("a"),c=(0,r.fLW)(p),d=(0,r.fLW)("\n          to download the example file for upload."),(0,r.Ljt)(i,"href",u=e[2].url),(0,r.Ljt)(i,"target","_blank"),(0,r.Ljt)(t,"class","alert alert-warning")},m(e,u){(0,r.$Tr)(e,t,u),(0,r.R3I)(t,n),f&&f.m(t,null),(0,r.R3I)(t,a),(0,r.R3I)(t,l),(0,r.R3I)(t,s),(0,r.R3I)(t,o),(0,r.R3I)(t,i),(0,r.R3I)(i,c),(0,r.R3I)(t,d)},p(e,n){e[2].error?f?f.p(e,n):(f=m(e),f.c(),f.m(t,a)):f&&(f.d(1),f=null),4&n&&p!==(p=e[2].url+"")&&(0,r.rTO)(c,p),4&n&&u!==(u=e[2].url)&&(0,r.Ljt)(i,"href",u)},d(e){e&&(0,r.ogt)(t),f&&f.d()}}}function m(e){let t,n,a=e[2].error+"";return{c(){t=(0,r.fLW)(": "),n=(0,r.fLW)(a)},m(e,a){(0,r.$Tr)(e,t,a),(0,r.$Tr)(e,n,a)},p(e,t){4&t&&a!==(a=e[2].error+"")&&(0,r.rTO)(n,a)},d(e){e&&(0,r.ogt)(t),e&&(0,r.ogt)(n)}}}function h(e){let t,n,a,l,s,c,u,d,p,f,g,m,h,R,I,k,v,y,x=Object.keys(e[0].examples).length>1,T=Object.keys(e[0].examples).length>1,B=x&&b(),$=Object.keys(e[0].examples),G=[];for(let t=0;t<$.length;t+=1)G[t]=L(i(e,$,t));let O=T&&j(),W=Object.keys(e[0].examples),D=[];for(let t=0;t<W.length;t+=1)D[t]=w(o(e,W,t));return{c(){t=(0,r.bGB)("div"),n=(0,r.bGB)("div"),a=(0,r.bGB)("span"),l=(0,r.fLW)("Load example"),B&&B.c(),s=(0,r.DhX)(),c=(0,r.bGB)("sup"),c.innerHTML='<i class="far fa-question-circle"></i>',u=(0,r.fLW)(":"),d=(0,r.DhX)(),p=(0,r.bGB)("div");for(let e=0;e<G.length;e+=1)G[e].c();f=(0,r.DhX)(),g=(0,r.bGB)("div"),m=(0,r.bGB)("span"),h=(0,r.fLW)("Download example"),O&&O.c(),R=(0,r.DhX)(),I=(0,r.bGB)("sup"),I.innerHTML='<i class="far fa-question-circle"></i>',k=(0,r.fLW)(":"),v=(0,r.DhX)(),y=(0,r.bGB)("div");for(let e=0;e<D.length;e+=1)D[e].c();(0,r.Ljt)(c,"data-toggle","tooltip"),(0,r.Ljt)(c,"title","Load the example file directly into the appyter"),(0,r.Ljt)(a,"class","d-table-cell mr-1 my-1 p-1 text-right"),(0,r.czc)(a,"white-space","nowrap"),(0,r.Ljt)(p,"class","d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center"),(0,r.Ljt)(n,"class","d-table-row"),(0,r.Ljt)(I,"data-toggle","tooltip"),(0,r.Ljt)(I,"title","Download the example file for inspection"),(0,r.Ljt)(m,"class","d-table-cell mr-1 my-1 p-1 text-right"),(0,r.czc)(m,"white-space","nowrap"),(0,r.Ljt)(y,"class","d-table-cell table-grow d-flex flex-wrap justify-content-start align-items-center"),(0,r.Ljt)(g,"class","d-table-row"),(0,r.Ljt)(t,"class","d-table")},m(e,o){(0,r.$Tr)(e,t,o),(0,r.R3I)(t,n),(0,r.R3I)(n,a),(0,r.R3I)(a,l),B&&B.m(a,null),(0,r.R3I)(a,s),(0,r.R3I)(a,c),(0,r.R3I)(a,u),(0,r.R3I)(n,d),(0,r.R3I)(n,p);for(let e=0;e<G.length;e+=1)G[e].m(p,null);(0,r.R3I)(t,f),(0,r.R3I)(t,g),(0,r.R3I)(g,m),(0,r.R3I)(m,h),O&&O.m(m,null),(0,r.R3I)(m,R),(0,r.R3I)(m,I),(0,r.R3I)(m,k),(0,r.R3I)(g,v),(0,r.R3I)(g,y);for(let e=0;e<D.length;e+=1)D[e].m(y,null)},p(e,t){if(1&t&&(x=Object.keys(e[0].examples).length>1),x?B||(B=b(),B.c(),B.m(a,s)):B&&(B.d(1),B=null),33&t){let n;for($=Object.keys(e[0].examples),n=0;n<$.length;n+=1){const r=i(e,$,n);G[n]?G[n].p(r,t):(G[n]=L(r),G[n].c(),G[n].m(p,null))}for(;n<G.length;n+=1)G[n].d(1);G.length=$.length}if(1&t&&(T=Object.keys(e[0].examples).length>1),T?O||(O=j(),O.c(),O.m(m,R)):O&&(O.d(1),O=null),1&t){let n;for(W=Object.keys(e[0].examples),n=0;n<W.length;n+=1){const r=o(e,W,n);D[n]?D[n].p(r,t):(D[n]=w(r),D[n].c(),D[n].m(y,null))}for(;n<D.length;n+=1)D[n].d(1);D.length=W.length}},d(e){e&&(0,r.ogt)(t),B&&B.d(),(0,r.RMB)(G,e),O&&O.d(),(0,r.RMB)(D,e)}}}function b(e){let t;return{c(){t=(0,r.fLW)("s")},m(e,n){(0,r.$Tr)(e,t,n)},d(e){e&&(0,r.ogt)(t)}}}function L(e){let t,n,a,l,s,o,i=e[11]+"";function c(){return e[8](e[11])}return{c(){t=(0,r.bGB)("span"),n=(0,r.bGB)("button"),a=(0,r.fLW)(i),l=(0,r.DhX)(),(0,r.Ljt)(n,"type","button"),(0,r.Ljt)(n,"class","text-btn"),(0,r.Ljt)(t,"class","text-sm m-1 p-1"),(0,r.czc)(t,"white-space","nowrap")},m(e,i){(0,r.$Tr)(e,t,i),(0,r.R3I)(t,n),(0,r.R3I)(n,a),(0,r.R3I)(t,l),s||(o=(0,r.oLt)(n,"click",c),s=!0)},p(t,n){e=t,1&n&&i!==(i=e[11]+"")&&(0,r.rTO)(a,i)},d(e){e&&(0,r.ogt)(t),s=!1,o()}}}function j(e){let t;return{c(){t=(0,r.fLW)("s")},m(e,n){(0,r.$Tr)(e,t,n)},d(e){e&&(0,r.ogt)(t)}}}function w(e){let t,n,a,l,s,o=e[11]+"";return{c(){t=(0,r.bGB)("span"),n=(0,r.bGB)("a"),a=(0,r.fLW)(o),s=(0,r.DhX)(),(0,r.Ljt)(n,"href",l=e[0].examples[e[11]]),(0,r.Ljt)(n,"target","_blank"),(0,r.Ljt)(t,"class","text-sm m-1 p-1"),(0,r.czc)(t,"white-space","nowrap")},m(e,l){(0,r.$Tr)(e,t,l),(0,r.R3I)(t,n),(0,r.R3I)(n,a),(0,r.R3I)(t,s)},p(e,t){1&t&&o!==(o=e[11]+"")&&(0,r.rTO)(a,o),1&t&&l!==(l=e[0].examples[e[11]])&&(0,r.Ljt)(n,"href",l)},d(e){e&&(0,r.ogt)(t)}}}function R(e){let t,n,a,l,s,o,i,d,p,f,g,m,b,L,j,w,R,I,k,v,y,x=e[0].label+"",T=(e[3]||"Choose file")+"",B=e[0].examples&&Object.keys(e[0].examples).length>0,$=e[0].description&&c(e),G=void 0!==e[2]&&u(e),O=B&&h(e);return{c(){t=(0,r.bGB)("div"),n=(0,r.bGB)("div"),a=(0,r.fLW)(x),l=(0,r.DhX)(),$&&$.c(),s=(0,r.fLW)(":"),o=(0,r.DhX)(),i=(0,r.bGB)("div"),d=(0,r.bGB)("div"),p=(0,r.bGB)("input"),g=(0,r.DhX)(),m=(0,r.bGB)("input"),L=(0,r.DhX)(),j=(0,r.bGB)("label"),w=(0,r.fLW)(T),I=(0,r.DhX)(),G&&G.c(),k=(0,r.DhX)(),O&&O.c(),(0,r.Ljt)(n,"class","col-lg-3 bold text-lg-right my-auto"),(0,r.Ljt)(p,"type","file"),(0,r.Ljt)(p,"class","custom-file-input"),(0,r.Ljt)(p,"id",f=e[0].name),(0,r.Ljt)(m,"type","text"),(0,r.Ljt)(m,"class","hidden"),(0,r.Ljt)(m,"name",b=e[0].name),(0,r.Ljt)(j,"class","custom-file-label"),(0,r.Ljt)(j,"for",R=e[0].name),(0,r.Ljt)(d,"class","custom-file"),(0,r.Ljt)(d,"dropzone","copy"),(0,r.Ljt)(i,"class","col-lg-6 pt-2 pt-lg-0"),(0,r.Ljt)(t,"class","row px-4 px-lg-3 pb-4")},m(c,u){(0,r.$Tr)(c,t,u),(0,r.R3I)(t,n),(0,r.R3I)(n,a),(0,r.R3I)(n,l),$&&$.m(n,null),(0,r.R3I)(n,s),(0,r.R3I)(t,o),(0,r.R3I)(t,i),(0,r.R3I)(i,d),(0,r.R3I)(d,p),e[6](p),(0,r.R3I)(d,g),(0,r.R3I)(d,m),(0,r.BmG)(m,e[4]),(0,r.R3I)(d,L),(0,r.R3I)(d,j),(0,r.R3I)(j,w),(0,r.R3I)(i,I),G&&G.m(i,null),(0,r.R3I)(i,k),O&&O.m(i,null),v||(y=(0,r.oLt)(m,"input",e[7]),v=!0)},p(e,[t]){1&t&&x!==(x=e[0].label+"")&&(0,r.rTO)(a,x),e[0].description?$?$.p(e,t):($=c(e),$.c(),$.m(n,s)):$&&($.d(1),$=null),1&t&&f!==(f=e[0].name)&&(0,r.Ljt)(p,"id",f),1&t&&b!==(b=e[0].name)&&(0,r.Ljt)(m,"name",b),16&t&&m.value!==e[4]&&(0,r.BmG)(m,e[4]),8&t&&T!==(T=(e[3]||"Choose file")+"")&&(0,r.rTO)(w,T),1&t&&R!==(R=e[0].name)&&(0,r.Ljt)(j,"for",R),void 0!==e[2]?G?G.p(e,t):(G=u(e),G.c(),G.m(i,k)):G&&(G.d(1),G=null),1&t&&(B=e[0].examples&&Object.keys(e[0].examples).length>0),B?O?O.p(e,t):(O=h(e),O.c(),O.m(i,null)):O&&(O.d(1),O=null)},i:r.ZTd,o:r.ZTd,d(n){n&&(0,r.ogt)(t),$&&$.d(),e[6](null),G&&G.d(),O&&O.d(),v=!1,y()}}}function I(e,t,s){let o;(0,r.FIv)(e,a.Z,(e=>s(9,o=e)));let i,c,u,d,{args:p}=t;async function f(e,t){s(2,c={striped:!0,animated:!0,bg:"primary",progress:0}),-1===e.indexOf("://")&&(e=new URL(e,document.baseURI).href);try{if(200!==(await fetch(`check/${e}`)).status)throw new Error;s(2,c={...c,bg:"success",animated:!1,striped:!1,progress:100}),s(3,u=`${t}`),s(4,d=`${e}#${t}`)}catch(t){s(2,c={progress:100,url:e,bg:"warning",striped:!1,animated:!1})}}return(0,l.H3)((async()=>{const{default:e}=await n.e(29).then(n.t.bind(n,9029,23)),{default:t}=await Promise.all([n.e(213),n.e(284)]).then(n.bind(n,1284));await async function(e){e.listenOnInput(i),e.addEventListener("start",(function(e){e.file.meta.auth=o.keycloak.token,s(2,c={striped:!0,bg:"primary",progress:0})})),e.addEventListener("progress",(function(e){s(2,c={...c,progress:e.bytesLoaded/e.file.size*100|0,animated:!0})})),e.addEventListener("complete",(function(e){s(2,c={progress:100,bg:"success",striped:!1,animated:!1}),s(3,u=e.file.name),s(4,d=e.detail.full_filename)})),e.addEventListener("error",(function(e){console.error(e),s(2,c={progress:100,bg:"danger",error:e.error,striped:!1,animated:!1})}))}(new e(t))})),e.$$set=e=>{"args"in e&&s(0,p=e.args)},[p,i,c,u,d,f,function(e){r.VnY[e?"unshift":"push"]((()=>{i=e,s(1,i)}))},function(){d=this.value,s(4,d)},e=>f(p.examples[e],e)]}class k extends r.f_C{constructor(e){super(),(0,r.S1n)(this,e,I,R,r.N8,{args:0},s)}}t.default=k},7909:function(e,t,n){var r=n(4683),a=n(9666);const l=function(){const{subscribe:e,set:t}=(0,r.fZ)({state:window._config.EXTRAS.includes("catalog-integration")?"init":"guest",keycloak:{}});return window._config.EXTRAS.includes("catalog-integration")&&void 0!==window._config.keycloak&&n.e(671).then(n.bind(n,4671)).then((async({default:e})=>{const n=new e(window._config.keycloak.params),r=n.logout;Object.assign(n,{getValidToken:async()=>{try{await n.updateToken(30)}catch(e){console.error(e),t({state:"guest",keycloak:n})}return n.token},logout:()=>{r(),t({state:"guest",keycloak:n})}});const l=await n.init({...window._config.keycloak.init,redirectUri:window.location.href+(window.location.href.includes("#")?"":"#")+(window.location.href.includes("?")?"":"?")});t({state:l?"auth":"guest",keycloak:n}),a.Z.update((e=>{const t={...e.params};return"code"in t&&delete t.code,"session_state"in t&&delete t.session_state,"state"in t&&delete t.state,{...e,params:t}}))})).catch((e=>{console.error(e),t({state:"error",keycloak:keycloak})})),{subscribe:e}}();l.subscribe((e=>{"auth"===e.state&&null===document.cookie.match(/^(.*;)?\s*authorization\s*=\s*[^;]+(.*)?$/)&&(document.cookie=`authorization=${e.keycloak.token}; expires=${new Date(1e3*e.keycloak.tokenParsed.exp).toUTCString()}; secure`)})),t.Z=l},9666:function(e,t,n){var r=n(4683);function a(e){const t=e.indexOf("?");if(-1===t)return{path:e,params:{}};{const[n,r]=[e.slice(0,t),e.slice(t+1)];return{path:n,params:function(e){return""===e?{}:e.split("&").map((e=>e.split("=").map(decodeURIComponent))).reduce(((e,[t,n])=>({...e,[t]:n})),{})}(r)}}}function l(){return(window.location.hash||"#").slice(1)}const s=function(){const{path:e,params:t,server:n}={...a(l()),server:a(`${window.location.pathname}${window.location.search}`)},{subscribe:s,update:o,set:i}=(0,r.fZ)({path:e,params:t,server:n});let c=e;return s((({path:e,params:t,server:n})=>{const r=function({path:e,params:t}){const n=function(e){return Object.keys(e).filter((t=>void 0!==e[t]&&""!==e[t])).map((t=>[t,e[t]].map(encodeURIComponent).join("="))).join("&")}(t);return""===n?e:`${e}?${n}`}({path:e,params:t});if(e!==c)window.location.hash=r,c=e;else{const e=`${window.location.origin}${window.location.pathname}${window.location.search}`;history.replaceState(void 0,void 0,""!==r?`${e}#${r}`:e)}})),window.addEventListener("hashchange",(()=>i({...a(l()),initServer:n}))),{subscribe:s,update:o,set:i}}();t.Z=s},4683:function(e,t,n){n.d(t,{fZ:function(){return l}});var r=n(8826);const a=[];function l(e,t=r.ZTd){let n;const l=new Set;function s(t){if((0,r.N8)(e,t)&&(e=t,n)){const t=!a.length;for(const t of l)t[1](),a.push(t,e);if(t){for(let e=0;e<a.length;e+=2)a[e][0](a[e+1]);a.length=0}}}return{set:s,update:function(t){s(t(e))},subscribe:function(a,o=r.ZTd){const i=[a,o];return l.add(i),1===l.size&&(n=t(s)||r.ZTd),a(e),()=>{l.delete(i),0===l.size&&(n(),n=null)}}}}}}]);