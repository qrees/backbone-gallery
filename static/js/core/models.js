define([
    'jQuery',
    'Underscore',
    'Backbone',
    'Reverse'
], function($, _, Backbone){
    var models = {};

    models.Model = Backbone.Model.extend({
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

    return models;
});
