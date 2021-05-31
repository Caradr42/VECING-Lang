import array

DEBUG_MODE = False

INITIAL_ADDRESS = 1000

GLOBAL_SIZE = 9000
LOCAL_SIZE = 10000
TEMPORAL_SIZE = 50000
LIST_SIZE = 50000
TEMPORAL_LIST_SIZE = 50000
STACK_SIZE = 50000

GLOBAL_FIRST = INITIAL_ADDRESS
LOCAL_FIRST = GLOBAL_FIRST + GLOBAL_SIZE
TEMPORAL_FIRST = LOCAL_FIRST + LOCAL_SIZE
LIST_FIRST = TEMPORAL_FIRST + TEMPORAL_SIZE
TEMPORAL_LIST_FIRST = LIST_FIRST + LIST_SIZE
LIMITS = {
    'GLOBAL_LIM_L':     GLOBAL_FIRST,
    'GLOBAL_LIM_R':     GLOBAL_FIRST + GLOBAL_SIZE - 1,
    'LOCAL_LIM_L':      LOCAL_FIRST,
    'LOCAL_LIM_R':      LOCAL_FIRST + LOCAL_SIZE - 1,
    'TEMPORAL_LIM_L':   TEMPORAL_FIRST,
    'TEMPORAL_LIM_R':   TEMPORAL_FIRST + TEMPORAL_SIZE - 1,
    'LIST_LIM_L':       LIST_FIRST,
    'LIST_LIM_R':       LIST_FIRST + LIST_SIZE - 1,
    'TEMPORAL_LIST_LIM_L':  TEMPORAL_LIST_FIRST,
    'TEMPORAL_LIST_LIM_R':  TEMPORAL_LIST_FIRST + TEMPORAL_LIST_SIZE - 1,
    'STACK_SIZE':  STACK_SIZE
}

semanticTable = {
    "cond":     ((tuple,), (tuple,)),       #
    "add":      ((tuple, tuple), (tuple,)), # ("add", ((1, None), (2, None)))
    "sub":      ((tuple, tuple), (tuple,)), #
    "mult":     ((tuple, tuple), (tuple,)), #
    "power":    ((tuple, tuple), (tuple,)), #
    "div":      ((tuple, tuple), (tuple,)), #
    "sqrt":     ((tuple,), (tuple,)),       #
    "abs":      ((tuple,), (tuple,)),       #
    "<=":       ((tuple, tuple), (bool,)),  #
    ">=":       ((tuple, tuple), (bool,)),  #
    "<":        ((tuple, tuple), (bool,)),  #
    ">":        ((tuple, tuple), (bool,)),  #
    "!=":       ((tuple, tuple), (bool,)),  #
    "=":        ((tuple, tuple), (bool,)),  #
    "map":      ((tuple, tuple), (tuple,)),
    "apply":    ((tuple, tuple), (tuple,)),
    "print":    ((tuple,), (None,)),        #
    "car":      ((tuple,), (tuple,)),       #
    "cdr":      ((tuple,), (tuple,)),       #
    "append":   ((tuple, tuple), (tuple,)),
    "and":      ((tuple, tuple), (tuple,)), #
    "or":       ((tuple, tuple), (tuple,)), #
    "not":      ((tuple,), (tuple,)),       #
    "empty":    ((tuple,), (bool,)),        #
    "single":   ((tuple,), (bool,)),        #
    "elemCount":((tuple,), (tuple,)),       #
    "lenght":   ((tuple,), (tuple,)),       #
    "screen":   ((array.array, (array.array, tuple)), (None,)),
    "pixel":    ((array.array, array.array), (None,)),
    "pixels":   ((array.array, array.array), (None,)),
    "getPixels": ((None,), (None,)),
    "background": ((array.array,), (None,)),
    "clear":    ((None,), (None,)),
    "timeStep": ((None,), (tuple,)),
    "deltaTime": ((None,), (tuple,)),
    "line":     ((array.array, (array.array, array.array)), (None,)),
    "curve":    ((array.array, (array.array, (array.array, array.array))), (None,)),
    "spline":   ((tuple,), (None,)),
    "triangle": ((array.array, (array.array, (array.array, array.array))), (None,)),
    "ellipse":  ((array.array, (array.array, array.array)), (None,)),
    "isNumber": ((tuple,), (bool,)),
    "isMatrix": ((tuple,), (bool,)),
    "isVector": ((tuple,), (bool,)),
    "isList":   ((tuple,), (bool,)),        #
    "isFunc":   ((tuple,), (bool,)),
    "isBool":   ((tuple,), (bool,)),
    "shape":    ((array.array,), (tuple,)),
    "get":      ((array.array,), (tuple,))
}