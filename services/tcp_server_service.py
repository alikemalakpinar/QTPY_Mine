"""TCP Server for Real-time Data Reception from Tracking Devices"""
from PyQt6.QtCore import QThread, pyqtSignal
import socket
import json
import threading
import time

class TCPServerService(QThread):
    """
    TCP sunucusu - Anchor cihazlarından gerçek zamanlı veri alır.
    Port 8888 üzerinden JSON formatında mesafe verilerini dinler.
    """
    
    # Signals
    data_received = pyqtSignal(dict)  # JSON verisi geldiğinde
    connection_status = pyqtSignal(str, bool)  # (client_address, connected)
    error_occurred = pyqtSignal(str)  # Hata mesajı
    
    def __init__(self, host='0.0.0.0', port=8888):
        super().__init__()
        self.host = host
        self.port = port
        self.running = False
        self.server_socket = None
        self.connected_clients = set()
        
        # İstatistikler
        self.total_messages = 0
        self.total_bytes = 0
        self.start_time = None
    
    def run(self):
        """Thread'in ana döngüsü."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1.0)  # Non-blocking accept
            
            self.running = True
            self.start_time = time.time()
            
            print(f"✅ TCP Server başlatıldı: {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    
                    # Yeni istemci
                    addr_str = f"{client_address[0]}:{client_address[1]}"
                    self.connected_clients.add(addr_str)
                    self.connection_status.emit(addr_str, True)
                    print(f"🔌 Yeni bağlantı: {addr_str}")
                    
                    # İstemciyi ayrı thread'de işle
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except socket.error as e:
                    if self.running:
                        self.error_occurred.emit(f"Socket hatası: {e}")
                    break
        
        except Exception as e:
            self.error_occurred.emit(f"Sunucu başlatma hatası: {e}")
            print(f"❌ TCP Server hatası: {e}")
    
    def handle_client(self, client_socket, client_address):
        """Bağlı bir istemciyi işler."""
        buffer = ""
        addr_str = f"{client_address[0]}:{client_address[1]}"
        
        try:
            while self.running:
                data = client_socket.recv(4096).decode('utf-8')
                
                if not data:
                    break
                
                buffer += data
                self.total_bytes += len(data)
                
                # JSON mesajlarını ayıkla
                while buffer:
                    buffer = buffer.strip()
                    if not buffer:
                        break
                    
                    try:
                        # JSON paketini bul (süslü parantez sayma)
                        brace_count = 0
                        end_pos = -1
                        
                        for i, char in enumerate(buffer):
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    end_pos = i + 1
                                    break
                        
                        if end_pos > 0:
                            json_str = buffer[:end_pos]
                            buffer = buffer[end_pos:].strip()
                            
                            # JSON parse et
                            json_data = json.loads(json_str)
                            
                            # İstatistik güncelle
                            self.total_messages += 1
                            
                            # Signal emit et
                            self.data_received.emit(json_data)
                        else:
                            break
                    
                    except json.JSONDecodeError as e:
                        # Hatalı JSON, buffer'ı temizle
                        if '{' in buffer:
                            buffer = buffer[buffer.find('{'):]
                        else:
                            buffer = ""
                        break
        
        except Exception as e:
            self.error_occurred.emit(f"İstemci işleme hatası ({addr_str}): {e}")
        
        finally:
            client_socket.close()
            if addr_str in self.connected_clients:
                self.connected_clients.remove(addr_str)
            self.connection_status.emit(addr_str, False)
            print(f"🔌 Bağlantı kesildi: {addr_str}")
    
    def stop(self):
        """Sunucuyu durdur."""
        print("⏸️  TCP Server durduruluyor...")
        self.running = False
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        # İstatistikler
        if self.start_time:
            runtime = time.time() - self.start_time
            print(f"📊 TCP Server İstatistikleri:")
            print(f"   • Çalışma süresi: {runtime:.1f} saniye")
            print(f"   • Toplam mesaj: {self.total_messages}")
            print(f"   • Toplam veri: {self.total_bytes / 1024:.2f} KB")
            if runtime > 0:
                print(f"   • Mesaj/saniye: {self.total_messages / runtime:.2f}")
    
    def get_statistics(self):
        """Sunucu istatistiklerini döndür."""
        runtime = 0
        if self.start_time:
            runtime = time.time() - self.start_time
        
        return {
            'running': self.running,
            'host': self.host,
            'port': self.port,
            'connected_clients': len(self.connected_clients),
            'total_messages': self.total_messages,
            'total_bytes': self.total_bytes,
            'runtime_seconds': runtime,
            'messages_per_second': self.total_messages / runtime if runtime > 0 else 0
        }
