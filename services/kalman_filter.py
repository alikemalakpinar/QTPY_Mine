"""2D Kalman Filter for Position Tracking - Enterprise Grade"""
import numpy as np

class KalmanFilter2D:
    """2D konum için Kalman filtresi - Gelişmiş tracking için."""
    
    def __init__(self, process_variance=0.005, measurement_variance=0.5, initial_value=(0, 0)):
        """
        Initialize Kalman Filter.
        
        Args:
            process_variance: İşlem varyansı (sistem belirsizliği)
            measurement_variance: Ölçüm varyansı (sensor gürültüsü)
            initial_value: Başlangıç konumu (x, y)
        """
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        
        # Durum vektörü: [x, y, vx, vy]
        self.state = np.array([
            initial_value[0], 
            initial_value[1], 
            0.0,  # x hızı
            0.0   # y hızı
        ], dtype=float)
        
        # Kovaryans matrisi (belirsizlik)
        self.P = np.eye(4) * 1.0
        
        # Durum geçiş matrisi (hareket modeli)
        dt = 0.1  # Zaman adımı
        self.F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=float)
        
        # Ölçüm matrisi (sadece pozisyon ölçülür)
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=float)
        
        # İşlem gürültüsü kovaryansı
        self.Q = np.eye(4) * process_variance
        
        # Ölçüm gürültüsü kovaryansı
        self.R = np.eye(2) * measurement_variance
    
    def predict(self):
        """Durumu bir zaman adımı ileriye tahmin et."""
        # Durum tahmini
        self.state = self.F @ self.state
        
        # Kovaryans tahmini
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        return (self.state[0], self.state[1])
    
    def update(self, measurement):
        """
        Ölçüm ile durumu güncelle.
        
        Args:
            measurement: Ölçüm (x, y) tuple
            
        Returns:
            Filtrelenmiş konum (x, y)
        """
        measurement = np.array([measurement[0], measurement[1]], dtype=float)
        
        # Yenilik (innovation) - ölçüm vs tahmin farkı
        y = measurement - self.H @ self.state
        
        # Yenilik kovaryansı
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman kazancı (optimal ağırlık)
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Durumu güncelle
        self.state = self.state + K @ y
        
        # Kovariyansı güncelle (Joseph form - numerical stability)
        I_KH = np.eye(4) - K @ self.H
        self.P = I_KH @ self.P @ I_KH.T + K @ self.R @ K.T
        
        return (self.state[0], self.state[1])
    
    def get_position(self):
        """Filtrelenmiş mevcut konumu döndür."""
        return (self.state[0], self.state[1])
    
    def get_velocity(self):
        """Tahmini hızı döndür."""
        return (self.state[2], self.state[3])
    
    def get_uncertainty(self):
        """Pozisyon belirsizliğini döndür (kovariyans)."""
        return (self.P[0, 0], self.P[1, 1])
    
    def reset(self, position):
        """Filtreyi yeni bir pozisyonla sıfırla."""
        self.state = np.array([position[0], position[1], 0.0, 0.0], dtype=float)
        self.P = np.eye(4) * 1.0
