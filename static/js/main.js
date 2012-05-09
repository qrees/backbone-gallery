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
        Backbone: 'backbone',
        Reverse: '/reverse',
        'jquery.ui.widget': 'jquery-file-upload/vendor/jquery.ui.widget'
    }
});

require(['albums/views',
    'albums/models',
    'core',
    req_tmpl('albums'),
    'order!jquery/jquery-1.7.2',
    'order!jquery/jquery.tmpl',
    'order!underscore/underscore',
    'order!backbone/backbone',
    'order!jquery-file-upload/jquery.fileupload'],
function(views, models, Core, tmpl){
    var $ = require('jQuery');
    var Backbone = require('Backbone');
    var _ = require('Underscore');

    function log(){
        console.log(arguments);
    }
    var albums = new models.Albums();
    albums.bind('all', log);

    var albums_view = new views.AlbumCollectionView({
        collection: albums
    });
    albums_view.setElement($('[data-ui=albums]'));
    albums_view.render();
    albums.fetch();

    var BaseView = Backbone.View.extend({
        events: {
            "click [data-action]": "_action"
        },
        _action: function(event){
            var $target = $(event.currentTarget);
            var action = "action_"+$target.data('action');
            if(action in this){
                this[action](event, $target);
            }else{
                console.error("Cannot find handler for action ", action, " in ", this);
            }
        }
    });

    var UploadFileView = BaseView.extend({
        template: tmpl['upload_file.html'],
        initialize : function(options) {
            _(this).bindAll('add', 'done', 'progress', 'progressall');
        },
        action_submit: function(){
            _.each(this._files, function(data){
                data.submit();
            });
        },
        add: function(event, data){
            var self = this;
            //console.log(arguments);
            var files = data.files;
            var $list = this.$el.find('[data-ui=list]');
            _.each(files, function(file){
                var rendered = $.tmpl(self.template, file);
                $list.append(rendered);
                file['$el'] = rendered;
            });
            this._files.push(data);
        },
        done: function (e, data) {
            $.each(data.result, function (index, file) {
                $('<p/>').text(file.name).appendTo(this.$el);
            });
        },
        progress: function(e, data){
            var file = data.files[0];
            var $progress = file.$el.find('[data-ui=progress]');
            var progress = parseInt(data.loaded / data.total * 100, 10);
            $progress.find('.bar').css('width', progress.toString() + "%");
            console.log("progress", file.name, progress);
        },
        progressall: function(e, data){
            console.log("progressall", parseInt(data.loaded / data.total * 100, 10));
        },
        render: function(){
            this.$el.find('input[type=file]').fileupload({
                dataType: 'json',
                add: this.add,
                done: this.done,
                progress: this.progress,
                progressall: this.progressall
            });
            this._files = [];
        }
    });

    var upload_view = new UploadFileView({
        el:$('[data-ui=upload]')
    });
    upload_view.render();
    /*
    $(function () {
        $('#fileupload').fileupload({
            dataType: 'json',
            add: function(e, data){
                console.log(arguments);
            },
            done: function (e, data) {
                $.each(data.result, function (index, file) {
                    $('<p/>').text(file.name).appendTo(document.body);
                });
            }
        });
    });
    */
});
