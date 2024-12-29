from picamera import PiCamera

class Camera:
    def __init__(self):
        self.camera = PiCamera()

    def take_photo(self, file_path):
        self.camera.capture(file_path)
