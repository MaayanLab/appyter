import path from 'path'
import glob from 'glob'
import webpack from 'webpack'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import CopyWebpackPlugin from 'copy-webpack-plugin'

export default function (_env, argv) {
  const __dirname = path.resolve();
  const isProduction = argv.mode === 'production'
  const isDevelopment = !isProduction;

  return {
    mode: isDevelopment ? 'development' : 'production',
    devtool: isDevelopment && 'cheap-module-source-map',
    entry: () => {
      const entrypoints = {}
      for (const entrypoint of [
        ...glob.sync('profiles/**/*.js'),
        ...glob.sync('profiles/**/*.svelte'),
      ]) {
        entrypoints[entrypoint.replace(/\.(js|svelte)$/, '')] = {
          import: ['./lib/webpack_public_path.js', `./${entrypoint}`],
          filename: entrypoint.replace(/\.(js|svelte)$/, '.js'),
        }
      }
      return entrypoints
    },
    output: {
      path: path.resolve(__dirname, '../appyter/static'),
      filename: 'profiles/default/js/base.js',
      assetModuleFilename: 'profiles/default/assets/[name].js',
      chunkFilename: 'profiles/default/js/chunks/[name].js',
      publicPath: '',
      library: {
        type: 'umd',
        umdNamedDefine: true,
      },
      clean: true,
    },
    resolve: {
      extensions: ['.mjs', '.js', '.svelte'],
      mainFields: ['svelte', 'browser', 'module', 'main'],
      alias: {
        '@': path.resolve(__dirname),
      },
    },
    module: {
      rules: [
        {
          test: /\.m?js$/,
          exclude: [
            {
              and: [path.resolve(__dirname, 'node_modules')],
              not: [/node_modules(\/|\\)svelte/],
            },
          ],
          use: 'babel-loader',
        },
        {
          test: /\.svelte$/,
          use: [
            'babel-loader',
            {
              loader: 'svelte-loader',
              options: {
                compilerOptions: {
                  dev: isDevelopment,
                },
                emitCss: false,
                hotReload: isDevelopment,
              },
            },
          ],
        },
        {
          test: /\.(png|jpg|gif|svg)$/,
          type: 'asset/resource',
        },
        {
          test: /\.(css|s[ac]ss)$/i,
          use: [
            MiniCssExtractPlugin.loader,
            'css-loader',
            'sass-loader',
          ],
        },
        {
          // required to prevent errors from Svelte on Webpack 5+
          test: /node_modules\/svelte\/.*\.mjs$/,
          resolve: {
            fullySpecified: false
          }
        },
      ]
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: ({ chunk }) => `${chunk.name.replace(/js\/(.+)$/, 'css/$1.css')}`,
      }),
      new webpack.DefinePlugin({
        'process.env.NODE_ENV': JSON.stringify(
          isProduction ? 'production' : 'development'
        )
      }),
      new CopyWebpackPlugin({
        patterns: [
          {
            from: path.resolve(__dirname, 'node_modules/requirejs/require.js'),
            to: path.resolve(__dirname, '../appyter/static/profiles/default/js/lib/require.js'),
          },
          {
            from: path.resolve(__dirname, 'node_modules/jquery/dist/jquery.min.js'),
            to: path.resolve(__dirname, '../appyter/static/profiles/default/js/lib/jquery.js'),
          },
          {
            from: path.resolve(__dirname, 'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'),
            to: path.resolve(__dirname, '../appyter/static/profiles/biojupies/js/lib/bootstrap.js'),
          },
          {
            from: path.resolve(__dirname, 'node_modules/@fortawesome/fontawesome-free/css/all.min.css'),
            to: path.resolve(__dirname, '../appyter/static/profiles/biojupies/css/fontawesome.css'),
          },
          {
            from: path.resolve(__dirname, 'node_modules/@fortawesome/fontawesome-free/webfonts'),
            to: path.resolve(__dirname, '../appyter/static/profiles/biojupies/webfonts'),
          },
          {
            from: path.resolve(__dirname, 'utils/silent-check-sso.html'),
            to: path.resolve(__dirname, '../appyter/static/silent-check-sso.html'),
          },
        ],
      }),
    ].filter(Boolean),
    externals: {
      'requirejs': 'requirejs',
      'jquery': 'jquery',
      'bootstrap': 'bootstrap',
    },
  };
};