from django.shortcuts import render
from .utils import algo_result
from .models import Algo
import requests

import matplotlib
import PIL, PIL.Image
matplotlib.use('agg')
from matplotlib import pylab
from django.http import HttpResponse
from io import BytesIO
from pylab import *


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
    algo_list = Algo.objects.all()
    if plot_id:
        current_algo = Algo.objects.get(id=plot_id)
        positions_y = current_algo.positions
        positions_x = [i for i in range(1, len(positions_y) + 1)]
        pnl_y = current_algo.daily_pnl
        pnl_x = [i for i in range(1, len(pnl_y) + 1)]

        fig = pylab.figure()
        fig.add_subplot(2, 2, 1)
        pylab.plot(positions_x, positions_y)
        fig.add_subplot(2, 2, 2)
        pylab.plot(pnl_x, pnl_y)

        buffer = BytesIO()
        canvas = pylab.get_current_fig_manager().canvas
        canvas.draw()
        pilImage = PIL.Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
        pilImage.save(buffer, "PNG")
        pylab.close()

        return HttpResponse(buffer.getvalue(), content_type="image/png")

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
