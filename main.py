import json
import argparse
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--fileName', type=str, help='El nombre del archivo del que obtener los datos')
    parser.add_argument('--version', type=str, choices=['v=1', 'v=2'],
                        help='La version del script de GA que se desea analizar')
    parser.add_argument('--resultFile', type=str, default='./res.csv', required=False,
                        help='La version del script de GA que se desea analizar')

    args = parser.parse_args()
    file_name = args.fileName
    version = args.version
    res_file = args.resultFile

    with open(file_name, 'r', encoding='utf-8') as f:
        json_file = json.loads(f.read())
    logger.info('Archivo HAR cargado correctamente')

    entries = json_file['log']['entries']

    logger.info('Se han detectado {} entradas'.format(len(entries)))

    ga_entries = list(filter(lambda entrie: 'collect?{}'.format(version) in entrie['request']['url'], entries))

    logger.info('Se han detectado {} requests provenientes de GA para la versión {}'.format(len(ga_entries), version))

    res = list(map(lambda entrie: entrie['request']['headers'][2]['value'], ga_entries))

    with open(res_file, 'w') as f:
        f.writelines(['{}\n'.format(req) for req in res])

    logger.info('Se ha escrito el archivo de resultados correctamente')


if __name__ == '__main__':
    main()