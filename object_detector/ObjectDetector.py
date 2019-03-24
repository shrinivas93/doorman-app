from imageai.Detection import ObjectDetection


class ObjectDetector:
    def __init__(self, model_name, model_path):
        self.model_path = model_path
        self.model_name = model_name
        self.object_detector = ObjectDetection()
        if model_name == 'yolov3':
            self.object_detector.setModelTypeAsYOLOv3()
        elif model_name == 'tinyyolov3':
            self.object_detector.setModelTypeAsTinyYOLOv3()
        elif model_name == 'retinanet':
            self.object_detector.setModelTypeAsRetinaNet()
        self.object_detector.setModelPath(model_path)
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
