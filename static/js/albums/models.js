define([
    'jQuery',
    'Underscore',
    'Backbone',
    'core'
], function($, _, Backbone, Core, tmpl){
    var models = {};
/*
    models.BaseModel = Backbone.Model.extend({
        name: 'BaseModel',
        view_name: null,
        idAttribute: 'uuid',
        url: function(){
            if (this.uuid){
                return urlreverse(this.view_name, {'uuid': this.uuid});
            }else{
                return this.collection.url;
            }
        }
    });
*/
    models.BaseCollection = Backbone.Collection.extend({
        name: 'BaseCollection',
        initialize: function(elements, options){
            /*
            if(_.isObject(this.options.filters)){
                this._filters = _.clone(this.options.filters);
            }else{
                this._filters = {};
            }*/
            this._filters = {};
        },
        filter: function(filters){
            var self = this;
            _.each(filters, function(value, name){
                self._filters[name] = value;
            });
        }
    });

    models.Photo = Core.models.BaseModel.extend({
        view_name: 'file-item'
    });

    models.PhotoCollection = models.BaseCollection.extend({
        model: models.Photo,
        url: urlreverse('file-list')
    });

    models.Album = Core.models.BaseModel.extend({
        view_name: 'album-item',
        fileCollection: function(){
            if(!this.id){
                console.error("Album id is not available");
                throw new Error("Album id is not available");
            }
            var photo_list = new models.PhotoCollection();
            photo_list.filter({'album_id': this.id});
            return photo_list;
        }
    });

    models.AlbumCollection = models.BaseCollection.extend({
        model: models.Album,
        url: urlreverse('album-list')
    });
    return models;
});
