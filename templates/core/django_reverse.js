/*
 * URL reverse for django URL resolver.
 */
(function() {
    var reverse_dict = {{ reverse_dict|safe }};
    var PYTHON_RE = /%\((\w+)\)s/g;
    function python_format(string, params) {
        params = params || {};
        return string.replace(PYTHON_RE, function(m) {
            var m = m.slice(2, -2);
            if(params[m] == undefined)
                throw "Missing attribute '" + m + "'";
            return params[m];
        })
    };

    window.urlreverse = function(view_name, args) {
        var posibilities = reverse_dict[view_name] || [];
        for(var pi=0; pi < posibilities.length; pi++) {
            var p = posibilities[pi];
            for(var i=0; i < p.opts.length; i++) {
                try {
                    return '/' + python_format(p.opts[i], args);
                }
                catch(e) {
                    // console.debug("Args didn't match option", p.opts[i], args);
                }
            };
        };
        throw new Error("Failed to reverse view: " + view_name, " with arguments: ", args);
    };

    window.absolute_url = function absolute_url(path) {
        return "{{ settings.USE_SSL|yesno:'https,http' }}://{{ HOST_NAME }}"+path;
    };
})();