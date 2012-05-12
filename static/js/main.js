/**
 * Created with PyCharm.
 * User: qrees
 * Date: 4/19/12
 * Time: 12:22 AM
 * To change this template use File | Settings | File Templates.
 */

require.config({
    paths: {
        jQuery: 'jquery',
        Underscore: 'underscore',
        Backbone: 'backbone',
        Reverse: '/reverse',
        'jquery.ui.widget': 'jquery-file-upload/vendor/jquery.ui.widget'
    }
});

require(['albums/views',
    'albums/models',
    'core',
    req_tmpl('albums'),
    'order!jquery/jquery-1.7.2',
    'order!jquery/jquery.tmpl',
    'order!underscore/underscore',
    'order!backbone/backbone',
    'order!jquery-file-upload/jquery.fileupload'],
function(views, models, Core, tmpl){
    var $ = require('jQuery');
    var Backbone = require('Backbone');
    var _ = require('Underscore');

    function log(){
        console.log(arguments);
    }
    var albums = new models.Albums();
    albums.bind('all', log);

    var albums_view = new views.AlbumCollectionView({
        collection: albums
    });
    albums_view.setElement($('[data-ui=albums]'));
    albums_view.render();
    albums.fetch();

    var upload_view = new Core.views.UploadFileView({
        template: tmpl['upload_file.html'],
        el:$('[data-ui=upload]')
    });
    upload_view.render();
});
