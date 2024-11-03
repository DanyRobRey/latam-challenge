from typing import List, Tuple
import ujson
from collections import defaultdict
from datetime import datetime
from dateutil import parser
import heapq

def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    date_user_counts = defaultdict(lambda: defaultdict(int))

    # Lectura del archivo línea por línea
    try:
        with open(file_path, 'r') as file:
            for line in file:  # Iterar directamente sobre el archivo
                try:
                    tweet = ujson.loads(line.strip())  # Uso de ujson para mejorar la velocidad
                    tweet_date = parser.parse(tweet['date']).date()
                    username = tweet['user']['username']

                    # Asegurarse de que username no esté vacío o sea None
                    if username:
                        date_user_counts[tweet_date][username] += 1
                    else:
                        print(f"Advertencia: Username vacío en el tweet de la fecha {tweet_date}")

                except ujson.JSONDecodeError as e:
                    print(f"Error al decodificar JSON en la línea: {line}. Error: {e}")
                except KeyError as e:
                    print(f"Error: Falta la clave esperada {e} en el tweet: {tweet}")

    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error inesperado al abrir el archivo: {e}")
        return []

    # Mantener solo los 10 días con más tweets
    top_dates = []
    
    for date_, user_counts in date_user_counts.items():
        total_tweets = sum(user_counts.values())
        if len(top_dates) < 10:
            heapq.heappush(top_dates, (total_tweets, date_, user_counts))
        else:
            heapq.heappushpop(top_dates, (total_tweets, date_, user_counts))

    # Obtener los resultados finales
    result = []
    for total, date_, user_counts in top_dates:
        if user_counts:  # Verificar que user_counts no esté vacío
            most_common_user = max(user_counts.items(), key=lambda item: item[1])[0]
            result.append((date_, most_common_user))
        else:
            print(f"Advertencia: No hay usuarios para la fecha {date_}")

    # Ordenar el resultado por fecha
    result.sort(key=lambda x: x[0])

    print(f"Resultado: {result}")
    
    return result

from memory_profiler import memory_usage
import time

def measure_performance(func, *args, **kwargs):
    start_time = time.time()
    mem_usage = memory_usage((func, args, kwargs), interval=0.1)
    end_time = time.time()

    execution_time = end_time - start_time
    memory_used = max(mem_usage) - min(mem_usage)

    return execution_time, memory_used


if __name__ == '__main__':
    exec_time, mem_used = measure_performance(q1_time, 'farmers-protest-tweets-2021-2-4.json')
    print(f"Tiempo de ejecución: {exec_time:.6f} segundos, Uso de memoria: {mem_used:.2f} MiB")
