from imageai.Detection import ObjectDetection


class YoloObjectDetector:
    def __init__(self, yolo_model_path):
        self.yolo_model_path = yolo_model_path
        self.object_detector = ObjectDetection()
        self.object_detector.setModelTypeAsYOLOv3()
        self.object_detector.setModelPath(yolo_model_path)
        self.object_detector.loadModel()

    def detect(self, input_image_path, output_image_path, extract_detected_objects=True, display_percentage_probability=False, display_object_name=False):
        detections, detected_objects_location = self.object_detector.detectObjectsFromImage(
            input_image=input_image_path,
            output_image_path=output_image_path,
            extract_detected_objects=extract_detected_objects,
            display_percentage_probability=display_percentage_probability,
            display_object_name=display_object_name
        )
        return detections, detected_objects_location
