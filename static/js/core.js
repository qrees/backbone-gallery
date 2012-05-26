define([
    'core/views',
    'core/models',
    'jQuery',
    'Underscore',
    'Backbone',
    'Reverse'
], function(views, models, $, _, Backbone){
    var app = {
        views: views,
        models: models
    };

    window.jssuper = function(_class, method){
        return function(self, arguments){
            return _class.__super__[method].call(self, arguments);
        };
    }

    Function.prototype.curry = function()
    {
        var method = this, args = Array.prototype.slice.call(arguments);
        return function()
        {
            return method.apply(this, args.concat(Array.prototype.slice.call(arguments)));
        };
    };

    return app;
});
