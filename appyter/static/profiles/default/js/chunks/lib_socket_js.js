"use strict";
(self["webpackChunkappyter_js"] = self["webpackChunkappyter_js"] || []).push([["lib_socket_js"],{

/***/ "./lib/socket.js":
/*!***********************!*\
  !*** ./lib/socket.js ***!
  \***********************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var uuid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! uuid */ "./node_modules/uuid/dist/esm-browser/v4.js");
/* harmony import */ var socket_io_client__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! socket.io-client */ "./node_modules/socket.io-client/build/esm/index.js");


const socket = (0,socket_io_client__WEBPACK_IMPORTED_MODULE_0__["default"])({
  path: `${window._config.PREFIX}/socket.io/`,
  extraHeaders: {
    Authorization: (0,uuid__WEBPACK_IMPORTED_MODULE_1__["default"])()
  }
});
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (socket);

/***/ })

}]);
//# sourceMappingURL=lib_socket_js.js.map