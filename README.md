# Todo & Pomodoro App

Modern, şık tasarımlı (Glassmorphism) ve gelişmiş özelliklerle donatılmış bir "Görev Yöneticisi ve Pomodoro" uygulamasıdır. Başlangıçta basit bir CLI uygulaması olarak doğan bu proje, artık hem güçlü bir web uygulaması hem de arka planda CLI ile senkronize çalışabilen sağlam bir Flask mimarisine sahiptir.

## 🚀 Özellikler

- **Gelişmiş Arayüz & Glassmorphism:** CSS değişkenleri ve modern UI prensipleri ile inşa edilmiş çarpıcı bir tasarım.
- **Görev Yönetimi:**
  - Ana görevler ve alt görevler (Subtasks).
  - İlerleme çubukları (Progress bars).
  - Görevlere "Düşük, Orta, Yüksek" öncelik atama ve rozetlerle görüntüleme.
  - Sürükle-bırak (Drag & Drop) ile görev sıralamasını değiştirme özelliği (SortableJS).
- **Pomodoro Zamanlayıcı:**
  - Görevlerinize odaklanmanız için entegre sayaç.
  - Özel ayarlarla (15, 25, 30, 45, 60 dk) varsayılan süre belirleme.
  - Süre dolduğunda çalan Alarm Sesini kişiselleştirme veya kendi dosyanızı (.mp3, .ogg) yükleme özelliği.
- **Kullanıcı Profili ve Ayarlar:**
  - Tek tıkla **Aydınlık (Light)** ve **Karanlık (Dark)** tema arasında geçiş.
  - Güvenli şifre değiştirme (Werkzeug hashing).
  - Tüm görev ve verilerinizi yedeklemek için JSON olarak **Dışa Aktarma (Export)** özelliği.
  - GDPR uyumlu: Tüm verilerle birlikte Hesabı Kalıcı Olarak Silme seçeneği.
  - Modern, şık ve animasyonlu (SweetAlert2) bildirim mesajları.
- **CLI Entegrasyonu:** `main.py` dosyası üzerinden de aynı SQLite veritabanına ulaşıp komut satırından işlem yapabilirsiniz.

## 🛠️ Teknolojiler

- **Backend:** Python, Flask, Flask-SQLAlchemy (Blueprints Mimarisi)
- **Veritabanı:** SQLite
- **Frontend:** HTML5, CSS3 (Vanilla), JavaScript, SortableJS, SweetAlert2, FontAwesome

## 📦 Kurulum ve Çalıştırma

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/HasanYazart/todo-cli-app.git
   cd todo-cli-app
   ```

2. Gerekli kütüphaneleri kurun (Eğer sanal ortam kullanıyorsanız önce onu aktif edin):
   ```bash
   pip install -r requirements.txt
   ```

   Üretimde güçlü bir oturum anahtarı tanımlayın:
   ```bash
   SECRET_KEY="uzun-rastgele-bir-deger" python app.py
   ```

3. Uygulamayı başlatın:
   ```bash
   python app.py
   ```

4. Tarayıcınızdan `http://127.0.0.1:5000` adresine giderek kullanmaya başlayabilirsiniz.

## 💻 CLI Kullanımı

`main.py` üzerinden komut satırından da uygulamanızı yönetebilirsiniz (Varsayılan kullanıcı ID=1 olarak baz alınır):
```bash
python main.py add "Yeni görev adı"
python main.py list
python main.py list done
python main.py done <GOREV_ID>
```
