define([
    'jQuery',
    'Underscore'
], function($, _){
    var path = "{{ request.GET.path }}";
    var templates = {{ templates|safe }};
    var compilled = {};
    _.each(templates, function(template, name){
        compilled[name] = $.template(name, template);
    });
    return compilled;
});
