var del = require('del');
var gulp = require('gulp');
var nunjucksRender = require('gulp-nunjucks-render');

// Delete everything in public_html except the placeholder .gitignore
gulp.task('clean', function(cb) {
  del(
    [
      'public_html/**/*',
      '!public_html/.gitignore',
    ],
    cb);
});

// Renders website in src and outputs files to public_html folder
gulp.task('nunjucks', function() {
  return gulp.src('src/pages/**/*.+(njk)')
    .pipe(nunjucksRender({ path: ['src/templates',] }))
    .pipe(gulp.dest('public_html'))
});