import json
import pathlib
import sys
import re

import requests


def get_most_recent_vaccine_file():

    pdf_folder = pathlib.Path('dgs-reports-archive/')

    pdf_files = list(pdf_folder.glob('*.pdf'))

    pdf_files.sort(key=lambda p: p.stem, reverse=True)

    last_pdf = str(pdf_files[0])
    # print(f'last_pdf={last_pdf}')
    last_date = last_pdf[-14:-4].replace('_', '-')
    #print(f'last_date={last_date}')

    return last_date


def get_vaccine_data_from_api():

    url = 'https://covid19.min-saude.pt/relatorio-de-situacao/'

    response = requests.get(url=url)

    if response.status_code != 200:
        raise ValueError('Unable to retrieve data from vaccine endpoint. Error %s: $s' % response.status_code, response.text)

    #print(response.text)
    matches = re.search(r'\| ([0-9][0-9]/[0-9][0-9]/20[0-9][0-9])</a>', response.text)
    latest_date = matches.group(1).replace('/', '-')
    #print(latest_date)

    return latest_date


if __name__ == '__main__':

    current_data = get_most_recent_vaccine_file()

    new_data = get_vaccine_data_from_api()

    try:
        assert current_data == new_data
    except AssertionError:
        print("TRUE")
        sys.exit()

    print("FALSE")