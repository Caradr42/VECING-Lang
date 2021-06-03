""" This file serves as a common import for constants.
    This includes the limits for the virtual memory addresses, and 
    stack size. And also this includes the semanticTable used by both the
    parser and virtual machine for semantic cheking of the language functions
"""
import array

DEBUG_MODE = False

INITIAL_ADDRESS = 1000

GLOBAL_SIZE = 9000
LOCAL_SIZE = 10000
TEMPORAL_SIZE = 50000
LIST_SIZE = 50000
TEMPORAL_LIST_SIZE = 50000
STACK_SIZE = 50000

GLOBAL_FIRST = INITIAL_ADDRESS                  #1 000
LOCAL_FIRST = GLOBAL_FIRST + GLOBAL_SIZE        #10 000
TEMPORAL_FIRST = LOCAL_FIRST + LOCAL_SIZE       #20 000
LIST_FIRST = TEMPORAL_FIRST + TEMPORAL_SIZE     #70 000
TEMPORAL_LIST_FIRST = LIST_FIRST + LIST_SIZE    #120 000

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
    "<=":       ((tuple, tuple), (tuple,)),  #
    ">=":       ((tuple, tuple), (tuple,)),  #
    "<":        ((tuple, tuple), (tuple,)),  #
    ">":        ((tuple, tuple), (tuple,)),  #
    "!=":       ((tuple, tuple), (tuple,)),  #
    "=":        ((tuple, tuple), (tuple,)),  #
    "map":      ((tuple, tuple), (tuple,)),
    "apply":    ((tuple, tuple), (tuple,)),
    "print":    ((tuple,), (tuple,)),        #
    "car":      ((tuple,), (tuple,)),       #
    "cdr":      ((tuple,), (tuple,)),       #
    "append":   ((tuple, tuple), (tuple,)), #
    "and":      ((tuple, tuple), (tuple,)), #
    "or":       ((tuple, tuple), (tuple,)), #
    "xor":      ((tuple, tuple), (tuple,)), #
    "not":      ((tuple,), (tuple,)),       #
    "empty":    ((tuple,), (tuple,)),        #
    "single":   ((tuple,), (tuple,)),        #
    "elemCount":((tuple,), (tuple,)),       #
    "length":   ((tuple,), (tuple,)),       #
    "isList":   ((tuple,), (tuple,)),       #
    #new graphics
    "setbgcolor":   ((tuple,), (None,)),
    "setdrawcolor": ((tuple,), (None,)),
    "clear":        ((None,), (None,)),
    "pixel":        ((tuple, tuple), (None,)),
    "getpixel":     ((tuple, tuple), (None,)),
    "createwindow": ((tuple, tuple, tuple), (None,)),
    "stopRender":   ((None,), (None,)),
    "pause":        ((None,), (None,)),
}

# semanticTable = {
#     "cond":     ((tuple,), (tuple,)),       
#     "add":      ((tuple, tuple), (tuple,)), 
#     "sub":      ((tuple, tuple), (tuple,)), 
#     "mult":     ((tuple, tuple), (tuple,)), 
#     "power":    ((tuple, tuple), (tuple,)), 
#     "div":      ((tuple, tuple), (tuple,)), 
#     "sqrt":     ((tuple,), (tuple,)),       
#     "abs":      ((tuple,), (tuple,)),       
#     "<=":       ((tuple, tuple), (tuple,)),  
#     ">=":       ((tuple, tuple), (tuple,)),  
#     "<":        ((tuple, tuple), (tuple,)),  
#     ">":        ((tuple, tuple), (tuple,)),  
#     "!=":       ((tuple, tuple), (tuple,)),  
#     "=":        ((tuple, tuple), (tuple,)),  
#     "map":      ((tuple, tuple), (tuple,)),
#     "apply":    ((tuple, tuple), (tuple,)),
#     "print":    ((tuple,), (tuple,)),        
#     "car":      ((tuple,), (tuple,)),       
#     "cdr":      ((tuple,), (tuple,)),       
#     "append":   ((tuple, tuple), (tuple,)), 
#     "and":      ((tuple, tuple), (tuple,)), 
#     "or":       ((tuple, tuple), (tuple,)), 
#     "xor":      ((tuple, tuple), (tuple,)), 
#     "not":      ((tuple,), (tuple,)),       
#     "empty":    ((tuple,), (tuple,)),        
#     "single":   ((tuple,), (tuple,)),        
#     "elemCount":((tuple,), (tuple,)),       
#     "length":   ((tuple,), (tuple,)),       
#     "isList":   ((tuple,), (tuple,)),       
#     "setbgcolor":   ((tuple,), (None,)),
#     "setdrawcolor": ((tuple,), (None,)),
#     "clear":        ((None,), (None,)),
#     "pixel":        ((tuple, tuple), (None,)),
#     "getpixel":     ((tuple, tuple), (None,)),
#     "createwindow": ((tuple, tuple, tuple), (None,)),
#     "stopRender":   ((None,), (None,)),
#     "pause":        ((None,), (None,)),
# }