import cv2


class Camera:

    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(camera_index)

    def capture(self, output_file_path):
        if not self.camera.isOpened():
            self.camera.open(self.camera_index)
        success, image = self.camera.read()
        if success:
            file_created = cv2.imwrite(output_file_path, image)
            self.camera.release()
        return success and file_created
