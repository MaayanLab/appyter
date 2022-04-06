"use strict";
(self["webpackChunkappyter_js"] = self["webpackChunkappyter_js"] || []).push([["lib_livereload_js"],{

/***/ "./lib/livereload.js":
/*!***************************!*\
  !*** ./lib/livereload.js ***!
  \***************************/
/***/ (function(__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": function() { return /* binding */ livereload; }
/* harmony export */ });
async function livereload(window) {
  const {
    default: socket
  } = await Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_socket_io-client_build_esm_index_js"), __webpack_require__.e("lib_socket_js")]).then(__webpack_require__.bind(__webpack_require__, /*! @/lib/socket */ "./lib/socket.js"));
  let first_connect = true;
  socket.on('connect', () => {
    if (first_connect) {
      console.debug('connected');
      first_connect = false;
    } else {
      console.debug('reconnect');
      window.location.reload();
    }
  });
  socket.on('livereload', data => {
    console.debug('livereload');
    window.location.reload();
  });
}

/***/ })

}]);
//# sourceMappingURL=lib_livereload_js.js.map