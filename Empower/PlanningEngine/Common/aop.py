from functools import wraps
import inspect
from Common.config import logging

LOG = logging.getLogger(__name__)


def get_value(parameter, parameters, arg_dict):
    if '.' in parameter:
        ob = parameter.split('.')[0]
        atr = parameter.split('.')[1]
        if ob in parameters:
            del parameters[ob]
        value = getattr(arg_dict[ob], atr)
        new_para = '.'.join(parameter.split('.')[1:])
        arg_dict[atr] = value
        return get_value(new_para, parameters, arg_dict)
    else:
        return arg_dict[parameter]


def before(args_to_track=None):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kws):
            if args_to_track:
                object_args = [arg.split('.')[0] for arg in args_to_track]
                param_names = inspect.signature(fn).parameters.keys()
                arg_dict = dict(tuple(zip(param_names, args)))
                parameters = {k: arg_dict[k] for k in param_names if k in object_args}
                for k in args_to_track:
                    parameters[k] = get_value(k, parameters, arg_dict)
                LOG.debug('about to call function %s with parameters %s' % (fn.__name__, parameters))
            else:
                LOG.debug('about to call function %s' % fn.__name__)
            return fn(*args, **kws)

        return wrapped

    return decorator


def after(fn):
    @wraps(fn)
    def wrapped(*args, **kws):
        retVal = fn(*args, **kws)
        LOG.debug('just returned from function %s' % fn.__name__)
        return retVal

    return wrapped
