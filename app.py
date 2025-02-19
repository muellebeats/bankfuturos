from flask import Flask, render_template
from datetime import datetime, timedelta, time, date
import math
import pytz  # Asegúrate de instalar pytz con: pip install pytz

app = Flask(__name__)

# Definimos la zona horaria UTC-3 (ejemplo: Buenos Aires)
tz = pytz.timezone('America/Argentina/Buenos_Aires')

# ─────────────────────────────────────────────────────────────────────────
# Funciones para calcular el próximo cierre de vela en UTC-3
# ─────────────────────────────────────────────────────────────────────────

def next_close_15m(now):
    interval = 15 * 60  # 15 minutos en segundos
    next_ts = math.floor(now.timestamp() / interval + 1) * interval
    return datetime.fromtimestamp(next_ts, tz)

def next_close_1h(now):
    interval = 3600  # 1 hora en segundos
    next_ts = math.floor(now.timestamp() / interval + 1) * interval
    return datetime.fromtimestamp(next_ts, tz)

def next_close_4h(now):
    interval = 4 * 3600
    next_ts = math.floor(now.timestamp() / interval + 1) * interval
    return datetime.fromtimestamp(next_ts, tz)

def next_close_8h(now):
    interval = 8 * 3600
    next_ts = math.floor(now.timestamp() / interval + 1) * interval
    return datetime.fromtimestamp(next_ts, tz)

def next_close_1d(now):
    # Cierre diario: definimos la "medianoche" local de mañana
    tomorrow = (now + timedelta(days=1)).date()
    local_midnight = datetime.combine(tomorrow, time.min)  # sin zona horaria
    # "localizamos" la fecha en tz UTC-3
    return tz.localize(local_midnight)

def next_close_3d(now):
    # Cada 3 días en segundos
    seconds_per_3d = 3 * 86400
    next_ts = math.floor(now.timestamp() / seconds_per_3d + 1) * seconds_per_3d
    return datetime.fromtimestamp(next_ts, tz)

def next_close_1w(now):
    # Suponiendo que la vela semanal cierra el LUNES a la medianoche local
    days_ahead = (7 - now.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_monday = (now + timedelta(days=days_ahead)).date()
    local_midnight = datetime.combine(next_monday, time.min)
    return tz.localize(local_midnight)

def next_close_1m(now):
    # Para la vela mensual, consideramos el primer día del mes siguiente
    year = now.year
    month = now.month
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    local_midnight = datetime.combine(next_month, time.min)
    return tz.localize(local_midnight)

# ─────────────────────────────────────────────────────────────────────────
# RUTA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    # Obtenemos la hora actual en UTC-3
    now = datetime.now(tz)

    # Calculamos el próximo cierre para cada intervalo en UTC-3
    countdowns = {
        "15m": next_close_15m(now).isoformat(),
        "1h": next_c
