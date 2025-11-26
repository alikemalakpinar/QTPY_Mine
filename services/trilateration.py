"""Trilateration Algorithm - 3D Position Calculation from Anchor Distances"""
import math
import numpy as np
from typing import List, Tuple, Optional

def trilaterate_2d(anchors: List[Tuple[float, float]], distances: List[float]) -> Optional[Tuple[float, float]]:
    """
    2D Trilateration - 3 anchor ile konum hesapla.
    
    Args:
        anchors: Anchor konumları [(x1,y1), (x2,y2), (x3,y3)]
        distances: Her anchor'dan mesafeler [r1, r2, r3]
        
    Returns:
        Hesaplanan konum (x, y) veya None (başarısız ise)
    """
    if len(anchors) < 3 or len(distances) < 3:
        return None
    
    # İlk 3 anchor'ı kullan
    x1, y1 = anchors[0]
    x2, y2 = anchors[1]
    x3, y3 = anchors[2]
    
    r1, r2, r3 = distances[0], distances[1], distances[2]
    
    try:
        # Trilateration formülü (lineer denklem sistemi çözümü)
        A = 2 * (x2 - x1)
        B = 2 * (y2 - y1)
        C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
        
        D = 2 * (x3 - x2)
        E = 2 * (y3 - y2)
        F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
        
        # Determinant hesapla
        det = A * E - B * D
        
        if abs(det) < 0.001:  # Singülar matris kontrolü
            return None
        
        # Çözüm
        x = (C * E - F * B) / det
        y = (A * F - D * C) / det
        
        return (x, y)
    
    except Exception as e:
        print(f"Trilateration error: {e}")
        return None

def trilaterate_3d(anchors: List[Tuple[float, float, float]], distances: List[float]) -> Optional[Tuple[float, float, float]]:
    """
    3D Trilateration - 4 anchor ile 3D konum hesapla.
    
    Args:
        anchors: Anchor konumları [(x1,y1,z1), (x2,y2,z2), ...]
        distances: Her anchor'dan mesafeler [r1, r2, r3, r4]
        
    Returns:
        Hesaplanan konum (x, y, z) veya None
    """
    if len(anchors) < 4 or len(distances) < 4:
        # 3 anchor ile 2D'ye düş
        result_2d = trilaterate_2d(
            [(a[0], a[1]) for a in anchors[:3]],
            distances[:3]
        )
        if result_2d:
            # Z'yi anchor ortalamalarından tahmin et
            avg_z = sum(a[2] for a in anchors[:3]) / 3
            return (result_2d[0], result_2d[1], avg_z)
        return None
    
    try:
        # 4 anchor ile least squares çözümü
        A = []
        b = []
        
        x1, y1, z1 = anchors[0]
        r1 = distances[0]
        
        for i in range(1, 4):
            xi, yi, zi = anchors[i]
            ri = distances[i]
            
            A.append([2*(xi - x1), 2*(yi - y1), 2*(zi - z1)])
            b.append([
                r1**2 - ri**2 - x1**2 + xi**2 - y1**2 + yi**2 - z1**2 + zi**2
            ])
        
        A = np.array(A)
        b = np.array(b)
        
        # Pseudo-inverse ile çözüm
        result = np.linalg.lstsq(A, b, rcond=None)[0]
        
        return (float(result[0][0]), float(result[1][0]), float(result[2][0]))
    
    except Exception as e:
        print(f"3D Trilateration error: {e}")
        return None

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """İki nokta arasındaki Öklid mesafesi."""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def calculate_distance_3d(point1: Tuple[float, float, float], point2: Tuple[float, float, float]) -> float:
    """3D Öklid mesafesi."""
    return math.sqrt(
        (point1[0] - point2[0])**2 + 
        (point1[1] - point2[1])**2 + 
        (point1[2] - point2[2])**2
    )

def select_best_anchors(tag_position: Tuple[float, float, float], 
                        anchor_data: List[dict]) -> List[dict]:
    """
    Tag konumuna göre en iyi 3-4 anchor'ı seç.
    
    Args:
        tag_position: Mevcut tag konumu (x, y, z)
        anchor_data: Anchor bilgileri [{'id':..., 'position':..., 'distance':...}, ...]
        
    Returns:
        En uygun anchor'lar (sıralı)
    """
    # Her anchor için hata hesapla
    anchor_scores = []
    
    for anchor in anchor_data:
        anchor_pos = anchor['position']
        measured_distance = anchor['distance']
        
        # Geometrik mesafe
        geometric_distance = calculate_distance_3d(tag_position, anchor_pos)
        
        # Hata
        error = abs(measured_distance - geometric_distance)
        
        anchor_scores.append({
            'anchor': anchor,
            'error': error,
            'geometric_distance': geometric_distance
        })
    
    # En düşük hata ile sırala
    anchor_scores.sort(key=lambda x: x['error'])
    
    # En iyi 3-4'ünü döndür
    return [item['anchor'] for item in anchor_scores[:4]]

def estimate_position_accuracy(anchors: List[Tuple[float, float]], 
                              distances: List[float],
                              calculated_position: Tuple[float, float]) -> float:
    """
    Hesaplanan pozisyonun doğruluk tahmini.
    
    Returns:
        Tahmin edilen hata (metre)
    """
    if not calculated_position or len(anchors) < 3:
        return float('inf')
    
    # Her anchor'dan hesaplanan mesafe
    calculated_distances = [
        calculate_distance(calculated_position, anchor)
        for anchor in anchors
    ]
    
    # RMSE (Root Mean Square Error)
    squared_errors = [
        (calc - meas)**2 
        for calc, meas in zip(calculated_distances, distances)
    ]
    
    rmse = math.sqrt(sum(squared_errors) / len(squared_errors))
    
    return rmse
