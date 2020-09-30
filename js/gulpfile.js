const path = require('path')
const gulp = require('gulp')
const log = require('gulplog')
const tap = require('gulp-tap')
const buffer = require('gulp-buffer')
const rename = require('gulp-rename')
const cleanCSS = require('gulp-clean-css')
const browserify = require('browserify')
const sveltify = require('sveltify')
const babelify = require('babelify')
const tinyify = require('tinyify')
const sass = require('gulp-sass')
const merge = require('merge-stream')
const root = path.join(__dirname, '..')

const js_files = {
  src: path.join(root, 'js/profiles/**/*.js'),
  dest: path.join(root, 'appyter', 'profiles'),
}

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
    src: path.join(root, 'js/node_modules/socket.io-client/dist/socket.io.slim.js'),
    dest: path.join(root, 'appyter/profiles/default/static/js/lib/socket.io'),
  },
  {
    src: path.join(root, 'js/node_modules/socketio-file-upload/client.min.js'),
    dest: path.join(root, 'appyter/profiles/default/static/js/lib/socketio-file-upload'),
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

gulp.task('build_js', function () {
  return gulp
    .src(js_files.src, { read: false, since: gulp.lastRun('build_js') })
    .pipe(tap(function (file) {
      log.info('bundling ' + file.path)
      file.contents = browserify(file.path, {
        debug: true,
        standalone: file.basename,
        transform: [
          [babelify, { presets: ['@babel/preset-env'] }],
        ],
        plugin: [
          tinyify,
        ],
      }).bundle()
    }))
    .pipe(buffer())
    .pipe(gulp.dest(js_files.dest))
})

gulp.task('build_svelte', function () {
  return gulp
    .src(svelte_files.src, { read: false, since: gulp.lastRun('build_svelte') })
    .pipe(tap(function (file) {
      log.info('bundling ' + file.path)
      file.contents = browserify(file.path, {
        debug: true,
        standalone: file.basename,
        transform: [
          [babelify, {presets: ['@babel/preset-env']}],
          sveltify,
        ],
        plugin: [
          tinyify,
        ],
      }).bundle()
    }))
    .pipe(buffer())
    .pipe(rename(function (path) {
      path.extname = ".js"
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
  'build_js',
  'build_svelte', 
  'build_css',
]))

gulp.task('watch', function () {
  gulp.watch(js_files.src, gulp.task('build_js'))
  gulp.watch(svelte_files.src, gulp.task('build_svelte'))
  gulp.watch(css_files.src, gulp.task('build_css'))
})

gulp.task('default', gulp.series(['build', 'watch']))
