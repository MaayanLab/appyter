// https://github.com/jupyter-widgets/ipywidgets/blob/master/examples/web1/manager.js
import * as base from '@jupyter-widgets/base'
import { ManagerBase } from '@jupyter-widgets/base-manager'
import * as controls from '@jupyter-widgets/controls'
import { Widget as LuminoWidget } from '@lumino/widgets'

export class IPYWidgetManager extends ManagerBase {
  constructor(el) {
    super();
    this.el = el;
    this.__lock = { lock: false, callbacks: [] }
    this.__models_state = {}
    this.__models_view = {}
    this.create_and_display_views = this.create_and_display_views.bind(this)
    this.register_view = this.register_view.bind(this)
    this.register_state = this.register_state.bind(this)
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

  async create_and_display_views() {
    // TODO: simplify/cleanup
    if (this.__lock.lock || this.__lock.callbacks.length > 0) {
      await new Promise((resolve, reject) => this.__lock.callbacks.push(resolve))
    }
    this.__lock.lock = true

    const add_state = {...this.__models_state, state: {}}
    for (const model_id in this.__models_state.state) {
      const model_view = this.__models_view[model_id]
      if (model_view === undefined || model_view.view !== undefined) continue
      add_state.state[model_id] = this.__models_state.state[model_id]
    }
    if (Object.keys(add_state.state).length > 0) {
      const model_list = await this.set_state(add_state)
      for (const model of model_list) {
        const viewTag = this.__models_view[model.model_id].el
        this.__models_view[model.model_id].view = await this.create_view(model)
        await this.display_view(this.__models_view[model.model_id].view, { el: viewTag })
      }
    }

    this.__lock.lock = false
    while (this.__lock.callbacks.length > 0) {
      await this.__lock.callbacks.shift()()
    }
  }

  async register_view({ metadata, el }) {
    this.__models_view[metadata.model_id] = { metadata, el }
    await this.create_and_display_views()
  }

  async register_state(state) {
    this.__models_state = state
    await this.create_and_display_views()
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