import os

from ultralytics import YOLO
import cv2
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

upload_path = 'static/upload'
result_path = "static/result"
model_path = "model/Cv3_best.pt"

PATH = [upload_path, result_path]
for path in PATH:
    if not os.path.exists(path):
        os.mkdir(path)

def detect_img(file):
    """
        yolo 모델로 이미지에서 재료 탐지 함수
    """
    model = YOLO(model_path)
    print(file)
    img_path = f'{upload_path}/{file}'
    print(img_path)
    img = cv2.imread(img_path)

    result = model.predict(source=img_path, conf=0.1)

    names = result[0].names
    print(names)
    detected_boxes = result[0].boxes
    class_ids = detected_boxes.cls.cpu().numpy()  # GPU 메모리에 있다면 CPU로 가져와 정수 변환
    # print(class_ids)
    # 4. 반복문을 돌며 클래스 ID를 이름으로 치환하여 출력
    cls = []
    for cls_id in class_ids:
        class_name = names[int(cls_id)]
        cls.append(class_name)
        print(f"탐지된 재료: {class_name}")
    det_class = list(set(cls))
    res_plot = result[0].plot()
    res_rgb = cv2.cvtColor(res_plot, cv2.COLOR_BGR2RGB)
    plt.imshow(res_rgb)
    plt.axis("off")
    plt.savefig(f"{result_path}/res_{file}", transparent = True, bbox_inches='tight', dpi=300)
    # plt.show()
    plt.close()

    return det_class