from ultralytics import YOLO

model = YOLO('./model/yolo11m.pt')

yaml = './data/snapcook_v10/data.yaml'

result = model.train(
    data = yaml,
    epochs = 150,
    batch = 8,
    patience = 15,
    freeze=10,
    lr0=0.001,
    lrf=0.01,
    name='model/SC_v10_m',
    device=0
)