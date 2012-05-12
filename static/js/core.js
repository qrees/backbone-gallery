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
