INITIAL_ADDRESS = 1000

GLOBAL_SIZE = 9000
LOCAL_SIZE = 10000
TEMPORAL_SIZE = 50000
LIST_SIZE = 50000
STACK_SIZE = 50000

GLOBAL_FIRST = INITIAL_ADDRESS
LOCAL_FIRST = GLOBAL_FIRST + GLOBAL_SIZE
TEMPORAL_FIRST = LOCAL_FIRST + LOCAL_SIZE
LIST_FIRST = TEMPORAL_FIRST + TEMPORAL_SIZE

LIMITS = {
    'GLOBAL_LIM_L':    GLOBAL_FIRST,
    'GLOBAL_LIM_R':    GLOBAL_FIRST + GLOBAL_SIZE - 1,
    'LOCAL_LIM_L':     LOCAL_FIRST,
    'LOCAL_LIM_R':     LOCAL_FIRST + LOCAL_SIZE - 1,
    'TEMPORAL_LIM_L':  TEMPORAL_FIRST,
    'TEMPORAL_LIM_R':  TEMPORAL_FIRST + TEMPORAL_SIZE - 1,
    'LIST_LIM_L':  LIST_FIRST,
    'LIST_LIM_R':  LIST_FIRST + LIST_SIZE - 1,
    'STACK_SIZE':  STACK_SIZE
}
