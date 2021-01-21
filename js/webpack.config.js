const path = require('path')
const glob = require('glob')

const root = path.resolve(__dirname, '..')

const mode = 'production'
const common = {
  mode,
  devtool: mode === 'production' ? false : 'inline-source-map',
  resolve: {
    extensions: ['.js', '.svelte'],
    mainFields: ['svelte', 'browser', 'module', 'main'],
  },
  module: {
    rules: [
      {
        test: /\.svelte$/,
        use: {
          loader: 'svelte-loader',
          options: {
            emitCss: false,
            hotReload: true,
          },
        },
      },
    ],
  },
}

const plan = {}
for (const file of glob.sync(path.join(root, 'js/profiles/**/*.svelte'))) {
  const relpath = path.relative(path.resolve(root, 'js/profiles'), file)
  const relpath_split = relpath.split('/')
  const profile = relpath_split.shift()
  const filename = relpath_split.pop()
  if (relpath_split.shift() !== 'static') throw new Error(':(')
  const dirname = relpath_split.join('/')
  const id = path.join(dirname, filename)
  if (plan[profile] === undefined) {
    plan[profile] = {}
  }
  plan[profile][id] = {
    input: path.resolve(root, 'js/profiles/', relpath),
    output: path.join(dirname, filename.replace(/\.svelte$/, '.js')),
  }
}

const _exports = []
for (const profile in plan) {
  const entry = {}
  if (profile !== 'default') {
    for (const id in plan['default']) {
      entry[id] = plan['default'][id].input
    }
  }
  for (const id in plan[profile]) {
    entry[id] = plan[profile][id].input
  }
  _exports.push({
    ...common,
    entry,
    output: {
      publicPath: '/static/',
      path: path.resolve(root, 'appyter/profiles', profile, 'static'),
      filename: (pathData) => plan[profile][pathData.chunk.name].output,
      chunkFilename: 'js/chunks/[name].js',
      libraryTarget: 'umd',
    }
  })
}

module.exports = _exports
