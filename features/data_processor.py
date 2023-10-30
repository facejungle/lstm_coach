"""Module with data processor"""
import asyncio
import io
import os
import aiofiles
import pandas as pd
from features.utils import create_folder, new_thread, resource_path


def instruments_to_csv(markets: list, instruments: list, filepath: str):
    """Import instruments to filepath"""
    res_path = resource_path(filepath)
    file = read_csv__(res_path)
    df = pd.DataFrame({"market": markets, "instrument": instruments})
    if file is not None:
        if not file.equals(df):
            write_csv_thread(df, res_path)
            print('Update: ', res_path)
    else:
        write_csv__(df, res_path)


def read_csv__(file_path: str) -> pd.DataFrame:
    """Read csv file"""
    while True:
        try:
            res_path = resource_path(file_path)
            df = pd.read_csv(res_path)
            return df
        except FileNotFoundError:
            create_folder(os.path.dirname(res_path))
            write_csv__(pd.DataFrame(), res_path)
        except pd.errors.EmptyDataError:
            return


def read_csv_thread(file_path: str) -> pd.DataFrame:
    """Async read csv file with new thread"""
    return new_thread(read_csv_async, ([file_path, True]), True)


async def read_csv_async(file_path: str, with_create=False) -> pd.DataFrame:
    """
    Reading csv file from file_path, if file not found - creating new empty file.
    file_path = /example/data.csv
    """
    res_path = resource_path(file_path)
    try:
        async with aiofiles.open(res_path, mode='r') as file:
            content = await file.read()
            if content.strip():
                df = pd.read_csv(io.StringIO(content))
                return df
            return pd.DataFrame()
    except FileNotFoundError:
        if with_create:
            create_folder(os.path.dirname(res_path))
            await write_csv_async(pd.DataFrame(), res_path)
        else:
            print('ERROR: FOLDER OR FILE NOT FOUND',
                  {file_path, read_csv_async})


def write_csv__(data: pd.DataFrame, file_path: str):
    """Write csv file"""
    while True:
        try:
            res_path = resource_path(file_path)
            df = data.to_csv(res_path, index=False)
            return df
        except FileNotFoundError:
            print('ERROR: FOLDER NOT FOUND', {file_path, write_csv_async})
            create_folder(os.path.dirname(file_path))


def write_csv_thread(data: pd.DataFrame, file_path: str):
    """Async write csv file with new thread"""
    return new_thread(write_csv_async, ([data, file_path]), True)


async def write_csv_async(data: pd.DataFrame, file_path: str):
    """
    Writing data to file_path
    @data = pd.DataFrame({"example": 1})
    @file_path = /example/data.csv
    """
    try:
        res_path = resource_path(file_path)
        async with aiofiles.open(res_path, mode='w') as file:
            csv_content = data.to_csv(index=False)
            await file.write(csv_content)
    except FileNotFoundError:
        print('ERROR: FOLDER NOT FOUND', {file_path, write_csv_async})
        create_folder(os.path.dirname(file_path))
