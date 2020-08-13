import asyncio
import pytoml as toml
import os
import time
import logging
import timeit
from aiohttp import ClientSession

log = logging.getLogger(__name__)


def load_config(config_path: str) -> dict:
    """Загрузка конфига."""
    with open(f'{os.getcwd()}{config_path}') as f:
        conf = toml.load(f)
    return conf


async def get_response(url, session):
    """"""
    async with session.get(url) as response:
        return await response.read()


async def fetch_worker(url_queue):
    """"""
    async with ClientSession() as session:
        while True:
            url = await url_queue.get()
            try:
                if url is None:
                    # all work is done
                    return

                response = await get_response(url, session)
                # ...do something with the response
            finally:
                url_queue.task_done()
                # for the url_queue.join() to work correctly


def create_sim_task(url_queue, qty_sim_con):
    """Создаём таски для начала одновременной обработки."""
    worker_tasks = []
    for _ in range(qty_sim_con):
        wt = asyncio.create_task(fetch_worker(url_queue))
        worker_tasks.append(wt)
    return worker_tasks


async def put_to_queue(url_queue, url, qty_request):
    """Кладём в очередь."""
    for _ in range(1, qty_request + 1):
        await url_queue.put(url)


async def work_is_done(url_queue, qty_sim_con):
    """Сообщить очереди, что работа выполнена."""
    for _ in range(qty_sim_con):
        await url_queue.put(None)


async def fetch_all(config: dict):
    """"""
    url = config.get('url')
    queue_size = config.get('queue_size')
    qty_sim_con = config.get('qty_simultaneous_connection')
    qty_request = config.get('qty_request')
    url_queue = asyncio.Queue(maxsize=queue_size)

    worker_tasks = create_sim_task(url_queue, qty_sim_con)

    await put_to_queue(url_queue, url, qty_request)
    await work_is_done(url_queue, qty_sim_con)
    await url_queue.join()

    await asyncio.gather(*worker_tasks)


def main(config_path: str):
    """"""
    logging.basicConfig(level=logging.DEBUG)
    config = load_config(config_path)

    # qty_runs = 100
    # res = timeit.timeit(lambda: asyncio.run(fetch_all(config)),
    #                     number=qty_runs)
    # print(f'{config.get("qty_request")} items: get_url takes {round(res, 3)}'
    #       f' for {qty_runs} runs\n')

    start = time.time()
    asyncio.run(fetch_all(config))
    end = time.time() - start
    log.debug(f'END   {round(end, 3)} sec ({round(end/60, 3)} min)')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()

    if args.config:
        main(args.config)
    else:
        parser.print_help()
