define([
    'jQuery',
    'Underscore',
    'Backbone',
    'Reverse'
], function($, _, Backbone){
    var views = {};

    views.BaseView = Backbone.View.extend({
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

    views.TemplateView = views.BaseView.extend({
        template: null,
        render: function() {
            this.$el.empty();
            this.$el.append($.tmpl(this.template, this.model.toJSON()));
            return this;
        }
    });

    views.UpdatingCollectionView = views.BaseView.extend({
        initialize : function(options) {
            _(this).bindAll('add', 'remove', 'reset');

            if (!this.options.childViewConstructor) throw "no child view constructor provided";

            this._childViewConstructor = this.options.childViewConstructor;

            this._childViews = [];

            this.collection.each(this.add);

            this.collection.bind('add', this.add);
            this.collection.bind('remove', this.remove);
            this.collection.bind('reset', this.reset);
        },
        add: function(model) {
            var childView = new this._childViewConstructor({
                model : model
            });

            this._childViews.push(childView);

            if (this._rendered) {
                this.$el.append(childView.render().$el);
            }
        },
        reset: function(collection){
            _(collection.models).each(this.add);
        },
        remove: function(model) {
            var viewToRemove = _(this._childViews).select(function(cv) { return cv.model === model; })[0];
            this._childViews = _(this._childViews).without(viewToRemove);

            if (this._rendered) $(viewToRemove.$el).remove();
        },
        render: function() {
            var that = this;
            this._rendered = true;

            this.$el.empty();
            _(this._childViews).each(function(childView) {
                that.$el.append(childView.render().$el);
            });

            return this;
        }
    });

    views.UploadFileView = views.BaseView.extend({
        options:{
            template: null
        },
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
            var files = data.files;
            var $list = this.$el.find('[data-ui=list]');
            _.each(files, function(file){
                var rendered = $.tmpl(self.options.template, file);
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
                progressall: this.progressall,
            });
            this._files = [];
        }
    });

    return views;
});
