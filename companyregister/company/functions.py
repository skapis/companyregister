import requests
import xmltodict
from bs4 import BeautifulSoup
from lxml import etree


def get_company(company_id):
    url = f'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_or.cgi?ico={company_id}&jazyk=cz&xml=1'
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = xmltodict.parse(response.content)
        resp_data = general_info(data)
        if get_nace(company_id) is not None:
            resp_data.update({'nace': get_nace(company_id)})
        return resp_data
    return requests.exceptions.RequestException


def general_info(data):
    response_number = data['are:Ares_odpovedi']['are:Odpoved']['D:PZA']
    if response_number != '0':
        if response_number == '1':
            data = data
        else:
            data = data[0]
        company_data = data['are:Ares_odpovedi']['are:Odpoved']['D:Vypis_OR']
        source = company_data['D:UVOD']['D:ND']
        date = company_data['D:UVOD']['D:DVY']
        time = company_data['D:UVOD']['D:CAS']
        timestamp = f'{date} {time}'
        company_name = company_data['D:ZAU']['D:OF']
        ic = company_data['D:ZAU']['D:ICO']
        incorporation_date = company_data['D:ZAU']['D:DZOR']
        legal_form = company_data['D:ZAU']['D:PFO']['D:NPF']
        legal_form_code = company_data['D:ZAU']['D:PFO']['D:KPF']
        state = company_data['D:ZAU']['D:S']['D:SSU']

        response = {
            'companyId': ic,
            'name': company_name,
            'legalFormCode': legal_form_code,
            'legalFormName': legal_form,
            'state': state,
            'dateOfIncorporation': incorporation_date,
            'source': source,
            'ts': timestamp,
            'address': company_address(company_data['D:ZAU']['D:SI'])
        }
        return response
    else:
        message = data['are:Ares_odpovedi']['are:Odpoved']['D:VH']['D:T']
        return {'error': message}


def company_address(element):
    output = {
        'id': element['D:IDA']
    }
    if element.get('D:AT') is not None:
        output.update({'fullAddress': element['D:AT']})
    if element.get('D:NS') is not None:
        output.update({'country': element['D:NS']})
    if element.get('D:NU') is not None:
        output.update({'street': element['D:NU']})
    if element.get('D:CD') is not None:
        output.update({'streetNo': element['D:CD']})
    if element.get('D:CO') is not None:
        output.update({'houseNo': element['D:CO']})
    if element.get('D:N') is not None:
        output.update({'city': element['D:N']})
    if element.get('D:NCO') is not None:
        output.update({'cityPart': element['D:NCO']})
    if element.get('D:PSC') is not None:
        output.update({'zipCode': element['D:PSC']})
    if element.get('D:CA') is not None:
        output.update({'streetHouseNo': element['D:CA']})

    return output


def get_nace(company_id):
    url = f'https://apl.czso.cz/res/detail?ico={company_id}'
    data = requests.get(url, timeout=10)
    soup = BeautifulSoup(data.text, 'html.parser')
    dom = etree.HTML(str(soup))
    try:
        main_nace = dom.xpath('/html/body/div[2]/div[2]/div[7]/div[2]')[0].text
        code = main_nace.split(" - ")[0]
        name = main_nace.split(" - ")[1]
        return {'code': code, 'name': name}
    except:
        return None


def get_entrepreneur(ico):
    url = f'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_res.cgi?ico={ico}&jazyk=cz&xml=1'
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = xmltodict.parse(response.content)
        resp_data = parse_entrepreneur_data(data)
        if get_nace(ico) is not None:
            resp_data.update({'nace': get_nace(ico)})
        return resp_data
    return requests.exceptions.RequestException


def parse_entrepreneur_data(data):
    response_number = data['are:Ares_odpovedi']['are:Odpoved']['D:PZA']
    if response_number != '0':
        if response_number == '1':
            data = data
        else:
            data = data[0]
        ent_data = data['are:Ares_odpovedi']['are:Odpoved']['D:Vypis_RES']
        source = ent_data['D:UVOD']['D:ND']
        date = ent_data['D:UVOD']['D:DVY']
        time = ent_data['D:UVOD']['D:CAS']
        timestamp = f'{date} {time}'
        name = ent_data['D:ZAU']['D:OF']
        ic = ent_data['D:ZAU']['D:ICO']
        legal_form_code = ent_data['D:ZAU']['D:PF']['D:KPF']
        legal_form = ent_data['D:ZAU']['D:PF']['D:NPF']
        incorporation_date = ent_data['D:ZAU']['D:DV']
        try:
            remove_date = ent_data['D:ZAU']['D:DZ']
            state = 'Zaniklý'
        except:
            state = 'Aktivní'

        response = {
            'entId': ic,
            'name': name,
            'legalFormCode': legal_form_code,
            'legalFormName': legal_form,
            'state': state,
            'dateOfIncorporation': incorporation_date,
            'source': source,
            'ts': timestamp,
            'address': company_address(ent_data['D:SI'])
        }

        return response


