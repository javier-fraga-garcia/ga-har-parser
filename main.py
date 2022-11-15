import json
import argparse
import logging
from urllib.parse import unquote
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def json_parser(text):
    text = text.replace('/collect?', '')
    info = text.split('&')
    info = [hit.split('=') for hit in info]
    return {p[0]:unquote(p[1]) for p in info}

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='El nombre del archivo del que obtener los datos')
    parser.add_argument('-v', '--version', type=str, choices=['v=1', 'v=2'],
                        help='La version del script de GA que se desea analizar')
    parser.add_argument('-r', '--result', type=str, default='./res.csv', required=False,
                        help='Ruta y nombre del archivo donde almacenar los datos procesados')
    parser.add_argument('-o', '--output', type=str, default='json', choices=['json', 'csv'], required=False,
                        help='El formato en el que se desea el archivo de resultados')

    args = parser.parse_args()
    file_name = args.file
    version = args.version
    res_file = args.result
    output = args.output

    with open(file_name, 'r', encoding='utf-8') as f:
        json_file = json.loads(f.read())
    logger.info('Archivo HAR cargado correctamente')

    entries = json_file['log']['entries']

    logger.info('Se han detectado {} entradas'.format(len(entries)))

    ga_entries = list(filter(lambda entrie: 'collect?{}'.format(version) in entrie['request']['url'], entries))

    logger.info('Se han detectado {} requests provenientes de GA para la versión {}'.format(len(ga_entries), version))

    res = list(map(lambda entrie: entrie['request']['headers'][2]['value'], ga_entries))
    with open(res_file, 'w', encoding='utf-8') as f:
        if (output == 'json'):
            jsonRes = list(map(lambda x: json_parser(x), res))
            f.write(json.dumps(jsonRes, ensure_ascii=False))
        else:
            f.writelines(['{}\n'.format(req) for req in res])

    logger.info('Se ha escrito el archivo de resultados correctamente')


if __name__ == '__main__':
    main()