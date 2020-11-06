"""
Description: This is a class declaration for the collecting information and configuring camera device.
Author: "Parth Desai"
"""
# Importing dependencies
# Libraries
from pypylon import pylon


class MyCameraInstance():
    def __init__(self):
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()
        # Image pre-processing parameters
        self.gain = self.camera.GainRaw
        self.gamma = self.camera.Gamma
        self.exposure = self.camera.ExposureTimeRaw
        # Network Parameters
        self.packet_size = self.camera.GevSCPSPacketSize
        # Acquisition Parameters
        self.acquisition_mode = self.camera.AcquisitionMode
        # Trigger parameters
        self.trigger_delay = self.camera.TriggerDelayAbs
        self.trigger_mode = self.camera.TriggerMode
        self.trigger_source = self.camera.TriggerSource
        self.trigger_acquisition = self.camera.TriggerActivation
        # Capture speed parameters
        self.enable_frame_rate = self.camera.AcquisitionFrameRateEnable
        self.frame_rate = self.camera.AcquisitionFrameRateAbs
        self.current_frame_count = self.camera.AcquisitionFrameCount
        # Image ouptut parameters
        self.pixel_format = self.camera.PixelFormat
        self.vertical_resolution = self.camera.Height
        self.horizontal_resolution = self.camera.Width
        # Hardware output parameters
        self.output_selector = self.camera.UserOutputSelector
        self.default_config = dict({'Gain': 1, 'Gamma': 1.0, 'Exposure': 5000, 'Packet_Size': 1500,
                                    'Acquisition_Mode': 'Continuous', 'Trigger_Delay': 0.0, 'Trigger_Mode': 'Off',
                                    'Trigger_Source': 'Line1', 'Trigger_Acquisition': 'RisingEdge',
                                    'Enable_Frame_Rate': False, 'Frame_Rate': 10, 'Pixel_Format': 'Mono8',
                                    'Vertical_Resolution': 1200, 'Horizontal_Resolution': 1600,
                                    'Output_Selector': 'UserOutput1'})
        # Define cv2 conveter for using images in OpenCV
        self.converter = pylon.ImageFormatConverter()
        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    def configure_my_camera(self, config_settings=None):
        if config_settings is None:
            config_settings = {}
        if config_settings == {}:
            config_settings = self.default_config
        self.gain.SetValue(config_settings['Gain'])
        self.gamma.SetValue(config_settings['Gamma'])
        self.exposure.SetValue(config_settings['Exposure'])
        self.packet_size.SetValue(config_settings['Packet_Size'])
        self.acquisition_mode.SetValue(config_settings['Acquisition_Mode'])         # Continuous, SingleFrame
        self.trigger_delay.SetValue(config_settings['Trigger_Delay'])               # In msec.
        self.trigger_mode.SetValue(config_settings['Trigger_Mode'])                 # On, Off
        self.trigger_source.SetValue(config_settings['Trigger_Source'])             # Line1, Action1, Software
        self.trigger_acquisition.SetValue(config_settings['Trigger_Acquisition'])   # RisingEdge, FallingEdge
        self.enable_frame_rate.SetValue(config_settings['Enable_Frame_Rate'])       # True, False
        self.frame_rate.SetValue(config_settings['Frame_Rate'])                     # If condition required fo upper limit based on hardware
        self.pixel_format.SetValue(config_settings['Pixel_Format'])                 # Mono8, Mono12, Mono12Packed, YUV422Packed, YUV422_YUYV_Packed
        self.vertical_resolution.SetValue(config_settings['Vertical_Resolution'])
        self.horizontal_resolution.SetValue(config_settings['Horizontal_Resolution'])
        self.output_selector.SetValue(config_settings['Output_Selector'])

    def get_my_camera_info(self):
        my_camera_info = dict({'Vendor Name':self.camera.DeviceVendorName.GetValue(),
                               'Model Name':self.camera.DeviceModelName.GetValue(),
                               'Serial No.':self.camera.DeviceID.GetValue(),
                               'Version No.':self.camera.DeviceVersion.GetValue(),
                               'Firmware Version No.':self.camera.DeviceFirmwareVersion.GetValue(),
                               'User ID':self.camera.DeviceUserID.GetValue(),
                               'IP Address':self.camera.GetDeviceInfo().GetIpAddress(),
                               'Port Address':self.camera.GetDeviceInfo().GetPortNr(),
                               'MAC Address':self.camera.GetDeviceInfo().GetMacAddress()})
        return my_camera_info

    def grab_image(self, timeout=5000):
        self.camera.StartGrabbing(self.capture_strategy())
        grab_result = self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)
        if grab_result.GrabSucceeded():
            # Access the image data
            image = self.converter.Convert(grab_result)
            img = image.GetArray()
        else:
            img = None
        grab_result.Release()
        self.camera.StopGrabbing()
        return img

    def close_my_camera(self):
        self.camera.Close()

    @staticmethod
    def capture_strategy(value = 1):
        if value == 1:
            camera_grab_strategy = pylon.GrabStrategy_LatestImageOnly
        else:
            camera_grab_strategy = pylon.GrabStrategy_OneByOne
        return camera_grab_strategy


if __name__ == "__main__":
    device01 = MyCameraInstance()

