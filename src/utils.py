import numpy as np
import math
import cv2

def compute_centroid(bbox):
    """
    Вычисляет центр bounding box в формате [x1, y1, x2, y2].
    """
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def euclidean_distance(p1, p2):
    """
    Вычисляет евклидово расстояние между двумя точками.
    """
    if p1 is None or p2 is None:
        return float('inf')
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def draw_mask(frame, mask, color, alpha=0.5):
    """
    Накладывает полупрозрачную маску на кадр.
    mask: бинарная маска (0 или 1), размером, соответствующим кадру.
    color: кортеж (B, G, R) – цвет для маски.
    alpha: коэффициент прозрачности.
    """
    # Убедимся, что маска имеет тип uint8 и размеры совпадают с изображением
    mask = mask.astype(np.uint8)
    if mask.shape[:2] != frame.shape[:2]:
        mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
    colored_mask = np.zeros_like(frame, dtype=np.uint8)
    colored_mask[mask == 1] = color
    frame = cv2.addWeighted(frame, 1, colored_mask, alpha, 0)
    return frame
