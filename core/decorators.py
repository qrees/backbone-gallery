import functools
import collections
from django import http
from django.db import transaction

import logging
logger = logging.getLogger("smartlead.commons")

def manualcache(method):
    cache_name = "__%s__cache" % method.__name__

    @property
    def cached_method(self):
        value = getattr(self, cache_name, None)
        return value if value is not None else method(self)

    @cached_method.setter
    def cached_method(self, value):
        setattr(self, cache_name, value)

    @cached_method.deleter
    def cached_method(self):
        setattr(self, cache_name, None)

    return cached_method

def decorator_with_kwargs(decorator):
    """
        There are many techniques to produce decorators that can be used with
        arguments and without them. Accepting only keyword arguments is the simples, IMHO.

        >>> def execution_decorator(view, opts):
        ...     return view(**opts)
        ...
        >>> def format_kwargs(**kwargs):
        ...     return "ARGS: %r" % kwargs
        ...
        >>> decorator_with_kwargs(execution_decorator)(format_kwargs)
        "ARGS: {}"

        >>> decorator_with_kwargs(execution_decorator)()(format_kwargs)
        "ARGS: {}"

        >>> decorator_with_kwargs(execution_decorator)(a=True, b='')(format_kwargs)
        "ARGS: {'a': True, 'b': ''}"

    """
    @functools.wraps(decorator)
    def kwargs_decorator(*args, **kwargs):
        if len(args) > 1:
            raise ValueError("This decorator accepts only keyword arguments.")
        if len(args) == 1:  # No arguments
            if not isinstance(args[0], collections.Callable):
                raise ValueError("This decorator accepts only keyword arguments.")
            return decorator(args[0], {})
        return functools.wraps(decorator)(lambda * a: decorator(* (a + (kwargs,))))
    return kwargs_decorator


class classonlymethod(classmethod):
    def __get__(self, instance, owner):
        if instance is not None:
            raise AttributeError("This method is available only on the view class.")
        return super(classonlymethod, self).__get__(instance, owner)

def view_decorator(fdec, subclass=False):
    """
    Change a function decorator into a view decorator.

    This is a simplest approach possible. `as_view()` is replaced, so
    that it applies the given decorator before returning.

    In this approach, decorators are always put on top - that means it's not
    possible to have functions called in this order:

       B.dispatch, login_required, A.dispatch

    NOTE: By default this modifies the given class, so be careful when doing this:

       TemplateView = view_decorator(login_required)(TemplateView)

    Because it will modify the TemplateView class. Instead create a fresh
    class first and apply the decorator there. A shortcut for this is
    specifying the ``subclass`` argument. But this is also dangerous. Consider:

        @view_decorator(login_required, subclass=True)
        class MyView(View):

            def get_context_data(self):
                data = super(MyView, self).get_context_data()
                data["foo"] = "bar"
                return data

    This looks like a normal Python code, but there is a hidden infinite
    recursion, because of how `super()` works in Python 2.x; By the time
    `get_context_data()` is invoked, MyView refers to a subclass created in
    the decorator. super() looks at the next class in the MRO of MyView,
    which is the original MyView class we created, so it contains the
    `get_context_data()` method. Which is exactly the method that was just
    called. BOOM!
    """
    def decorator(cls):
        if subclass:
            cls = type("%sWithDecorator(%s)" % (cls.__name__, fdec.__name__), (cls,), {})
        original = cls.as_view.im_func
        @functools.wraps(original)
        def as_view(current, **initkwargs):
            return fdec(original(current, **initkwargs))
        cls.as_view = classonlymethod(as_view)
        return cls
    return decorator

@decorator_with_kwargs
def deprecated(func, options):
    import warnings
    options = dict({"extra_message": ""}, **options)
    @functools.wraps(func)
    def deprecated_func(*args, **kwargs):
        warnings.warn("Function %s is deprecated.%s" % (func.__name__, options["extra_message"]),
                DeprecationWarning, stacklevel=2)
        return func(*args, **kwargs)
    # warnings.warn("Definition of deprecated function: %s" % func.__name__, DeprecationWarning, stacklevel=3)
    return deprecated_func

