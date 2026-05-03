# 🚀 Gelişmiş To-Do & Pomodoro Uygulaması

Modern web teknolojileri kullanılarak geliştirilmiş, asenkron (AJAX) yapıya sahip, alt görev destekli ve Pomodoro entegreli tam teşekküllü bir görev yönetim sistemidir. 

Başlangıçta basit bir CLI uygulaması olarak tasarlanan bu proje, sonrasında **Flask, SQLAlchemy ORM ve Fetch API** kullanılarak modern bir Full-Stack web uygulamasına dönüştürülmüştür.

## ✨ Özellikler

- **🔒 Kullanıcı Yetkilendirme:** Güvenli şifreleme (hash) ile kayıt olma ve giriş yapma sistemi. Her kullanıcının verisi sadece kendine özeldir.
- **⚡ Asenkron İşlemler (AJAX):** Görev tamamlama, silme ve alt görev işaretleme işlemleri sayfa yenilenmeden (Fetch API ile) anında gerçekleşir.
- **📊 Dinamik İlerleme Çubuğu:** Eklenen alt görevlerin tamamlanma durumuna göre ana görevin ilerleme yüzdesi (`%`) anlık olarak hesaplanır ve renk değiştirir.
- **⏱️ Pomodoro Sayacı:** Odaklanmayı artırmak için tasarlanmış, 25, 15 ve 5 dakikalık periyotlara ayarlanabilen, süre bitiminde sesli uyarı veren entegre zamanlayıcı.
- **📅 Tarih ve Filtreleme:** Görevlerin bitiş tarihine kaç gün kaldığını otomatik hesaplar. Kalan veya tamamlanan görevleri tek tuşla filtreleme imkanı sunar.
- **✏️ Tam CRUD Desteği:** Görev ekleme, okuma, düzenleme (Update) ve silme (Delete) işlemleri.

## 🛠️ Kullanılan Teknolojiler

**Backend:**
- Python
- Flask
- Flask-SQLAlchemy (ORM Mimarisi)
- SQLite
- Werkzeug (Şifre Güvenliği)

**Frontend:**
- HTML5 / CSS3 (Flexbox & CSS Variables)
- JavaScript (Fetch API)
- Jinja2 Template Engine
- FontAwesome Icons & Google Fonts (Inter)

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Projeyi klonlayın:
   ```bash
   git clone [https://github.com/HasanYazart/todo-cli-app.git](https://github.com/HasanYazart/todo-cli-app.git)
   cd todo-cli-app
   ```
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install Flask Flask-SQLAlchemy Werkzeug
```
3. Uygulamayı başlatın:
```bash
python app.py
```
4. Tarayıcınızda açın:
http://127.0.0.1:5000 adresine giderek uygulamayı kullanmaya başlayabilirsiniz. Veritabanı (database.db) ilk çalıştırmada otomatik olarak oluşturulacaktır.
