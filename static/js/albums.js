define([
    'jQuery',
    'Underscore',
    'Backbone',
    'core',
    '/templates.js?path='
], function($, _, Backbone, Core){
    var models = {};
    var views = {};
    var app = {
        models: models,
        views: views
    };

    models.Album = Backbone.Model.extend({
        url: function(){
            if (this.uuid){
                return urlreverse('albums-item', {'uuid': this.uuid});
            }else{
                return this.collection.url;
            }
        },
        parse: function(obj){
            return obj.fields;
        }
    });

    models.Albums = Backbone.Collection.extend({
        model: models.Album,
        url: urlreverse('albums-list')
    });

    views.AlbumView = Backbone.View.extend({
        className : "album",
        render : function() {
            this.$el.empty();
            this.$el.append($.tmpl('album.html', this.model.toJSON()));
            return this;
        }
    });

    views.AlbumCollectionView = Core.views.UpdatingCollectionView.extend({
        options: {
            childViewConstructor: views.AlbumView
        }
    });
    return app;
});
