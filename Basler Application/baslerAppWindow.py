"""
Description: This is a class declaration for the application window using python tkinter module.
Author: "Parth Desai"
"""
# Importing dependencies
from __future__ import print_function
# Libraries
import threading
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
from pypylon import pylon
# Own modules
from cameraDevice import MyCameraInstance
from inspectionModule import *


class ApplicationWindow:
    def __init__(self, app_name='New Window', video_source=0):
        # Initialize the tkinter interface window
        self.appName = app_name
        self.window = Tk()
        # Set the title and window size
        self.window.title(self.appName)
        self.window.geometry('925x630')

        # Create a frame for placing elements & a canvas to fit above video source o/p within tkinter window
        self.frame = Frame(self.window, relief=RIDGE, borderwidth=2)
        self.canvas = Canvas(self.window, width = 800, height = 600, bg = 'white')

        self.variable = StringVar(self.window)      # Declare a string variable used by the application
        self.vid = MyCameraInstance()               # Create the basler camera device instance
        self.inspect_module = MyInspectionModule()  # Create the inspection module instance
        self.configure_window_layout()              # Configure the app window with control & display elements

        # Run window in loop mode
        self.window.mainloop()

    def configure_window_layout(self):
        # Apply the application label on the top of the application window. Disabled
        # When enabled, the window component positions needs to be shifted accordingly.
        # label = Label(frame, text=self.appName, bg='gray', font=('Calibri 16 bold'))
        # label.pack(side=TOP)
        # Configure frame placement and pack
        self.frame.config(background='gray')
        self.frame.pack(fill=BOTH, expand=1)
        # Configure canvas placement
        self.canvas.place(x= 110, y=15)
        # Configure application menus and sub-menus , control buttons, etc.
        self.configure_menus()
        self.configure_buttons()
        self.configure_other_controls()

    def configure_menus(self):
        # Configuring the menu bar for the application window
        menu = Menu(self.window)
        self.window.config(menu=menu)
        # Defining a sub menu for 'Guides'
        submenu1 = Menu(menu)
        menu.add_cascade(label="Guide", menu=submenu1)
        submenu1.add_command(label="Help", command=self.app_help_menu)
        submenu1.add_command(label = "OpenCV Guide", command=self.cv_help_menu)
        # Defining a sub menu for application information
        submenu2 = Menu(menu)
        menu.add_cascade(label="About", menu=submenu2)
        submenu2.add_command(label="Information", command=self.about_menu)

    def configure_buttons(self):
        # Configuring application control buttons.
        self.control_button_01 = Button(self.frame, width=10, font='calibri 12 bold', relief=FLAT,
                                   text='Snapshot', command=self.cam_snapshot)
        self.control_button_01.place(x=5, y=15)
        self.control_button_02 = Button(self.frame, width=10, font='calibri 12 bold', relief=FLAT,
                                        text='Inspect', command=self.inspect_image)
        self.control_button_02.place(x=5, y=65)
        self.control_button_03 = Button(self.frame, width=10, font='calibri 12 bold', relief=FLAT,
                                   text='Live', command=self.cam_live_start)
        self.control_button_03.place(x=5, y=115)
        self.control_button_04 = Button(self.frame, width=10, font='calibri 12 bold', relief=FLAT,
                                   text='Stop Live', command=self.stop_live)
        self.control_button_04.place(x=5, y=165)
        self.control_button_05 = Button(self.frame, width=10, font='calibri 12 bold', relief=FLAT,
                                        text='Cam Info', command=self.cam_info)
        self.control_button_05.place(x=5, y=215)
        self.control_button_06 = Button(self.frame, width=10, font='calibri 12 bold', relief=FLAT,
                                        text='Config Cam', command=self.cam_config)
        self.control_button_06.place(x=5, y=265)
        self.control_button_07 = Button(self.frame, width=10, font='calibri 12 bold', relief=FLAT,
                                        text='Test', command=self.return_to_main)
        self.control_button_10 = Button(self.frame, width=10, font='calibri 12 bold', relief=FLAT,
                                   text='Exit', command=self.exit_application)
        self.control_button_10.place(x=5, y=583)
        self.default_button_funcs()

    def configure_other_controls(self):
        # Select an operation from drop down menu
        drop_options = ['None', 'EAN-13', 'QRCode', 'Pharma', 'EAN-8', 'Data Matrix']
        self.variable.set("None")  # default value
        self.dropdown_01 = OptionMenu(self.window, self.variable, *drop_options)
        self.dropdown_01.config(width = 8)
        self.dropdown_01.place(x=5, y=365)

    def default_button_funcs(self):
        self.control_button_01['state'] = NORMAL
        self.control_button_02['state'] = NORMAL
        self.control_button_03['state'] = NORMAL
        self.control_button_04['state'] = DISABLED
        self.control_button_05['state'] = NORMAL
        self.control_button_06['state'] = NORMAL
        self.dropdown_01['state'] = NORMAL

    def live_button_funcs(self):
        self.control_button_01['state'] = DISABLED
        self.control_button_02['state'] = DISABLED
        self.control_button_03['state'] = DISABLED
        self.control_button_04['state'] = NORMAL
        self.control_button_05['state'] = DISABLED
        self.control_button_06['state'] = DISABLED
        self.dropdown_01['state'] = DISABLED

    def cam_live_start(self):
        # Reducing camera frame rate to avoid frame missing.
        self.vid.frame_rate.SetValue(20)
        self.vid.enable_frame_rate.SetValue(True)
        self.live_button_funcs()                            # Set the live mode button functions
        tf = threading.Thread(target=self.cam_live)         # Create a thread to run live mode
        tf.start()                                          # Enable the live mode thread running
        tf.join()
        pass

    def cam_live(self):
        if not self.vid.camera.IsOpen():                    # Check if camera device is already open
            self.vid.camera.Open()
        # Enable the camera in live video streaming using camera event handler
        self.display_update_handler = ApplicationWindow.DisplayUpdateHandler(self)
        self.display_update_handler_hdl = self.vid.camera.RegisterImageEventHandler(self.display_update_handler,
                                                                                    pylon.RegistrationMode_ReplaceAll,
                                                                                    pylon.Cleanup_None)
        self.vid.camera.StartGrabbing(self.vid.capture_strategy(), pylon.GrabLoop_ProvidedByInstantCamera)
        pass

    def stop_live(self):
        # Disable the camera live streaming - clear canvas, stop grabbing and release all capture events
        self.canvas.delete("all")
        self.vid.camera.StopGrabbing()
        self.vid.camera.DeregisterImageEventHandler(self.display_update_handler_hdl)
        del self.display_update_handler
        self.vid.enable_frame_rate.SetValue(False)
        self.default_button_funcs()                         # Set the default button functions
        self.vid.camera.Close()
        pass

    def cam_snapshot(self, value = 0):
        if not self.vid.camera.IsOpen():                    # Check if camera device is already open
            self.vid.camera.Open()
        # Enables the camera in single frame capture mode
        self.snap = self.vid.grab_image()
        # Scaling the image as per the canvas size for full view of frame
        self.canvas_image_packer(self.snap)

    def cam_info(self):
        if not self.vid.camera.IsOpen():                    # Check if camera device is already open
            self.vid.camera.Open()
        # Read hardware device information of the camera connected and display
        camera_info = self.vid.get_my_camera_info()
        # Read the camera information dictionary data and convert to displayable string
        # camInfoValuesList = [(key, ":", value) for key, value in self.cameraInfo.items()]
        # camInfoStringList = [''.join(i) for i in values]
        # camInfoString = '\n'.join(test)
        # Above 3 steps run as list comprehension
        data = '\n'.join([''.join(i) for i in [(key, ":", value) for key, value in camera_info.items()]])
        tkinter.messagebox.showinfo("Camera Information", data)

    def cam_config(self):
        # Configure the camera parameters for usage. WIP
        self.canvas.place_forget()
        self.control_button_06.place_forget()
        self.control_button_07.place(x=5, y=265)
        pass

    def return_to_main(self):
        self.canvas.place(x=110, y=15)
        self.control_button_07.place_forget()
        self.control_button_06.place(x=5, y=265)
        pass

    def inspect_image(self):
        # Capture a new image for inspection and call the inspection routine based on selected dropdown option.
        self.cam_snapshot()
        inspection_result = self.inspect_module.inspect_image(image=self.snap, inspectionlogic=self.variable.get())
        # Scaling the image as per the canvas size for full view of frame
        self.canvas_image_packer(inspection_result)

    def canvas_image_packer(self, image):
        # Resize input image based on image display window size
        image_resized = cv2.resize(image, (800, 600))
        # Converting the the array based image received from camera to displayable format
        self.window.photoView = ImageTk.PhotoImage(Image.fromarray(image_resized))
        self.canvas.create_image(0, 0, image=self.window.photoView, anchor=NW)

    def exit_application(self):
        # Exit the application window. Optional to display a confirmation message
        # tkinter.messagebox.showinfo("Exiting...", "\nThe application will now close\n")
        self.vid.enable_frame_rate.SetValue(False)
        self.vid.close_my_camera()
        self.window.destroy()

    @staticmethod
    def app_help_menu():
        # Help window explaining control button functions for the application
        helpString = '\n'.join(['Snapshot: Captures current frame from camera.',
                                'Info: Displays all camera device information.',
                                'Live: Enable camera live streaming - Function Disabled',
                                'Exit: Exit the application.'])
        tkinter.messagebox.showinfo("Help ", helpString)

    @staticmethod
    def cv_help_menu():
        # Help window with link to documentation for OpenCV library
        tkinter.messagebox.showinfo("OpenCV Help",
                                    "OpenCV Python Documentation: https://docs.opencv.org/master/index.html")

    def about_menu(self):
        # Application information window
        tkinter.messagebox.showinfo("About", 'Application Name: ' + self.appName +
                                    '\nVersion No.: 1.0.0\nDeveloped by: Parth Desai')


    class DisplayUpdateHandler(pylon.ImageEventHandler):
        def __init__(self, application):
            # Linking the pypylon event handler class for continuous frame capture.
            super().__init__()
            self.app = application

        def OnImageGrabbed(self, camera, grabResult):
            # Grabbing the image and converting to and array for processing
            if grabResult.GrabSucceeded():
                image = self.app.vid.converter.Convert(grabResult)
                image = image.GetArray()
                self.app.canvas_image_packer(image)


if __name__ == "__main__":
    ApplicationWindow(app_name='My window')