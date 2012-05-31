define([
    'jQuery',
    'Underscore',
    'Backbone',
    'core',
    req_tmpl('albums')
], function($, _, Backbone, Core, tmpl){
    var views = {};

    views.PhotoView = Core.views.ModelTemplateView.extend({
        template:tmpl['photo.html'],
        className : "photo"
    });

    views.PhotoCollectionView = Core.views.UpdatingCollectionView.extend({
        options: {
            childViewConstructor: views.PhotoView
        }
    });

    views.AlbumItem = Core.views.ModelTemplateView.extend({
        template:tmpl['album_item.html'],
        className : "album"
    });

    views.AlbumCollectionView = Core.views.UpdatingCollectionView.extend({
        options: {
            childViewConstructor: views.AlbumItem
        }
    });

    views.FilesLayout = Core.views.LayoutManager.extend({
        options: {
            views: {
                uploader: {
                    view: Core.views.UploadFileView,
                    view_args: {
                        item_template: tmpl['upload_file.html'],
                        template: tmpl['upload_form.html']
                    },
                    selector: '[data-ui=upload_form]'
                },
                file_list: {
                    view: Core.views.UploadFileView,
                    selector: '[data-ui=files]'
                }
            }
        }
    });

    return views;
});
