idf_component_register(SRCS "abort.c"
                "edassert.c"
                "clockCorrectionEngine.c"
                "configblockeeprom.c"
                "cpuid.c"
                "crc_bosch.c"
                "crc.c"
                "debug_ed.c"
                "eprintf.c"
                "filter.c"
                "FreeRTOS-openocd.c"
                "num.c"
                "sleepus.c"
                "statsCnt.c"
                "version.c"
              INCLUDE_DIRS "." "include"
              REQUIRES platform espdrone config)