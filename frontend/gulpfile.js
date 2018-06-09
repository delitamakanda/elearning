var gulp = require('gulp');
var sass = require('gulp-sass');
var iconfont = require('gulp-iconfont');
var consolidate = require('gulp-consolidate');
var imagemin = require('gulp-imagemin');

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

gulp.task('sass', function () {
    gulp.src('scss/**/*.scss')
    .pipe(sass({
      indentWidth: 4,
      outputStyle: 'compact'
    }))
    .pipe(gulp.dest('../courses/static/styles'));
});

gulp.task('image', function() {
    gulp.src('images/*')
    .pipe(imagemin([
        imagemin.gifsicle({interlaced: true}),
        imagemin.jpegtran({progressive: true}),
        imagemin.optipng({optimizationLevel: 5}),
        imagemin.svgo({
        plugins: [
            { removeViewBox: true },
            { cleanupIDs: false }
        ]
    })
    ]))
    .pipe(gulp.dest('../courses/static/images'));
});

gulp.task('watch', function() {
    gulp.watch('scss/**/*.scss', ['sass'])
})

gulp.task('default', ['sass'], function () {
    gulp.watch('scss/**/*.scss', ['sass', 'watch']);
});
