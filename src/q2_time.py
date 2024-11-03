from typing import List, Tuple
import json
from collections import Counter
import emoji

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    emoji_counter = Counter()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Procesar solo líneas no vacías
                    try:
                        tweet = json.loads(line)
                        content = tweet.get('content', '')
                        
                        # Usar emoji.emoji_list() para obtener todos los emojis en el contenido
                        emojis_in_tweet = [e['emoji'] for e in emoji.emoji_list(content)]
                        emoji_counter.update(emojis_in_tweet)

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

    # Obtener los 10 emojis más comunes
    top_emojis = emoji_counter.most_common(10)

    print(f"Top 10 emojis: {top_emojis}")
    return top_emojis

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
    exec_time, mem_used = measure_performance(q2_time, 'farmers-protest-tweets-2021-2-4.json')
    print(f"Tiempo de ejecución: {exec_time:.6f} segundos, Uso de memoria: {mem_used:.2f} MiB")