# import the necessary packages
import base64
import io
from PIL import Image
import numpy as np
import time
import cv2
import os
import json
import threading
import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus

# construct the argument parse and parse the arguments
confthres = 0.3
nmsthres = 0.1


def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on
    lpath = os.path.sep.join([yolo_path, labels_path])

    print(yolo_path)
    LABELS = open(lpath).read().strip().split("\n")
    return LABELS


def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([yolo_path, weights_path])
    return weightsPath


def get_config(config_path):
    configPath = os.path.sep.join([yolo_path, config_path])
    return configPath


def load_model(configpath, weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net


def do_prediction(image, net, LABELS, id):
    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    # print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])

                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # TODO Prepare the output as required to the assignment specification
    # ensure at least one detection exists
    if len(idxs) > 0:
        # 初始化一个空列表，用于存储检测结果
        detections = []

        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # 创建一个字典，包含物体类别、置信度和边界框坐标
            detection = {
                'label': LABELS[classIDs[i]],
                'accuracy': round(confidences[i], 2),
                'rectangle': {
                    'height': boxes[i][3],
                    'left': boxes[i][0],
                    'top': boxes[i][1],
                    'width': boxes[i][2]
                }
            }
            # 将检测结果添加到列表中
            detections.append(detection)

        # 如果有任何检测结果，请将它们转换为JSON格式并打印输出
        if len(detections) > 0:
            json_data = json.dumps({'id': id, 'objects': detections}, indent=4)
            detection_result[id] = json_data
    else:
        detections = []
        json_data = json.dumps({'id': id, 'objects': detections}, indent=4)
        detection_result[id] = json_data


def worker(event, data_id, image):
    # 在线程中加载模型
    nets = load_model(CFG, Weights)

    # 执行预测
    do_prediction(image, nets, Lables, data_id)

    # 设置事件，通知主线程子线程已经完成任务
    event.set()


yolo_path = "yolo_tiny_configs/"

## Yolov3-tiny versrion
labelsPath = "coco.names"
cfgpath = "yolov3-tiny.cfg"
wpath = "yolov3-tiny.weights"

Lables = get_labels(labelsPath)
CFG = get_config(cfgpath)
Weights = get_weights(wpath)

detection_result = {}

s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
TABLE_NAME = 'todos'

def lambda_handler(event, context):
   for record in event['Records']:
       bucket = record['s3']['bucket']['name']
       key = unquote_plus(record['s3']['object']['key'])
       print("File {0} uploaded to {1} bucket".format(key, bucket))
       img = s3_client.get_object(Bucket=bucket, Key=key)

        

       csvcontent = csvfile['Body'].read().decode('utf8').splitlines()
       for line in csvcontent:
           tokens = line.strip().split(",")
           if len(tokens) > 2:
               data = {}
               data['id'] = {'S': str(uuid.uuid4())}
               data['title'] = {'S': tokens[0].strip()}
               data['desc'] = {'S': tokens[1].strip()}
               data['done'] = {'S': tokens[2].strip()}
               response = dynamodb.put_item(TableName=TABLE_NAME, Item=data)
   return {
       'statusCode': 200,
       'body': json.dumps('Records successfully inserted into database...')
   }



@app.route('/api/object_detection', methods=['POST'])
def main():
    data = request.get_json()
    # 将JSON字符串转换为Python对象
    parsed_data = json.loads(data)

    # 提取image和id字段的值
    image_data = parsed_data["image"]
    id_data = parsed_data["id"]

    # 从JSON数据中获取图像数据并解码Base64字符串
    image_data = base64.b64decode(image_data)

    # 将图像数据转换为PIL Image对象
    imgSave = Image.open(io.BytesIO(image_data))

    # 将图像保存到文件
    imgSave.save(id_data + '.jpg')

    imagefile = id_data + ".jpg"
    img = cv2.imread(imagefile)
    os.remove(imagefile)
    npimg = np.array(img)
    image = npimg.copy()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    event = threading.Event()
    thread = threading.Thread(target=worker, args=(event, id_data, image,))
    thread.start()
    event.wait()

    if id_data in detection_result:
        rtn = detection_result[id_data]
    else:
        rtn = None
    return rtn