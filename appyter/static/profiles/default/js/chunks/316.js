"use strict";(self.webpackChunkappyter_js=self.webpackChunkappyter_js||[]).push([[316],{6523:function(t,e,n){n.r(e),n.d(e,{default:function(){return g}});var r=n(8826),a=n(9980),o=n(8486),s=n(837),i=n(5037),c=n(7919),u=n(6167);s.Z.registerLanguage("python",i.Z),s.Z.registerLanguage("markdown",c.Z),s.Z.registerLanguage("bash",u.Z);const l={};var d=new a({html:!0,highlight:function(t,e){if(e&&s.Z.getLanguage(e))try{return s.Z.highlight(t,{language:e}).value}catch(t){}return""}}).use(o.Z,{permalink:o.Z.permalink.linkInsideHeader({symbol:"¶",placement:"after"}),slugify:t=>function(t){let e=t,n=1;for(;Object.prototype.hasOwnProperty.call(l,e);)e=`${t}-${n}`,n+=1;return l[e]=!0,e}(t.toLowerCase().replace(/[^A-Za-z0-9_-]/g,"-").replace(/^-+/g,"").replace(/-+$/g,""))});function p(t){let e,n;return{c(){e=new r.FWw,n=(0,r.cSb)(),e.a=n},m(a,o){e.m(t[0],a,o),(0,r.$Tr)(a,n,o)},p(t,[n]){1&n&&e.p(t[0])},i:r.ZTd,o:r.ZTd,d(t){t&&(0,r.ogt)(n),t&&e.d()}}}function $(t,e,n){let r,{data:a}=e;return t.$$set=t=>{"data"in t&&n(1,a=t.data)},t.$$.update=()=>{2&t.$$.dirty&&n(0,r=d.render(a))},[r,a]}class f extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,$,p,r.N8,{data:1})}}var g=f},2316:function(t,e,n){n.r(e),n.d(e,{default:function(){return ye}});var r=n(8826),a=n(966);function o(t){let e,n,a;const o=t[2].default,s=(0,r.nuO)(o,t,t[1],null);return{c(){e=(0,r.bGB)("div"),s&&s.c(),(0,r.Ljt)(e,"class",n="cell border-box-sizing "+t[0]+"_cell rendered")},m(t,n){(0,r.$Tr)(t,e,n),s&&s.m(e,null),a=!0},p(t,[i]){s&&s.p&&(!a||2&i)&&(0,r.kmG)(s,o,t,t[1],a?(0,r.u2N)(o,t[1],i,null):(0,r.VOJ)(t[1]),null),(!a||1&i&&n!==(n="cell border-box-sizing "+t[0]+"_cell rendered"))&&(0,r.Ljt)(e,"class",n)},i(t){a||((0,r.Ui)(s,t),a=!0)},o(t){(0,r.etI)(s,t),a=!1},d(t){t&&(0,r.ogt)(e),s&&s.d(t)}}}function s(t,e,n){let{$$slots:r={},$$scope:a}=e,{type:o}=e;return t.$$set=t=>{"type"in t&&n(0,o=t.type),"$$scope"in t&&n(1,a=t.$$scope)},[o,a,r]}class i extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,s,o,r.N8,{type:0})}}var c=i;function u(t){let e,n;const a=t[1].default,o=(0,r.nuO)(a,t,t[0],null);return{c(){e=(0,r.bGB)("div"),o&&o.c(),(0,r.Ljt)(e,"class","input")},m(t,a){(0,r.$Tr)(t,e,a),o&&o.m(e,null),n=!0},p(t,[e]){o&&o.p&&(!n||1&e)&&(0,r.kmG)(o,a,t,t[0],n?(0,r.u2N)(a,t[0],e,null):(0,r.VOJ)(t[0]),null)},i(t){n||((0,r.Ui)(o,t),n=!0)},o(t){(0,r.etI)(o,t),n=!1},d(t){t&&(0,r.ogt)(e),o&&o.d(t)}}}function l(t,e,n){let{$$slots:r={},$$scope:a}=e;return t.$$set=t=>{"$$scope"in t&&n(0,a=t.$$scope)},[a,r]}class d extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,l,u,r.N8,{})}}var p=d;function $(t){let e;function n(t,e){return t[4]?y:t[5]?m:t[3]?g:f}let a=n(t),o=a(t);return{c(){o.c(),e=(0,r.cSb)()},m(t,n){o.m(t,n),(0,r.$Tr)(t,e,n)},p(t,r){a===(a=n(t))&&o?o.p(t,r):(o.d(1),o=a(t),o&&(o.c(),o.m(e.parentNode,e)))},d(t){o.d(t),t&&(0,r.ogt)(e)}}}function f(t){let e;return{c(){e=(0,r.fLW)("In [ ]")},m(t,n){(0,r.$Tr)(t,e,n)},p:r.ZTd,d(t){t&&(0,r.ogt)(e)}}}function g(t){let e,n,a;return{c(){e=(0,r.fLW)("In ["),n=(0,r.fLW)(t[3]),a=(0,r.fLW)("]")},m(t,o){(0,r.$Tr)(t,e,o),(0,r.$Tr)(t,n,o),(0,r.$Tr)(t,a,o)},p(t,e){8&e&&(0,r.rTO)(n,t[3])},d(t){t&&(0,r.ogt)(e),t&&(0,r.ogt)(n),t&&(0,r.ogt)(a)}}}function m(t){let e;return{c(){e=(0,r.bGB)("b"),e.textContent="In [E]:",(0,r.czc)(e,"color","red")},m(t,n){(0,r.$Tr)(t,e,n)},p:r.ZTd,d(t){t&&(0,r.ogt)(e)}}}function y(t){let e;return{c(){e=(0,r.fLW)("In [*]")},m(t,n){(0,r.$Tr)(t,e,n)},p:r.ZTd,d(t){t&&(0,r.ogt)(e)}}}function _(t){let e,n,a,o,s,i,c,u="code"===t[2]&&$(t);return{c(){e=(0,r.bGB)("div"),u&&u.c(),n=(0,r.DhX)(),a=(0,r.bGB)("a"),o=(0,r.fLW)("¶"),(0,r.Ljt)(a,"class","prompt-anchor"),(0,r.Ljt)(a,"href",s="#"+t[1]+"-prompt-"+t[0]),(0,r.Ljt)(e,"id",i=t[1]+"-prompt-"+t[0]),(0,r.Ljt)(e,"class",c="prompt "+t[1]+"_prompt")},m(t,s){(0,r.$Tr)(t,e,s),u&&u.m(e,null),(0,r.R3I)(e,n),(0,r.R3I)(e,a),(0,r.R3I)(a,o)},p(t,[o]){"code"===t[2]?u?u.p(t,o):(u=$(t),u.c(),u.m(e,n)):u&&(u.d(1),u=null),3&o&&s!==(s="#"+t[1]+"-prompt-"+t[0])&&(0,r.Ljt)(a,"href",s),3&o&&i!==(i=t[1]+"-prompt-"+t[0])&&(0,r.Ljt)(e,"id",i),2&o&&c!==(c="prompt "+t[1]+"_prompt")&&(0,r.Ljt)(e,"class",c)},i:r.ZTd,o:r.ZTd,d(t){t&&(0,r.ogt)(e),u&&u.d()}}}function v(t,e,n){let{index:r}=e,{prompt_type:a}=e,{cell_type:o}=e,{counter:s}=e,{running:i}=e,{error:c}=e;return t.$$set=t=>{"index"in t&&n(0,r=t.index),"prompt_type"in t&&n(1,a=t.prompt_type),"cell_type"in t&&n(2,o=t.cell_type),"counter"in t&&n(3,s=t.counter),"running"in t&&n(4,i=t.running),"error"in t&&n(5,c=t.error)},[r,a,o,s,i,c]}class h extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,v,_,r.N8,{index:0,prompt_type:1,cell_type:2,counter:3,running:4,error:5})}}var L=h,b=n(6523);function x(t){let e,n,a,o,s;return o=new b.default({props:{data:"\n```"+t[0]+"\n"+t[1]+"\n```\n"}}),{c(){e=(0,r.bGB)("div"),n=(0,r.bGB)("div"),a=(0,r.bGB)("div"),(0,r.YCL)(o.$$.fragment),(0,r.Ljt)(a,"class","highlight hl-ipython3"),(0,r.Ljt)(n,"class","input_area"),(0,r.Ljt)(e,"class","inner_cell")},m(t,i){(0,r.$Tr)(t,e,i),(0,r.R3I)(e,n),(0,r.R3I)(n,a),(0,r.yef)(o,a,null),s=!0},p(t,[e]){const n={};3&e&&(n.data="\n```"+t[0]+"\n"+t[1]+"\n```\n"),o.$set(n)},i(t){s||((0,r.Ui)(o.$$.fragment,t),s=!0)},o(t){(0,r.etI)(o.$$.fragment,t),s=!1},d(t){t&&(0,r.ogt)(e),(0,r.vpE)(o)}}}function w(t,e,n){let{language:r}=e,{source:a}=e;return t.$$set=t=>{"language"in t&&n(0,r=t.language),"source"in t&&n(1,a=t.source)},[r,a]}class I extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,w,x,r.N8,{language:0,source:1})}}var T=I,U=n(9150);function j({nb:t,type:e,error:n}){if(console.error(`[${e}]`,n),-1!==window._config.EXTRAS.indexOf("catalog-integration"))if(void 0!==window._config.report_error)try{window._config.report_error({appyter:((window._config.nb||{}).metadata||{}).appyter||null,url:window.location.href,type:e,error:n})}catch(t){console.error(t)}else console.warn("[catalog-integration:report_error]: attempting deprecated requirejs resolution"),(0,U.Z)(window,"report_error").then((t=>{console.warn("[catalog-integration:report_error]: deprecated report_error"),t({appyter:((window._config.nb||{}).metadata||{}).appyter||null,url:window.location.href,type:e,error:n})})).catch((t=>{}))}function C(t){let e;return{c(){e=(0,r.bGB)("div"),(0,r.Ljt)(e,"class",t[0])},m(n,a){(0,r.$Tr)(n,e,a),e.innerHTML=t[1],t[3](e)},p(t,[n]){2&n&&(e.innerHTML=t[1]),1&n&&(0,r.Ljt)(e,"class",t[0])},i:r.ZTd,o:r.ZTd,d(n){n&&(0,r.ogt)(e),t[3](null)}}}function G(t,e,n){let a,{classes:o=""}=e,{data:s=""}=e,i={};return t.$$set=t=>{"classes"in t&&n(0,o=t.classes),"data"in t&&n(1,s=t.data)},t.$$.update=()=>{4&t.$$.dirty&&a&&a.querySelectorAll("script").forEach((t=>{"application/json"!==t.type&&function(t){if(void 0===i[t]){i[t]=!0;try{new Function(t)()}catch(t){j({type:"javascript-cell",error:t.toString()})}}}(t.innerHTML)}))},[o,s,a,function(t){r.VnY[t?"unshift":"push"]((()=>{a=t,n(2,a)}))}]}class S extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,G,C,r.N8,{classes:0,data:1})}}var N=S;function B(t,e=""){return Array.isArray(t)?t.join(e):t}function E(t){let e,n;return e=new N({props:{classes:"output_javascript",data:"<script>"+B(t[0])+"<\/script>"}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,[n]){const r={};1&n&&(r.data="<script>"+B(t[0])+"<\/script>"),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}function Z(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class Y extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,Z,E,r.N8,{data:0})}}var k=Y;function R(t){let e,n,a;return{c(){e=(0,r.bGB)("div"),n=(0,r.bGB)("img"),(0,r.Ljt)(n,"class","img-fluid"),(0,r.Ljt)(n,"alt","Output figure"),(0,r.Jn4)(n.src,a="data:img/png;base64,"+B(t[0]))||(0,r.Ljt)(n,"src",a),(0,r.Ljt)(e,"class","output_png")},m(t,a){(0,r.$Tr)(t,e,a),(0,r.R3I)(e,n)},p(t,[e]){1&e&&!(0,r.Jn4)(n.src,a="data:img/png;base64,"+B(t[0]))&&(0,r.Ljt)(n,"src",a)},i:r.ZTd,o:r.ZTd,d(t){t&&(0,r.ogt)(e)}}}function D(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class O extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,D,R,r.N8,{data:0})}}var H=O;function X(t){let e,n;return e=new N({props:{classes:"output_svg",data:B(t[0])}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,[n]){const r={};1&n&&(r.data=B(t[0])),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}function M(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class W extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,M,X,r.N8,{data:0})}}var A=W;function V(t){let e,n;return e=new N({props:{classes:"output_html rendered_html",data:B(t[0])}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,[n]){const r={};1&n&&(r.data=B(t[0])),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}function J(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class z extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,J,V,r.N8,{data:0})}}var q=z;function F(t){let e,n,a;return n=new b.default({props:{data:B(t[0])}}),{c(){e=(0,r.bGB)("div"),(0,r.YCL)(n.$$.fragment),(0,r.Ljt)(e,"class","output_markdown")},m(t,o){(0,r.$Tr)(t,e,o),(0,r.yef)(n,e,null),a=!0},p(t,[e]){const r={};1&e&&(r.data=B(t[0])),n.$set(r)},i(t){a||((0,r.Ui)(n.$$.fragment,t),a=!0)},o(t){(0,r.etI)(n.$$.fragment,t),a=!1},d(t){t&&(0,r.ogt)(e),(0,r.vpE)(n)}}}function P(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class Q extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,P,F,r.N8,{data:0})}}var K=Q,tt=n(4431),et=n.n(tt);function nt(t){let e;return{c(){e=(0,r.bGB)("pre")},m(n,a){(0,r.$Tr)(n,e,a),e.innerHTML=t[0]},p(t,[n]){1&n&&(e.innerHTML=t[0])},i:r.ZTd,o:r.ZTd,d(t){t&&(0,r.ogt)(e)}}}function rt(t,e,n){let r,{data:a}=e;const o=new(et());return t.$$set=t=>{"data"in t&&n(1,a=t.data)},t.$$.update=()=>{2&t.$$.dirty&&n(0,r=o.ansi_to_html(a))},[r,a]}class at extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,rt,nt,r.N8,{data:1})}}var ot=at;function st(t){let e,n,a;return n=new ot({props:{data:t[0]}}),{c(){e=(0,r.bGB)("div"),(0,r.YCL)(n.$$.fragment),(0,r.Ljt)(e,"class","output_text")},m(t,o){(0,r.$Tr)(t,e,o),(0,r.yef)(n,e,null),a=!0},p(t,e){const r={};1&e&&(r.data=t[0]),n.$set(r)},i(t){a||((0,r.Ui)(n.$$.fragment,t),a=!0)},o(t){(0,r.etI)(n.$$.fragment,t),a=!1},d(t){t&&(0,r.ogt)(e),(0,r.vpE)(n)}}}function it(t){let e,n,a=t[0]&&'""'!==t[0]&&"''"!==t[0]&&st(t);return{c(){a&&a.c(),e=(0,r.cSb)()},m(t,o){a&&a.m(t,o),(0,r.$Tr)(t,e,o),n=!0},p(t,[n]){t[0]&&'""'!==t[0]&&"''"!==t[0]?a?(a.p(t,n),1&n&&(0,r.Ui)(a,1)):(a=st(t),a.c(),(0,r.Ui)(a,1),a.m(e.parentNode,e)):a&&((0,r.dvw)(),(0,r.etI)(a,1,1,(()=>{a=null})),(0,r.gbL)())},i(t){n||((0,r.Ui)(a),n=!0)},o(t){(0,r.etI)(a),n=!1},d(t){a&&a.d(t),t&&(0,r.ogt)(e)}}}function ct(t,e,n){let r,{data:a}=e;return t.$$set=t=>{"data"in t&&n(1,a=t.data)},t.$$.update=()=>{2&t.$$.dirty&&n(0,r=B(a))},[r,a]}class ut extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,ct,it,r.N8,{data:1})}}const lt={"image/svg+xml":A,"image/png":H,"text/html":q,"application/javascript":k,"text/markdown":K,"text/plain":ut},dt={"application/vnd.bokehjs_load.v0+json":!0,"application/vnd.bokehjs_exec.v0+json":!0};function pt(t){let e,n,a,o=t[2].length>0&&window._config.DEBUG&&$t(t),s=t[1]&&ft(t);return{c(){e=(0,r.bGB)("div"),o&&o.c(),n=(0,r.DhX)(),s&&s.c(),(0,r.Ljt)(e,"class","output_display_data")},m(t,i){(0,r.$Tr)(t,e,i),o&&o.m(e,null),(0,r.R3I)(e,n),s&&s.m(e,null),a=!0},p(t,a){t[2].length>0&&window._config.DEBUG?o?o.p(t,a):(o=$t(t),o.c(),o.m(e,n)):o&&(o.d(1),o=null),t[1]?s?(s.p(t,a),2&a&&(0,r.Ui)(s,1)):(s=ft(t),s.c(),(0,r.Ui)(s,1),s.m(e,null)):s&&((0,r.dvw)(),(0,r.etI)(s,1,1,(()=>{s=null})),(0,r.gbL)())},i(t){a||((0,r.Ui)(s),a=!0)},o(t){(0,r.etI)(s),a=!1},d(t){t&&(0,r.ogt)(e),o&&o.d(),s&&s.d()}}}function $t(t){let e,n,a,o;return{c(){e=(0,r.bGB)("div"),n=(0,r.bGB)("p"),n.innerHTML='Unhandled output_mimetype renderer. This message only appears in development, if there is a rendering issue, please report this on <a href="https://github.com/MaayanLab/appyter/issues">Appyter Issues</a> with this information:',a=(0,r.DhX)(),o=(0,r.bGB)("code"),o.textContent=`${t[3]()}`,(0,r.Ljt)(e,"class","alert"),(0,r.VHj)(e,"alert-danger",!t[1]),(0,r.VHj)(e,"alert-warning",t[1])},m(t,s){(0,r.$Tr)(t,e,s),(0,r.R3I)(e,n),(0,r.R3I)(e,a),(0,r.R3I)(e,o)},p(t,n){2&n&&(0,r.VHj)(e,"alert-danger",!t[1]),2&n&&(0,r.VHj)(e,"alert-warning",t[1])},d(t){t&&(0,r.ogt)(e)}}}function ft(t){let e,n,a;var o=lt[t[1]];function s(t){return{props:{data:t[0].data[t[1]]}}}return o&&(e=new o(s(t))),{c(){e&&(0,r.YCL)(e.$$.fragment),n=(0,r.cSb)()},m(t,o){e&&(0,r.yef)(e,t,o),(0,r.$Tr)(t,n,o),a=!0},p(t,a){const i={};if(3&a&&(i.data=t[0].data[t[1]]),o!==(o=lt[t[1]])){if(e){(0,r.dvw)();const t=e;(0,r.etI)(t.$$.fragment,1,0,(()=>{(0,r.vpE)(t,1)})),(0,r.gbL)()}o?(e=new o(s(t)),(0,r.YCL)(e.$$.fragment),(0,r.Ui)(e.$$.fragment,1),(0,r.yef)(e,n.parentNode,n)):e=null}else o&&e.$set(i)},i(t){a||(e&&(0,r.Ui)(e.$$.fragment,t),a=!0)},o(t){e&&(0,r.etI)(e.$$.fragment,t),a=!1},d(t){t&&(0,r.ogt)(n),e&&(0,r.vpE)(e,t)}}}function gt(t){let e,n,a=t[0].data&&pt(t);return{c(){a&&a.c(),e=(0,r.cSb)()},m(t,o){a&&a.m(t,o),(0,r.$Tr)(t,e,o),n=!0},p(t,[n]){t[0].data?a?(a.p(t,n),1&n&&(0,r.Ui)(a,1)):(a=pt(t),a.c(),(0,r.Ui)(a,1),a.m(e.parentNode,e)):a&&((0,r.dvw)(),(0,r.etI)(a,1,1,(()=>{a=null})),(0,r.gbL)())},i(t){n||((0,r.Ui)(a),n=!0)},o(t){(0,r.etI)(a),n=!1},d(t){a&&a.d(t),t&&(0,r.ogt)(e)}}}function mt(t,e,n){let r,{data:a}=e,o=[];return t.$$set=t=>{"data"in t&&n(0,a=t.data)},t.$$.update=()=>{if(1&t.$$.dirty&&a&&a.data){let t={},e=[];for(const n in a.data)n in lt||n in dt?t[n]=1:e.push(n);for(const e in lt)if(e in t){n(1,r=e);break}n(2,o=e)}},[a,r,o,function(){const t={type:"output-mimetype",error:{missing:o,data_keys:Object.keys(a.data)}};return j(t),JSON.stringify(t)}]}class yt extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,mt,gt,r.N8,{data:0})}}var _t=yt;function vt(t){let e,n,a;return n=new _t({props:{data:t[0]}}),{c(){e=(0,r.bGB)("div"),(0,r.YCL)(n.$$.fragment),(0,r.Ljt)(e,"class","output_display_data")},m(t,o){(0,r.$Tr)(t,e,o),(0,r.yef)(n,e,null),a=!0},p(t,[e]){const r={};1&e&&(r.data=t[0]),n.$set(r)},i(t){a||((0,r.Ui)(n.$$.fragment,t),a=!0)},o(t){(0,r.etI)(n.$$.fragment,t),a=!1},d(t){t&&(0,r.ogt)(e),(0,r.vpE)(n)}}}function ht(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class Lt extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,ht,vt,r.N8,{data:0})}}var bt=Lt,xt=n(7003);function wt(t){let e,n;return e=new ot({props:{data:t[0].ename+": "+t[0].evalue}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,n){const r={};1&n&&(r.data=t[0].ename+": "+t[0].evalue),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}function It(t){let e,n;return e=new ot({props:{data:B(t[0].traceback,"\n")}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,n){const r={};1&n&&(r.data=B(t[0].traceback,"\n")),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}function Tt(t){let e,n,a,o;const s=[It,wt],i=[];function c(t,e){return void 0!==t[0].traceback?0:1}return n=c(t),a=i[n]=s[n](t),{c(){e=(0,r.bGB)("div"),a.c(),(0,r.Ljt)(e,"class","output_subarea output_test output_error")},m(t,a){(0,r.$Tr)(t,e,a),i[n].m(e,null),o=!0},p(t,[o]){let u=n;n=c(t),n===u?i[n].p(t,o):((0,r.dvw)(),(0,r.etI)(i[u],1,1,(()=>{i[u]=null})),(0,r.gbL)(),a=i[n],a?a.p(t,o):(a=i[n]=s[n](t),a.c()),(0,r.Ui)(a,1),a.m(e,null))},i(t){o||((0,r.Ui)(a),o=!0)},o(t){(0,r.etI)(a),o=!1},d(t){t&&(0,r.ogt)(e),i[n].d()}}}function Ut(t,e,n){let{data:r}=e;return(0,xt.H3)((()=>{j({type:"runtime-error",error:r})})),t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class jt extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,Ut,Tt,r.N8,{data:0})}}var Ct=jt;function Gt(t){let e,n,a;return n=new _t({props:{data:t[0]}}),{c(){e=(0,r.bGB)("div"),(0,r.YCL)(n.$$.fragment),(0,r.Ljt)(e,"class","output_execute_result")},m(t,o){(0,r.$Tr)(t,e,o),(0,r.yef)(n,e,null),a=!0},p(t,[e]){const r={};1&e&&(r.data=t[0]),n.$set(r)},i(t){a||((0,r.Ui)(n.$$.fragment,t),a=!0)},o(t){(0,r.etI)(n.$$.fragment,t),a=!1},d(t){t&&(0,r.ogt)(e),(0,r.vpE)(n)}}}function St(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class Nt extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,St,Gt,r.N8,{data:0})}}var Bt=Nt;function Et(t){let e,n,a,o;return n=new ot({props:{data:B(t[0].text)}}),{c(){e=(0,r.bGB)("div"),(0,r.YCL)(n.$$.fragment),(0,r.Ljt)(e,"class",a="output_stream output_"+t[0].name+" output_text")},m(t,a){(0,r.$Tr)(t,e,a),(0,r.yef)(n,e,null),o=!0},p(t,[s]){const i={};1&s&&(i.data=B(t[0].text)),n.$set(i),(!o||1&s&&a!==(a="output_stream output_"+t[0].name+" output_text"))&&(0,r.Ljt)(e,"class",a)},i(t){o||((0,r.Ui)(n.$$.fragment,t),o=!0)},o(t){(0,r.etI)(n.$$.fragment,t),o=!1},d(t){t&&(0,r.ogt)(e),(0,r.vpE)(n)}}}function Zt(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r]}class Yt extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,Zt,Et,r.N8,{data:0})}}var kt={display_data:bt,error:Ct,execute_result:Bt,stream:Yt};function Rt(t){let e,n,a,o;const s=[Ot,Dt],i=[];function c(t,e){return t[0].output_type in kt?0:1}return e=c(t),n=i[e]=s[e](t),{c(){n.c(),a=(0,r.cSb)()},m(t,n){i[e].m(t,n),(0,r.$Tr)(t,a,n),o=!0},p(t,o){let u=e;e=c(t),e===u?i[e].p(t,o):((0,r.dvw)(),(0,r.etI)(i[u],1,1,(()=>{i[u]=null})),(0,r.gbL)(),n=i[e],n?n.p(t,o):(n=i[e]=s[e](t),n.c()),(0,r.Ui)(n,1),n.m(a.parentNode,a))},i(t){o||((0,r.Ui)(n),o=!0)},o(t){(0,r.etI)(n),o=!1},d(t){i[e].d(t),t&&(0,r.ogt)(a)}}}function Dt(t){let e,n,a,o;return{c(){e=(0,r.bGB)("div"),n=(0,r.bGB)("p"),n.innerHTML='Unhandled output_type renderer, please report this on <a href="https://github.com/MaayanLab/appyter/issues">Appyter Issues</a> with this information:',a=(0,r.DhX)(),o=(0,r.bGB)("code"),o.textContent=`${t[1]()}`,(0,r.Ljt)(e,"class","alert alert-danger")},m(t,s){(0,r.$Tr)(t,e,s),(0,r.R3I)(e,n),(0,r.R3I)(e,a),(0,r.R3I)(e,o)},p:r.ZTd,i:r.ZTd,o:r.ZTd,d(t){t&&(0,r.ogt)(e)}}}function Ot(t){let e,n,a;var o=kt[t[0].output_type];function s(t){return{props:{data:t[0]}}}return o&&(e=new o(s(t))),{c(){e&&(0,r.YCL)(e.$$.fragment),n=(0,r.cSb)()},m(t,o){e&&(0,r.yef)(e,t,o),(0,r.$Tr)(t,n,o),a=!0},p(t,a){const i={};if(1&a&&(i.data=t[0]),o!==(o=kt[t[0].output_type])){if(e){(0,r.dvw)();const t=e;(0,r.etI)(t.$$.fragment,1,0,(()=>{(0,r.vpE)(t,1)})),(0,r.gbL)()}o?(e=new o(s(t)),(0,r.YCL)(e.$$.fragment),(0,r.Ui)(e.$$.fragment,1),(0,r.yef)(e,n.parentNode,n)):e=null}else o&&e.$set(i)},i(t){a||(e&&(0,r.Ui)(e.$$.fragment,t),a=!0)},o(t){e&&(0,r.etI)(e.$$.fragment,t),a=!1},d(t){t&&(0,r.ogt)(n),e&&(0,r.vpE)(e,t)}}}function Ht(t){let e,n,a=t[0]&&Rt(t);return{c(){a&&a.c(),e=(0,r.cSb)()},m(t,o){a&&a.m(t,o),(0,r.$Tr)(t,e,o),n=!0},p(t,[n]){t[0]?a?(a.p(t,n),1&n&&(0,r.Ui)(a,1)):(a=Rt(t),a.c(),(0,r.Ui)(a,1),a.m(e.parentNode,e)):a&&((0,r.dvw)(),(0,r.etI)(a,1,1,(()=>{a=null})),(0,r.gbL)())},i(t){n||((0,r.Ui)(a),n=!0)},o(t){(0,r.etI)(a),n=!1},d(t){a&&a.d(t),t&&(0,r.ogt)(e)}}}function Xt(t,e,n){let{data:r}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data)},[r,function(){const t={type:"output-type",error:{keys:Object.keys(r),output_type:r.output_type||null,data_keys:Object.keys(r.data||{})}};return j(t),JSON.stringify(t)}]}class Mt extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,Xt,Ht,r.N8,{data:0})}}var Wt=Mt,At=n(1782);function Vt(t,e,n){const r=t.slice();return r[4]=e[n],r}function Jt(t,e){let n,a,o,s,i,c;return a=new L({props:{index:e[1]+"-"+e[4].index,prompt_type:"output"}}),i=new Wt({props:{data:e[4]}}),{key:t,first:null,c(){n=(0,r.bGB)("div"),(0,r.YCL)(a.$$.fragment),o=(0,r.DhX)(),s=(0,r.bGB)("div"),(0,r.YCL)(i.$$.fragment),(0,r.Ljt)(s,"class","output_subarea"),(0,r.Ljt)(n,"class","output_area"),this.first=n},m(t,e){(0,r.$Tr)(t,n,e),(0,r.yef)(a,n,null),(0,r.R3I)(n,o),(0,r.R3I)(n,s),(0,r.yef)(i,s,null),c=!0},p(t,n){e=t;const r={};3&n&&(r.index=e[1]+"-"+e[4].index),a.$set(r);const o={};1&n&&(o.data=e[4]),i.$set(o)},i(t){c||((0,r.Ui)(a.$$.fragment,t),(0,r.Ui)(i.$$.fragment,t),c=!0)},o(t){(0,r.etI)(a.$$.fragment,t),(0,r.etI)(i.$$.fragment,t),c=!1},d(t){t&&(0,r.ogt)(n),(0,r.vpE)(a),(0,r.vpE)(i)}}}function zt(t){let e,n,a,o,s,i;return n=new L({props:{index:t[1]+"-loader",prompt_type:"output"}}),s=new At.Z({}),{c(){e=(0,r.bGB)("div"),(0,r.YCL)(n.$$.fragment),a=(0,r.DhX)(),o=(0,r.bGB)("div"),(0,r.YCL)(s.$$.fragment),(0,r.Ljt)(o,"class","output_subarea"),(0,r.Ljt)(e,"class","output_area")},m(t,c){(0,r.$Tr)(t,e,c),(0,r.yef)(n,e,null),(0,r.R3I)(e,a),(0,r.R3I)(e,o),(0,r.yef)(s,o,null),i=!0},p(t,e){const r={};2&e&&(r.index=t[1]+"-loader"),n.$set(r)},i(t){i||((0,r.Ui)(n.$$.fragment,t),(0,r.Ui)(s.$$.fragment,t),i=!0)},o(t){(0,r.etI)(n.$$.fragment,t),(0,r.etI)(s.$$.fragment,t),i=!1},d(t){t&&(0,r.ogt)(e),(0,r.vpE)(n),(0,r.vpE)(s)}}}function qt(t){let e,n,a,o,s=[],i=new Map,c=[...t[3](t[0])];const u=t=>t[4].index;for(let e=0;e<c.length;e+=1){let n=Vt(t,c,e),r=u(n);i.set(r,s[e]=Jt(r,n))}let l=t[1]===t[2]&&zt(t);return{c(){e=(0,r.bGB)("div"),n=(0,r.bGB)("div");for(let t=0;t<s.length;t+=1)s[t].c();a=(0,r.DhX)(),l&&l.c(),(0,r.Ljt)(n,"class","output"),(0,r.Ljt)(e,"class","output_wrapper")},m(t,i){(0,r.$Tr)(t,e,i),(0,r.R3I)(e,n);for(let t=0;t<s.length;t+=1)s[t].m(n,null);(0,r.R3I)(n,a),l&&l.m(n,null),o=!0},p(t,[e]){11&e&&(c=[...t[3](t[0])],(0,r.dvw)(),s=(0,r.GQg)(s,e,u,1,t,c,i,n,r.cly,Jt,a,Vt),(0,r.gbL)()),t[1]===t[2]?l?(l.p(t,e),6&e&&(0,r.Ui)(l,1)):(l=zt(t),l.c(),(0,r.Ui)(l,1),l.m(n,null)):l&&((0,r.dvw)(),(0,r.etI)(l,1,1,(()=>{l=null})),(0,r.gbL)())},i(t){if(!o){for(let t=0;t<c.length;t+=1)(0,r.Ui)(s[t]);(0,r.Ui)(l),o=!0}},o(t){for(let t=0;t<s.length;t+=1)(0,r.etI)(s[t]);(0,r.etI)(l),o=!1},d(t){t&&(0,r.ogt)(e);for(let t=0;t<s.length;t+=1)s[t].d();l&&l.d()}}}function Ft(t,e,n){let{data:r=[]}=e,{index:a}=e,{loading:o}=e;return t.$$set=t=>{"data"in t&&n(0,r=t.data),"index"in t&&n(1,a=t.index),"loading"in t&&n(2,o=t.loading)},[r,a,o,function*(t){let e=0,n={};for(const r of t)if("stream"===r.output_type)if(void 0===n[r.name]){const t=B(r.text,"\n");n[r.name]={...r,text:t,index:e++}}else{const t=B(r.text,"\n");t.startsWith("\r")?n[r.name].text=t:n[r.name].text+=t}else yield{...r,index:e++};for(const t in n)n[t].text=n[t].text.replace(/^\r/,"").replace(/(\r?\n)+$/,""),n[t].text&&(yield n[t])}]}class Pt extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,Ft,qt,r.N8,{data:0,index:1,loading:2})}}var Qt=Pt;function Kt(t){for(const e of t)if(e)return!0;return!1}function te(t,e,n){const r=t.slice();return r[3]=e[n],r}function ee(t){let e,n,a,o;const s=[re,ne],i=[];function c(t,e){return"code"===t[3].cell_type?0:"markdown"===t[3].cell_type?1:-1}return~(e=c(t))&&(n=i[e]=s[e](t)),{c(){n&&n.c(),a=(0,r.cSb)()},m(t,n){~e&&i[e].m(t,n),(0,r.$Tr)(t,a,n),o=!0},p(t,o){let u=e;e=c(t),e===u?~e&&i[e].p(t,o):(n&&((0,r.dvw)(),(0,r.etI)(i[u],1,1,(()=>{i[u]=null})),(0,r.gbL)()),~e?(n=i[e],n?n.p(t,o):(n=i[e]=s[e](t),n.c()),(0,r.Ui)(n,1),n.m(a.parentNode,a)):n=null)},i(t){o||((0,r.Ui)(n),o=!0)},o(t){(0,r.etI)(n),o=!1},d(t){~e&&i[e].d(t),t&&(0,r.ogt)(a)}}}function ne(t){let e,n;return e=new c({props:{type:"text",$$slots:{default:[oe]},$$scope:{ctx:t}}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,n){const r={};65&n&&(r.$$scope={dirty:n,ctx:t}),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}function re(t){let e,n;return e=new c({props:{type:"code",$$slots:{default:[ce]},$$scope:{ctx:t}}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,n){const r={};71&n&&(r.$$scope={dirty:n,ctx:t}),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}function ae(t){let e,n,o,s,i,c;return e=new L({props:{prompt_type:"input",index:t[3].index}}),i=new a.Z({props:{module:$e,props:{data:B(t[3].source)}}}),{c(){(0,r.YCL)(e.$$.fragment),n=(0,r.DhX)(),o=(0,r.bGB)("div"),s=(0,r.bGB)("div"),(0,r.YCL)(i.$$.fragment),(0,r.Ljt)(s,"class","text_cell_render border-box-sizing rendered_html"),(0,r.Ljt)(o,"class","inner_cell")},m(t,a){(0,r.yef)(e,t,a),(0,r.$Tr)(t,n,a),(0,r.$Tr)(t,o,a),(0,r.R3I)(o,s),(0,r.yef)(i,s,null),c=!0},p(t,n){const r={};1&n&&(r.index=t[3].index),e.$set(r);const a={};1&n&&(a.props={data:B(t[3].source)}),i.$set(a)},i(t){c||((0,r.Ui)(e.$$.fragment,t),(0,r.Ui)(i.$$.fragment,t),c=!0)},o(t){(0,r.etI)(e.$$.fragment,t),(0,r.etI)(i.$$.fragment,t),c=!1},d(t){(0,r.vpE)(e,t),t&&(0,r.ogt)(n),t&&(0,r.ogt)(o),(0,r.vpE)(i)}}}function oe(t){let e,n,a;return e=new p({props:{$$slots:{default:[ae]},$$scope:{ctx:t}}}),{c(){(0,r.YCL)(e.$$.fragment),n=(0,r.DhX)()},m(t,o){(0,r.yef)(e,t,o),(0,r.$Tr)(t,n,o),a=!0},p(t,n){const r={};65&n&&(r.$$scope={dirty:n,ctx:t}),e.$set(r)},i(t){a||((0,r.Ui)(e.$$.fragment,t),a=!0)},o(t){(0,r.etI)(e.$$.fragment,t),a=!1},d(t){(0,r.vpE)(e,t),t&&(0,r.ogt)(n)}}}function se(t){let e,n;return e=new p({props:{$$slots:{default:[ie]},$$scope:{ctx:t}}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,n){const r={};69&n&&(r.$$scope={dirty:n,ctx:t}),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}function ie(t){let e,n,a,o;return e=new L({props:{prompt_type:"input",index:t[3].index,running:void 0!==t[2]?t[3].index>=t[2]:void 0,error:Kt(t[3].outputs.map(pe)),counter:t[3].execution_count,cell_type:t[3].cell_type}}),a=new T({props:{language:"python",source:B(t[3].source)}}),{c(){(0,r.YCL)(e.$$.fragment),n=(0,r.DhX)(),(0,r.YCL)(a.$$.fragment)},m(t,s){(0,r.yef)(e,t,s),(0,r.$Tr)(t,n,s),(0,r.yef)(a,t,s),o=!0},p(t,n){const r={};1&n&&(r.index=t[3].index),5&n&&(r.running=void 0!==t[2]?t[3].index>=t[2]:void 0),1&n&&(r.error=Kt(t[3].outputs.map(pe))),1&n&&(r.counter=t[3].execution_count),1&n&&(r.cell_type=t[3].cell_type),e.$set(r);const o={};1&n&&(o.source=B(t[3].source)),a.$set(o)},i(t){o||((0,r.Ui)(e.$$.fragment,t),(0,r.Ui)(a.$$.fragment,t),o=!0)},o(t){(0,r.etI)(e.$$.fragment,t),(0,r.etI)(a.$$.fragment,t),o=!1},d(t){(0,r.vpE)(e,t),t&&(0,r.ogt)(n),(0,r.vpE)(a,t)}}}function ce(t){let e,n,a,o,s=t[1]&&se(t);return n=new Qt({props:{index:t[3].index,data:t[3].outputs||[],loading:t[2]}}),{c(){s&&s.c(),e=(0,r.DhX)(),(0,r.YCL)(n.$$.fragment),a=(0,r.DhX)()},m(t,i){s&&s.m(t,i),(0,r.$Tr)(t,e,i),(0,r.yef)(n,t,i),(0,r.$Tr)(t,a,i),o=!0},p(t,a){t[1]?s?(s.p(t,a),2&a&&(0,r.Ui)(s,1)):(s=se(t),s.c(),(0,r.Ui)(s,1),s.m(e.parentNode,e)):s&&((0,r.dvw)(),(0,r.etI)(s,1,1,(()=>{s=null})),(0,r.gbL)());const o={};1&a&&(o.index=t[3].index),1&a&&(o.data=t[3].outputs||[]),4&a&&(o.loading=t[2]),n.$set(o)},i(t){o||((0,r.Ui)(s),(0,r.Ui)(n.$$.fragment,t),o=!0)},o(t){(0,r.etI)(s),(0,r.etI)(n.$$.fragment,t),o=!1},d(t){s&&s.d(t),t&&(0,r.ogt)(e),(0,r.vpE)(n,t),t&&(0,r.ogt)(a)}}}function ue(t,e){let n,a,o,s=""!==B(e[3].source),i=s&&ee(e);return{key:t,first:null,c(){n=(0,r.cSb)(),i&&i.c(),a=(0,r.cSb)(),this.first=n},m(t,e){(0,r.$Tr)(t,n,e),i&&i.m(t,e),(0,r.$Tr)(t,a,e),o=!0},p(t,n){e=t,1&n&&(s=""!==B(e[3].source)),s?i?(i.p(e,n),1&n&&(0,r.Ui)(i,1)):(i=ee(e),i.c(),(0,r.Ui)(i,1),i.m(a.parentNode,a)):i&&((0,r.dvw)(),(0,r.etI)(i,1,1,(()=>{i=null})),(0,r.gbL)())},i(t){o||((0,r.Ui)(i),o=!0)},o(t){(0,r.etI)(i),o=!1},d(t){t&&(0,r.ogt)(n),i&&i.d(t),t&&(0,r.ogt)(a)}}}function le(t){let e,n,a=[],o=new Map,s=t[0].cells;const i=t=>t[3].index;for(let e=0;e<s.length;e+=1){let n=te(t,s,e),r=i(n);o.set(r,a[e]=ue(r,n))}return{c(){for(let t=0;t<a.length;t+=1)a[t].c();e=(0,r.cSb)()},m(t,o){for(let e=0;e<a.length;e+=1)a[e].m(t,o);(0,r.$Tr)(t,e,o),n=!0},p(t,n){7&n&&(s=t[0].cells,(0,r.dvw)(),a=(0,r.GQg)(a,n,i,1,t,s,o,e.parentNode,r.cly,ue,e,te),(0,r.gbL)())},i(t){if(!n){for(let t=0;t<s.length;t+=1)(0,r.Ui)(a[t]);n=!0}},o(t){for(let t=0;t<a.length;t+=1)(0,r.etI)(a[t]);n=!1},d(t){for(let e=0;e<a.length;e+=1)a[e].d(t);t&&(0,r.ogt)(e)}}}function de(t){let e,n;return e=new a.Z({props:{module:fe,children:!0,$$slots:{default:[le]},$$scope:{ctx:t}}}),{c(){(0,r.YCL)(e.$$.fragment)},m(t,a){(0,r.yef)(e,t,a),n=!0},p(t,[n]){const r={};71&n&&(r.$$scope={dirty:n,ctx:t}),e.$set(r)},i(t){n||((0,r.Ui)(e.$$.fragment,t),n=!0)},o(t){(0,r.etI)(e.$$.fragment,t),n=!1},d(t){(0,r.vpE)(e,t)}}}const pe=({output_type:t})=>"error"===t,$e=()=>Promise.resolve().then(n.bind(n,6523)),fe=()=>n.e(494).then(n.bind(n,7494));function ge(t,e,n){let{nb:r}=e,{show_code:a}=e,{current_code_cell:o}=e;return t.$$set=t=>{"nb"in t&&n(0,r=t.nb),"show_code"in t&&n(1,a=t.show_code),"current_code_cell"in t&&n(2,o=t.current_code_cell)},[r,a,o]}class me extends r.f_C{constructor(t){super(),(0,r.S1n)(this,t,ge,de,r.N8,{nb:0,show_code:1,current_code_cell:2})}}var ye=me}}]);