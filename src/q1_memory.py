from typing import List, Tuple
import json
from datetime import datetime
from collections import defaultdict, Counter
from datetime import datetime

from dateutil import parser 
from itertools import islice

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_user_counts = defaultdict(lambda: Counter())

    # Lectura del archivo línea por línea sin cargar todo en memoria
    try:
        with open(file_path, 'r') as file:
            for line in islice(file, None):  # islice puede ayudar a limitar si es necesario
                try:
                    tweet = json.loads(line.strip())
                    tweet_date = parser.parse(tweet['date']).date()
                    username = tweet['user']['username']

                    # Asegurarse de que username no esté vacío o sea None
                    if username:
                        date_user_counts[tweet_date][username] += 1
                    else:
                        print(f"Advertencia: Username vacío en el tweet de la fecha {tweet_date}")

                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON en la línea: {line}. Error: {e}")
                except KeyError as e:
                    print(f"Error: Falta la clave esperada {e} en el tweet: {tweet}")

    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error inesperado al abrir el archivo: {e}")
        return []

    # Mantener solo los 10 días con más tweets en memoria
    top_dates = sorted(date_user_counts.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]
    
    result = []
    for date_, user_counts in top_dates:
        if user_counts:
            most_common_user = user_counts.most_common(1)[0][0]
            result.append((date_, most_common_user))
        else:
            print(f"Advertencia: No hay usuarios para la fecha {date_}")

    print(f"Resultado: {result}")
    
    return result

import time
from memory_profiler import memory_usage

def measure_performance(func, *args, **kwargs):
    start_time = time.time()
    mem_usage = memory_usage((func, args, kwargs), interval=0.1)
    end_time = time.time()

    execution_time = end_time - start_time
    memory_used = max(mem_usage) - min(mem_usage)

    return execution_time, memory_used


if __name__ == '__main__':
    exec_time, mem_used = measure_performance(q1_memory, 'farmers-protest-tweets-2021-2-4.json')
    print(f"Tiempo de ejecución: {exec_time:.6f} segundos, Uso de memoria: {mem_used:.2f} MiB")
