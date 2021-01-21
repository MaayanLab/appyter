// https://github.com/jupyter-widgets/ipywidgets/blob/master/examples/web1/manager.js
import * as base from '@jupyter-widgets/base'
import { ManagerBase } from '@jupyter-widgets/base-manager'
import * as controls from '@jupyter-widgets/controls'
import { Widget as LuminoWidget } from '@lumino/widgets'

export class IPYWidgetManager extends ManagerBase {
  constructor(el) {
    super();
    this.el = el;
    window.define('@jupyter-widgets/controls', function () { return controls })
    window.define('@jupyter-widgets/base', function () { return base })
  }

  loadClass(className, moduleName, moduleVersion) {
    return new Promise(function(resolve, reject) {
      if (!window.require.defined(moduleName)) {
        window.require.config({
          paths: {
            [moduleName]: `https://unpkg.com/${moduleName}@${moduleVersion}/dist/index`,
          }
        })
      }
      window.require([moduleName], resolve, reject)
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

  display_view(view, options) {
    return Promise.resolve(view).then((view) => {
        LuminoWidget.attach(view.pWidget, options.el);
        view.on('remove', () => {
            console.log('View removed', view);
        });
        return view;
    });
  }

  _get_comm_info() {
    return Promise.resolve({});
  }

  _create_comm(comm_target_name, model_id, data, metadata, buffers) {
    return Promise.resolve({
      on_close: () => { return; },
      on_msg: () => { return; },
      close: () => { return; }
    });
  }
}