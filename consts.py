initialAddress = 1000
globalSize = 10000
localSize = 20000
temporalSize = 20000
pointerSize = 20000

globalFirst = initialAddress
localFirst = globalFirst + globalSize
temporalFirst = localFirst + localSize
pointerFirst = temporalFirst + temporalSize


LIMITS = {
            'GLOBAL_LIM_L' :    globalFirst,
            'GLOBAL_LIM_R' :    globalFirst + globalSize - 1,
            'LOCAL_LIM_L' :     localFirst,
            'LOCAL_LIM_R' :     localFirst + localSize - 1,
            'TEMPORAL_LIM_L' :  temporalFirst,
            'TEMPORAL_LIM_R' :  temporalFirst + temporalSize - 1,
            'POINTERS_LIM_L' :  pointerFirst,
            'POINTERS_LIM_R' :  pointerFirst + pointerSize -  1
        }