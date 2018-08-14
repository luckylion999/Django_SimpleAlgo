from django.shortcuts import render
from django.http import HttpResponse
from .utils import algo_result
from .models import Algo
import requests

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


def index(request):
    algo_list = Algo.objects.all()
    return render(
        request, 'index.html',
        {
            'algo_list': algo_list
        }
    )


def plot(request):
    plot_id = request.GET.get('id')
    if plot_id:
        algo_list = Algo.objects.all()
        current_algo = Algo.objects.get(id=plot_id)
        positions_y = current_algo.positions
        positions_x = [i for i in range(1, len(positions_y) + 1)]
        pnl_y = current_algo.daily_pnl
        pnl_x = [i for i in range(1, len(pnl_y) + 1)]

        plt.figure(1)
        plt.title('Positions Chart')
        plt.plot(positions_x, positions_y)
        plt.figure(2)
        plt.title('PNL Chart')
        plt.plot(pnl_x, pnl_y)

        return render(
            request, 'index.html',
            {
                'algo_list': algo_list,
                'plt': plt
            }
        )


def save_data(request):
    algo_name = request.POST.get('algo_name')
    signal = request.POST.get('signal')
    trade = request.POST.get('trade')
    ticker = request.POST.get('ticker')

    api_url = 'https://api.iextrading.com/1.0/stock/{}/chart/1y'.format(ticker)
    try:
        json_data = requests.get(api_url).json()
        prices = [j.get('close') for j in json_data]
        [positions, PnL] = algo_result(signal, trade, prices)
        avg_pnl = sum(PnL) / len(PnL)
        algo = Algo(algo_name=algo_name, positions=positions, daily_pnl=PnL, avg_pnl=avg_pnl)
        algo.save()
    except:
        print('error while parsing json')

    return HttpResponse("Algo data saved successfully!")
