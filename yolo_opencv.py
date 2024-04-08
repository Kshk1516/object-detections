import cv2
import numpy as np
import tg_bot_act
import db_servise

# FILE_NAME = 'tarelka-s-fruktami.jpg'
# FILE_NAME = 'яблочный тест.jpg'
# FILE_NAME = 'pictures/pizza_1.png'
# FILE_NAME = 'pictures/ball.png'
# FILE_NAME = 'pictures/broccoli.png'
# FILE_NAME = 'pictures/pizza_cake.png'
# FILE_NAME = 'pictures/pizza_cake_1.png'
FILE_NAME = 'pictures/donut_fake.png'
class Detected_Object:
    def __init__(self, id, confidence):
        self.id = id
        self.confidence = confidence
    def set_desc(self, desc) :
        self.desc = desc
    def set_calorie(self, calorie):
        self.calorie = calorie
    def __str__(self):
        return ' Объект - ' + self.desc + ' ккал/100г -'+ str(self.calorie) + ' (точность определения - ' + str(self.confidence) + ')\n'
    def __repr__(self):
        return ' Объект - ' + self.desc + ' ккал/100г -'+ str(self.calorie) + ' (точность определения - ' + str(self.confidence) + ')\n'




def search_description_by_index(index):
    File_thins_by_index = open('yolov3.txt')
    index_count = 0
    for line in File_thins_by_index:
        index_count = index_count + 1
        if index_count == index + 1:
            return line.replace('\n', '')


def detect_objects(image):
    image = cv2.imread(image)


    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392 #TODO поэкспериментировать



    net = cv2.dnn.readNet(weights, config)

    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = [] # Процент доверия
    boxes = [] # Границы объектов
    conf_threshold = 0.5 # Порог доверия необходимый для вывода 0.5
    nms_threshold = 0.4 # 0.4 коэффицент отвечающий за объеденение прямоугольников

    for out in outs:
        for detection in out:
            scores = detection[5:]
            # print(scores)
            class_id = np.argmax(scores)

            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)

                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    detected_objects_list = []
    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]

        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))
        detected_object = Detected_Object(class_ids[i],confidences[i])
        detected_objects_list.append(detected_object)


    cv2.imshow("object detection", image)
    cv2.waitKey()

    cv2.imwrite("object-detection.jpg", image)
    cv2.destroyAllWindows()
    return detected_objects_list


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

weights = 'yolov3.weights'
config = 'yolov3.cfg'
classes_file = 'yolov3.txt'
with open(classes_file, 'r') as f:
    classes = [line.strip() for line in f.readlines()]
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))


# Вызываем поиск объектов по картинке

detected_object_list = detect_objects(FILE_NAME)



# поиск описания для каждого объекта из файла
for detected_object in detected_object_list:
    object_description = search_description_by_index(detected_object.id)
    detected_object.set_desc(object_description)

# поиск калорийности в бд по описанию объекта
for detected_object in detected_object_list:
    detected_calorie = db_servise.get_calorie_by_description(detected_object.desc)
    detected_object.set_calorie(detected_calorie)


print(*detected_object_list)
massage = 'найденные объекты на фотографии: \n'
for detected_object in detected_object_list:
    massage = massage + str(detected_object)

tg_bot_act.send_massage(massage)
