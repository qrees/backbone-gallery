define([
    'jQuery',
    'Underscore',
    'Backbone',
    'core',
    req_tmpl('albums')
], function($, _, Backbone, Core, tmpl){
    var views = {};

    views.PhotoView = Core.views.TemplateView.extend({
        template:tmpl['photo.html'],
        className : "photo"
    });

    views.AlbumItem = Core.views.TemplateView.extend({
        template:tmpl['album_item.html'],
        className : "album"
    });

    views.AlbumCollectionView = Core.views.UpdatingCollectionView.extend({
        options: {
            childViewConstructor: views.AlbumItem
        },
        render: function(){
            jssuper(views.AlbumCollectionView, 'render')(this, arguments);
        }
    });

    views.AlbumDetailsView = Core.views.LayoutManager.extend({
        options: {
            views: {
                uploader: {
                    view: Core.views.UploadFileView,
                    collection: function(layout){
                        return layout.model.photo_collection();
                    }
                },
                photo_list: {

                }
            }
        }
    });

    return views;
});
