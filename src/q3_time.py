from typing import List, Tuple
import json
from collections import defaultdict

def q3_time(file_path: str) -> List[Tuple[str, int]]:
    mention_counts = defaultdict(int)

    try:
        # Lectura del archivo línea por línea para no cargar todo en memoria
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Procesar solo líneas no vacías
                    try:
                        tweet = json.loads(line.strip())
                        # Obtención de usuarios mencionados en cada tweet
                        mentioned_users = tweet.get("mentionedUsers", [])
                        
                        if mentioned_users:  # Verifica si la lista no está vacía
                            for user in mentioned_users:
                                username = user.get("username")
                                if username:
                                    mention_counts[username] += 1

                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar JSON en la línea: {line}. Error: {e}")
                    except KeyError as e:
                        print(f"Error: Falta la clave esperada {e} en el tweet: {tweet}")
                    except Exception as e:
                        print(f"Error inesperado al procesar la línea: {line}. Error: {e}")

    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no fue encontrado.")
        return []
    except Exception as e:
        print(f"Error inesperado al abrir el archivo: {e}")
        return []

    # Obtener los 10 usuarios más mencionados
    top_influential = sorted(mention_counts.items(), key=lambda item: item[1], reverse=True)[:10]

    print(f"Top 10 usuarios más influyentes: {top_influential}")
    
    return top_influential


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
    exec_time, mem_used = measure_performance(q3_time, 'farmers-protest-tweets-2021-2-4.json')
    print(f"Tiempo de ejecución: {exec_time:.6f} segundos, Uso de memoria: {mem_used:.2f} MiB")