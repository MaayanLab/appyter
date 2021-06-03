const path = require('path')
const gulp = require('gulp')
const rename = require('gulp-rename')
const cleanCSS = require('gulp-clean-css')
const sass = require('gulp-sass')
const merge = require('merge-stream')
const webpack = require('webpack-stream')
const named = require('vinyl-named')
const root = path.join(__dirname, '..')

const svelte_files = {
  src: path.join(root, 'js/profiles/**/*.svelte'),
  dest: path.join(root, 'appyter', 'profiles'),
}

const css_files = {
  src: path.join(root, 'js/profiles/**/*.scss'),
  dest: path.join(root, 'appyter', 'profiles'),
}

const cp_files = [
  {
    src: path.join(root, 'js/node_modules/requirejs/require.js'),
    dest: path.join(root, 'appyter/profiles/default/static/js/lib/requirejs'),
  },
  {
    src: path.join(root, 'js/node_modules/jquery/dist/jquery.min.js'),
    dest: path.join(root, 'appyter/profiles/default/static/js/lib/jquery'),
  },
  {
    src: path.join(root, 'js/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'),
    dest: path.join(root, 'appyter/profiles/biojupies/static/js/lib/bootstrap'),
  },
  {
    src: path.join(root, 'js/node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'),
    dest: path.join(root, 'appyter/profiles/bootstrap/static/js/lib/bootstrap'),
  },
  {
    src: path.join(root, 'js/node_modules/socket.io-client/dist/socket.io.min.js'),
    dest: path.join(root, 'appyter/profiles/default/static/js/lib/socket.io'),
  },
  {
    src: path.join(root, 'js/node_modules/socketio-file-upload/client.min.js'),
    dest: path.join(root, 'appyter/profiles/default/static/js/lib/socketio-file-upload'),
  },
  {
    src: path.join(root, 'js/node_modules/@fortawesome/fontawesome-free/css/all.min.css'),
    dest: path.join(root, 'appyter/profiles/biojupies/static/css/lib/fontawesome/css'),
  },
  {
    src: path.join(root, 'js/node_modules/@fortawesome/fontawesome-free/webfonts/*'),
    dest: path.join(root, 'appyter/profiles/biojupies/static/css/lib/fontawesome/webfonts'),
  },
  {
    src: path.join(root, 'js/node_modules/select2/dist/js/select2.min.js'),
    dest: path.join(root, 'appyter/profiles/bootstrap/static/js/lib/select2'),
  },
]

gulp.task('copy_files', function () {
  return merge(
    cp_files.map(
      function ({ src, dest}) {
        return gulp
          .src(src)
          .pipe(gulp.dest(dest))
      }
    )
  )
})

gulp.task('build_svelte', function () {
  return gulp
    .src(svelte_files.src, { since: gulp.lastRun('build_svelte') })
    .pipe(named(function (file) {
      const [_0, profile, path] = /profiles\/([^\/]+)\/(.+)\.svelte$/.exec(file.history[0])
      return `${profile}/${path}`
    }))
    .pipe(webpack({
      mode: 'production',
      devtool: 'production',
      resolve: {
        extensions: ['.js', '.svelte'],
        mainFields: ['svelte', 'browser', 'module', 'main'],
        alias: {
          '@': path.resolve(__dirname),
        },
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
      output: {
        publicPath: '/static/',
        chunkFilename: 'js/chunks/[name].js',
        libraryTarget: 'umd',
      }
    }))
    .pipe(gulp.dest(svelte_files.dest))
})

gulp.task('build_css', function () {
  return gulp
    .src(css_files.src, { since: gulp.lastRun('build_css') })
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSS())
    .pipe(rename(function (path) {
      path.extname = ".css"
    }))
    .pipe(gulp.dest(css_files.dest))
})

gulp.task('build', gulp.series([
  'copy_files',
  'build_svelte',
  'build_css',
]))

gulp.task('watch', function () {
  gulp.watch(svelte_files.src, gulp.task('build_svelte'))
  gulp.watch(css_files.src, gulp.task('build_css'))
})

gulp.task('default', gulp.series(['build', 'watch']))
