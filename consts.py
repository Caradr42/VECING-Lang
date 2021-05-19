initialAddress = 1000
globalSize = 9000
localSize = 10000
temporalSize = 50000
pointerSize = 10000

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