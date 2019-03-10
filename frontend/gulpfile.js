var gulp        = require('gulp'),
    gulpif      = require('gulp-if'),
    prefix      = require('gulp-autoprefixer'),
    browserSync = require('browser-sync'),
    sourcemaps  = require('gulp-sourcemaps'),
    imagemin    = require('gulp-imagemin'),
    plumber     = require('gulp-plumber'),
    uglify      = require('gulp-uglify'),
    concatJs    = require('gulp-concat'),
    path        = require('path'),
    iconfont    = require('gulp-iconfont'),
    consolidate = require('gulp-consolidate'),
    sass        = require('gulp-sass');

function onError(err) {
    console.log(err);
}

var paths = {
    sass: {
        src: './scss/styles.{scss,sass}',
        dest: '../courses/static/styles/',
        opts: {}
    },
    images: {
        imgSrc: './images/',
        imgDir: '../courses/static/images/',
    },
    js: {
        jsCoreSrc: './scripts/*.{js}',
        jsDir: '../courses/static/scripts/',
    },
    vendors: {
        jsLibSrc: './scripts/libs/',
        jsLibDir: '../courses/static/scripts/libs/',
    },
    tplSrc: '../courses/templates/'
};

// ---------------------------------------------- Gulp Tasks
gulp.task('sass', function () {
  return gulp.src(paths.sass.src)
    .pipe(sourcemaps.init())
    .pipe(sass({
        outputStyle: 'compressed',
        sourceComments: 'normal',
        errLogToConsole: true
    }).on('error', sass.logError))
    .pipe(prefix(
        'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'
    ))
    .pipe(plumber({
        errorHandler: onError
    }))
    .pipe(gulp.dest(paths.sass.dest))
});

// Compile JS
gulp.task('compressCoreJs', function() {
   return gulp.src(paths.js.jsCoreSrc)
    .pipe(concatJs('main.min.js'))
    .pipe(gulp.dest(paths.js.jsDir))
});

// Compile Lib JS
gulp.task('compressLibJs', function() {
   return gulp.src(paths.vendors.jsLibSrc+'/**/*.min.js')
    .pipe(uglify())
    .pipe(gulp.dest(paths.vendors.jsLibDir))
});

// Generate IMG
gulp.task('images', function() {
   return gulp.src(paths.images.imgSrc)
    .pipe(imagemin())
    .pipe(gulpif('*.png', gulp.dest(paths.images.imgDir)))
    .pipe(gulpif('*.svg', gulp.dest(paths.images.imgDir)))
    .pipe(gulpif('*.jpg', gulp.dest(paths.images.imgDir)))
    .pipe(gulpif('*.gif', gulp.dest(paths.images.imgDir)))
});

gulp.task('iconfont', function () {
    gulp.src('icons/**/*.svg')
    .pipe(iconfont({
        fontName: 'custom',
        centerHorizontally: true,
        normalize: true,
        prependUnicode: true,
        fontHeight: 1001
    })).on('glyphs', function (glyphs) {
    gulp.src('scss/templates/_icons.scss')
        .pipe(consolidate('lodash', {
            glyphs: glyphs,
            fontName: 'custom',
            fontPath: '../fonts/custom/',
            className: 'icon'
        }))
        .pipe(gulp.dest('scss'));
    })
    .pipe(gulp.dest('../courses/static/fonts/custom'));
});

// ---------------------------------------------- Gulp Watch
gulp.task('watch:styles', function () {
  gulp.watch('./scss/' + '*.scss', gulp.series('sass'));
});

gulp.task('watch', gulp.series('sass',
  gulp.parallel('watch:styles')
));


// -------------------------------------------- Default task
gulp.task('default', gulp.series('sass',
  gulp.parallel('watch')
));
