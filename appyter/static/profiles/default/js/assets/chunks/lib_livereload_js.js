"use strict";
(self["webpackChunkappyter_js"] = self["webpackChunkappyter_js"] || []).push([["lib_livereload_js"],{

/***/ "./lib/livereload.js":
/*!***************************!*\
  !*** ./lib/livereload.js ***!
  \***************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ livereload)
/* harmony export */ });
/* harmony import */ var _babel_runtime_helpers_asyncToGenerator__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/asyncToGenerator */ "./node_modules/@babel/runtime/helpers/esm/asyncToGenerator.js");
/* harmony import */ var _babel_runtime_regenerator__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @babel/runtime/regenerator */ "./node_modules/@babel/runtime/regenerator/index.js");
/* harmony import */ var socket_io_client__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! socket.io-client */ "./node_modules/socket.io-client/build/esm/index.js");



function livereload(_x) {
  return _livereload.apply(this, arguments);
}

function _livereload() {
  _livereload = (0,_babel_runtime_helpers_asyncToGenerator__WEBPACK_IMPORTED_MODULE_0__["default"])( /*#__PURE__*/_babel_runtime_regenerator__WEBPACK_IMPORTED_MODULE_1__.mark(function _callee(window) {
    var socket, first_connect;
    return _babel_runtime_regenerator__WEBPACK_IMPORTED_MODULE_1__.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            socket = (0,socket_io_client__WEBPACK_IMPORTED_MODULE_2__["default"])({
              path: window._config.PREFIX + 'socket.io'
            });
            first_connect = true;
            socket.on('connect', function () {
              if (first_connect) {
                console.debug('connected');
                first_connect = false;
              } else {
                console.debug('reconnect');
                window.location.reload();
              }
            });
            socket.on('livereload', function (data) {
              console.debug('livereload');
              window.location.reload();
            });

          case 4:
          case "end":
            return _context.stop();
        }
      }
    }, _callee);
  }));
  return _livereload.apply(this, arguments);
}

/***/ })

}]);
//# sourceMappingURL=lib_livereload_js.js.map