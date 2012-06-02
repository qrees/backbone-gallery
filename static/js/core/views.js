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
        },
        remove: function(){
            this._rendered = false;
        },
        render: function(){
            this._rendered = true;
        }
    });

    views.TemplateView = views.BaseView.extend({
        options: {
            template: null
        },
        getContext: function(){
            return {};
        },
        render: function() {
            jssuper(views.TemplateView, 'render')(this, arguments);
            this.$el.empty();
            this.$el.append($.tmpl(this.options.template, this.getContext()));
            return this;
        }
    });

    views.ModelTemplateView = views.TemplateView.extend({
        getContext: function(){
            return this.model.toJSON();
        },
        action_select: function(){
            $(this.$el).trigger('item_selected', this.model);
        }
    });

    views.UpdatingCollectionView = views.BaseView.extend({
        events: {
            "item_selected": "_item_selected"
        },
        initialize : function(options) {
            _(this).bindAll('add', 'remove', 'reset', '_item_selected');

            if (!this.options.childViewConstructor) throw "no child view constructor provided";

            this._childViewConstructor = this.options.childViewConstructor;

            this._childViews = [];

            this.collection.each(this.add);

            this.collection.bind('add', this.add);
            this.collection.bind('remove', this.removeItem);
            this.collection.bind('reset', this.reset);
        },
        _item_selected: function(){
            console.log("item selected in updating collection view", arguments);
        },
        add: function(model) {
            var childView = new this._childViewConstructor({
                model: model,
                parent: this
            });

            this._childViews.push(childView);

            if (this._rendered) {
                this.$el.append(childView.render().$el);
            }
            //$(childView).bind('item_selected', this._item_selected);
        },
        reset: function(collection){
            _(collection.models).each(this.add);
        },
        removeItem: function(model){
            var viewToRemove = _(this._childViews).select(function(cv) { return cv.model === model; })[0];
            this._childViews = _(this._childViews).without(viewToRemove);
            viewToRemove.remove();
        },
        remove: function(model) {
            this.collection.unbind('add', this.add);
            this.collection.unbind('remove', this.removeItem);
            this.collection.unbind('reset', this.reset);
            _.each(this._childViews, this.removeItem);

            jssuper(views.UpdatingCollectionView, 'remove')(this, arguments);
        },
        render: function() {
            jssuper(views.UpdatingCollectionView, 'render')(this, arguments);
            var that = this;

            this.$el.empty();
            _(this._childViews).each(function(childView) {
                that.$el.append(childView.render().$el);
            });

            return this;
        }
    });

    views.LayoutManager = views.TemplateView.extend({
        /**
         *
         */
        options: {
            views: {
                /*
                name: {
                    view: Backbone.View,
                    collection: function(self){
                        return that.collection;
                    },
                    selector: function|text
                }
                 */
            }
        },
        initialize: function(){
            var self = this;
            self._views = {};
            _.each(this.options.views, function(name, partial){
                var collection;
                if(_.isFunction(partial.collection)){
                    collection = partial.collection(self);
                }
                if(_.isBoolean(partial.collection)){
                    if(partial.collection)
                        collection = self.collection;
                }
                if(_.isObject(partial.collection)){
                    collection = partial.collection
                }
                var view = new partial.view({collection:collection});
                self._views[name] = view;
            });
        },
        render: function(){
            var self = this;
            jssuper(this.LeyoutManager, 'render')(this, arguments);
            _.each(this._views, function(name, view){
                var $view_el = self.$el.find(self.options[name].selector);
                if($view_el.length === 1){
                    view.setElement($view_el);
                    view.render();
                }
                if($view_el.length === 0){
                    console.log("Cannot display", name," in ", self,". Element not found.");
                }
                if($view_el.length > 1){
                    console.log("Cannot display", name," in ", self,". Multiple elements found.");
                }
            });
        }
    });

    views.UploadFileView = views.TemplateView.extend({
        options:{
            item_template: null
        },
        initialize : function(options) {
            _(this).bindAll('add', 'done', 'progress', 'progressall', 'formData');
        },
        action_submit: function(){
            _.each(this._files, function(data){
                data.submit();
            });
        },
        formData: function(){
            return this.options.formData
        },
        add: function(event, data){
            var self = this;
            var files = data.files;
            var $list = this.$el.find('[data-ui=list]');
            _.each(files, function(file){
                var rendered = $.tmpl(self.options.item_template, file);
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
            jssuper(views.UploadFileView, 'render')(this, arguments);
            this.$el.find('input[type=file]').fileupload({
                dataType: 'json',
                add: this.add,
                done: this.done,
                progress: this.progress,
                progressall: this.progressall,
                formData: this.formData
            });
            this._files = [];
        }
    });

    return views;
});
