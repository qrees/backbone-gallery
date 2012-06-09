define([
    'jQuery',
    'Underscore',
    'Backbone',
    'Reverse'
], function($, _, Backbone){
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
        },
        parse: function(obj){
            if(!_.isObject(obj.fields)){
                console.error("malformed object", obj);
            }
            return obj.fields;
        }
    });

    return models;
});
