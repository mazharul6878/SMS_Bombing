import asyncio
import aiohttp
import time
import datetime
import os

# Color
_c = {
    'g': '\033[92m', 'r': '\033[91m', 'y': '\033[93m',
    'c': '\033[96m', 'p': '\033[95m', 'b': '\033[94m', 'e': '\033[0m'
}

# State
_state = {'total': 0, 'success': 0, 'paused': False}

# Dashboard
def _print_dashboard():
    os.system('clear')
    now = datetime.datetime.now().strftime("%H:%M:%S")

    print(f"{_c['b']}==== SAFE DASHBOARD ===={_c['e']}")
    print(f"Time     : {now}")
    print(f"Total    : {_state['total']}")
    print(f"Success  : {_state['success']}")
    print(f"Failed   : {_state['total'] - _state['success']}")
    print(f"{_c['b']}{'='*28}{_c['e']}\n")

# Logging
def log_request(name, status, duration):
    _print_dashboard()

    now = datetime.datetime.now().strftime("%H:%M:%S")
    color = _c['g'] if status == 200 else _c['r']

    print(f"{_c['c']}[{now}]{_c['e']} {color}{name}{_c['e']}")
    print(f"{_c['y']}Status:{_c['e']} {status} | {duration}s")
    print(f"{_c['p']}{'-'*30}{_c['e']}")

# Dummy Request (Safe)
async def safe_request(session, name):
    url = "https://httpbin.org/post"  # safe test API

    start = time.time()

    try:
        async with session.post(url, json={"test": "ok"}) as resp:
            await resp.text()

        end = time.time()
        duration = round(end - start, 2)

        _state['total'] += 1
        if resp.status == 200:
            _state['success'] += 1

        log_request(name, resp.status, duration)

    except Exception as e:
        _state['total'] += 1
        log_request(name, 0, 0)

# Main Runner
async def main():
    async with aiohttp.ClientSession() as session:
        for i in range(10):  # test loop
            await safe_request(session, f"TestAPI-{i+1}")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
