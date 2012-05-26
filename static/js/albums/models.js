define([
    'jQuery',
    'Underscore',
    'Backbone',
    'core'
], function($, _, Backbone, Core, tmpl){
    var models = {};

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

    models.BaseCollection = Backbone.Collection.extend({
        name: 'BaseCollection',
        initialize: function(){
            if(_.isObject(this.options.filters)){
                this._filters = _.clone(this.options.filters);
            }else{
                this._filters = {};
            }
        },
        filter: function(filters){
            _.each(filters, function(name, value){

            });
        }
    });

    models.Photo = models.BaseModel.extend({
        view_name: 'file-item'
    });

    models.PhotoCollection = Backbone.Collection.extend({
        model: models.Photo,
        url: urlreverse('file-list')
    });

    models.Album = models.BaseModel.extend({
        view_name: 'album-item',
        parse: function(obj){
            return obj.fields;
        },
        photo_collection: function(){
            if(!this.uuid){
                console.error("Album id is not available");
                throw new Error("Album id is not available");
            }
            var photo_list = models.PhotoCollection.make();
            photo_list.filter({'album_id': this.uuid});
            return photo_list;
        }
    });

    models.Albums = Backbone.Collection.extend({
        model: models.Album,
        url: urlreverse('album-list')
    });
    return models;
});
