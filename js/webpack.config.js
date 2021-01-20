const path = require('path')
const glob = require('glob')

const root = path.resolve(__dirname, '..')

const components = {}
for (const file of glob.sync(path.join(root, 'js/profiles/**/*.svelte'))) {
  const relpath = path.relative(path.resolve(root, 'js'), file)
  components[file] = {
    import: file,
    filename: relpath.replace(/\.svelte$/, '.js'),
  }
}

const mode = 'development'

module.exports = {
  mode,
  devtool: mode === 'production' ? false : 'inline-source-map',
  entry: components,
  resolve: {
    extensions: ['.js', '.svelte'],
    mainFields: ['svelte', 'browser', 'module', 'main'],
  },
  output: {
    path: path.resolve(__dirname, '../appyter/'),
    libraryTarget: 'umd',
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
  }
}
