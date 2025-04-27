# rAAt-ekip Projesi

Bu proje rAAt ekibi için hazırlanmış bir Python tabanlı Django uygulamasıdır.

## Kurulum Adımları

1. Reponun klonlanması:
   ```bash
   git clone https://github.com/nslzsn/rAAt-ekip.git
   ```

2. Proje dizinine geçin:
   ```bash
   cd rAAt-ekip
   ```

3. Sanal ortam oluşturun ve aktive edin:
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

4. Gereksinimleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

5. Veritabanı migrasyonları:
   ```bash
   python manage.py migrate
   ```

6. Sunucuyu çalıştırın:
   ```bash
   python manage.py runserver
   ```

## Katkıda Bulunma
- Forklayın, değişiklik yapın ve Pull Request gönderin 🎉

## Lisans
Bu proje sadece eğitim ve geliştirme amacıyla kullanılabilir.