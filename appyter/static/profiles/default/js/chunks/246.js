"use strict";(self.webpackChunkappyter_js=self.webpackChunkappyter_js||[]).push([[246,798],{3798:function(t,e,n){n.r(e);var c=n(8826);function o(t){let e,n,o;const l=t[1].default,r=(0,c.nuO)(l,t,t[0],null);return{c(){e=(0,c.bGB)("div"),n=(0,c.bGB)("div"),r&&r.c(),(0,c.Ljt)(n,"class","col col-lg-9 px-lg-3 my-auto px-4"),(0,c.Ljt)(e,"class","row px-4 px-lg-3 pb-4 justify-content-center")},m(t,l){(0,c.$Tr)(t,e,l),(0,c.R3I)(e,n),r&&r.m(n,null),o=!0},p(t,[e]){r&&r.p&&(!o||1&e)&&(0,c.kmG)(r,l,t,t[0],o?(0,c.u2N)(l,t[0],e,null):(0,c.VOJ)(t[0]),null)},i(t){o||((0,c.Ui)(r,t),o=!0)},o(t){(0,c.etI)(r,t),o=!1},d(t){t&&(0,c.ogt)(e),r&&r.d(t)}}}function l(t,e,n){let{$$slots:c={},$$scope:o}=e;return t.$$set=t=>{"$$scope"in t&&n(0,o=t.$$scope)},[o,c]}class r extends c.f_C{constructor(t){super(),(0,c.S1n)(this,t,l,o,c.N8,{})}}e.default=r},3246:function(t,e,n){n.r(e),n.d(e,{default:function(){return P}});var c=n(8826),o=n(7909),l=n(1782);function r(t){const e=["B","KB","MB","GB","TB"];let n;for(let c=0;c<e.length-1&&(n=e[c],!(t<1e3));c++)t/=1e3;return`${t.toFixed(2)} ${n}`}function i(t,e,n){const c=t.slice();return c[12]=e[n],c}function a(t,e,n){const c=t.slice();return c[12]=e[n],c}function s(t,e,n){const c=t.slice();return c[12]=e[n],c}function u(t,e,n){const c=t.slice();return c[12]=e[n],c}function d(t,e,n){const c=t.slice();return c[12]=e[n],c}function f(t,e,n){const c=t.slice();return c[12]=e[n],c}function p(t){let e,n,o,l;return{c(){e=(0,c.bGB)("sup"),n=(0,c.bGB)("i"),l=(0,c.DhX)(),(0,c.Ljt)(n,"class","far fa-question-circle"),(0,c.Ljt)(e,"data-toggle","tooltip"),(0,c.Ljt)(e,"title",o=t[0].description)},m(t,o){(0,c.$Tr)(t,e,o),(0,c.R3I)(e,n),(0,c.$Tr)(t,l,o)},p(t,n){1&n&&o!==(o=t[0].description)&&(0,c.Ljt)(e,"title",o)},d(t){t&&(0,c.ogt)(e),t&&(0,c.ogt)(l)}}}function g(t){let e;return{c(){e=(0,c.bGB)("span"),e.innerHTML='<i class="far fa-folder"></i>'},m(t,n){(0,c.$Tr)(t,e,n)},d(t){t&&(0,c.ogt)(e)}}}function m(t){let e;return{c(){e=(0,c.bGB)("span"),e.innerHTML='<i class="far fa-folder"></i>'},m(t,n){(0,c.$Tr)(t,e,n)},d(t){t&&(0,c.ogt)(e)}}}function h(t){let e,n="directory"===t[12].type&&m();return{c(){n&&n.c(),e=(0,c.cSb)()},m(t,o){n&&n.m(t,o),(0,c.$Tr)(t,e,o)},p(t,c){"directory"===t[12].type?n||(n=m(),n.c(),n.m(e.parentNode,e)):n&&(n.d(1),n=null)},d(t){n&&n.d(t),t&&(0,c.ogt)(e)}}}function $(t){let e;return{c(){e=(0,c.bGB)("span"),e.innerHTML='<i class="far fa-file"></i>  '},m(t,n){(0,c.$Tr)(t,e,n)},d(t){t&&(0,c.ogt)(e)}}}function b(t){let e,n="file"===t[12].type&&$();return{c(){n&&n.c(),e=(0,c.cSb)()},m(t,o){n&&n.m(t,o),(0,c.$Tr)(t,e,o)},p(t,c){"file"===t[12].type?n||(n=$(),n.c(),n.m(e.parentNode,e)):n&&(n.d(1),n=null)},d(t){n&&n.d(t),t&&(0,c.ogt)(e)}}}function y(t){let e,n,o,l,r;return{c(){e=(0,c.bGB)("button"),n=(0,c.fLW)(".. "),o=(0,c.fLW)(t[5]),(0,c.Ljt)(e,"type","button"),(0,c.Ljt)(e,"class","text-btn")},m(i,a){(0,c.$Tr)(i,e,a),(0,c.R3I)(e,n),(0,c.R3I)(e,o),l||(r=(0,c.oLt)(e,"click",t[8]),l=!0)},p(t,e){32&e&&(0,c.rTO)(o,t[5])},d(t){t&&(0,c.ogt)(e),l=!1,r()}}}function L(t){let e,n,o,l,r=t[12].name.slice(t[2].length).replace(/^\//,"")+"";function i(){return t[9](t[12])}return{c(){e=(0,c.bGB)("button"),n=(0,c.fLW)(r),(0,c.Ljt)(e,"type","button"),(0,c.Ljt)(e,"class","text-btn")},m(t,r){(0,c.$Tr)(t,e,r),(0,c.R3I)(e,n),o||(l=(0,c.oLt)(e,"click",i),o=!0)},p(e,o){t=e,12&o&&r!==(r=t[12].name.slice(t[2].length).replace(/^\//,"")+"")&&(0,c.rTO)(n,r)},d(t){t&&(0,c.ogt)(e),o=!1,l()}}}function w(t){let e,n="directory"===t[12].type&&L(t);return{c(){n&&n.c(),e=(0,c.cSb)()},m(t,o){n&&n.m(t,o),(0,c.$Tr)(t,e,o)},p(t,c){"directory"===t[12].type?n?n.p(t,c):(n=L(t),n.c(),n.m(e.parentNode,e)):n&&(n.d(1),n=null)},d(t){n&&n.d(t),t&&(0,c.ogt)(e)}}}function I(t){let e,n,o;function l(t,e){return t[1]===t[12].name?k:T}let r=l(t),i=r(t);function a(){return t[10](t[12])}return{c(){e=(0,c.bGB)("button"),i.c(),(0,c.Ljt)(e,"type","button"),(0,c.Ljt)(e,"class","text-btn")},m(t,l){(0,c.$Tr)(t,e,l),i.m(e,null),n||(o=(0,c.oLt)(e,"click",a),n=!0)},p(n,c){r===(r=l(t=n))&&i?i.p(t,c):(i.d(1),i=r(t),i&&(i.c(),i.m(e,null)))},d(t){t&&(0,c.ogt)(e),i.d(),n=!1,o()}}}function T(t){let e,n=t[12].name.slice(t[2].length).replace(/^\//,"")+"";return{c(){e=(0,c.fLW)(n)},m(t,n){(0,c.$Tr)(t,e,n)},p(t,o){12&o&&n!==(n=t[12].name.slice(t[2].length).replace(/^\//,"")+"")&&(0,c.rTO)(e,n)},d(t){t&&(0,c.ogt)(e)}}}function k(t){let e,n,o=t[12].name.slice(t[2].length).replace(/^\//,"")+"";return{c(){e=(0,c.bGB)("span"),n=(0,c.fLW)(o),(0,c.czc)(e,"font-weight","600")},m(t,o){(0,c.$Tr)(t,e,o),(0,c.R3I)(e,n)},p(t,e){12&e&&o!==(o=t[12].name.slice(t[2].length).replace(/^\//,"")+"")&&(0,c.rTO)(n,o)},d(t){t&&(0,c.ogt)(e)}}}function R(t){let e,n="file"===t[12].type&&I(t);return{c(){n&&n.c(),e=(0,c.cSb)()},m(t,o){n&&n.m(t,o),(0,c.$Tr)(t,e,o)},p(t,c){"file"===t[12].type?n?n.p(t,c):(n=I(t),n.c(),n.m(e.parentNode,e)):n&&(n.d(1),n=null)},d(t){n&&n.d(t),t&&(0,c.ogt)(e)}}}function x(t){let e,n;return e=new l.Z({}),{c(){(0,c.YCL)(e.$$.fragment)},m(t,o){(0,c.yef)(e,t,o),n=!0},i(t){n||((0,c.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,c.etI)(e.$$.fragment,t),n=!1},d(t){(0,c.vpE)(e,t)}}}function v(t){let e;return{c(){e=(0,c.bGB)("span"),e.textContent=" "},m(t,n){(0,c.$Tr)(t,e,n)},d(t){t&&(0,c.ogt)(e)}}}function B(t){let e;return{c(){e=(0,c.bGB)("span"),e.textContent=" "},m(t,n){(0,c.$Tr)(t,e,n)},d(t){t&&(0,c.ogt)(e)}}}function j(t){let e,n="directory"===t[12].type&&B();return{c(){n&&n.c(),e=(0,c.cSb)()},m(t,o){n&&n.m(t,o),(0,c.$Tr)(t,e,o)},p(t,c){"directory"===t[12].type?n||(n=B(),n.c(),n.m(e.parentNode,e)):n&&(n.d(1),n=null)},d(t){n&&n.d(t),t&&(0,c.ogt)(e)}}}function G(t){let e;function n(t,e){return t[1]===t[12].name?X:z}let o=n(t),l=o(t);return{c(){l.c(),e=(0,c.cSb)()},m(t,n){l.m(t,n),(0,c.$Tr)(t,e,n)},p(t,c){o===(o=n(t))&&l?l.p(t,c):(l.d(1),l=o(t),l&&(l.c(),l.m(e.parentNode,e)))},d(t){l.d(t),t&&(0,c.ogt)(e)}}}function z(t){let e,n,o=r(t[12].size)+"";return{c(){e=(0,c.bGB)("span"),n=(0,c.fLW)(o),(0,c.czc)(e,"white-space","nowrap")},m(t,o){(0,c.$Tr)(t,e,o),(0,c.R3I)(e,n)},p(t,e){12&e&&o!==(o=r(t[12].size)+"")&&(0,c.rTO)(n,o)},d(t){t&&(0,c.ogt)(e)}}}function X(t){let e,n,o=r(t[12].size)+"";return{c(){e=(0,c.bGB)("span"),n=(0,c.fLW)(o),(0,c.czc)(e,"white-space","nowrap"),(0,c.czc)(e,"font-weight","600")},m(t,o){(0,c.$Tr)(t,e,o),(0,c.R3I)(e,n)},p(t,e){12&e&&o!==(o=r(t[12].size)+"")&&(0,c.rTO)(n,o)},d(t){t&&(0,c.ogt)(e)}}}function Z(t){let e,n="file"===t[12].type&&G(t);return{c(){n&&n.c(),e=(0,c.cSb)()},m(t,o){n&&n.m(t,o),(0,c.$Tr)(t,e,o)},p(t,c){"file"===t[12].type?n?n.p(t,c):(n=G(t),n.c(),n.m(e.parentNode,e)):n&&(n.d(1),n=null)},d(t){n&&n.d(t),t&&(0,c.ogt)(e)}}}function D(t){let e,n,o,l,r,m,$,L,I,T,k,B,G,z,X,D,U,C,S,W,O,N,_,M,E,Y,F,H,A,P,V,q,J,K,Q=t[0].label+"",tt=t[0].description&&p(t),et=t[5]!==t[2]&&g(),nt=t[3][t[2]]||[],ct=[];for(let e=0;e<nt.length;e+=1)ct[e]=h(f(t,nt,e));let ot=t[3][t[2]]||[],lt=[];for(let e=0;e<ot.length;e+=1)lt[e]=b(d(t,ot,e));let rt=t[5]!==t[2]&&y(t),it=t[3][t[2]]||[],at=[];for(let e=0;e<it.length;e+=1)at[e]=w(u(t,it,e));let st=t[3][t[2]]||[],ut=[];for(let e=0;e<st.length;e+=1)ut[e]=R(s(t,st,e));let dt=t[4]&&x(),ft=t[5]!==t[2]&&v(),pt=t[3][t[2]]||[],gt=[];for(let e=0;e<pt.length;e+=1)gt[e]=j(a(t,pt,e));let mt=t[3][t[2]]||[],ht=[];for(let e=0;e<mt.length;e+=1)ht[e]=Z(i(t,mt,e));return{c(){e=(0,c.bGB)("div"),n=(0,c.bGB)("div"),o=(0,c.fLW)(Q),l=(0,c.DhX)(),tt&&tt.c(),r=(0,c.fLW)(":"),m=(0,c.DhX)(),$=(0,c.bGB)("div"),L=(0,c.bGB)("div"),I=(0,c.bGB)("div"),et&&et.c(),T=(0,c.DhX)(),k=(0,c.bGB)("span"),k.innerHTML='<i class="far fa-folder-open"></i>',B=(0,c.DhX)();for(let t=0;t<ct.length;t+=1)ct[t].c();G=(0,c.DhX)();for(let t=0;t<lt.length;t+=1)lt[t].c();z=(0,c.DhX)(),X=(0,c.bGB)("div"),rt&&rt.c(),D=(0,c.DhX)(),U=(0,c.bGB)("button"),C=(0,c.fLW)(". "),S=(0,c.fLW)(t[2]),W=(0,c.DhX)();for(let t=0;t<at.length;t+=1)at[t].c();O=(0,c.DhX)();for(let t=0;t<ut.length;t+=1)ut[t].c();N=(0,c.DhX)(),dt&&dt.c(),_=(0,c.DhX)(),M=(0,c.bGB)("div"),ft&&ft.c(),E=(0,c.DhX)(),Y=(0,c.bGB)("span"),Y.textContent=" ",F=(0,c.DhX)();for(let t=0;t<gt.length;t+=1)gt[t].c();H=(0,c.DhX)();for(let t=0;t<ht.length;t+=1)ht[t].c();A=(0,c.DhX)(),P=(0,c.bGB)("input"),(0,c.Ljt)(n,"class","col-lg-3 bold text-lg-right my-auto"),(0,c.czc)(I,"display","flex"),(0,c.czc)(I,"flex-direction","column"),(0,c.czc)(I,"align-items","center"),(0,c.czc)(I,"padding-right","5px"),(0,c.Ljt)(U,"type","button"),(0,c.Ljt)(U,"class","text-btn"),(0,c.czc)(X,"display","flex"),(0,c.czc)(X,"flex-direction","column"),(0,c.czc)(X,"align-items","start"),(0,c.czc)(X,"white-space","nowrap"),(0,c.czc)(X,"overflow-x","auto"),(0,c.czc)(X,"flex","1 1 auto"),(0,c.czc)(M,"display","flex"),(0,c.czc)(M,"flex-direction","column"),(0,c.czc)(M,"align-items","start"),(0,c.czc)(M,"padding-left","5px"),(0,c.czc)(L,"display","flex"),(0,c.czc)(L,"flex-direction","row"),(0,c.czc)(L,"max-height","500px"),(0,c.czc)(L,"overflow-x","hidden"),(0,c.czc)(L,"overflow-y","auto"),(0,c.Ljt)(L,"class","pl-0"),(0,c.Ljt)(P,"type","text"),(0,c.czc)(P,"display","none"),(0,c.Ljt)(P,"name",V=t[0].name),(0,c.Ljt)($,"class","col-lg-6 pt-2 pt-lg-0"),(0,c.Ljt)(e,"class","row px-4 px-lg-3 pb-4")},m(i,a){(0,c.$Tr)(i,e,a),(0,c.R3I)(e,n),(0,c.R3I)(n,o),(0,c.R3I)(n,l),tt&&tt.m(n,null),(0,c.R3I)(n,r),(0,c.R3I)(e,m),(0,c.R3I)(e,$),(0,c.R3I)($,L),(0,c.R3I)(L,I),et&&et.m(I,null),(0,c.R3I)(I,T),(0,c.R3I)(I,k),(0,c.R3I)(I,B);for(let t=0;t<ct.length;t+=1)ct[t].m(I,null);(0,c.R3I)(I,G);for(let t=0;t<lt.length;t+=1)lt[t].m(I,null);(0,c.R3I)(L,z),(0,c.R3I)(L,X),rt&&rt.m(X,null),(0,c.R3I)(X,D),(0,c.R3I)(X,U),(0,c.R3I)(U,C),(0,c.R3I)(U,S),(0,c.R3I)(X,W);for(let t=0;t<at.length;t+=1)at[t].m(X,null);(0,c.R3I)(X,O);for(let t=0;t<ut.length;t+=1)ut[t].m(X,null);(0,c.R3I)(X,N),dt&&dt.m(X,null),(0,c.R3I)(L,_),(0,c.R3I)(L,M),ft&&ft.m(M,null),(0,c.R3I)(M,E),(0,c.R3I)(M,Y),(0,c.R3I)(M,F);for(let t=0;t<gt.length;t+=1)gt[t].m(M,null);(0,c.R3I)(M,H);for(let t=0;t<ht.length;t+=1)ht[t].m(M,null);(0,c.R3I)($,A),(0,c.R3I)($,P),(0,c.BmG)(P,t[0].value),q=!0,J||(K=(0,c.oLt)(P,"input",t[11]),J=!0)},p(t,[e]){if((!q||1&e)&&Q!==(Q=t[0].label+"")&&(0,c.rTO)(o,Q),t[0].description?tt?tt.p(t,e):(tt=p(t),tt.c(),tt.m(n,r)):tt&&(tt.d(1),tt=null),t[5]!==t[2]?et||(et=g(),et.c(),et.m(I,T)):et&&(et.d(1),et=null),12&e){let n;for(nt=t[3][t[2]]||[],n=0;n<nt.length;n+=1){const c=f(t,nt,n);ct[n]?ct[n].p(c,e):(ct[n]=h(c),ct[n].c(),ct[n].m(I,G))}for(;n<ct.length;n+=1)ct[n].d(1);ct.length=nt.length}if(12&e){let n;for(ot=t[3][t[2]]||[],n=0;n<ot.length;n+=1){const c=d(t,ot,n);lt[n]?lt[n].p(c,e):(lt[n]=b(c),lt[n].c(),lt[n].m(I,null))}for(;n<lt.length;n+=1)lt[n].d(1);lt.length=ot.length}if(t[5]!==t[2]?rt?rt.p(t,e):(rt=y(t),rt.c(),rt.m(X,D)):rt&&(rt.d(1),rt=null),(!q||4&e)&&(0,c.rTO)(S,t[2]),12&e){let n;for(it=t[3][t[2]]||[],n=0;n<it.length;n+=1){const c=u(t,it,n);at[n]?at[n].p(c,e):(at[n]=w(c),at[n].c(),at[n].m(X,O))}for(;n<at.length;n+=1)at[n].d(1);at.length=it.length}if(14&e){let n;for(st=t[3][t[2]]||[],n=0;n<st.length;n+=1){const c=s(t,st,n);ut[n]?ut[n].p(c,e):(ut[n]=R(c),ut[n].c(),ut[n].m(X,N))}for(;n<ut.length;n+=1)ut[n].d(1);ut.length=st.length}if(t[4]?dt?16&e&&(0,c.Ui)(dt,1):(dt=x(),dt.c(),(0,c.Ui)(dt,1),dt.m(X,null)):dt&&((0,c.dvw)(),(0,c.etI)(dt,1,1,(()=>{dt=null})),(0,c.gbL)()),t[5]!==t[2]?ft||(ft=v(),ft.c(),ft.m(M,E)):ft&&(ft.d(1),ft=null),12&e){let n;for(pt=t[3][t[2]]||[],n=0;n<pt.length;n+=1){const c=a(t,pt,n);gt[n]?gt[n].p(c,e):(gt[n]=j(c),gt[n].c(),gt[n].m(M,H))}for(;n<gt.length;n+=1)gt[n].d(1);gt.length=pt.length}if(14&e){let n;for(mt=t[3][t[2]]||[],n=0;n<mt.length;n+=1){const c=i(t,mt,n);ht[n]?ht[n].p(c,e):(ht[n]=Z(c),ht[n].c(),ht[n].m(M,null))}for(;n<ht.length;n+=1)ht[n].d(1);ht.length=mt.length}(!q||1&e&&V!==(V=t[0].name))&&(0,c.Ljt)(P,"name",V),1&e&&P.value!==t[0].value&&(0,c.BmG)(P,t[0].value)},i(t){q||((0,c.Ui)(dt),q=!0)},o(t){(0,c.etI)(dt),q=!1},d(t){t&&(0,c.ogt)(e),tt&&tt.d(),et&&et.d(),(0,c.RMB)(ct,t),(0,c.RMB)(lt,t),rt&&rt.d(),(0,c.RMB)(at,t),(0,c.RMB)(ut,t),dt&&dt.d(),ft&&ft.d(),(0,c.RMB)(gt,t),(0,c.RMB)(ht,t),J=!1,K()}}}function U(t,e,n){let l;(0,c.FIv)(t,o.Z,(t=>n(7,l=t)));let{args:r}=e,{backend:i="StorageFileField"}=e,a=r.value||r.default||"",s=!1,u="",d="",f={};return t.$$set=t=>{"args"in t&&n(0,r=t.args),"backend"in t&&n(6,i=t.backend)},t.$$.update=()=>{3&t.$$.dirty&&n(0,r.value=`${r.storage}${a}#${a.split("/").slice(-1)[0]}`,r),4&t.$$.dirty&&n(5,d=u.split("/").slice(0,-1).join("/")),205&t.$$.dirty&&(u in f||(n(4,s=!0),async function(t){let e;return"auth"===t.state&&(e=await t.keycloak.getValidToken()),null!=e?{Authorization:`Bearer ${e}`}:{}}(l).then((async t=>{try{const e=await fetch(`${i}/ls/${r.storage}${u}`,{headers:t});n(3,f[u]=await e.json(),f),n(4,s=!1)}catch(t){n(3,f[u]=[],f),n(4,s=!1)}}))))},[r,a,u,f,s,d,i,l,()=>{n(2,u=d)},t=>{n(2,u=t.name)},t=>{n(1,a=t.name)},function(){r.value=this.value,n(0,r),n(1,a)}]}class C extends c.f_C{constructor(t){super(),(0,c.S1n)(this,t,U,D,c.N8,{args:0,backend:6})}}var S=C,W=n(3798);function O(t){let e,n,o,l,r,i,a,s;const u=[E,M,_],d=[];function f(t,e){return"init"===t[1].state?0:"error"===t[1].state?1:2}return o=f(t),l=d[o]=u[o](t),{c(){e=(0,c.bGB)("div"),n=(0,c.bGB)("div"),l.c(),r=(0,c.DhX)(),i=(0,c.bGB)("input"),(0,c.Ljt)(n,"class","row px-4 px-lg-3 pb-4 justify-content-center"),(0,c.Ljt)(e,"class","pt-3"),(0,c.Ljt)(i,"type","text"),(0,c.czc)(i,"display","none"),(0,c.Ljt)(i,"name",a=t[0].name),i.value=""},m(t,l){(0,c.$Tr)(t,e,l),(0,c.R3I)(e,n),d[o].m(n,null),(0,c.$Tr)(t,r,l),(0,c.$Tr)(t,i,l),s=!0},p(t,e){let r=o;o=f(t),o===r?d[o].p(t,e):((0,c.dvw)(),(0,c.etI)(d[r],1,1,(()=>{d[r]=null})),(0,c.gbL)(),l=d[o],l?l.p(t,e):(l=d[o]=u[o](t),l.c()),(0,c.Ui)(l,1),l.m(n,null)),(!s||1&e&&a!==(a=t[0].name))&&(0,c.Ljt)(i,"name",a)},i(t){s||((0,c.Ui)(l),s=!0)},o(t){(0,c.etI)(l),s=!1},d(t){t&&(0,c.ogt)(e),d[o].d(),t&&(0,c.ogt)(r),t&&(0,c.ogt)(i)}}}function N(t){let e,n,o,l;return e=new W.default({props:{$$slots:{default:[Y]},$$scope:{ctx:t}}}),o=new S({props:{backend:"locate",args:{...t[0],label:"Browse Your Uploads & Integrations",storage:"user://"}}}),{c(){(0,c.YCL)(e.$$.fragment),n=(0,c.DhX)(),(0,c.YCL)(o.$$.fragment)},m(t,r){(0,c.yef)(e,t,r),(0,c.$Tr)(t,n,r),(0,c.yef)(o,t,r),l=!0},p(t,n){const c={};18&n&&(c.$$scope={dirty:n,ctx:t}),e.$set(c);const l={};1&n&&(l.args={...t[0],label:"Browse Your Uploads & Integrations",storage:"user://"}),o.$set(l)},i(t){l||((0,c.Ui)(e.$$.fragment,t),(0,c.Ui)(o.$$.fragment,t),l=!0)},o(t){(0,c.etI)(e.$$.fragment,t),(0,c.etI)(o.$$.fragment,t),l=!1},d(t){(0,c.vpE)(e,t),t&&(0,c.ogt)(n),(0,c.vpE)(o,t)}}}function _(t){let e,n,o,l,r;return{c(){e=(0,c.bGB)("div"),n=(0,c.bGB)("button"),n.textContent="Login",o=(0,c.fLW)(" to access uploads and integration storage."),(0,c.Ljt)(n,"type","button"),(0,c.Ljt)(n,"class","text-btn"),(0,c.Ljt)(e,"class","col col-lg-9 px-lg-3 my-auto px-4 text-center alert alert-info")},m(i,a){(0,c.$Tr)(i,e,a),(0,c.R3I)(e,n),(0,c.R3I)(e,o),l||(r=(0,c.oLt)(n,"click",t[3]),l=!0)},p:c.ZTd,i:c.ZTd,o:c.ZTd,d(t){t&&(0,c.ogt)(e),l=!1,r()}}}function M(t){let e;return{c(){e=(0,c.bGB)("div"),e.textContent="Unable to access authentication at this time, please try again later.",(0,c.Ljt)(e,"class","col col-lg-9 px-lg-3 my-auto px-4 text-center alert alert-warning")},m(t,n){(0,c.$Tr)(t,e,n)},p:c.ZTd,i:c.ZTd,o:c.ZTd,d(t){t&&(0,c.ogt)(e)}}}function E(t){let e,n;return e=new l.Z({}),{c(){(0,c.YCL)(e.$$.fragment)},m(t,o){(0,c.yef)(e,t,o),n=!0},p:c.ZTd,i(t){n||((0,c.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,c.etI)(e.$$.fragment,t),n=!1},d(t){(0,c.vpE)(e,t)}}}function Y(t){let e,n,o,l,r,i,a,s,u=t[1].keycloak.tokenParsed.email+"";return{c(){e=(0,c.bGB)("div"),n=(0,c.fLW)("Logged in as "),o=(0,c.fLW)(u),l=(0,c.fLW)(", "),r=(0,c.bGB)("button"),r.textContent="click here",i=(0,c.fLW)(" to logout."),(0,c.Ljt)(r,"type","button"),(0,c.Ljt)(r,"class","text-btn"),(0,c.Ljt)(e,"class","text-center")},m(u,d){(0,c.$Tr)(u,e,d),(0,c.R3I)(e,n),(0,c.R3I)(e,o),(0,c.R3I)(e,l),(0,c.R3I)(e,r),(0,c.R3I)(e,i),a||(s=(0,c.oLt)(r,"click",t[2]),a=!0)},p(t,e){2&e&&u!==(u=t[1].keycloak.tokenParsed.email+"")&&(0,c.rTO)(o,u)},d(t){t&&(0,c.ogt)(e),a=!1,s()}}}function F(t){let e,n,o,l;const r=[N,O],i=[];function a(t,e){return"auth"===t[1].state?0:1}return e=a(t),n=i[e]=r[e](t),{c(){n.c(),o=(0,c.cSb)()},m(t,n){i[e].m(t,n),(0,c.$Tr)(t,o,n),l=!0},p(t,[l]){let s=e;e=a(t),e===s?i[e].p(t,l):((0,c.dvw)(),(0,c.etI)(i[s],1,1,(()=>{i[s]=null})),(0,c.gbL)(),n=i[e],n?n.p(t,l):(n=i[e]=r[e](t),n.c()),(0,c.Ui)(n,1),n.m(o.parentNode,o))},i(t){l||((0,c.Ui)(n),l=!0)},o(t){(0,c.etI)(n),l=!1},d(t){i[e].d(t),t&&(0,c.ogt)(o)}}}function H(t,e,n){let l;(0,c.FIv)(t,o.Z,(t=>n(1,l=t)));let{args:r}=e;return t.$$set=t=>{"args"in t&&n(0,r=t.args)},[r,l,()=>l.keycloak.logout(),()=>l.keycloak.login()]}class A extends c.f_C{constructor(t){super(),(0,c.S1n)(this,t,H,F,c.N8,{args:0})}}var P=A},7909:function(t,e,n){var c=n(4683),o=n(9666);const l=function(){const{subscribe:t,set:e}=(0,c.fZ)({state:window._config.EXTRAS.includes("catalog-integration")?"init":"guest",keycloak:{}});return window._config.EXTRAS.includes("catalog-integration")&&void 0!==window._config.keycloak&&n.e(671).then(n.bind(n,4671)).then((async({default:t})=>{const n=new t(window._config.keycloak.params),c=n.logout;Object.assign(n,{getValidToken:async()=>{try{await n.updateToken(30)}catch(t){console.error(t),e({state:"guest",keycloak:n})}return n.token},logout:()=>{c(),e({state:"guest",keycloak:n})}});const l=await n.init({...window._config.keycloak.init,redirectUri:window.location.href+(window.location.href.includes("#")?"":"#")+(window.location.href.includes("?")?"":"?")});e({state:l?"auth":"guest",keycloak:n}),o.Z.update((t=>{const e={...t.params};return"code"in e&&delete e.code,"session_state"in e&&delete e.session_state,"state"in e&&delete e.state,{...t,params:e}}))})).catch((t=>{console.error(t),e({state:"error",keycloak:keycloak})})),{subscribe:t}}();l.subscribe((t=>{"auth"===t.state&&null===document.cookie.match(/^(.*;)?\s*authorization\s*=\s*[^;]+(.*)?$/)&&(document.cookie=`authorization=${t.keycloak.token}; expires=${new Date(1e3*t.keycloak.tokenParsed.exp).toUTCString()}; secure`)})),e.Z=l},9666:function(t,e,n){var c=n(4683);function o(t){const e=t.indexOf("?");if(-1===e)return{path:t,params:{}};{const[n,c]=[t.slice(0,e),t.slice(e+1)];return{path:n,params:function(t){return""===t?{}:t.split("&").map((t=>t.split("=").map(decodeURIComponent))).reduce(((t,[e,n])=>({...t,[e]:n})),{})}(c)}}}function l(){return(window.location.hash||"#").slice(1)}const r=function(){const{path:t,params:e,server:n}={...o(l()),server:o(`${window.location.pathname}${window.location.search}`)},{subscribe:r,update:i,set:a}=(0,c.fZ)({path:t,params:e,server:n});let s=t;return r((({path:t,params:e,server:n})=>{const c=function({path:t,params:e}){const n=function(t){return Object.keys(t).filter((e=>void 0!==t[e]&&""!==t[e])).map((e=>[e,t[e]].map(encodeURIComponent).join("="))).join("&")}(e);return""===n?t:`${t}?${n}`}({path:t,params:e});if(t!==s)window.location.hash=c,s=t;else{const t=`${window.location.origin}${window.location.pathname}${window.location.search}`;history.replaceState(void 0,void 0,""!==c?`${t}#${c}`:t)}})),window.addEventListener("hashchange",(()=>a({...o(l()),initServer:n}))),{subscribe:r,update:i,set:a}}();e.Z=r},4683:function(t,e,n){n.d(e,{fZ:function(){return l}});var c=n(8826);const o=[];function l(t,e=c.ZTd){let n;const l=new Set;function r(e){if((0,c.N8)(t,e)&&(t=e,n)){const e=!o.length;for(const e of l)e[1](),o.push(e,t);if(e){for(let t=0;t<o.length;t+=2)o[t][0](o[t+1]);o.length=0}}}return{set:r,update:function(e){r(e(t))},subscribe:function(o,i=c.ZTd){const a=[o,i];return l.add(a),1===l.size&&(n=e(r)||c.ZTd),o(t),()=>{l.delete(a),0===l.size&&(n(),n=null)}}}}}}]);