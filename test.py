import concurrent.futures
import numpy as np
from app.shared.exchanges.binance import Binance


def sma(data: list, length: int, is_array=False):
    data = np.array(data, dtype=float)
    if len(data) < length:
        raise ValueError(
            "Length of data should be greater than or equal to 'length'")
    sum_val = np.sum(data[:length])
    if not is_array:
        return sum_val / length
    results = []
    for r in range(len(data) - length + 1):
        data_sliced = data[r:]
        sum_val = np.sum(data_sliced[:length])
        results.append(sum_val / length)
    return results


def calculate_profit(args):
    ratio_mult, prices, investments = args
    ratio, mult = ratio_mult
    balance = investments
    basis_length = int(round(ratio * mult))
    basis = sma(prices, basis_length, True)
    signal = sma(prices, mult, True)
    arrays_length = len(signal) - mult
    positions = [{'size': None, 'entry': 0}]
    counter = 0
    for i in range(arrays_length, -1, -1):
        if prices[i] is not None:
            price = prices[i]
            position_size_prev = positions[-1]['size']
            position_entry_prev = positions[-1]['entry']
            if balance > 0:
                if basis[i] > signal[i] and basis[i + 1] > signal[i + 1]:
                    counter += 1
                    if position_size_prev is None:
                        position_size = balance / price
                        positions.append(
                            {'size': position_size, 'entry': price})
                    elif position_size_prev < 0:
                        commission = (
                            (position_entry_prev * position_size_prev * -1) / 100) * 0.1
                        profit = (position_entry_prev -
                                  price) * position_size_prev
                        balance += -profit - commission
                        position_size = balance / price
                        positions.append(
                            {'size': position_size, 'entry': price})
                elif price < signal[i] and basis[i + 1] < signal[i + 1]:
                    if position_size_prev is None:
                        position_size = balance / price
                        positions.append(
                            {'size': -position_size, 'entry': price})
                    elif position_size_prev > 0:
                        commission = (
                            (position_entry_prev * position_size_prev) / 100) * 0.1
                        profit = (position_entry_prev -
                                  price) * position_size_prev
                        balance += profit - commission
                        position_size = balance / price
                        positions.append(
                            {'size': -position_size, 'entry': price})
    return {
        'ratio': ratio,
        'mult': mult,
        'positions': positions,
        'profit': balance - investments,
    }


def calculateMaxProfit(data: list, investments=100):
    prices = [float(i) for i in data]
    if len(prices) < 100:
        return
    all_positions = [{'ratio': 0, 'mult': 0, 'positions': [
        {'size': 0, 'entry': 0}], 'profit': 0}]
    print('Start calculate...')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        ratio_mults = [(x * 0.01, y) for x in range(101, 150)
                       for y in range(10, 200)]
        args = [(ratio_mult, prices, investments)
                for ratio_mult in ratio_mults]
        results = executor.map(calculate_profit, args)

        for result in results:
            all_positions.append(result)
            if result['profit'] > 20:
                print(result)

    max_profit_profit = max(all_positions, key=lambda x: x['profit'])
    return max_profit_profit


prices = [price[4] for price in Binance().parse_candles('BTCUSDC', '1h', 2000)]
print(prices)
t = calculateMaxProfit(prices)
print(t)
