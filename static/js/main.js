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

require(['app',
    'order!jquery/jquery-1.7.2',
    'order!underscore/underscore',
    'order!backbone/backbone'], function(){
    console.log("Main loaded");
});
