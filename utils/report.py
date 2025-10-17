"""
Rapor Oluşturma Modülü
TXT, JSON ve HTML formatlarında rapor üretme
"""

import json
import os
from datetime import datetime


class ReportGenerator:
    """Tarama sonuçlarından rapor oluşturma"""
    
    def __init__(self, logger):
        self.logger = logger
        
        # Reports klasörünü oluştur
        self.report_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'Reports'
        )
        os.makedirs(self.report_dir, exist_ok=True)
    
    def generate(self, scan_result, format_type='txt'):
        """
        Rapor oluştur
        
        Args:
            scan_result: Tarama sonuçları (dict)
            format_type: Rapor formatı ('txt', 'json', 'html')
            
        Returns:
            str: Oluşturulan dosyanın yolu veya None
        """
        if not scan_result:
            self.logger.error("Rapor oluşturulamadı: Tarama sonucu yok")
            return None
        
        # Dosya adı oluştur
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"security_report_{timestamp}.{format_type}"
        filepath = os.path.join(self.report_dir, filename)
        
        try:
            if format_type == 'txt':
                self._generate_txt(scan_result, filepath)
            elif format_type == 'json':
                self._generate_json(scan_result, filepath)
            elif format_type == 'html':
                self._generate_html(scan_result, filepath)
            else:
                self.logger.error(f"Geçersiz rapor formatı: {format_type}")
                return None
            
            self.logger.info(f"Rapor oluşturuldu: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Rapor oluşturma hatası: {e}")
            return None
    
    def _generate_txt(self, scan_result, filepath):
        """TXT formatında rapor oluştur"""
        vulnerabilities = scan_result.get('vulnerabilities', [])
        scan_info = scan_result.get('scan_info', {})
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # Başlık
            f.write("=" * 70 + "\n")
            f.write("SİBER GÜVENLİK TARAMA RAPORU\n")
            f.write("=" * 70 + "\n\n")
            
            # Tarama bilgileri
            f.write("TARAMA BİLGİLERİ\n")
            f.write("-" * 70 + "\n")
            f.write(f"Tarih: {scan_info.get('date', 'Bilinmiyor')}\n")
            f.write(f"Sistem: {scan_info.get('system', 'Bilinmiyor')}\n")
            f.write(f"Tarama Süresi: {scan_info.get('duration', 0):.2f} saniye\n")
            f.write(f"Toplam Kontrol: {scan_info.get('total_checks', 0)}\n")
            f.write(f"Bulunan Açık: {scan_info.get('vulnerabilities_found', 0)}\n")
            f.write("\n")
            
            # Özet
            f.write("ÖZET\n")
            f.write("-" * 70 + "\n")
            
            if not vulnerabilities:
                f.write("✓ Herhangi bir güvenlik açığı tespit edilmedi.\n")
                f.write("  Sisteminiz temel güvenlik kontrollerini başarıyla geçti.\n")
            else:
                # Risk seviyesine göre sınıflandır
                risk_counts = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
                for vuln in vulnerabilities:
                    risk = vuln.get('risk', 'medium').lower()
                    risk_counts[risk] = risk_counts.get(risk, 0) + 1
                
                f.write(f"Toplam Güvenlik Açığı: {len(vulnerabilities)}\n\n")
                f.write("Risk Dağılımı:\n")
                if risk_counts['critical'] > 0:
                    f.write(f"  • KRİTİK: {risk_counts['critical']} ⚠️⚠️⚠️\n")
                if risk_counts['high'] > 0:
                    f.write(f"  • Yüksek: {risk_counts['high']} ⚠️⚠️\n")
                if risk_counts['medium'] > 0:
                    f.write(f"  • Orta: {risk_counts['medium']} ⚠️\n")
                if risk_counts['low'] > 0:
                    f.write(f"  • Düşük: {risk_counts['low']}\n")
                
                # Kritik uyarı
                if risk_counts['critical'] > 0:
                    f.write("\n" + "!" * 70 + "\n")
                    f.write("UYARI: KRİTİK SEVİYE GÜVENLİK AÇIKLARI TESPİT EDİLDİ!\n")
                    f.write("Bu açıklar derhal düzeltilmelidir!\n")
                    f.write("!" * 70 + "\n")
            
            f.write("\n")
            
            # Detaylı bulgular
            if vulnerabilities:
                f.write("DETAYLI BULGULAR\n")
                f.write("=" * 70 + "\n\n")
                
                for idx, vuln in enumerate(vulnerabilities, 1):
                    f.write(f"[{idx}] {vuln['message']}\n")
                    f.write("-" * 70 + "\n")
                    f.write(f"Risk Seviyesi: {vuln.get('risk', 'orta').upper()}\n")
                    
                    if vuln.get('details'):
                        f.write(f"Detay: {vuln['details']}\n")
                    
                    if vuln.get('solution'):
                        f.write(f"Çözüm: {vuln['solution']}\n")
                    
                    f.write("\n")
            
            # Alt bilgi
            f.write("=" * 70 + "\n")
            f.write("Bu rapor otomatik olarak oluşturulmuştur.\n")
            f.write("Siber Güvenlik Tarama Aracı v1.0\n")
            f.write("=" * 70 + "\n")
    
    def _generate_json(self, scan_result, filepath):
        """JSON formatında rapor oluştur"""
        report_data = {
            'report_info': {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'report_version': '1.0',
                'tool': 'Siber Güvenlik Tarama Aracı'
            },
            'scan_info': scan_result.get('scan_info', {}),
            'vulnerabilities': scan_result.get('vulnerabilities', []),
            'summary': {
                'total_vulnerabilities': len(scan_result.get('vulnerabilities', [])),
                'risk_distribution': self._calculate_risk_distribution(
                    scan_result.get('vulnerabilities', [])
                )
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
    
    def _generate_html(self, scan_result, filepath):
        """HTML formatında rapor oluştur"""
        vulnerabilities = scan_result.get('vulnerabilities', [])
        scan_info = scan_result.get('scan_info', {})
        
        # Risk dağılımı
        risk_dist = self._calculate_risk_distribution(vulnerabilities)
        
        html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Güvenlik Tarama Raporu</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .info-box {{
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 5px;
        }}
        
        .info-box h2 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5em;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        
        .info-item {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #e0e0e0;
        }}
        
        .info-item label {{
            font-weight: bold;
            color: #666;
            display: block;
            margin-bottom: 5px;
            font-size: 0.9em;
        }}
        
        .info-item value {{
            color: #333;
            font-size: 1.1em;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-top: 4px solid;
        }}
        
        .summary-card.critical {{ border-top-color: #dc3545; }}
        .summary-card.high {{ border-top-color: #fd7e14; }}
        .summary-card.medium {{ border-top-color: #ffc107; }}
        .summary-card.low {{ border-top-color: #28a745; }}
        .summary-card.total {{ border-top-color: #667eea; }}
        
        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .summary-card .label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .vulnerability {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }}
        
        .vulnerability:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        
        .vulnerability-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .vulnerability-number {{
            background: #667eea;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }}
        
        .vulnerability-title {{
            flex: 1;
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }}
        
        .risk-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .risk-critical {{ background: #dc3545; color: white; }}
        .risk-high {{ background: #fd7e14; color: white; }}
        .risk-medium {{ background: #ffc107; color: #333; }}
        .risk-low {{ background: #28a745; color: white; }}
        
        .vulnerability-details {{
            margin: 15px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            color: #666;
        }}
        
        .vulnerability-solution {{
            margin-top: 15px;
            padding: 15px;
            background: #d4edda;
            border-left: 4px solid #28a745;
            border-radius: 5px;
        }}
        
        .vulnerability-solution strong {{
            color: #155724;
            display: block;
            margin-bottom: 5px;
        }}
        
        .no-vulnerabilities {{
            text-align: center;
            padding: 60px 20px;
            background: #d4edda;
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        .no-vulnerabilities .icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}
        
        .no-vulnerabilities h3 {{
            color: #155724;
            font-size: 1.8em;
            margin-bottom: 10px;
        }}
        
        .no-vulnerabilities p {{
            color: #155724;
            font-size: 1.1em;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .vulnerability {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Güvenlik Tarama Raporu</h1>
            <p>Sistem Güvenlik Analizi ve Değerlendirme</p>
        </div>
        
        <div class="content">
            <!-- Tarama Bilgileri -->
            <div class="info-box">
                <h2>📋 Tarama Bilgileri</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <label>Tarih</label>
                        <value>{scan_info.get('date', 'Bilinmiyor')}</value>
                    </div>
                    <div class="info-item">
                        <label>Sistem</label>
                        <value>{scan_info.get('system', 'Bilinmiyor')}</value>
                    </div>
                    <div class="info-item">
                        <label>Tarama Süresi</label>
                        <value>{scan_info.get('duration', 0):.2f} saniye</value>
                    </div>
                    <div class="info-item">
                        <label>Toplam Kontrol</label>
                        <value>{scan_info.get('total_checks', 0)}</value>
                    </div>
                </div>
            </div>
            
            <!-- Özet -->
            <div class="summary">
                <div class="summary-card total">
                    <div class="label">Toplam Açık</div>
                    <div class="number">{len(vulnerabilities)}</div>
                </div>
                <div class="summary-card critical">
                    <div class="label">Kritik</div>
                    <div class="number">{risk_dist.get('critical', 0)}</div>
                </div>
                <div class="summary-card high">
                    <div class="label">Yüksek</div>
                    <div class="number">{risk_dist.get('high', 0)}</div>
                </div>
                <div class="summary-card medium">
                    <div class="label">Orta</div>
                    <div class="number">{risk_dist.get('medium', 0)}</div>
                </div>
                <div class="summary-card low">
                    <div class="label">Düşük</div>
                    <div class="number">{risk_dist.get('low', 0)}</div>
                </div>
            </div>
            
            <!-- Bulgular -->
"""
        
        if not vulnerabilities:
            html_content += """
            <div class="no-vulnerabilities">
                <div class="icon">✓</div>
                <h3>Güvenlik Açığı Bulunamadı</h3>
                <p>Sisteminiz temel güvenlik kontrollerini başarıyla geçti.</p>
            </div>
"""
        else:
            html_content += """
            <div class="info-box">
                <h2>🔍 Detaylı Bulgular</h2>
            </div>
"""
            
            for idx, vuln in enumerate(vulnerabilities, 1):
                risk = vuln.get('risk', 'medium').lower()
                html_content += f"""
            <div class="vulnerability">
                <div class="vulnerability-header">
                    <div class="vulnerability-number">{idx}</div>
                    <div class="vulnerability-title">{vuln['message']}</div>
                    <span class="risk-badge risk-{risk}">{risk.upper()}</span>
                </div>
"""
                
                if vuln.get('details'):
                    html_content += f"""
                <div class="vulnerability-details">
                    <strong>📌 Detay:</strong><br>
                    {vuln['details']}
                </div>
"""
                
                if vuln.get('solution'):
                    html_content += f"""
                <div class="vulnerability-solution">
                    <strong>✓ Çözüm Önerisi:</strong>
                    {vuln['solution']}
                </div>
"""
                
                html_content += """
            </div>
"""
        
        html_content += f"""
        </div>
        
        <div class="footer">
            <p>Bu rapor otomatik olarak oluşturulmuştur.</p>
            <p><strong>Siber Güvenlik Tarama Aracı v1.0</strong></p>
            <p>Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def _calculate_risk_distribution(self, vulnerabilities):
        """Risk dağılımını hesapla"""
        risk_counts = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
        
        for vuln in vulnerabilities:
            risk = vuln.get('risk', 'medium').lower()
            risk_counts[risk] = risk_counts.get(risk, 0) + 1
        
        return risk_counts
    
    def list_Reports(self):
        """Oluşturulmuş raporları listele"""
        try:
            Reports = []
            for filename in os.listdir(self.report_dir):
                if filename.startswith('security_report_'):
                    filepath = os.path.join(self.report_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getctime(filepath))
                    
                    Reports.append({
                        'filename': filename,
                        'path': filepath,
                        'created': file_time.strftime('%d.%m.%Y %H:%M:%S'),
                        'size': os.path.getsize(filepath)
                    })
            
            # Tarihe göre sırala (yeniden eskiye)
            Reports.sort(key=lambda x: x['created'], reverse=True)
            return Reports
            
        except Exception as e:
            self.logger.error(f"Rapor listesi alınamadı: {e}")
            return []