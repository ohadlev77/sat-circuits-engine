import numpy as np
from multiprocessing import Pool
from time import sleep
from util import timer_dec

def sleep_and_return_args(*args):
    sleep_time = np.random.default_rng().choice(10)
    sleep(sleep_time)

    return {'sleep_time': sleep_time, 'args': args}

@timer_dec
def main():
    with Pool() as pool:
        doubled_items = pool.map_async(sleep_and_return_args, [1,2,3,4])
        
        # for index, item in enumerate(dir(doubled_items)):
        #     print(f"{index}. {item}")

        print(doubled_items.ready())

        for item in doubled_items.get():
            print(item)

        # for item in doubled_items:
        #     print(item)
        #     if item['sleep_time'] > 6:
        #         pool.terminate()
        #         print('TEST')
        #         break

if __name__ == "__main__":
    main()