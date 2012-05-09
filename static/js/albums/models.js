define([
    'jQuery',
    'Underscore',
    'Backbone',
    'core'
], function($, _, Backbone, Core, tmpl){
    var models = {};

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
    return models;
});
