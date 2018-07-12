
"""
    Live camera sample showing the camera information and video in real time and allows to control the different
    settings.
"""

import cv2
import pyzed.camera as zcam
import pyzed.types as tp
import pyzed.core as core
import pyzed.defines as sl

camera_settings = sl.PyCAMERA_SETTINGS.PyCAMERA_SETTINGS_BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1


def main():
    print("Running...")
    init = zcam.PyInitParameters()
    init.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE
    init.coordinate_units = sl.PyUNIT.PyUNIT_CENTIMETER

    cam = zcam.PyZEDCamera()
    if not cam.is_opened():
        print("Opening ZED Camera...")
    status = cam.open(init)
    if status != tp.PyERROR_CODE.PySUCCESS:
        print(repr(status))
        print('error opening camera!! abort abort')
        exit()

    runtime = zcam.PyRuntimeParameters()
    mat = core.PyMat()

    print_camera_information(cam)

    key = ''
    while key != 113:  # for 'q' key
        err = cam.grab(runtime)
        if err == tp.PyERROR_CODE.PySUCCESS:
            cam.retrieve_image(mat, sl.PyVIEW.PyVIEW_DEPTH)

            cv2.imshow("ZED", mat.get_data())
            key = cv2.waitKey(5)
            # settings(key, cam, runtime, mat)
        else:
            key = cv2.waitKey(5)
    cv2.destroyAllWindows()

    cam.close()
    print("\nFINISH")


def print_camera_information(cam):
    print("Resolution: {0}, {1}.".format(round(cam.get_resolution().width, 2), cam.get_resolution().height))
    print("Camera FPS: {0}.".format(cam.get_camera_fps()))
    print("Firmware: {0}.".format(cam.get_camera_information().firmware_version))
    print("Serial number: {0}.\n".format(cam.get_camera_information().serial_number))




if __name__ == "__main__":
    main()
