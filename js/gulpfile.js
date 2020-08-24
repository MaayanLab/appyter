const path = require('path')
const gulp = require('gulp')
const log = require('gulplog')
const tap = require('gulp-tap')
const buffer = require('gulp-buffer')
const sourcemaps = require('gulp-sourcemaps')
const rename = require('gulp-rename')
const browserify = require('browserify')
const sveltify = require('sveltify')
const babelify = require('babelify')
const root = path.join(__dirname, '..')

const js = {
  src: path.join(root, 'js/profiles/**/*.svelte'),
  dest: path.join(root, 'appyter', 'profiles'),
}

gulp.task('build', function () {
  return gulp
    .src(js.src, { read: false, since: gulp.lastRun('build') })
    .pipe(tap(function (file) {
      log.info('bundling ' + file.path)
      file.contents = browserify(file.path, {
        debug: true,
        standalone: file.basename,
        transform: [
          [babelify, {presets: ['@babel/preset-env']}],
          sveltify,
        ],
      }).bundle()
    }))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(rename(function (path) {
      path.extname = ".js"
    }))
    .pipe(gulp.dest(js.dest))
})

gulp.task('watch', function () {
  return gulp.watch(js.src, gulp.task('build'))
})

gulp.task('default', gulp.series(['build', 'watch']))
