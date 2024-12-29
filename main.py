import pandas as pd

# CSV dosyasını farklı encoding ile yükleme
try:
    df = pd.read_csv('HBVS.csv', encoding='ISO-8859-1')
except UnicodeDecodeError:
    print("ISO-8859-1 encoding ile okunamadı. Diğer encoding türleri deneniyor...")

    # UTF-8 encoding ile yükleme
    try:
        df = pd.read_csv('HBVS.csv', encoding='utf-8')
    except UnicodeDecodeError:
        print("UTF-8 encoding ile okunamadı.")
        # Dosyayı farklı bir encoding ile yüklemeyi deneyin (örneğin, 'latin1')
        df = pd.read_csv('HBVS.csv', encoding='latin1')

# .arff dosyasına dönüştürme
with open('HBVS.arff', 'w', encoding='utf-8') as f:
    f.write('@RELATION HBVS\n\n')

    # Sütunların veri türlerini belirleme
    for column in df.columns:
        if df[column].dtype == 'object':
            # STRING veri türü için sınıf belirlemeleri
            unique_values = df[column].unique()
            if len(unique_values) > 10:  # Çok fazla benzersiz değer varsa STRING olarak belirleyin
                f.write(f'@ATTRIBUTE {column} STRING\n')
            else:
                values = ','.join(f'"{value}"' for value in unique_values)
                f.write(f'@ATTRIBUTE {column} {{{values}}}\n')  # Sınıflandırılabilir değerler
        else:
            f.write(f'@ATTRIBUTE {column} NUMERIC\n')

    f.write('\n@DATA\n')

    for index, row in df.iterrows():
        row_data = [f'"{value}"' if isinstance(value, str) else str(value) for value in row]
        f.write(','.join(row_data) + '\n')

print(
    "Veri seti .arff formatına dönüştürüldü ve 'HBVS.arff' dosyasına kaydedildi.")
