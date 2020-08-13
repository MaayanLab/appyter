const path = require('path')
const gulp = require('gulp')
const log = require('gulplog')
const tap = require('gulp-tap')
const buffer = require('gulp-buffer')
const sourcemaps = require('gulp-sourcemaps')
const rename = require('gulp-rename')
const browserify = require('browserify')
const sveltify = require('sveltify')
const root = path.join(__dirname, '..')

gulp.task('build', function () {
  return gulp
    .src(path.join(root, 'js/profiles/**/*.svelte'), { read: false })
    .pipe(tap(function (file) {
      log.info('bundling ' + file.path)
      file.contents = browserify(file.path, {
        debug: true,
        standalone: file.basename,
        transform: [
          sveltify,
        ],
      }).bundle()
    }))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
    .pipe(rename(function (path) {
      path.extname = ".js"
    }))
    .pipe(gulp.dest(path.join(root, 'appyter', 'profiles')))
})
