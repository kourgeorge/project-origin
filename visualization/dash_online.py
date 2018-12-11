__author__ = 'gkour'
from bokeh.plotting import figure, output_file, show, save
from bokeh.models import ColumnDataSource, Slider, Select
import numpy as np


def _create_prices(t):
    last_average = 100
    returns = np.asarray(np.random.lognormal(mean.value, stddev.value, 1))
    average = last_average * np.cumprod(returns)
    high = average * np.exp(abs(np.random.gamma(1, 0.03, size=1)))
    low = average / np.exp(abs(np.random.gamma(1, 0.03, size=1)))
    delta = high - low
    open = low + delta * np.random.uniform(0.05, 0.95, size=1)
    close = low + delta * np.random.uniform(0.05, 0.95, size=1)
    return open[0], high[0], low[0], close[0], average[0]


def _moving_avg(prices, days=10):
    if len(prices) < days: return [100]
    return np.convolve(prices[-days:], np.ones(days, dtype=float), mode="valid") / days


def _ema(prices, days=10):
    if len(prices) < days or days < 2: return [prices[-1]]
    a = 2.0 / (days + 1)
    kernel = np.ones(days, dtype=float)
    kernel[1:] = 1 - a
    kernel = a * np.cumprod(kernel)
    # The 0.8647 normalizes out that we stop the EMA after a finite number of terms
    return np.convolve(prices[-days:], kernel, mode="valid") / (0.8647)


MA12, MA26, EMA12, EMA26 = '12-tick Moving Avg', '26-tick Moving Avg', '12-tick EMA', '26-tick EMA'
mean = Slider(title="mean", value=0, start=-0.01, end=0.01, step=0.001)
stddev = Slider(title="stddev", value=0.04, start=0.01, end=0.1, step=0.01)
mavg = Select(value=MA12, options=[MA12, MA26, EMA12, EMA26])


class Dashborad:
    def __init__(self, file_path="lines.html"):
        self._source = ColumnDataSource(dict(
            time=[], average=[], low=[], high=[], open=[], close=[],
            ma=[], macd=[], macd9=[], macdh=[], color=[]))

        output_file(file_path)

        p = figure(plot_height=500, tools="xpan,xwheel_zoom,xbox_zoom,reset", x_axis_type=None, y_axis_location="right")
        p.x_range.follow = "end"
        p.x_range.follow_interval = 100
        p.x_range.range_padding = 0

        p.line(x='time', y='average', alpha=0.2, line_width=3, color='navy', source=self._source)
        p.line(x='time', y='ma', alpha=0.8, line_width=2, color='orange', source=self._source)
        p.segment(x0='time', y0='low', x1='time', y1='high', line_width=2, color='black', source=self._source)
        p.segment(x0='time', y0='open', x1='time', y1='close', line_width=8, color='color', source=self._source)

        show(p)

    def update(self, t):
        # df = pd.DataFrame.from_csv(path=self._input_csv, header=0, index_col=0)
        #
        # x = [1, 2, 3, 4, 5]
        # y = np.random.randint(1, 10, 5)
        #
        # self._p.line(x, y, legend="Temp.", line_width=2)
        # save(self._p)

        open, high, low, close, average = _create_prices(t)
        color = "green" if open < close else "red"

        new_data = dict(
            time=[t],
            open=[open],
            high=[high],
            low=[low],
            close=[close],
            average=[average],
            color=[color],
        )

        close = self._source.data['close'] + [close]
        ma12 = _moving_avg(close[-12:], 12)[0]
        ma26 = _moving_avg(close[-26:], 26)[0]
        ema12 = _ema(close[-12:], 12)[0]
        ema26 = _ema(close[-26:], 26)[0]

        if mavg.value == MA12:
            new_data['ma'] = [ma12]
        elif mavg.value == MA26:
            new_data['ma'] = [ma26]
        elif mavg.value == EMA12:
            new_data['ma'] = [ema12]
        elif mavg.value == EMA26:
            new_data['ma'] = [ema26]

        macd = ema12 - ema26
        new_data['macd'] = [macd]

        macd_series = self._source.data['macd'] + [macd]
        macd9 = _ema(macd_series[-26:], 9)[0]
        new_data['macd9'] = [macd9]
        new_data['macdh'] = [macd - macd9]

        self._source.stream(new_data, 300)

dash = Dashborad()
for t in range(1000):
    dash.update(t)
