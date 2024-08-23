import os
import csv
import re

def format_and_collect_data(directory):
    all_data = []
    
    # Gehe durch alle Dateien im angegebenen Verzeichnis
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                
                if not rows:
                    continue
                
                # Extrahiere das Datum aus dem Dateinamen
                # Beispiel: "TeamA_28.10.2023.csv" -> "28.10.2023"
                date_match = re.search(r'_(\d{2}\.\d{2}\.\d{4})\.csv$', filename)
                date_str = date_match.group(1) if date_match else 'Unbekannt'
                
                # Extrahiere die Wettkampf- und Mannschaftsnamen aus der ersten Zeile
                wettkampf = rows[0][0] + ' - ' + rows[0][2]
                
                # Durchlaufe die Tabelle und formatiere die Daten
                current_gerät = ""
                for row in rows[1:]:
                    if len(row) == 1 and row[0] != "":
                        current_gerät = row[0]
                    elif len(row) > 1 and "Turner" not in row[0]:
                        # Prüfe, ob es sich um eine "Summe" oder "Gesamt"-Zeile handelt
                        if row[0] not in ["Summe", "Gesamt"]:
                            if row[0]:  # Daten auf der linken Seite
                                all_data.append([date_str, wettkampf, current_gerät, rows[0][0], row[0], row[1], row[2], row[3]])
                            if row[5]:  # Daten auf der rechten Seite
                                all_data.append([date_str, wettkampf, current_gerät, rows[0][2], row[5], row[6], row[7], row[8]])
    
    return all_data

def save_to_full_csv(data, file_path):
    # Speichere die gesammelten und formatierten Daten in eine CSV-Datei
    header = ["Datum", "Wettkampf", "Gerät", "Mannschaft", "Turner", "D-Note", "Endwert", "Score"]
    
    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)


def format_and_save_data():
    base_directory = 'Daten'
    input_directory = os.path.join(base_directory, 'Einzelwettkämpfe')
    output_file = os.path.join(base_directory, 'FullData.csv')
    
    collected_data = format_and_collect_data(input_directory)
    save_to_full_csv(collected_data, output_file)
    
    print(f"Alle Daten wurden erfolgreich in {output_file} gespeichert.")

if __name__ == "__main__":
    format_and_save_data()