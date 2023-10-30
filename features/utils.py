"""Module with utils"""
from queue import Queue
import sys
from threading import Thread
import os
import asyncio
from typing import Callable, List


def create_folder(path: str):
    """Function creating folder if folder not found"""
    try:
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
        base_path = sys._MEIPASS  # pylint: disable=no-member,protected-access
    except Exception:  # pylint: disable=broad-exception-caught
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
