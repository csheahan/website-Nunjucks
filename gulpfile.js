var data = require('gulp-data');
var del = require('del');
var gulp = require('gulp');
var nunjucksRender = require('gulp-nunjucks-render');

// Source and destination locations
var srcDir = 'src'
var dropDir = 'public_html'

// Delete everything in drop except the placeholder .gitignore, if exists
gulp.task('clean', function(cb) {
  del(
    [
      dropDir + '/**/*',
      '!' + dropDir + '/.gitignore',
    ],
    cb);
});

// Copy css files to drop
gulp.task('css', function () {
  return gulp.src(srcDir + '/css/**/*.css')
    .pipe(gulp.dest(dropDir + '/css'));
});

// Render nunjuck files in src to drop
gulp.task('nunjucksRender', function () {
  return gulp.src(srcDir + '/pages/**/*.+(njk)')
    .pipe(nunjucksRender({ path: [srcDir + '/templates',] }))
    .pipe(gulp.dest(dropDir));
})

// Creates website in drop directory
gulp.task('website', ['nunjucksRender', 'css']);