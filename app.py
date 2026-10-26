"""
InvestQuant Pro — Cartera de Inversión & Análisis Técnico Cuantitativo
Arquitectura Mobile-First Ultra-Moderna para Streamlit Community Cloud
"""

import json
import os
import textwrap
import uuid
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple, Any

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import streamlit as st
import yfinance as yf

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA (MOBILE-FIRST) & SISTEMA DE DISEÑO ULTRA-MODERNO
# ==============================================================================

st.set_page_config(
    page_title="InvestQuant Pro | Fintech Mobile-First",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def render_html(html_content: str):
    """
    Renderiza HTML de forma 100% segura limpiando cualquier espacio inicial de cada
    línea y eliminando líneas en blanco intermedias, evitando de raíz que el motor
    de Markdown lo interprete como un bloque de código (<pre><code>).
    """
    clean_lines = [line.strip() for line in html_content.strip().splitlines() if line.strip()]
    st.markdown("".join(clean_lines), unsafe_allow_html=True)


# Inyección global de estilos CSS: forzado de modo oscuro, glassmorphism y fintech UI
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    /* 1. Reset Global y Forzado de Fondo Oscuro Fintech */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #080c15 !important;
        color: #f1f5f9 !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Espaciado responsivo compacto Mobile-First */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;
        max-width: 1380px !important;
    }

    /* 2. Barra Lateral Oscura */
    [data-testid="stSidebar"] {
        background-color: #0d1322 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* 3. Pestañas (Tabs) con Estilo Cápsula Moderna (Elimina la barra roja) */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0f172a !important;
        padding: 5px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        gap: 6px !important;
        margin-bottom: 1rem !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        padding: 8px 16px !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35) !important;
    }

    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }

    /* 4. Selector de Activos Pills (Elimina círculos y color rojo feo) */
    div[data-testid="stRadio"] > div {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        background: #0d1424 !important;
        padding: 6px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 12px !important;
    }

    div[data-testid="stRadio"] label {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        margin: 0 !important;
    }

    div[data-testid="stRadio"] label:hover {
        color: #f8fafc !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        background: rgba(56, 189, 248, 0.08) !important;
    }

    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, #2563eb 0%, #38bdf8 100%) !important;
        color: #ffffff !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
        font-weight: 700 !important;
    }

    div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
    
    div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        margin: 0 !important;
        font-size: 0.88rem !important;
    }

    /* 5. Botones Modernos Fintech */
    div.stButton > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.1rem !important;
        min-height: 42px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        background: #1e293b !important;
        color: #f8fafc !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        background: #334155 !important;
        border-color: rgba(56, 189, 248, 0.5) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35) !important;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        border: 1px solid #3b82f6 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4) !important;
    }

    div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    }

    /* 6. Expanders y Formularios */
    [data-testid="stExpander"] {
        background: #0d1322 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        margin-bottom: 12px !important;
    }

    [data-testid="stExpander"] details summary {
        font-weight: 600 !important;
        color: #e2e8f0 !important;
    }

    /* 7. Tablas y DataFrames */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# 2. GESTIÓN DE SECRETS Y CREDENCIALES TELEGRAM
# ==============================================================================

def get_telegram_config() -> Tuple[str, str]:
    """Obtiene las credenciales de Telegram priorizando st.secrets con fallback a manual."""
    bot_token = ""
    chat_id = ""

    try:
        if "TELEGRAM_BOT_TOKEN" in st.secrets:
            bot_token = str(st.secrets["TELEGRAM_BOT_TOKEN"]).strip()
        if "TELEGRAM_CHAT_ID" in st.secrets:
            chat_id = str(st.secrets["TELEGRAM_CHAT_ID"]).strip()
    except Exception:
        pass

    if "user_tg_token" in st.session_state and st.session_state.user_tg_token:
        bot_token = st.session_state.user_tg_token.strip()
    if "user_tg_chat" in st.session_state and st.session_state.user_tg_chat:
        chat_id = st.session_state.user_tg_chat.strip()

    return bot_token, chat_id


def send_telegram_alert(message: str) -> Tuple[bool, str]:
    """Envía un mensaje formateado a Telegram mediante la API oficial de Bots."""
    token, chat_id = get_telegram_config()
    if not token or not chat_id:
        return False, "Faltan credenciales de Telegram (Token o Chat ID)."

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload, timeout=8)
        data = response.json()
        if response.status_code == 200 and data.get("ok"):
            return True, "Mensaje enviado exitosamente a Telegram."
        else:
            return False, f"Error Telegram: {data.get('description', 'HTTP ' + str(response.status_code))}"
    except Exception as e:
        return False, f"Excepción de conexión: {str(e)}"


# ==============================================================================
# 3. GESTIÓN DE CARTERA (WALLET) CON PERSISTENCIA EN 'portfolio.json'
# ==============================================================================

PORTFOLIO_FILE = "portfolio.json"

DEFAULT_PORTFOLIO = [
    {
        "id": "tx-vuaa-init",
        "asset_name": "S&P 500 (VUAA)",
        "ticker": "VUAA.DE",
        "date": "2024-02-15",
        "price_eur": 88.50,
        "shares": 12.0,
        "commission_eur": 1.50,
        "notes": "Aportación DCA inicial",
    },
    {
        "id": "tx-4gld-init",
        "asset_name": "Oro Físico ETC (4GLD)",
        "ticker": "4GLD.DE",
        "date": "2024-03-20",
        "price_eur": 68.20,
        "shares": 10.0,
        "commission_eur": 1.25,
        "notes": "Reserva de valor",
    },
    {
        "id": "tx-silver-init",
        "asset_name": "Plata Futuros (SI=F)",
        "ticker": "SI=F",
        "date": "2024-04-10",
        "price_eur": 26.80,
        "shares": 20.0,
        "commission_eur": 2.00,
        "notes": "Posición táctica materias primas",
    },
]


def load_portfolio() -> List[Dict[str, Any]]:
    """Carga la cartera desde 'portfolio.json'. Si no existe, crea la plantilla por defecto."""
    if not os.path.exists(PORTFOLIO_FILE):
        save_portfolio(DEFAULT_PORTFOLIO)
        return DEFAULT_PORTFOLIO
    try:
        with open(PORTFOLIO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return DEFAULT_PORTFOLIO
    except Exception:
        return DEFAULT_PORTFOLIO


def save_portfolio(portfolio_data: List[Dict[str, Any]]) -> bool:
    """Guarda las transacciones en 'portfolio.json' de manera segura."""
    try:
        with open(PORTFOLIO_FILE, "w", encoding="utf-8") as f:
            json.dump(portfolio_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


# ==============================================================================
# 4. MOTOR DE DESCARGA DE MERCADO CON CACHEO INTELIGENTE (@st.cache_data)
# ==============================================================================

DEFAULT_ASSETS = {
    "S&P 500 (VUAA)": {
        "ticker": "VUAA.DE",
        "fallback": "^GSPC",
        "currency": "EUR",
        "category": "Índice / ETF",
    },
    "Oro (4GLD)": {
        "ticker": "4GLD.DE",
        "fallback": "GC=F",
        "currency": "EUR",
        "category": "Materia Prima",
    },
    "Plata": {
        "ticker": "SI=F",
        "fallback": None,
        "currency": "USD",
        "category": "Materia Prima",
    },
}


@st.cache_data(ttl=900)
def fetch_eur_usd_rate() -> float:
    """Obtiene la tasa de cambio EUR/USD para convertir activos en USD a Euros."""
    try:
        fx = yf.download("EURUSD=X", period="5d", interval="1d", progress=False)
        if fx is not None and not fx.empty:
            if isinstance(fx.columns, pd.MultiIndex):
                fx.columns = fx.columns.get_level_values(0)
            rate = float(fx["Close"].dropna().iloc[-1])
            if rate > 0:
                return rate
    except Exception:
        pass
    return 1.08


@st.cache_data(ttl=900)
def fetch_market_data(ticker: str, fallback_ticker: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], str, str]:
    """
    Descarga velas diarias (1D) de los últimos 2 años con soporte de fallback y
    conversión automática a Euros si la divisa es USD.
    """
    target_ticker = ticker
    used_ticker = ticker
    currency_note = "EUR"

    try:
        df = yf.download(target_ticker, period="2y", interval="1d", progress=False)
        if df is None or df.empty or len(df) < 30:
            if fallback_ticker:
                used_ticker = fallback_ticker
                df = yf.download(fallback_ticker, period="2y", interval="1d", progress=False)
    except Exception:
        if fallback_ticker:
            used_ticker = fallback_ticker
            try:
                df = yf.download(fallback_ticker, period="2y", interval="1d", progress=False)
            except Exception:
                df = None
        else:
            df = None

    if df is None or df.empty:
        return None, used_ticker, currency_note

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.dropna(subset=["Close"]).copy()
    if len(df) < 30:
        return None, used_ticker, currency_note

    is_usd = any(p in used_ticker.upper() for p in ["SI=F", "GC=F", "^GSPC", "=X", "USD"])
    if is_usd:
        currency_note = "USD (Convertido a EUR)"
        eur_usd = fetch_eur_usd_rate()
        if eur_usd > 0:
            for col in ["Open", "High", "Low", "Close"]:
                if col in df.columns:
                    df[col] = df[col] / eur_usd
    else:
        currency_note = "EUR"

    return df, used_ticker, currency_note


# ==============================================================================
# 5. MOTOR CUANTITATIVO: TENDENCIAS, TECHOS, SUELOS Y EVENTOS DE PRECIO
# ==============================================================================

def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calcula el RSI clásico de Wilder usando suavizado exponencial (EMA)."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50.0)


def run_quantitative_diagnosis(df: pd.DataFrame) -> Dict[str, Any]:
    """Ejecuta el análisis técnico algorítmico estricto sobre el DataFrame diario."""
    data = df.copy()

    data["SMA_50"] = data["Close"].rolling(window=50, min_periods=20).mean()
    data["SMA_200"] = data["Close"].rolling(window=200, min_periods=50).mean()
    data["Vol_SMA_20"] = data["Volume"].rolling(window=20, min_periods=5).mean()
    data["RSI_14"] = calculate_rsi(data["Close"], period=14)

    curr = data.iloc[-1]
    prev = data.iloc[-2] if len(data) >= 2 else curr

    current_price = float(curr["Close"])
    open_price = float(curr["Open"])
    high_price = float(curr["High"])
    low_price = float(curr["Low"])
    volume = float(curr["Volume"]) if "Volume" in curr else 0.0

    sma_50 = float(curr["SMA_50"]) if pd.notna(curr["SMA_50"]) else current_price
    sma_200 = float(curr["SMA_200"]) if pd.notna(curr["SMA_200"]) else sma_50
    vol_sma_20 = float(curr["Vol_SMA_20"]) if pd.notna(curr["Vol_SMA_20"]) else 0.0
    rsi = float(curr["RSI_14"]) if pd.notna(curr["RSI_14"]) else 50.0

    # Niveles Clave 30s y Anual (250s)
    soporte_local = float(data["Low"].iloc[-30:].min())
    techo_local = float(data["High"].iloc[-30:].max())
    prev_30_high = float(data["High"].iloc[-31:-1].max()) if len(data) >= 32 else techo_local
    max_anual = float(data["High"].iloc[-250:].max()) if len(data) >= 250 else float(data["High"].max())

    dist_soporte = ((current_price - soporte_local) / current_price) * 100.0
    dist_techo = ((techo_local - current_price) / current_price) * 100.0
    dist_anual = ((max_anual - current_price) / current_price) * 100.0

    # Rango 20 sesiones y pendiente de SMA 50
    rango_20_max = float(data["High"].iloc[-20:].max())
    rango_20_min = float(data["Low"].iloc[-20:].min())
    rango_20_pct = (rango_20_max - rango_20_min) / rango_20_min if rango_20_min > 0 else 0.0

    sma_50_prev = float(data["SMA_50"].iloc[-15]) if len(data) >= 65 and pd.notna(data["SMA_50"].iloc[-15]) else sma_50
    sma_50_flat = (abs(sma_50 - sma_50_prev) / sma_50_prev) < 0.012

    recent_5_high = float(data["High"].iloc[-5:].max())
    prior_15_high = float(data["High"].iloc[-20:-5].max()) if len(data) >= 20 else recent_5_high
    maximos_crecientes = recent_5_high >= prior_15_high
    maximos_decrecientes = recent_5_high < prior_15_high

    # Evaluación de Tendencia
    if rango_20_pct < 0.04 and sma_50_flat:
        tendencia = "↔️ Movimiento Lateral"
        tendencia_code = "LATERAL"
        badge_trend_style = "background: rgba(100, 116, 139, 0.18); color: #94a3b8; border: 1px solid rgba(100, 116, 139, 0.4);"
    elif sma_50 > sma_200 and current_price > sma_50 and maximos_crecientes:
        tendencia = "📈 Tendencia Alcista"
        tendencia_code = "ALCISTA"
        badge_trend_style = "background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4);"
    elif sma_50 < sma_200 and current_price < sma_50 and maximos_decrecientes:
        tendencia = "📉 Tendencia Bajista"
        tendencia_code = "BAJISTA"
        badge_trend_style = "background: rgba(244, 63, 94, 0.18); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4);"
    else:
        if sma_50 >= sma_200:
            tendencia = "📈 Alcista (En Consolidación)"
            tendencia_code = "ALCISTA"
            badge_trend_style = "background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4);"
        else:
            tendencia = "📉 Bajista (En Transición)"
            tendencia_code = "BAJISTA"
            badge_trend_style = "background: rgba(244, 63, 94, 0.18); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4);"

    # Detección de Eventos Clave
    candle_range = high_price - low_price
    upper_wick = high_price - max(current_price, open_price)
    has_prominent_upper_wick = (upper_wick >= 0.38 * candle_range) if candle_range > 0 else False
    is_red_candle = current_price < open_price
    is_green_candle = current_price > open_price

    has_volume_data = volume > 0 and vol_sma_20 > 0
    vol_ratio = (volume / vol_sma_20) if has_volume_data else 1.0
    vol_breakout_confirmed = (vol_ratio >= 1.28) if has_volume_data else True
    vol_growing = (volume > float(prev["Volume"])) if has_volume_data else True

    # 1. Ruptura de Techo (Nuevo Máximo)
    is_breakout = (current_price >= prev_30_high * 0.999) and vol_breakout_confirmed

    # 2. Choque / Rechazo en Techo
    touches_resistance = high_price >= (techo_local * 0.99)
    is_resistance_rejection = touches_resistance and (is_red_candle or has_prominent_upper_wick) and not is_breakout

    # 3. Rebote en Soporte (Suelo Defendido)
    touches_support = low_price <= (soporte_local * 1.01)
    rsi_oversold = (rsi < 42.0) or (float(prev["RSI_14"]) < 38.0)
    bullish_candle = is_green_candle and (current_price > float(prev["High"]) or current_price > float(prev["Close"]))
    is_support_bounce = touches_support and rsi_oversold and bullish_candle and vol_growing

    # Estado Técnico Final y Estilo
    if is_breakout:
        estado_tecnico = "🚀 Ruptura de Techo (Nuevo Máximo)"
        estado_code = "RUPTURA_TECHO"
        estado_style = "background: rgba(168, 85, 247, 0.22); color: #c084fc; border: 1.5px solid #a855f7;"
        alerta_activa = True
    elif is_resistance_rejection:
        estado_tecnico = "🔴 Choque / Rechazo en Techo"
        estado_code = "CHOQUE_TECHO"
        estado_style = "background: rgba(244, 63, 94, 0.22); color: #fb7185; border: 1.5px solid #f43f5e;"
        alerta_activa = True
    elif is_support_bounce:
        estado_tecnico = "🟢 Rebote en Soporte (Suelo Defendido)"
        estado_code = "REBOTE_SUELO"
        estado_style = "background: rgba(16, 185, 129, 0.22); color: #34d399; border: 1.5px solid #10b981;"
        alerta_activa = True
    else:
        estado_tecnico = "📦 Movimiento Lateral / Rango"
        estado_code = "RANGO"
        estado_style = "background: rgba(71, 85, 105, 0.22); color: #cbd5e1; border: 1px solid #64748b;"
        alerta_activa = False

    last_dt_val = data.index[-1]
    last_date_str = last_dt_val.strftime("%d/%m/%Y") if hasattr(last_dt_val, "strftime") else str(last_dt_val)[:10]

    return {
        "df": data,
        "current_price": current_price,
        "open_price": open_price,
        "high_price": high_price,
        "low_price": low_price,
        "volume": volume,
        "sma_50": sma_50,
        "sma_200": sma_200,
        "vol_ratio": vol_ratio,
        "rsi": rsi,
        "soporte_local": soporte_local,
        "techo_local": techo_local,
        "max_anual": max_anual,
        "dist_soporte": dist_soporte,
        "dist_techo": dist_techo,
        "dist_anual": dist_anual,
        "rango_20_pct": rango_20_pct * 100.0,
        "tendencia": tendencia,
        "tendencia_code": tendencia_code,
        "badge_trend_style": badge_trend_style,
        "estado_tecnico": estado_tecnico,
        "estado_code": estado_code,
        "estado_style": estado_style,
        "alerta_activa": alerta_activa,
        "last_date": last_date_str,
    }


# ==============================================================================
# 6. GRÁFICO INTERACTIVO TOUCH OPTIMIZADO CON PLOTLY
# ==============================================================================

def create_interactive_chart(
    df: pd.DataFrame,
    asset_name: str,
    soporte: float,
    techo: float,
    max_anual: float,
) -> go.Figure:
    """Genera un gráfico financiero móvil con velas, SMAs, niveles de suelo/techo y volumen."""
    view_df = df.iloc[-180:].copy()

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.76, 0.24],
    )

    # 1. Velas Japonesas
    fig.add_trace(
        go.Candlestick(
            x=view_df.index,
            open=view_df["Open"],
            high=view_df["High"],
            low=view_df["Low"],
            close=view_df["Close"],
            name="Precio (€)",
            increasing_line_color="#10b981",
            decreasing_line_color="#f43f5e",
        ),
        row=1,
        col=1,
    )

    # 2. SMA 50
    if "SMA_50" in view_df.columns:
        fig.add_trace(
            go.Scatter(
                x=view_df.index,
                y=view_df["SMA_50"],
                mode="lines",
                name="SMA 50",
                line=dict(color="#f59e0b", width=1.8),
            ),
            row=1,
            col=1,
        )

    # 3. SMA 200
    if "SMA_200" in view_df.columns:
        fig.add_trace(
            go.Scatter(
                x=view_df.index,
                y=view_df["SMA_200"],
                mode="lines",
                name="SMA 200",
                line=dict(color="#38bdf8", width=2.0),
            ),
            row=1,
            col=1,
        )

    # 4. Líneas Horizontales de Suelo y Techo
    fig.add_hline(
        y=techo,
        line_dash="dash",
        line_color="#f43f5e",
        line_width=1.6,
        annotation_text=f"Techo: {techo:.2f}€",
        annotation_position="top left",
        annotation_font=dict(color="#fb7185", size=10),
        row=1,
        col=1,
    )

    fig.add_hline(
        y=soporte,
        line_dash="dash",
        line_color="#10b981",
        line_width=1.6,
        annotation_text=f"Suelo: {soporte:.2f}€",
        annotation_position="bottom left",
        annotation_font=dict(color="#34d399", size=10),
        row=1,
        col=1,
    )

    if max_anual > techo:
        fig.add_hline(
            y=max_anual,
            line_dash="dot",
            line_color="#eab308",
            line_width=1.4,
            annotation_text=f"Máx Anual: {max_anual:.2f}€",
            annotation_position="top right",
            annotation_font=dict(color="#facc15", size=10),
            row=1,
            col=1,
        )

    # 5. Volumen
    bar_colors = [
        "#10b981" if c >= o else "#f43f5e"
        for c, o in zip(view_df["Close"], view_df["Open"])
    ]
    fig.add_trace(
        go.Bar(
            x=view_df.index,
            y=view_df["Volume"].fillna(0),
            marker_color=bar_colors,
            name="Volumen",
            opacity=0.55,
        ),
        row=2,
        col=1,
    )

    if "Vol_SMA_20" in view_df.columns:
        fig.add_trace(
            go.Scatter(
                x=view_df.index,
                y=view_df["Vol_SMA_20"],
                mode="lines",
                name="Vol SMA 20",
                line=dict(color="#94a3b8", width=1.2),
            ),
            row=2,
            col=1,
        )

    # Layout responsivo dark fintech
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#090e1c",
        margin=dict(l=8, r=8, t=26, b=8),
        height=430,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10, color="#94a3b8"),
        ),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.05)",
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1M", step="month", stepmode="backward"),
                dict(count=3, label="3M", step="month", stepmode="backward"),
                dict(count=6, label="6M", step="month", stepmode="backward"),
                dict(step="all", label="TODO"),
            ]),
            bgcolor="#131b2e",
            activecolor="#2563eb",
            font=dict(size=11, color="#f8fafc"),
        ),
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255, 255, 255, 0.05)",
        row=1,
        col=1,
    )
    fig.update_yaxes(
        showgrid=False,
        row=2,
        col=1,
    )

    return fig


# ==============================================================================
# 7. GENERADOR DE REPORTES Y ALERTAS PARA TELEGRAM
# ==============================================================================

def build_market_summary_message(
    diagnostics_map: Dict[str, Dict[str, Any]],
    portfolio_metrics: Dict[str, Any],
) -> str:
    """Genera un reporte conciso y elegante en Markdown para Telegram."""
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    lines = [
        "📊 *INFORME CUANTITATIVO — INVESTQUANT PRO*",
        f"⏰ *Actualizado:* {now_str}",
        "━━━━━━━━━━━━━━━━━━━━━━",
    ]

    for name, diag in diagnostics_map.items():
        if not diag:
            continue
        p = diag["current_price"]
        trend = diag["tendencia"]
        state = diag["estado_tecnico"]
        dist_s = diag["dist_soporte"]
        dist_t = diag["dist_techo"]

        lines.append(f"🔹 *{name}*: `{p:.2f} €`")
        lines.append(f"  • *Tendencia:* {trend}")
        lines.append(f"  • *Diagnóstico:* {state}")
        lines.append(f"  • *Suelo 30d:* `{diag['soporte_local']:.2f} €` (-{dist_s:.1f}%)")
        lines.append(f"  • *Techo 30d:* `{diag['techo_local']:.2f} €` (+{dist_t:.1f}%)")
        lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("💼 *RESUMEN DE CARTERA:*")
    lines.append(f"• *Total Invertido:* `{portfolio_metrics['total_invested']:.2f} €`")
    lines.append(f"• *Valor Actual:* `{portfolio_metrics['current_value']:.2f} €`")
    pnl_sign = "+" if portfolio_metrics["pnl_eur"] >= 0 else ""
    lines.append(
        f"• *Rendimiento:* `{pnl_sign}{portfolio_metrics['pnl_eur']:.2f} €` "
        f"({pnl_sign}{portfolio_metrics['pnl_pct']:.2f}%)"
    )

    return "\n".join(lines)


def build_event_alert_message(asset_name: str, diag: Dict[str, Any]) -> str:
    """Construye un mensaje de alerta prioritaria cuando ocurre un evento técnico clave."""
    p = diag["current_price"]
    code = diag["estado_code"]
    today = diag["last_date"]

    if code == "REBOTE_SUELO":
        return (
            "🟢 *ALERTA TÉCNICA: REBOTE CONFIRMADO EN SOPORTE*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ *Activo:* {asset_name}\n"
            f"💶 *Precio Actual:* `{p:.2f} €`\n"
            f"🛡️ *Suelo Defendido:* `{diag['soporte_local']:.2f} €` (mínimo 30 sesiones)\n"
            f"📊 *RSI 14:* `{diag['rsi']:.1f}` (Sobreventa defendida)\n"
            "📈 *Patrón:* Vela verde superando máximo previo con giro de impulso.\n"
            f"📅 *Sesión:* {today}"
        )
    elif code == "CHOQUE_TECHO":
        return (
            "🔴 *ALERTA TÉCNICA: CHOQUE / FRENO EN RESISTENCIA*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ *Activo:* {asset_name}\n"
            f"💶 *Precio Actual:* `{p:.2f} €`\n"
            f"🧱 *Techo Local:* `{diag['techo_local']:.2f} €` (resistencia 30 sesiones)\n"
            f"⚠️ *Distancia al Techo:* `+{diag['dist_techo']:.2f}%`\n"
            "📉 *Patrón:* Rechazo intradía con vela bajista o mecha superior pronunciada.\n"
            f"📅 *Sesión:* {today}"
        )
    elif code == "RUPTURA_TECHO":
        return (
            "🚀 *ALERTA TÉCNICA: RUPTURA DE TECHO (NUEVO MÁXIMO)*\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ *Activo:* {asset_name}\n"
            f"💶 *Precio de Ruptura:* `{p:.2f} €`\n"
            f"💥 *Resistencia Superada:* `{diag['techo_local']:.2f} €`\n"
            f"📊 *Volumen Confirmado:* `{diag['vol_ratio']:.1f}x` sobre media de 20 sesiones.\n"
            "🏆 *Nuevo máximo relativo con confirmación algorítmica.*\n"
            f"📅 *Sesión:* {today}"
        )
    return ""


# ==============================================================================
# 8. CÁLCULO DE MÉTRICAS DE CARTERA (WALLET)
# ==============================================================================

def compute_portfolio_analytics(
    portfolio_data: List[Dict[str, Any]],
    price_cache: Dict[str, float],
) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Calcula las métricas consolidadas, costes, valor actual y rentabilidad por posición."""
    if not portfolio_data:
        empty_metrics = {
            "total_invested": 0.0,
            "current_value": 0.0,
            "pnl_eur": 0.0,
            "pnl_pct": 0.0,
            "total_commissions": 0.0,
        }
        return empty_metrics, pd.DataFrame()

    rows = []
    total_invested_global = 0.0
    current_value_global = 0.0
    commissions_global = 0.0

    for tx in portfolio_data:
        ticker = tx.get("ticker", "").strip()
        shares = float(tx.get("shares", 0.0))
        buy_price = float(tx.get("price_eur", 0.0))
        comm = float(tx.get("commission_eur", 0.0))

        cost = (shares * buy_price) + comm
        mkt_price = price_cache.get(ticker, buy_price)
        cur_val = shares * mkt_price
        pnl = cur_val - cost
        pnl_pct = (pnl / cost) * 100.0 if cost > 0 else 0.0

        total_invested_global += cost
        current_value_global += cur_val
        commissions_global += comm

        rows.append({
            "ID": tx.get("id"),
            "Activo": tx.get("asset_name", ticker),
            "Ticker": ticker,
            "Fecha": tx.get("date", ""),
            "Títulos": shares,
            "Precio Compra (€)": buy_price,
            "Precio Actual (€)": mkt_price,
            "Coste Total (€)": cost,
            "Valor Actual (€)": cur_val,
            "P&L (€)": pnl,
            "P&L (%)": pnl_pct,
            "Comisión (€)": comm,
            "Notas": tx.get("notes", ""),
        })

    df_pos = pd.DataFrame(rows)
    pnl_global = current_value_global - total_invested_global
    pnl_global_pct = (pnl_global / total_invested_global) * 100.0 if total_invested_global > 0 else 0.0

    if current_value_global > 0 and not df_pos.empty:
        df_pos["Peso (%)"] = (df_pos["Valor Actual (€)"] / current_value_global) * 100.0
    else:
        df_pos["Peso (%)"] = 0.0

    metrics = {
        "total_invested": total_invested_global,
        "current_value": current_value_global,
        "pnl_eur": pnl_global,
        "pnl_pct": pnl_global_pct,
        "total_commissions": commissions_global,
    }

    return metrics, df_pos


# ==============================================================================
# 9. INTERFAZ DE USUARIO — STREAMLIT PRINCIPAL
# ==============================================================================

def main():
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = load_portfolio()

    # Barra lateral: Configuración y Credenciales Telegram
    with st.sidebar:
        st.markdown("### ⚙️ Centro de Control")
        st.caption("Configura las alertas de Telegram y el entorno de ejecución.")

        env_token, env_chat = get_telegram_config()
        tg_configured = bool(env_token and env_chat)

        if tg_configured:
            st.success("🟢 Telegram Conectado")
        else:
            st.warning("🟠 Telegram sin configurar")

        with st.expander("🔑 Credenciales de Telegram", expanded=not tg_configured):
            manual_token = st.text_input(
                "Bot Token",
                value=env_token if "user_tg_token" not in st.session_state else st.session_state.user_tg_token,
                type="password",
                help="Obtenido en Telegram con @BotFather.",
                key="input_tg_token",
            )
            manual_chat = st.text_input(
                "Chat ID",
                value=env_chat if "user_tg_chat" not in st.session_state else st.session_state.user_tg_chat,
                help="Obtenido en Telegram con @userinfobot.",
                key="input_tg_chat",
            )

            col_btn1, col_btn2 = st.columns(2)
            if col_btn1.button("💾 Guardar", use_container_width=True):
                st.session_state.user_tg_token = manual_token
                st.session_state.user_tg_chat = manual_chat
                st.rerun()

            if col_btn2.button("🧪 Probar", use_container_width=True):
                st.session_state.user_tg_token = manual_token
                st.session_state.user_tg_chat = manual_chat
                ok, msg = send_telegram_alert(
                    "🔔 *Test InvestQuant*: Conexión con Telegram verificada correctamente."
                )
                if ok:
                    st.toast("✅ Test exitoso enviado a Telegram", icon="🚀")
                else:
                    st.error(msg)

        st.markdown("---")
        eur_usd = fetch_eur_usd_rate()
        st.caption(f"💶 Referencia EUR/USD: **{eur_usd:.4f}**")
        if st.button("🔄 Refrescar Datos", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

    # -------------------------------------------------------------
    # Descarga de Datos de Mercado
    # -------------------------------------------------------------
    diagnostics = {}
    current_prices_cache = {}
    active_alerts = []

    for asset_name, meta in DEFAULT_ASSETS.items():
        ticker = meta["ticker"]
        fallback = meta.get("fallback")
        df, used_tk, _ = fetch_market_data(ticker, fallback)
        if df is not None and not df.empty:
            diag = run_quantitative_diagnosis(df)
            diagnostics[asset_name] = diag
            current_prices_cache[ticker] = diag["current_price"]
            if fallback:
                current_prices_cache[fallback] = diag["current_price"]
            if diag["alerta_activa"]:
                active_alerts.append((asset_name, diag))
        else:
            diagnostics[asset_name] = None

    for tx in st.session_state.portfolio:
        tk = tx.get("ticker", "").strip()
        if tk and tk not in current_prices_cache:
            df_custom, _, _ = fetch_market_data(tk)
            if df_custom is not None and not df_custom.empty:
                current_prices_cache[tk] = float(df_custom["Close"].iloc[-1])

    portfolio_metrics, df_positions = compute_portfolio_analytics(
        st.session_state.portfolio, current_prices_cache
    )

    # -------------------------------------------------------------
    # Cabecera Principal Ultra-Moderna
    # -------------------------------------------------------------
    header_html = f"""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 1rem; padding: 12px 18px; background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; backdrop-filter: blur(10px);">
        <div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.55rem; font-weight: 800; color: #f8fafc; letter-spacing: -0.02em;">
                    ⚡ InvestQuant <span style="background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PRO</span>
                </span>
                <span style="background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 12px;">EN VIVO</span>
            </div>
            <div style="color: #94a3b8; font-size: 0.82rem; margin-top: 2px;">
                Cartera & Análisis Técnico Cuantitativo Algorítmico • FX EUR/USD: {eur_usd:.4f}
            </div>
        </div>
    </div>
    """
    render_html(header_html)

    # Fila de acciones rápidas superiores
    col_act1, col_act2 = st.columns([0.7, 0.3])
    with col_act2:
        if st.button("📢 Reporte a Telegram", use_container_width=True, type="primary"):
            summary_msg = build_market_summary_message(diagnostics, portfolio_metrics)
            ok, msg = send_telegram_alert(summary_msg)
            if ok:
                st.toast("✅ Reporte completo enviado a Telegram", icon="📨")
            else:
                st.error(msg)

    # Banner de Alertas Activas en Tiempo Real
    if active_alerts:
        for a_name, a_diag in active_alerts:
            code = a_diag["estado_code"]
            color = "#f43f5e" if code == "CHOQUE_TECHO" else ("#10b981" if code == "REBOTE_SUELO" else "#a855f7")
            alert_banner_html = f"""
            <div style="background: rgba(15, 23, 42, 0.9); border-left: 5px solid {color}; padding: 12px 16px; border-radius: 10px; margin-bottom: 14px; border-top: 1px solid rgba(255,255,255,0.06); border-right: 1px solid rgba(255,255,255,0.06); border-bottom: 1px solid rgba(255,255,255,0.06);">
                <span style="font-weight: 800; color: {color}; font-size: 0.85rem; letter-spacing: 0.04em;">SEÑAL ALGORÍTMICA [{a_name.upper()}]:</span> 
                <strong style="color: #f8fafc; margin-left: 6px;">{a_diag['estado_tecnico']}</strong> 
                <span style="color: #94a3b8; font-size: 0.85rem; margin-left: 8px;">(Precio: {a_diag['current_price']:.2f} €)</span>
            </div>
            """
            render_html(alert_banner_html)

    # -------------------------------------------------------------
    # Pestañas Principales de la Aplicación
    # -------------------------------------------------------------
    tab_quant, tab_portfolio, tab_alerts = st.tabs([
        "📊 Motor Cuantitativo",
        "💼 Cartera (Wallet)",
        "🔔 Alertas & Telegram",
    ])

    # =============================================================
    # TAB 1: MOTOR CUANTITATIVO (ANÁLISIS TÉCNICO Y GRÁFICOS)
    # =============================================================
    with tab_quant:
        asset_options = list(DEFAULT_ASSETS.keys())
        selected_asset = st.radio(
            "Selecciona Activo:",
            options=asset_options,
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )

        diag = diagnostics.get(selected_asset)

        if diag is None:
            st.warning(f"No se pudieron descargar datos para {selected_asset}. Intenta refrescar más tarde.")
        else:
            p = diag["current_price"]
            diff_open = p - diag["open_price"]
            diff_pct = (diff_open / diag["open_price"]) * 100.0 if diag["open_price"] > 0 else 0.0
            pnl_color = "#34d399" if diff_open >= 0 else "#fb7185"
            pnl_bg = "rgba(16, 185, 129, 0.15)" if diff_open >= 0 else "rgba(244, 63, 94, 0.15)"
            sign_str = "+" if diff_open >= 0 else ""

            # Tarjeta Táctil Ultra-Moderna
            card_html = f"""
            <div style="background: linear-gradient(180deg, #0e1526 0%, #0a0f1d 100%); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 18px; padding: 20px; margin-bottom: 16px; box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.6);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div style="font-size: 0.8rem; color: #60a5fa; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase;">
                            {DEFAULT_ASSETS[selected_asset]['ticker']} • Velas Diarias (1D)
                        </div>
                        <div style="display: flex; align-items: baseline; gap: 10px; margin-top: 4px;">
                            <span style="font-size: 2.2rem; font-weight: 800; color: #f8fafc; font-family: 'JetBrains Mono', monospace;">
                                {p:.2f} €
                            </span>
                            <span style="background: {pnl_bg}; color: {pnl_color}; font-size: 0.95rem; font-weight: 700; padding: 3px 10px; border-radius: 8px;">
                                {sign_str}{diff_open:.2f} € ({sign_str}{diff_pct:.2f}%)
                            </span>
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap; align-items: center;">
                        <span style="{diag['badge_trend_style']} display: inline-flex; align-items: center; padding: 6px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 700;">
                            {diag['tendencia']}
                        </span>
                        <span style="{diag['estado_style']} display: inline-flex; align-items: center; padding: 6px 14px; border-radius: 20px; font-size: 0.82rem; font-weight: 800;">
                            {diag['estado_tecnico']}
                        </span>
                    </div>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 18px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.08);">
                    <div style="flex: 1 1 130px; background: rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 12px; padding: 12px 14px;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #34d399; letter-spacing: 0.05em; text-transform: uppercase;">🛡️ Suelo 30D</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin: 3px 0; font-family: 'JetBrains Mono', monospace;">{diag['soporte_local']:.2f} €</div>
                        <div style="font-size: 0.74rem; color: #10b981; font-weight: 600;">Distancia: -{diag['dist_soporte']:.1f}%</div>
                    </div>
                    <div style="flex: 1 1 130px; background: rgba(244, 63, 94, 0.06); border: 1px solid rgba(244, 63, 94, 0.25); border-radius: 12px; padding: 12px 14px;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #fb7185; letter-spacing: 0.05em; text-transform: uppercase;">🧱 Techo 30D</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin: 3px 0; font-family: 'JetBrains Mono', monospace;">{diag['techo_local']:.2f} €</div>
                        <div style="font-size: 0.74rem; color: #f43f5e; font-weight: 600;">Distancia: +{diag['dist_techo']:.1f}%</div>
                    </div>
                    <div style="flex: 1 1 130px; background: rgba(234, 179, 8, 0.06); border: 1px solid rgba(234, 179, 8, 0.25); border-radius: 12px; padding: 12px 14px;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #facc15; letter-spacing: 0.05em; text-transform: uppercase;">🏆 Máx Anual (250D)</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin: 3px 0; font-family: 'JetBrains Mono', monospace;">{diag['max_anual']:.2f} €</div>
                        <div style="font-size: 0.74rem; color: #eab308; font-weight: 600;">Distancia: +{diag['dist_anual']:.1f}%</div>
                    </div>
                    <div style="flex: 1 1 130px; background: rgba(56, 189, 248, 0.06); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 12px; padding: 12px 14px;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #38bdf8; letter-spacing: 0.05em; text-transform: uppercase;">📊 RSI 14 / Rango 20D</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #f8fafc; margin: 3px 0; font-family: 'JetBrains Mono', monospace;">{diag['rsi']:.1f}</div>
                        <div style="font-size: 0.74rem; color: #94a3b8; font-weight: 600;">Oscilación: {diag['rango_20_pct']:.1f}%</div>
                    </div>
                </div>
            </div>
            """
            render_html(card_html)

            # Gráfico Interactivo Plotly
            fig = create_interactive_chart(
                diag["df"],
                selected_asset,
                diag["soporte_local"],
                diag["techo_local"],
                diag["max_anual"],
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # Diagnóstico Cuantitativo Detallado (Acordeón)
            with st.expander("🔬 Parámetros Algorítmicos y Criterios Cuantitativos", expanded=False):
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.markdown("**Reglas de Tendencia:**")
                    st.write(f"• **SMA 50:** `{diag['sma_50']:.2f} €`")
                    st.write(f"• **SMA 200:** `{diag['sma_200']:.2f} €`")
                    st.write(f"• **Relación SMA 50 vs 200:** {'Cruz Dorada (SMA 50 > 200)' if diag['sma_50'] > diag['sma_200'] else 'Cruz de Muerte (SMA 50 < 200)'}")
                    st.write(f"• **Ancho de oscilación 20 días:** `{diag['rango_20_pct']:.2f}%` (< 4% activa rango lateral)")
                with col_c2:
                    st.markdown("**Reglas de Ruptura y Rebote:**")
                    st.write(f"• **Volumen última sesión:** `{diag['volume']:,.0f}`")
                    st.write(f"• **Ratio de volumen vs Media 20:** `{diag['vol_ratio']:.2f}x` (Confirmación si > 1.3x)")
                    st.write(f"• **RSI (14 períodos):** `{diag['rsi']:.1f}` (Suelo defendido si RSI < 38)")
                    st.write(f"• **Última sesión procesada:** `{diag['last_date']}`")

        # Buscador / Analizador de Activo Personalizado
        st.markdown("---")
        with st.expander("🔍 Analizar Cualquier Otro Ticker de Yahoo Finance", expanded=False):
            custom_col1, custom_col2 = st.columns([0.7, 0.3])
            with custom_col1:
                custom_tk = st.text_input("Ticker (ej. AAPL, NVDA, BTC-USD, IWDA.AS):", placeholder="BTC-USD").upper().strip()
            with custom_col2:
                btn_analyze = st.button("Analizar Ticker", use_container_width=True)

            if btn_analyze and custom_tk:
                with st.spinner(f"Descargando y analizando {custom_tk}..."):
                    df_custom, used_tk, curr_note = fetch_market_data(custom_tk)
                    if df_custom is not None and not df_custom.empty:
                        diag_c = run_quantitative_diagnosis(df_custom)
                        st.success(f"Análisis de {custom_tk} completado.")
                        fig_c = create_interactive_chart(
                            diag_c["df"],
                            custom_tk,
                            diag_c["soporte_local"],
                            diag_c["techo_local"],
                            diag_c["max_anual"],
                        )
                        st.plotly_chart(fig_c, use_container_width=True)
                    else:
                        st.error(f"No se encontraron datos para el ticker '{custom_tk}'.")

    # =============================================================
    # TAB 2: GESTIÓN DE CARTERA (WALLET)
    # =============================================================
    with tab_portfolio:
        # 4 Tarjetas de Métricas Fintech Ultra-Modernas
        pnl_val = portfolio_metrics["pnl_eur"]
        pnl_pct_val = portfolio_metrics["pnl_pct"]
        pnl_color = "#34d399" if pnl_val >= 0 else "#fb7185"
        pnl_prefix = "+" if pnl_val >= 0 else ""

        portfolio_kpis_html = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 1.2rem;">
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 14px 16px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">💰 Total Invertido</div>
                <div style="font-size: 1.55rem; font-weight: 800; color: #f8fafc; margin: 4px 0; font-family: 'JetBrains Mono', monospace;">{portfolio_metrics['total_invested']:.2f} €</div>
                <div style="font-size: 0.75rem; color: #64748b;">Coste base acumulado</div>
            </div>
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 14px 16px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">📊 Valor Actual</div>
                <div style="font-size: 1.55rem; font-weight: 800; color: #f8fafc; margin: 4px 0; font-family: 'JetBrains Mono', monospace;">{portfolio_metrics['current_value']:.2f} €</div>
                <div style="font-size: 0.75rem; color: #38bdf8;">A cotización en vivo</div>
            </div>
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 14px 16px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">🚀 Rendimiento P&L</div>
                <div style="font-size: 1.55rem; font-weight: 800; color: {pnl_color}; margin: 4px 0; font-family: 'JetBrains Mono', monospace;">{pnl_prefix}{pnl_val:.2f} €</div>
                <div style="font-size: 0.75rem; color: {pnl_color}; font-weight: 700;">{pnl_prefix}{pnl_pct_val:.2f}% global</div>
            </div>
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 14px 16px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">🏷️ Comisiones Totales</div>
                <div style="font-size: 1.55rem; font-weight: 800; color: #cbd5e1; margin: 4px 0; font-family: 'JetBrains Mono', monospace;">{portfolio_metrics['total_commissions']:.2f} €</div>
                <div style="font-size: 0.75rem; color: #64748b;">Tarifas de broker</div>
            </div>
        </div>
        """
        render_html(portfolio_kpis_html)

        # Gráfico Donut de Desglose de Cartera
        if not df_positions.empty and portfolio_metrics["current_value"] > 0:
            alloc_df = df_positions.groupby("Activo")["Valor Actual (€)"].sum().reset_index()
            fig_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=alloc_df["Activo"],
                        values=alloc_df["Valor Actual (€)"],
                        hole=0.64,
                        textinfo="label+percent",
                        hoverinfo="label+value+percent",
                        marker=dict(colors=["#38bdf8", "#818cf8", "#10b981", "#f59e0b", "#ec4899"]),
                    )
                ]
            )
            fig_donut.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=260,
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # Tabla de Posiciones
        st.markdown("#### 📋 Posiciones Abiertas")
        if not df_positions.empty:
            display_df = df_positions[[
                "Activo", "Ticker", "Títulos", "Precio Compra (€)",
                "Precio Actual (€)", "Coste Total (€)", "Valor Actual (€)",
                "P&L (€)", "P&L (%)", "Peso (%)"
            ]].copy()

            st.dataframe(
                display_df.style.format({
                    "Títulos": "{:.4f}",
                    "Precio Compra (€)": "{:.2f} €",
                    "Precio Actual (€)": "{:.2f} €",
                    "Coste Total (€)": "{:.2f} €",
                    "Valor Actual (€)": "{:.2f} €",
                    "P&L (€)": "{:+.2f} €",
                    "P&L (%)": "{:+.2f}%",
                    "Peso (%)": "{:.1f}%",
                }),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Tu cartera está vacía. Añade tu primera compra en el formulario inferior.")

        # Formulario para Registrar Nueva Operación
        with st.expander("➕ Registrar Nueva Compra / Operación", expanded=False):
            with st.form("form_add_transaction", clear_on_submit=True):
                col_f1, col_f2 = st.columns(2)

                asset_choices = list(DEFAULT_ASSETS.keys()) + ["Otro (Personalizado)"]
                selected_form_asset = col_f1.selectbox("Activo a registrar:", asset_choices)

                tx_ticker = ""
                tx_name = selected_form_asset
                if selected_form_asset == "Otro (Personalizado)":
                    tx_name = col_f1.text_input("Nombre del Activo (ej. Bitcoin, Apple):")
                    tx_ticker = col_f2.text_input("Ticker de Yahoo Finance (ej. BTC-USD, AAPL):").upper().strip()
                else:
                    tx_ticker = DEFAULT_ASSETS[selected_form_asset]["ticker"]

                col_f3, col_f4, col_f5 = st.columns(3)
                tx_date = col_f3.date_input("Fecha de compra:", value=date.today())
                tx_price = col_f4.number_input("Precio de compra (€):", min_value=0.0001, value=100.0, step=1.0)
                tx_shares = col_f5.number_input("Cantidad / Títulos:", min_value=0.0001, value=1.0, step=0.1)

                col_f6, col_f7 = st.columns(2)
                tx_commission = col_f6.number_input("Comisiones (€):", min_value=0.0, value=1.0, step=0.5)
                tx_notes = col_f7.text_input("Notas / Estrategia (opcional):", placeholder="Aportación mensual")

                submit_tx = st.form_submit_button("💾 Guardar Transacción", use_container_width=True, type="primary")

                if submit_tx:
                    if not tx_name or not tx_ticker:
                        st.error("Por favor completa el nombre y el ticker del activo.")
                    else:
                        new_tx = {
                            "id": f"tx-{uuid.uuid4().hex[:8]}",
                            "asset_name": tx_name,
                            "ticker": tx_ticker,
                            "date": str(tx_date),
                            "price_eur": float(tx_price),
                            "shares": float(tx_shares),
                            "commission_eur": float(tx_commission),
                            "notes": tx_notes,
                        }
                        st.session_state.portfolio.append(new_tx)
                        save_portfolio(st.session_state.portfolio)
                        st.success(f"✅ Compra de {tx_name} guardada correctamente.")
                        st.rerun()

        # Gestión y Eliminación de Transacciones
        with st.expander("🗑️ Administrar / Eliminar Transacciones", expanded=False):
            if st.session_state.portfolio:
                tx_options = {
                    f"{t.get('date')} — {t.get('asset_name')} ({t.get('shares')} uds @ {t.get('price_eur')}€) [ID: {t.get('id')}]": t.get("id")
                    for t in st.session_state.portfolio
                }
                selected_del = st.selectbox("Selecciona la transacción a eliminar:", list(tx_options.keys()))
                if st.button("Eliminar Transacción Seleccionada", type="secondary"):
                    target_id = tx_options[selected_del]
                    st.session_state.portfolio = [t for t in st.session_state.portfolio if t.get("id") != target_id]
                    save_portfolio(st.session_state.portfolio)
                    st.toast("Transacción eliminada.", icon="🗑️")
                    st.rerun()
            else:
                st.caption("No hay transacciones registradas.")

    # =============================================================
    # TAB 3: ALERTAS CUANTITATIVAS & TELEGRAM BOT
    # =============================================================
    with tab_alerts:
        st.markdown("### 🔔 Centro de Alertas Cuantitativas a Telegram")
        st.caption("Monitorización continua de los 3 eventos críticos de precio en velas diarias.")

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.markdown(
                """
                **Condiciones Algorítmicas de Disparo:**
                - 🟢 **Rebote en Soporte:** Suelo 30d alcanzado, RSI < 38 y vela alcista con volumen creciente.
                - 🔴 **Choque en Techo:** Precio a menos del 1% del techo 30d y cierre en vela bajista o mecha superior.
                - 🚀 **Ruptura de Techo:** Cierre sobre la resistencia de 30 sesiones con volumen > 1.3x SMA 20.
                """
            )

        with col_a2:
            st.markdown(
                f"""
                **Estado de Conexión:**  
                • Bot Token: `{'Configurado' if env_token else 'No configurado'}`  
                • Chat ID: `{'Configurado' if env_chat else 'No configurado'}`  
                """
            )

        st.markdown("---")
        st.markdown("#### 📢 Enviar Alertas Individuales de Mercado")

        for name, d in diagnostics.items():
            if d:
                c_card1, c_card2 = st.columns([0.75, 0.25])
                with c_card1:
                    st.markdown(
                        f"**{name}** (`{d['current_price']:.2f} €`) — *{d['estado_tecnico']}* | {d['tendencia']}"
                    )
                with c_card2:
                    if st.button(f"Enviar Alerta {name}", key=f"btn_send_{name}", use_container_width=True):
                        if d["alerta_activa"]:
                            msg = build_event_alert_message(name, d)
                        else:
                            msg = (
                                f"📊 *ACTUALIZACIÓN {name.upper()}*\n"
                                f"💶 *Precio:* `{d['current_price']:.2f} €`\n"
                                f"📈 *Tendencia:* {d['tendencia']}\n"
                                f"📦 *Estado:* {d['estado_tecnico']}\n"
                                f"🛡️ *Suelo 30d:* `{d['soporte_local']:.2f} €` (-{d['dist_soporte']:.1f}%)\n"
                                f"🧱 *Techo 30d:* `{d['techo_local']:.2f} €` (+{d['dist_techo']:.1f}%)\n"
                                f"📊 *RSI:* `{d['rsi']:.1f}`"
                            )
                        ok, res = send_telegram_alert(msg)
                        if ok:
                            st.toast(f"✅ Alerta de {name} enviada", icon="🚀")
                        else:
                            st.error(res)

        st.markdown("---")
        st.markdown("#### 📋 Historial de Diagnóstico Reciente")
        diag_summary_rows = []
        for name, d in diagnostics.items():
            if d:
                diag_summary_rows.append({
                    "Activo": name,
                    "Precio (€)": f"{d['current_price']:.2f} €",
                    "Tendencia": d["tendencia"],
                    "Estado Cuantitativo": d["estado_tecnico"],
                    "Suelo 30d": f"{d['soporte_local']:.2f} €",
                    "Techo 30d": f"{d['techo_local']:.2f} €",
                    "RSI 14": f"{d['rsi']:.1f}",
                    "Alerta Activa": "🔔 SÍ" if d["alerta_activa"] else "No",
                })
        if diag_summary_rows:
            st.table(pd.DataFrame(diag_summary_rows))


if __name__ == "__main__":
    main()
