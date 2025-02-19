from flask import Flask, render_template
from datetime import datetime, timedelta, time, date
import math

app = Flask(__name__)

# Funciones para calcular el próximo cierre de vela para cada timeframe

def next_close_15m(now):
    interval = 15 * 60  # 15 minutos en segundos
    next_ts = math.floor(now.timestamp() / interval + 1) * interval
    return datetime.fromtimestamp(next_ts)

def next_close_1h(now):
    interval = 3600  # 1 hora en segundos
    next_ts = math.floor(now.timestamp() / interval + 1) * interval
    return datetime.fromtimestamp(next_ts)

def next_close_4h(now):
    interval = 4 * 3600
    next_ts = math.floor(now.timestamp() / interval + 1) * interval
    return datetime.fromtimestamp(next_ts)

def next_close_8h(now):
    interval = 8 * 3600
    next_ts = math.floor(now.timestamp() / interval + 1) * interval
    return datetime.fromtimestamp(next_ts)

def next_close_1d(now):
    # El cierre diario se asume a la medianoche del día siguiente
    tomorrow = now.date() + timedelta(days=1)
    return datetime.combine(tomorrow, time.min)

def next_close_3d(now):
    seconds_per_3d = 3 * 86400
    next_ts = math.floor(now.timestamp() / seconds_per_3d + 1) * seconds_per_3d
    return datetime.fromtimestamp(next_ts)

def next_close_1w(now):
    # Suponiendo que la vela semanal cierra el lunes a la medianoche
    days_ahead = (7 - now.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_monday = now.date() + timedelta(days=days_ahead)
    return datetime.combine(next_monday, time.min)

def next_close_1m(now):
    # Para la vela mensual, se considera el primer día del mes siguiente
    year = now.year
    month = now.month
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    return datetime.combine(next_month, time.min)

@app.route("/")
def index():
    now = datetime.now()
    # Calculamos el próximo cierre para cada intervalo y lo pasamos en formato ISO
    countdowns = {
        "15m": next_close_15m(now).isoformat(),
        "1h": next_close_1h(now).isoformat(),
        "4h": next_close_4h(now).isoformat(),
        "8h": next_close_8h(now).isoformat(),
        "1d": next_close_1d(now).isoformat(),
        "3d": next_close_3d(now).isoformat(),
        "1w": next_close_1w(now).isoformat(),
        "1m": next_close_1m(now).isoformat(),
    }
    return render_template("index.html", countdowns=countdowns)

if __name__ == "__main__":
    app.run(debug=True)
