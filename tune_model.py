import os
from ultralytics import YOLO
from ultralytics import settings
from roboflow import Roboflow
from settings import get_settings


os.environ["CUDA_VISIBLE_DEVICES"] = "1"

settings.update({"runs_dir": "tune_runs", "tensorboard": False, "wandb": True})
settings.reset()

project_settings = get_settings()

rf = Roboflow(api_key=project_settings.roboflow_api_key)

project = rf.workspace().project("cavitation_bubbles_segmentation")

dataset = project.version(3).download("yolov11")

model = YOLO("yolo11x-seg", task="segment")

model.tune(data=os.path.join(dataset.location, "data.yaml"),
           use_ray=True,
           project="cavitation_bubbles_segmentation",
           name="yolov11x",
        #    exist_ok=True,
           seed=42,
           plots=True,
           save=True,
           val=True,
           gpu_per_trial=1,
           workers=1,
           iterations=50,
           device=1)

