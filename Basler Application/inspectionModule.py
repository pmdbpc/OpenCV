"""
Description: This is a class declaration for the running different inspection algorithms on incoming image.
Author: "Parth Desai"
"""
# Importing dependencies
# Built-in/Generic Imports
import cv2, time, numpy
# Libraries
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol


class MyInspectionModule:
    def __init__(self):
        pass

    def inspect_image(self, image=None, insp_logic=None, inspection_settings=None):
        if inspection_settings is None:
            inspection_settings = []
        self.image = image
        self.inspection_logic = insp_logic
        self.insection_settings = inspection_settings
        if self.inspection_logic == 'EAN-13':
            return self.run_barcode_ean13_inspection()
        elif self.inspection_logic == 'QRCode':
            return self.run_qr_code_inspection()
        else:
            return cv2.putText(self.image, "No Inspection selected for the Image", (50, 50),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

    def run_barcode_ean13_inspection(self):
        # find the EAN-13 barcodes in the image & decode each of the barcodes
        ean_codes = pyzbar.decode(self.image, symbols=[ZBarSymbol.EAN13])
        # loop over the detected barcodes and add overlay text of the barcode value
        if ean_codes:
            output_image = self.add_overlay(detected_codes=ean_codes)
        else:
            output_image = cv2.putText(self.image, "No Barcode Found in Image", (50, 50),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        return output_image

    def run_qr_code_inspection(self):
        # find the barcodes in the image and decode each of the barcodes
        read_2d_codes = pyzbar.decode(self.image, symbols=[ZBarSymbol.QRCODE])
        # loop over the detected qr-codes and add overlay text of the qr-code value
        if read_2d_codes:
            output_image = self.add_overlay(detected_codes=read_2d_codes)
        else:
            output_image = cv2.putText(self.image, "No QR Code Found in Image", (50, 50),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        return output_image

    def add_overlay(self, detected_codes=None):
        overlay_image = None
        for codes in detected_codes:
            # extract the bounding box location of the barcode & draw box surrounding the barcode
            (x, y, w, h) = codes.rect
            overlay_image = cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # converting barcode data (a bytes object) to a string (for overlaying on image)
            code_data = codes.data.decode("utf-8")
            code_type = codes.type
            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(code_data, code_type)
            overlay_image = cv2.putText(self.image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (0, 0, 255), 2)
        return overlay_image


if __name__ == "__main__":
    MyInspectionModule()