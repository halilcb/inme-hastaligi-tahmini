# İnme Hastalığı Tahmini Projesi

Bu proje inme hastalığının tahmini için makine öğrenmesi yöntemlerini kullanmaktadır. Bu proje kapsamında, veriler üzerinde ön işlemler uygulanmış, eksik değerler tahmin edilmiş, dengesiz veri sorunu giderilmiş ve son olarak lojistik regresyon modeli ile tahminleme yapılmıştır.



## Veri Seti

Bu projede kullanılan veri seti, Dünya Sağlık Örgütü (WHO) tarafından paylaşılan "Healthcare Dataset Stroke Data" veri setidir. Bu veri seti, bir hastanede kayıt altına alınan hastaların bazı klinik ve demografik bilgilerini içermektedir.  Veri setinde bireylerin yaş, cinsiyet, hipertansiyon, kalp hastalığı geçmişi, glikoz seviyesi, vücut kitle indeksi (BMI) gibi faktörleri yer almaktadır.

### Veri Setindeki Değişkenler:
- gender: Cinsiyet (Male, Female, Other)
- age: Hastanın yaşı
- hypertension: Hipertansiyon (0: Yok, 1: Var)
- heart_disease: Kalp hastalığı (0: Yok, 1: Var)
- ever_married: Evlenme durumu (Yes/No)
- work_type: Çalışma tipi (Private, Self-employed, Govt_job vb.)
- Residence_type: Yaşam alanı (Rural, Urban)
- avg_glucose_level: Kan şeker seviyesi
- bmi: Vücut kitle indeksi
- smoking_status: Sigara içme durumu (formerly smoked, never smoked, smokes, Unknown)
- stroke: İnme (1: Geçirdi, 0: Geçirmedi)



## Proje Aşamaları

### 1. Veri Keşfi ve Ön İşleme
- Veri setindeki gereksiz "id" sütunu kaldırıldı.
- Eksik değerlerin olup olmadığı kontrol edildi.
- BMI (Vücut Kitle İndeksi) eksik değerleri, Karar Ağacı Regresyonu (DecisionTreeRegressor) ile tahmin edilerek dolduruldu.
- Kategorik değişkenler sayısal değerlere dönüştürüldü:
  - "Male" → 0, "Female" → 1, "Other" → -1
  - "Rural" → 0, "Urban" → 1
  - "Private" → 0, "Self-employed" → 1 vb.

### 2. Dengesiz Veri Sorununun Giderilmesi
- Veri setinde inme geçiren hasta sayısı, inme geçirmeyenlere göre çok az olduğu için SMOTE (Synthetic Minority Over-sampling Technique) kullanılarak veri dengesizliği giderildi.

### 3. Model Seçimi ve Tahminleme
- Bağımsız değişkenler (X) ve bağımlı değişken (y) ayrıldı.
- Veriler %90 - %10 oranında eğitim ve test setlerine bölünerek Lojistik Regresyon Modeli (LogisticRegression) eğitildi.



## Model Performansı ve Değerlendirme
Aşağıda modelin test seti üzerinde elde edilen doğruluk (Accuracy), karmaşıklık matrisi (Confusion Matrix) ve sınıflandırma raporu (Classification Report) değerleri verilmiştir.

### 1. Doğruluk Skoru (Accuracy)
Modelin test seti üzerindeki doğruluğu: %80.57

### 2. Karmaşıklık Matrisi (Confusion Matrix)
| Gerçek / Tahmin | 0 (İnme Yok) | 1 (İnme Var) |
|------------------|------------|------------|
| 0 (İnme Yok) | 353        | 119        |
| 1 (İnme Var) | 70         | 431        |

- Model 119 sağlıklı bireyi yanlışlıkla inme geçirdi diye sınıflandırmış.
- 70 inme hastası yanlışlıkla sağlıklı olarak tahmin edilmiştir.

### 3. Sınıflandırma Raporu (Classification Report)
| Sınıf | Precision | Recall | F1-Score | Support |
|--------|-----------|--------|---------|----------------|
| 0  | 0.83      | 0.75   | 0.79    | 472            |
| 1  | 0.78      | 0.86   | 0.82    | 501            |

- Macro Ortalama Doğruluk: %80
- Ağırlıklı Ortalama Doğruluk: %81

