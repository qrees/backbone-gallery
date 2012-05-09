define([
    'jQuery',
    'Underscore',
    'Backbone',
    'core',
    req_tmpl('albums')
], function($, _, Backbone, Core, tmpl){
    var views = {};

    views.UploadFileView = Core.views.TemplateView.extend({
        template:tmpl['upload_file.html'],
        className : "upload-file"
    });

    views.PhotoView = Core.views.TemplateView.extend({
        template:tmpl['photo.html'],
        className : "photo"
    });

    views.AlbumView = Core.views.TemplateView.extend({
        template:tmpl['album.html'],
        className : "album"
    });

    views.AlbumCollectionView = Core.views.UpdatingCollectionView.extend({
        options: {
            childViewConstructor: views.AlbumView
        }
    });
    return views;
});
