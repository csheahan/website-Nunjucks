var data = require('gulp-data');
var del = require('del');
var gulp = require('gulp');
var nunjucksRender = require('gulp-nunjucks-render');
var exec = require('child_process').exec;

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


// Spellcheck html files
gulp.task('spellcheck', ['website'], function(cb) {
  var task = [
    'python',
    'scripts/spellcheck.py',
    '--word_lists=scripts/wordlists/*.txt',
    'public_html/*.html',
  ].join(' ');

  exec(task, function(err, stdout, stderr) {
    if (err) {
      console.log(err);
    }

    console.log(stdout);
    console.log(stderr);
  });
});

// Check links in html files
gulp.task('check404', ['website'], function(cb) {
  var task = [
    'python',
    'scripts/check404.py',
    'public_html/*.html',
  ].join(' ');

  exec(task, function(err, stdout, stderr) {
    if (err) {
      console.log(err);
    }

    console.log(stdout);
    console.log(stderr);
  });
});

// Run post validation on a website build
gulp.task(
  'validate',
  [
    'website',
    'spellcheck',
    'check404'
  ]);


// Copy css files to drop
gulp.task('css', function () {
  return gulp.src(srcDir + '/css/**/*.css')
    .pipe(gulp.dest(dropDir + '/css'));
});

// Copy font files to drop
gulp.task('font', function () {
  return gulp.src(srcDir + '/fonts/**/*')
    .pipe(gulp.dest(dropDir + '/fonts'));
});

// Copy image files to drop
gulp.task('img', function() {
  return gulp.src(srcDir + '/img/**/*')
    .pipe(gulp.dest(dropDir + '/img'));
});

// Copy js files to drop
gulp.task('js', function() {
  return gulp.src(srcDir + '/js/**/*.js')
    .pipe(gulp.dest(dropDir + '/js'));
});

// Copy resume to drop
gulp.task('resume', function() {
  return gulp.src(srcDir + '/resume/**/*.pdf')
    .pipe(gulp.dest(dropDir));
});

// Custom functions for nunjucks rendering
var requireJson = function(fileName) {
  return require('./' + srcDir + '/data/' + fileName +'.json')
}

var manageEnvironment = function(environment) {
  environment.addFilter('isArray', function(obj) {
    return Array.isArray(obj);
  });
}

// Render nunjuck files in src to drop
gulp.task('nunjucksRender', function () {
  return gulp.src(srcDir + '/pages/**/*.+(njk)')
    .pipe(data(requireJson('work')))
    .pipe(data(requireJson('projects')))
    .pipe(data(requireJson('school')))
    .pipe(data(requireJson('timeline')))
    .pipe(nunjucksRender({
      path: [srcDir + '/templates',],
      manageEnv: manageEnvironment,
    }))
    .pipe(gulp.dest(dropDir));
})

// Creates website in drop directory
gulp.task(
  'website',
  [
    'nunjucksRender',
    'css',
    'font',
    'js',
    'img',
    'resume',
  ]);