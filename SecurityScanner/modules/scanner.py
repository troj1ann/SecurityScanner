"""
Güvenlik Tarama Motoru
Ana tarama mantığı ve kontrol yönetimi
"""

import time
import platform
from datetime import datetime
import json
import os

from modules.checks import SecurityChecks


class SecurityScanner:
    """Güvenlik tarama motoru"""
    
    def __init__(self, logger):
        self.logger = logger
        self.checks = SecurityChecks(logger)
        self.last_scan_result = None
        self.scan_history = []
        self.config = self.load_config()
        
        # Veri klasörünü oluştur
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Geçmişi yükle
        self.load_history()
    
    def load_config(self):
        """Yapılandırmayı yükle"""
        default_config = {
            'auto_report': False,
            'report_format': 'txt',
            'log_level': 'INFO',
            'detailed_scan': True,
            'scan_timeout': 30
        }
        
        try:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                'data', 
                'config.json'
            )
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
                    self.logger.info("Yapılandırma yüklendi")
        except Exception as e:
            self.logger.error(f"Yapılandırma yüklenemedi: {e}")
        
        return default_config
    
    def save_config(self):
        """Yapılandırmayı kaydet"""
        try:
            config_path = os.path.join(self.data_dir, 'config.json')
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            self.logger.info("Yapılandırma kaydedildi")
        except Exception as e:
            self.logger.error(f"Yapılandırma kaydedilemedi: {e}")
    
    def load_history(self):
        """Tarama geçmişini yükle"""
        try:
            history_path = os.path.join(self.data_dir, 'scan_history.json')
            
            if os.path.exists(history_path):
                with open(history_path, 'r', encoding='utf-8') as f:
                    self.scan_history = json.load(f)
                    self.logger.info(f"{len(self.scan_history)} tarama geçmişi yüklendi")
        except Exception as e:
            self.logger.error(f"Geçmiş yüklenemedi: {e}")
            self.scan_history = []
    
    def save_history(self):
        """Tarama geçmişini kaydet"""
        try:
            history_path = os.path.join(self.data_dir, 'scan_history.json')
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(self.scan_history, f, indent=4, ensure_ascii=False)
            self.logger.info("Tarama geçmişi kaydedildi")
        except Exception as e:
            self.logger.error(f"Geçmiş kaydedilemedi: {e}")
    
    def perform_scan(self, progress_callback=None):
        """
        Güvenlik taraması yap
        
        Args:
            progress_callback: İlerleme bildirimi için callback fonksiyonu
            
        Returns:
            dict: Tarama sonuçları
        """
        self.logger.info("Güvenlik taraması başlatıldı")
        start_time = time.time()
        
        # Kontrol listesi
        check_list = [
            ("Windows Defender", self.checks.check_windows_defender),
            ("Güvenlik Duvarı", self.checks.check_firewall),
            ("Açık Portlar", self.checks.check_open_ports),
            ("Administrator Hesabı", self.checks.check_admin_account),
            ("Şifre Politikası", self.checks.check_password_policy),
            ("Otomatik Güncellemeler", self.checks.check_auto_updates),
            ("Paylaşılan Klasörler", self.checks.check_shared_folders),
            ("UAC Ayarları", self.checks.check_uac_settings),
            ("Uzak Masaüstü", self.checks.check_remote_desktop),
            ("USB Otomatik Çalıştırma", self.checks.check_usb_autorun),
            ("BitLocker Şifreleme", self.checks.check_bitlocker),
            ("SMBv1 Protokol", self.checks.check_smb_v1),
            ("PowerShell Logging", self.checks.check_powershell_logging),
            ("Windows Script Host", self.checks.check_wsh),
            ("Misafir Hesabı", self.checks.check_guest_account),
            ("Boş Şifreler", self.checks.check_blank_passwords),
            ("Ekran Koruyucu Şifre", self.checks.check_screen_saver_password),
            ("Ağ Keşfi", self.checks.check_network_discovery),
        ]
        
        vulnerabilities = []
        total_checks = len(check_list)
        
        # Her kontrolü çalıştır
        for idx, (check_name, check_func) in enumerate(check_list, 1):
            self.logger.info(f"Kontrol yapılıyor: {check_name}")
            
            # İlerleme callback'i varsa çağır
            if progress_callback:
                progress_callback(check_name, idx, total_checks)
            
            try:
                # Kontrolü çalıştır
                result = check_func()
                
                if result:
                    vulnerabilities.append(result)
                    self.logger.warning(f"Güvenlik açığı bulundu: {result['message']}")
                
                # Gerçekçi tarama süresi için kısa bekleme
                time.sleep(0.5)
                
            except Exception as e:
                self.logger.error(f"{check_name} kontrolünde hata: {e}")
        
        # Tarama süresi
        duration = time.time() - start_time
        
        # Tarama bilgileri
        scan_info = {
            'date': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            'system': f"{platform.system()} {platform.release()}",
            'duration': duration,
            'total_checks': total_checks,
            'vulnerabilities_found': len(vulnerabilities)
        }
        
        # Sonuçları kaydet
        self.last_scan_result = {
            'vulnerabilities': vulnerabilities,
            'scan_info': scan_info
        }
        
        # Geçmişe ekle
        history_entry = {
            'date': scan_info['date'],
            'vulnerability_count': len(vulnerabilities),
            'duration': duration,
            'system': scan_info['system']
        }
        self.scan_history.append(history_entry)
        self.save_history()
        
        self.logger.info(f"Tarama tamamlandı: {len(vulnerabilities)} açık bulundu, {duration:.2f} saniye")
        
        # Otomatik rapor oluşturma
        if self.config.get('auto_report', False):
            self.generate_report(self.config.get('report_format', 'txt'))
        
        return self.last_scan_result
    
    def get_history(self):
        """Tarama geçmişini döndür"""
        return self.scan_history
    
    def get_config(self):
        """Yapılandırmayı döndür"""
        return self.config
    
    def update_config(self, key, value):
        """Yapılandırmayı güncelle"""
        self.config[key] = value
        self.save_config()
        self.logger.info(f"Yapılandırma güncellendi: {key} = {value}")
    
    def generate_report(self, format_type='txt'):
        """
        Rapor oluştur
        
        Args:
            format_type: Rapor formatı ('txt', 'json', 'html')
            
        Returns:
            str: Oluşturulan rapor dosyasının yolu veya None
        """
        if not self.last_scan_result:
            self.logger.warning("Rapor oluşturulamadı: Tarama sonucu yok")
            return None
        
        try:
            from utils.report import ReportGenerator
            
            report_gen = ReportGenerator(self.logger)
            filename = report_gen.generate(
                self.last_scan_result,
                format_type
            )
            
            self.logger.info(f"Rapor oluşturuldu: {filename}")
            return filename
            
        except ImportError:
            self.logger.error("ReportGenerator modülü yüklenemedi")
            return None
        except Exception as e:
            self.logger.error(f"Rapor oluşturulamadı: {e}")
            return None
    
    def get_last_scan(self):
        """Son tarama sonucunu döndür"""
        return self.last_scan_result
    
    def clear_history(self):
        """Tarama geçmişini temizle"""
        self.scan_history = []
        self.save_history()
        self.logger.info("Tarama geçmişi temizlendi")
    
    def export_scan_data(self, filepath):
        """
        Tarama verilerini dışa aktar
        
        Args:
            filepath: Dışa aktarılacak dosya yolu
        """
        try:
            export_data = {
                'last_scan': self.last_scan_result,
                'history': self.scan_history,
                'config': self.config,
                'export_date': datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
            
            self.logger.info(f"Tarama verileri dışa aktarıldı: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Veri dışa aktarılamadı: {e}")
            return False
    
    def get_statistics(self):
        """
        Tarama istatistiklerini döndür
        
        Returns:
            dict: İstatistikler
        """
        if not self.scan_history:
            return {
                'total_scans': 0,
                'total_vulnerabilities': 0,
                'average_vulnerabilities': 0,
                'last_scan_date': 'Henüz tarama yapılmadı'
            }
        
        total_vulns = sum(scan.get('vulnerability_count', 0) for scan in self.scan_history)
        avg_vulns = total_vulns / len(self.scan_history) if self.scan_history else 0
        
        return {
            'total_scans': len(self.scan_history),
            'total_vulnerabilities': total_vulns,
            'average_vulnerabilities': round(avg_vulns, 2),
            'last_scan_date': self.scan_history[-1].get('date', 'Bilinmiyor') if self.scan_history else 'Bilinmiyor',
            'most_vulnerable_scan': max(self.scan_history, key=lambda x: x.get('vulnerability_count', 0)) if self.scan_history else None
        }