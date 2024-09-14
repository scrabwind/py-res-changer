#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void clone_extend()
{
    // To identify the current configuration:

    UINT32 PathArraySize = 0;
    UINT32 ModeArraySize = 0;
    DISPLAYCONFIG_PATH_INFO* PathArray;
    DISPLAYCONFIG_MODE_INFO* ModeArray;
    DISPLAYCONFIG_TOPOLOGY_ID CurrentTopology;

    GetDisplayConfigBufferSizes(QDC_ALL_PATHS, &PathArraySize, &ModeArraySize);

    PathArray = (DISPLAYCONFIG_PATH_INFO*)malloc(PathArraySize * sizeof(DISPLAYCONFIG_PATH_INFO));
    memset(PathArray, 0, PathArraySize * sizeof(DISPLAYCONFIG_PATH_INFO));

    ModeArray = (DISPLAYCONFIG_MODE_INFO*)malloc(ModeArraySize * sizeof(DISPLAYCONFIG_MODE_INFO));
    memset(ModeArray, 0, ModeArraySize * sizeof(DISPLAYCONFIG_MODE_INFO));

    LONG ret = QueryDisplayConfig(QDC_DATABASE_CURRENT, &PathArraySize, PathArray, &ModeArraySize, ModeArray, &CurrentTopology);
    // Above CurrentTopology variable will acquire the current display setting (ie Extend, Duplicate, etc.)

    free(PathArray);
    free(ModeArray);

    // To set the required display setting (Extend, Duplicate, etc.):

    if (CurrentTopology == DISPLAYCONFIG_TOPOLOGY_EXTEND) {
        SetDisplayConfig(0, NULL, 0, NULL, SDC_TOPOLOGY_CLONE | SDC_APPLY);
    } else {
        SetDisplayConfig(0, NULL, 0, NULL, SDC_TOPOLOGY_EXTEND | SDC_APPLY);
    }

    // SetDisplayConfig(0, NULL, 0, NULL, SDC_TOPOLOGY_EXTEND | SDC_APPLY);
    // To set to Duplicate:
    // SetDisplayConfig(0, NULL, 0, NULL, SDC_TOPOLOGY_CLONE | SDC_APPLY);
}

void set_resolution(const unsigned int *width, const unsigned int *height) {
    DEVMODE dev;
    ZeroMemory(&dev, sizeof(DEVMODE));

    // Get the current display settings
    if (EnumDisplaySettings(NULL, ENUM_CURRENT_SETTINGS, &dev)) {
        // Set the new resolution
        dev.dmPelsWidth = *width;
        dev.dmPelsHeight = *height;
        dev.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT;
        dev.dmSize = sizeof(DEVMODE);

        // Change the display settings
        ChangeDisplaySettings(&dev, 0);
    }
}