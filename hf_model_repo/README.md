---
tags:
- segmentation
- yolo
- ultralytics
- cavitation
- bubbles
library_name: ultralytics
license: mit
datasets:
  - custom
model-index:
  - name: cavitation_bubbles_segmentation
    results:
      - task:
          type: image-segmentation
        dataset:
          name: Custom Dataset
          type: image
        metrics:
          - type: IoU
            value: 0.8
---

# Cavitation bubbles segmentation

## Introduction

This repository contatins a pretrained YOLOv11 model for cavitation bubbles segmentation.