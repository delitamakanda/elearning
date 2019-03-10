var gulp        = require('gulp'),
    gulpif      = require('gulp-if'),
    browserSync = require('browser-sync'),
    sass        = require('gulp-sass'),
    prefix      = require('gulp-autoprefixer'),
    imagemin    = require('gulp-imagemin'),
    reload      = browserSync.reload,
    plumber     = require('gulp-plumber'),
    uglify      = require('gulp-uglify'),
    concatJs    = require('gulp-concat'),
    folders     = require('gulp-folders'),
    path        = require('path'),
    sourcemaps = require('gulp-sourcemaps'),
    iconfont = require('gulp-iconfont'),
    consolidate = require('gulp-consolidate');

function onError(err) {
    console.log(err);
}

var paths = {
    sassSrc:        './scss/',
    cssDir:         '../courses/static/styles/',
    imgSrc:         './images/',
    imgDir:         '../courses/static/images/',
    jsCoreSrc:      './scripts/',
    jsDir:          '../courses/static/scripts/',
    jsLibSrc:       './scripts/libs/',
    jsLibDir:       '../courses/static/scripts/libs/',
    tplSrc:         '../courses/templates/'
}


gulp.task('serve', ['sass'], function() {
    browserSync({
        open: false,
        proxy: "http://localhost:8000/"
    });
    gulp.watch(paths.sassSrc+'*.scss', ['sass']);
    gulp.watch(paths.sassSrc+'/**/*.scss', ['sass']);
    gulp.watch(paths.jsCoreSrc+'/**/*.js', ['compressCoreJs']);
    gulp.watch(paths.tplSrc+'/**/*.html').on('change', reload);
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

// Compile Sass
gulp.task('sass', function () {
    return gulp.src([paths.sassSrc+'styles.scss'])
    .pipe(sourcemaps.init())
    .pipe(sass({
        outputStyle: 'compressed',
        //outputStyle: 'nested',
        sourceComments: 'normal',
        errLogToConsole: true,
        includePaths : [paths.sassSrc]
    }))
    .pipe(prefix(
        'safari 5', 'ie 8', 'ie 9', 'opera 12.1', 'ios 6', 'android 4'
    ))
    //.pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.cssDir))
    .pipe(plumber({
        errorHandler: onError
    }))
    .pipe(reload({stream: true}))
});

// Compile JS
gulp.task('compressCoreJs', function() {
   return gulp.src(paths.jsCoreSrc+'*.js')
    .pipe(concatJs('main.min.js'))
    //.pipe(uglify())
    .pipe(gulp.dest(paths.jsDir))
    .pipe(reload({stream: true}))
});

// Compile Lib JS
gulp.task('compressLibJs', function() {
   return gulp.src(paths.jsLibSrc+'/**/*.min.js')
    .pipe(uglify())
    .pipe(gulp.dest(paths.jsLibDir))
    .pipe(reload({stream: true}))
});

// Generate IMG
gulp.task('images', function() {
   return gulp.src(paths.imgSrc)
    .pipe(imagemin())
    .pipe(gulpif('*.png', gulp.dest(paths.imgDir)))
    .pipe(gulpif('*.svg', gulp.dest(paths.imgDir)))
    .pipe(gulpif('*.jpg', gulp.dest(paths.imgDir)))
    .pipe(gulpif('*.gif', gulp.dest(paths.imgDir)))
    .pipe(reload({stream: true}))
});

gulp.task('sprites', ['images']);
gulp.task('default', ['serve', 'sprites', 'sass', 'compressCoreJs', 'compressLibJs']);
