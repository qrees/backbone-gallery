define([
    'jQuery',
    'Underscore',
    'Backbone'
], function($, _, Backbone){
    var views = {}, models = {};
    var app = {
        views: views,
        models: models
    };

    views.UpdatingCollectionView = Backbone.View.extend({
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
        add : function(model) {
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

    return app;
});