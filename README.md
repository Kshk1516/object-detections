## Распознование объектов на изображении
`pip install numpy opencv-python`
 Скачиваем веса модели по ссылке: [link](https://pjreddie.com/media/files/yolov3.weights) добавляем в корень проекта
 `$ wget https://pjreddie.com/media/files/yolov3.weights`
 
 `$ python yolo_opencv.py --image dog.jpg --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt`
 Полезная информация [blog post](http://www.arunponnusamy.com/yolo-object-detection-opencv-python.html)

