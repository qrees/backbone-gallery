/**
 * Created with PyCharm.
 * User: qrees
 * Date: 4/19/12
 * Time: 12:22 AM
 * To change this template use File | Settings | File Templates.
 */

require.config({
    paths: {
        jQuery: 'jquery',
        Underscore: 'underscore',
        Backbone: 'backbone'
    }
});

require(['albums',
    'order!jquery/jquery-1.7.2',
    'order!underscore/underscore',
    'order!backbone/backbone'], function(albums_app){

    function log(){
        console.log(arguments);
    }
    var albums = new albums_app.models.Albums();
    albums.bind('add', log);
    albums.bind('refresh', log);
    albums.bind('all', log);
    albums.fetch();

    console.log("Main loaded");
});
