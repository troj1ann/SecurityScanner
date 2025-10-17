"""
Log Sistemi Modülü
Program aktivitelerini kaydetme ve izleme
"""

import logging
import os
from datetime import datetime


class Logger:
    """Log yönetimi sınıfı"""
    
    def __init__(self, name='SecurityScanner', log_level='INFO'):
        """
        Logger başlatıcı
        
        Args:
            name: Logger adı
            log_level: Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.name = name
        self.logger = logging.getLogger(name)
        
        # Log seviyesini ayarla
        level = getattr(logging, log_level.upper(), logging.INFO)
        self.logger.setLevel(level)
        
        # Logs klasörünü oluştur
        self.log_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'logs'
        )
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Log dosya yolu
        log_filename = f"scanner_{datetime.now().strftime('%Y%m%d')}.log"
        self.log_file = os.path.join(self.log_dir, log_filename)
        
        # Handler'ları temizle (çift log yazımını önle)
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Dosya handler
        file_handler = logging.FileHandler(
            self.log_file,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        
        # Console handler (sadece WARNING ve üzeri)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Handler'ları ekle
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        self.info(f"Logger başlatıldı: {name}")
    
    def debug(self, message):
        """Debug seviyesi log"""
        self.logger.debug(message)
    
    def info(self, message):
        """Info seviyesi log"""
        self.logger.info(message)
    
    def warning(self, message):
        """Warning seviyesi log"""
        self.logger.warning(message)
    
    def error(self, message):
        """Error seviyesi log"""
        self.logger.error(message)
    
    def critical(self, message):
        """Critical seviyesi log"""
        self.logger.critical(message)
    
    def log_scan_start(self):
        """Tarama başlangıcını logla"""
        self.info("=" * 50)
        self.info("YENİ TARAMA BAŞLATILDI")
        self.info("=" * 50)
    
    def log_scan_end(self, duration, vulnerability_count):
        """Tarama bitişini logla"""
        self.info("=" * 50)
        self.info(f"TARAMA TAMAMLANDI - {duration:.2f} saniye")
        self.info(f"Bulunan güvenlik açığı sayısı: {vulnerability_count}")
        self.info("=" * 50)
    
    def log_vulnerability(self, vulnerability):
        """Güvenlik açığını logla"""
        self.warning(f"GÜVENLİK AÇIĞI: {vulnerability.get('message', 'Bilinmeyen')}")
        if vulnerability.get('details'):
            self.warning(f"  Detay: {vulnerability['details']}")
        if vulnerability.get('risk'):
            self.warning(f"  Risk: {vulnerability['risk'].upper()}")
    
    def get_log_file_path(self):
        """Log dosyasının yolunu döndür"""
        return self.log_file
    
    def get_recent_logs(self, lines=50):
        """Son N satır logu oku"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except Exception as e:
            self.error(f"Log dosyası okunamadı: {e}")
            return []
    
    def clear_old_logs(self, days=30):
        """Eski log dosyalarını temizle"""
        try:
            current_time = datetime.now()
            deleted_count = 0
            
            for filename in os.listdir(self.log_dir):
                if filename.startswith('scanner_') and filename.endswith('.log'):
                    file_path = os.path.join(self.log_dir, filename)
                    
                    # Dosya oluşturma tarihini kontrol et
                    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    age_days = (current_time - file_time).days
                    
                    if age_days > days:
                        os.remove(file_path)
                        deleted_count += 1
                        self.info(f"Eski log dosyası silindi: {filename}")
            
            if deleted_count > 0:
                self.info(f"{deleted_count} adet eski log dosyası temizlendi")
                
        except Exception as e:
            self.error(f"Eski loglar temizlenirken hata: {e}")
    
    def get_log_statistics(self):
        """Log istatistiklerini döndür"""
        try:
            stats = {
                'total_lines': 0,
                'info_count': 0,
                'warning_count': 0,
                'error_count': 0,
                'critical_count': 0
            }
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    stats['total_lines'] += 1
                    
                    if ' - INFO - ' in line:
                        stats['info_count'] += 1
                    elif ' - WARNING - ' in line:
                        stats['warning_count'] += 1
                    elif ' - ERROR - ' in line:
                        stats['error_count'] += 1
                    elif ' - CRITICAL - ' in line:
                        stats['critical_count'] += 1
            
            return stats
            
        except Exception as e:
            self.error(f"Log istatistikleri alınamadı: {e}")
            return None
    
    def export_logs(self, output_file):
        """Logları başka bir dosyaya dışa aktar"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as src:
                with open(output_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            self.info(f"Loglar dışa aktarıldı: {output_file}")
            return True
            
        except Exception as e:
            self.error(f"Log dışa aktarma hatası: {e}")
            return False
    
    def set_level(self, level):
        """Log seviyesini değiştir"""
        log_level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        self.info(f"Log seviyesi değiştirildi: {level.upper()}")
    
    def __del__(self):
        """Logger sonlandırıcı"""
        # Handler'ları kapat
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)