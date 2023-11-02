"""Module with utils"""
from queue import Queue
import sys
from threading import Thread
import os
import asyncio
from typing import Callable, List
import aiohttp


def async_wrapper(f: Callable, f_args: List = ()) -> any:
    """Function wrapper for async functions"""
    def wrapper(q):
        x = asyncio.run(f(*f_args))
        q.put(x)
    q = Queue()
    wrapper(q)
    return q.get()


async def request_async(url: str):
    """Async request"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data


def create_folder(path: str):
    """Function creating folder if folder not found"""
    try:
        if sys.version_info[0] == 3:
            os.makedirs(path)
        else:
            path.replace("/", "\\")
            os.makedirs(path)
    except FileExistsError:
        return


def new_thread(f: Callable, f_args: List = (), f_async: bool = False) -> any:
    """
    Creates a new thread from the passed function f(f_args)
    and returns the result of executing this function.

    @f: function.
    @f_args: [args] for function.
    @f_async: run an asynchronous function.
    """
    def result(q):
        if f_async:
            x = asyncio.run(f(*f_args))
            q.put(x)
        else:
            x = f(*f_args)
            q.put(x)

    q = Queue()
    t = Thread(target=result, args=(q,))
    t.start()
    t.join()

    return q.get()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = os.path.abspath(
            ".")  # pylint: disable=no-member,protected-access
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
