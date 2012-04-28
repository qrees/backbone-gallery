require([
    'jQuery',
    'Underscore'
], function($, _){
    var path = "{{ request.GET.path }}";
    var templates = {{ templates|safe }};
    _.each(templates, function(template, name){
        $.template(name, template);
    })
});
