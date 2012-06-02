define([
    'core/views',
    'core/models',
    'jQuery',
    'Underscore',
    'Backbone',
    'Reverse',
    'order!jquery/jquery-1.7.2',
    'order!jquery/jquery.cookies'
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
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function safeMethod(method) {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            if (!safeMethod(settings.type) ) {
                xhr.setRequestHeader("X-CSRFToken", $.cookies.get('csrftoken'));
            }
        }
    });

    return app;
});
