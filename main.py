from modules import scrape_data, format_and_save_data


def main():
    base_url = 'https://www.deutsche-turnliga.de/dtl/historie/archiv/detailsm0.html?ID='
    start_id = 2466
    end_id = 2605
    table_selector = 'table.Einzelnachweis.table.table-condensed'
    date_container_selector = 'div.artikel.topbalken:has(h3.balken:has-text("Infos zum Wettkampf"))'

    scrape_data(base_url, start_id, end_id, table_selector, date_container_selector)
    format_and_save_data()

if __name__ == "__main__":
    main()