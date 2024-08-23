import csv
import os
from playwright.sync_api import sync_playwright

def create_directories():
    # Erstelle den Hauptordner "Daten" falls er nicht existiert
    main_folder = 'Daten'
    if not os.path.exists(main_folder):
        os.mkdir(main_folder)
        print(f"Ordner {main_folder} erstellt.")

    # Erstelle den Unterordner "Einzelwettkämpfe" oder "Einzelwettkämpfe_2", wenn er bereits existiert
    sub_folder = 'Einzelwettkämpfe'
    sub_folder_path = os.path.join(main_folder, sub_folder)
    if os.path.exists(sub_folder_path):
        count = 2
        while os.path.exists(os.path.join(main_folder, f"{sub_folder}_{count}")):
            count += 1
        sub_folder = f"{sub_folder}_{count}"
        sub_folder_path = os.path.join(main_folder, sub_folder)
    
    os.mkdir(sub_folder_path)
    print(f"Unterordner {sub_folder_path} erstellt.")
    
    return sub_folder_path

def extract_table_content(page, table_selector, date_container_selector):
    # Finde die spezifische Tabelle auf der Seite
    table = page.query_selector(table_selector)
    
    if table is None:
        print("Tabelle nicht gefunden!")
        return [], "", ""
    
    # Extrahiere alle Zeilen der Tabelle
    rows = table.query_selector_all('tr')
    
    table_data = []
    team_names = ""
    
    for i, row in enumerate(rows):
        # Extrahiere die Zellen der aktuellen Zeile
        cells = row.query_selector_all('th, td')
        row_data = [cell.inner_text().strip() for cell in cells]
        table_data.append(row_data)
        
        # Verwende die erste Zeile für den Dateinamen
        if i == 0:
            team_names = row_data[0].replace(',', '').replace(' ', '_') + '-' + row_data[2].replace(',', '').replace(' ', '_')
    
    # Extrahiere das Datum aus der spezifischen Container-Tabelle
    date_container = page.query_selector(date_container_selector)
    date_text = ""
    if date_container:
        date_table = date_container.query_selector('table.table.table-condensed')
        if date_table:
            date_rows = date_table.query_selector_all('tr')
            for row in date_rows:
                cells = row.query_selector_all('td')
                if len(cells) > 1:
                    label = cells[0].inner_text().strip()
                    if label == "Termin:":
                        date_text = cells[1].inner_text().strip().split(' ')[0]
                        break
    
    return table_data, team_names, date_text

def save_to_csv(directory, file_name, table_data):
    # Speichere die Tabelle in eine CSV-Datei im angegebenen Verzeichnis
    file_path = os.path.join(directory, file_name)
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(table_data)

def process_urls(base_url, start_id, end_id, table_selector, date_container_selector):
    # Erstelle die notwendigen Ordner und bekomme den Pfad zurück
    target_directory = create_directories()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i in range(start_id, end_id + 1):
            url = f"{base_url}{i}"
            print(f"Verarbeite URL: {url}")
            page.goto(url)
            
            # Extrahiere den Inhalt der spezifischen Tabelle, den Dateinamen und das Datum
            table_data, team_names, date_text = extract_table_content(page, table_selector, date_container_selector)
            
            if table_data:
                # Verwende die ersten Teamnamen und das Datum für den Dateinamen
                file_name = f"{team_names}_{date_text}.csv" if date_text else f"{team_names}.csv"
                save_to_csv(target_directory, file_name, table_data)
                print(f"Tabelle gespeichert in: {os.path.join(target_directory, file_name)}")
            else:
                print(f"Keine Tabelle auf Seite {url} gefunden.")
        
        browser.close()

def process_urls(base_url, start_id, end_id, table_selector, date_container_selector):
    target_directory = create_directories()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i in range(start_id, end_id + 1):
            url = f"{base_url}{i}"
            print(f"Verarbeite URL: {url}")
            page.goto(url)
            
            table_data, team_names, date_text = extract_table_content(page, table_selector, date_container_selector)
            
            if table_data:
                file_name = f"{team_names}_{date_text}.csv" if date_text else f"{team_names}.csv"
                save_to_csv(target_directory, file_name, table_data)
                print(f"Tabelle gespeichert in: {os.path.join(target_directory, file_name)}")
            else:
                print(f"Keine Tabelle auf Seite {url} gefunden.")
        
        browser.close()

def scrape_data(base_url, start_id, end_id, table_selector, date_container_selector):
    process_urls(base_url, start_id, end_id, table_selector, date_container_selector)