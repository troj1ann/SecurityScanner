"""
Siber Güvenlik Tarama Aracı
Ana Program Dosyası
"""

import sys
import os

# Proje dizinini al
current_dir = os.path.dirname(os.path.abspath(__file__))

# Modül yollarını ekle
modules_path = os.path.join(current_dir, 'modules')
utils_path = os.path.join(current_dir, 'utils')

sys.path.insert(0, modules_path)
sys.path.insert(0, utils_path)

# Import'lar (artık doğrudan)
from ui import SecurityUI
from scanner import SecurityScanner
from logger import Logger

def main():
    """Ana program fonksiyonu"""
    try:
        # Logger başlat
        logger = Logger()
        logger.info("Program başlatıldı")
        
        # Scanner ve UI oluştur
        scanner = SecurityScanner(logger)
        ui = SecurityUI(scanner, logger)
        
        # Programı çalıştır
        ui.run()
        
        logger.info("Program normal şekilde sonlandırıldı")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Program kullanıcı tarafından sonlandırıldı.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        if 'logger' in locals():
            logger.error(f"Kritik hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()