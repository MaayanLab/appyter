// https://github.com/jupyter-widgets/ipywidgets/blob/master/examples/web1/manager.js
import * as base from '@jupyter-widgets/base'
import { ManagerBase } from '@jupyter-widgets/base-manager'
import * as controls from '@jupyter-widgets/controls'
import { Widget as LuminoWidget } from '@lumino/widgets'

export class IPYWidgetManager extends ManagerBase {
  constructor(el) {
    super();
    this.el = el;
  }

  loadClass(className, moduleName, moduleVersion) {
    return new Promise(function(resolve, reject) {
      if (moduleName === '@jupyter-widgets/controls') {
        resolve(controls);
      } else if (moduleName === '@jupyter-widgets/base') {
        resolve(base);
      } else {
        var fallback = function(err) {
          let failedId = err.requireModules && err.requireModules[0];
          if (failedId) {
            console.log(
              `Falling back to unpkg.com for ${moduleName}@${moduleVersion}`
            );
            window.require(
              [
                `https://unpkg.com/${moduleName}@${moduleVersion}/dist/index.js`
              ],
              resolve,
              reject
            );
          } else {
            throw err;
          }
        };
        window.require([`${moduleName}.js`], resolve, fallback);
      }
    }).then(function(module) {
      if (module[className]) {
        return module[className];
      } else {
        return Promise.reject(
          `Class ${className} not found in module ${moduleName}@${moduleVersion}`
        );
      }
    });
  }

  display_view(view) {
    var that = this;
    return Promise.resolve(view).then(view => {
      LuminoWidget.attach(view.pWidget, that.el);
      return view;
    });
  }

  _get_comm_info() {
    return Promise.resolve({});
  }

  _create_comm() {
    return Promise.reject('no comms available');
  }
}