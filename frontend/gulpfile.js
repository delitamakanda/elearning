var gulp            = require('gulp'),
    gulpif          = require('gulp-if'),
    prefix          = require('gulp-autoprefixer'),
    autoprefixer    = require('autoprefixer'),
    browserSync     = require('browser-sync'),
    sourcemaps      = require('gulp-sourcemaps'),
    imagemin        = require('gulp-imagemin'),
    plumber         = require('gulp-plumber'),
    uglify          = require('gulp-uglify'),
    concatJs        = require('gulp-concat'),
    path            = require('path'),
    iconfont        = require('gulp-iconfont'),
    consolidate     = require('gulp-consolidate'),
    postcss         = require("gulp-postcss"),
    cssnano         = require("cssnano"),
    rename          = require('gulp-rename'),
    tailwindcss     = require('tailwindcss'),
    sass            = require('gulp-sass');

function onError(err) {
    console.log(err);
}

var browserSync = require("browser-sync").create();

function reload() {
    browserSync.reload();
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
        jsCoreSrc: './scripts/',
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
    //.pipe(prefix(
        //'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'
    //))
    .pipe(postcss([
        tailwindcss('tailwind.config.js'),
        autoprefixer(), 
        cssnano()
    ]))
    .pipe(sourcemaps.write())
    .pipe(plumber({
        errorHandler: onError
    }))
    .pipe(gulp.dest(paths.sass.dest))
    .pipe(browserSync.stream())
});

// Compile JS
gulp.task('compressCoreJs', function () {
   return gulp.src(paths.js.jsCoreSrc + '*.js')
    .pipe(concatJs('main.js'))
    .pipe(gulp.dest(paths.js.jsDir))
    .pipe(rename('main.min.js'))
    //.pipe(uglify())
    .pipe(gulp.dest(paths.js.jsDir))
    .pipe(browserSync.stream())
});

// Compile Lib JS
gulp.task('compressLibJs', function () {
   return gulp.src(paths.vendors.jsLibSrc+'/**/*.min.js')
    .pipe(uglify())
    .pipe(gulp.dest(paths.vendors.jsLibDir))
    .pipe(browserSync.stream())
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
    return gulp.src('icons/**/*.svg')
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

gulp.task('serve', function () {

    browserSync.init({
        open: false,
        proxy: "http://localhost:8000/"
    });
});

// ---------------------------------------------- Gulp Watch
gulp.task('watch:styles', function () {
  gulp.watch('./scss/' + '*.scss', gulp.series('sass'));
});

gulp.task('watch:scripts', function () {
  gulp.watch('./scripts/' + '**/*.js', gulp.series('compressCoreJs'));
});

gulp.task('watch:libs', function () {
  gulp.watch('./scripts/libs/' + '*.js', gulp.series('compressLibJs'));
});

gulp.task('watch:images', function () {
    gulp.watch(paths.images.imgSrc +'**/*.{gif,jpeg,jpg,png}', gulp.series('images'));
})

gulp.task('watch:templates', function () {
    gulp.watch(paths.tplSrc+'**/*.html').on('change', reload);
})

gulp.task('watch', gulp.series('sass', 'compressCoreJs', 'compressLibJs', 'images',
  gulp.parallel('watch:styles', 'watch:scripts', 'watch:libs', 'watch:images','watch:templates')
));


// -------------------------------------------- Default task
gulp.task('default', gulp.parallel('watch', 'serve', 'compressCoreJs', 'compressLibJs', 'images'));
