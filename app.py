import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import datetime

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(layout="wide", page_title="Mapa de Calor Nasdaq 100")
st.title("🌡️ Mapa de Calor Nasdaq 100 - Fuerza Relativa")

# ==========================================
# DATOS (Se cachean para no descargar siempre)
# ==========================================
@st.cache_data(ttl=300) # Cachea los datos por 5 minutos
def cargar_datos():
    tickers_nasdaq = [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'GOOG', 'META', 'AVGO', 'TSLA', 'COST', 
        'NFLX', 'AMD', 'PEP', 'ADBE', 'CSCO', 'TMUS', 'INTC', 'CMCSA', 'QCOM', 'TXN', 
        'AMGN', 'INTU', 'ISRG', 'AMAT', 'HON', 'BKNG', 'MU', 'LRCX', 'ADP', 'ADI', 
        'VRTX', 'REGN', 'PANW', 'KLAC', 'SBUX', 'MDLZ', 'SNPS', 'CDNS', 'MELI', 'CRWD', 
        'MAR', 'ABNB', 'CTAS', 'PYPL', 'ORLY', 'CSX', 'NXPI', 'ROP', 'FTNT', 'WDAY', 
        'MNST', 'AEP', 'PCAR', 'CPRT', 'ROST', 'ODFL', 'KDP', 'DXCM', 'KHC', 'IDXX', 
        'LULU', 'FAST', 'VRSK', 'CTSH', 'BIIB', 'EXC', 'XEL', 'CCEP', 'GEHC', 
        'ON', 'DASH', 'TTD', 'TEAM', 'MRNA', 'ZS', 'DLTR', 'BKR', 
        'GFS', 'ARM', 'SMCI', 'AZN', 'PDD', 'LIN', 'CSGP', 'CDW', 'MDB', 
        'APP', 'PLTR', 'DDOG', 'TTWO', 'LCID', 'RIVN', 'ENPH', 'SIRI', 'JD'
    ]
    
    mapa_sectores = {
        'AAPL': 'Technology', 'MSFT': 'Technology', 'NVDA': 'Technology', 'AVGO': 'Technology', 
        'AMD': 'Technology', 'INTC': 'Technology', 'QCOM': 'Technology', 'TXN': 'Technology', 
        'ADBE': 'Technology', 'CSCO': 'Technology', 'INTU': 'Technology', 'AMAT': 'Technology', 
        'MU': 'Technology', 'LRCX': 'Technology', 'ADI': 'Technology', 'KLAC': 'Technology', 
        'SNPS': 'Technology', 'CDNS': 'Technology', 'CRWD': 'Technology', 'NXPI': 'Technology', 
        'ROP': 'Technology', 'FTNT': 'Technology', 'WDAY': 'Technology', 'ON': 'Technology', 
        'TEAM': 'Technology', 'ZS': 'Technology', 'CDW': 'Technology', 
        'MDB': 'Technology', 'APP': 'Technology', 'PLTR': 'Technology', 'DDOG': 'Technology', 
        'SMCI': 'Technology', 'GFS': 'Technology', 'ARM': 'Technology', 'PANW': 'Technology',
        'AMZN': 'Consumer Discretionary', 'TSLA': 'Consumer Discretionary', 'BKNG': 'Consumer Discretionary', 
        'ABNB': 'Consumer Discretionary', 'MAR': 'Consumer Discretionary', 'ORLY': 'Consumer Discretionary', 
        'ROST': 'Consumer Discretionary', 'LULU': 'Consumer Discretionary', 'DLTR': 'Consumer Discretionary', 
        'LCID': 'Consumer Discretionary', 'RIVN': 'Consumer Discretionary', 'PDD': 'Consumer Discretionary',
        'GOOGL': 'Communication Services', 'GOOG': 'Communication Services', 'META': 'Communication Services', 
        'NFLX': 'Communication Services', 'TMUS': 'Communication Services', 'CMCSA': 'Communication Services', 
        'TTWO': 'Communication Services', 'SIRI': 'Communication Services', 'TTD': 'Communication Services',
        'COST': 'Consumer Staples', 'PEP': 'Consumer Staples', 'SBUX': 'Consumer Staples', 
        'MDLZ': 'Consumer Staples', 'MNST': 'Consumer Staples', 'KDP': 'Consumer Staples', 
        'KHC': 'Consumer Staples',
        'AMGN': 'Health Care', 'ISRG': 'Health Care', 'VRTX': 'Health Care', 'REGN': 'Health Care', 
        'BIIB': 'Health Care', 'DXCM': 'Health Care', 'IDXX': 'Health Care', 'GEHC': 'Health Care', 
        'MRNA': 'Health Care', 'AZN': 'Health Care',
        'HON': 'Industrials', 'ADP': 'Industrials', 'CSX': 'Industrials', 'CTAS': 'Industrials', 
        'PCAR': 'Industrials', 'CPRT': 'Industrials', 'ODFL': 'Industrials', 'FAST': 'Industrials', 
        'VRSK': 'Industrials', 'CTSH': 'Industrials', 'BKR': 'Industrials',
        'AEP': 'Utilities', 'EXC': 'Utilities', 'XEL': 'Utilities', 'CCEP': 'Utilities',
        'PYPL': 'Financials', 'MELI': 'Financials',
        'LIN': 'Materials', 'CSGP': 'Real Estate'
    }
    
    benchmark = '^NDX'
    datos = yf.download(tickers_nasdaq + [benchmark], period='1d', interval='5m', progress=False, threads=True)
    return datos, mapa_sectores, benchmark

datos, mapa_sectores, benchmark = cargar_datos()

# ==========================================
# INTERFAZ DE USUARIO (SLIDER)
# ==========================================
max_indice = len(datos) - 1
indice_tiempo = st.slider("⏰ Mueve la barra para viajar en el tiempo", 0, max_indice, max_indice)

# ==========================================
# CÁLCULO Y GRÁFICO
# ==========================================
datos_hasta_ahora = datos.iloc[:indice_tiempo+1]

apertura = datos_hasta_ahora['Open'].iloc[0]
actual = datos_hasta_ahora['Close'].iloc[-1]

cambio_pct = ((actual - apertura) / apertura) * 100
cambio_indice = cambio_pct[benchmark]

fuerza_relativa = cambio_pct - cambio_indice
fuerza_relativa = fuerza_relativa.drop(benchmark, errors='ignore')

df = pd.DataFrame({
    'Ticker': fuerza_relativa.index,
    'Cambio %': cambio_pct[fuerza_relativa.index].values,
    'Fuerza Relativa (RS)': fuerza_relativa.values
})

df['Sector'] = df['Ticker'].map(mapa_sectores).fillna('Otros')
df = df.dropna(subset=['Sector'])
df['Tamaño'] = df['Fuerza Relativa (RS)'].abs() + 0.5

hora = datos_hasta_ahora.index[-1].strftime('%H:%M')

fig = go.Figure(go.Treemap(
    labels=df['Ticker'],
    parents=df['Sector'],
    values=df['Tamaño'],
    customdata=df[['Cambio %', 'Fuerza Relativa (RS)', 'Sector']],
    hovertemplate='<b>%{label}</b><br>Sector: %{customdata[2]}<br>Cambio: %{customdata[0]:.2f}%<br>Fuerza Relativa: %{customdata[1]:.2f}<extra></extra>',
    marker=dict(
        colors=df['Fuerza Relativa (RS)'],
        colorscale=[[0.0, '#d32f2f'], [0.5, '#f5f5f5'], [1.0, '#388e3c']],
        cmid=0,
        colorbar=dict(title="Fuerza Relativa")
    )
))

fig.update_layout(
    title=f'🌡️ Mapa de Calor Nasdaq 100 - {hora}',
    margin=dict(t=50, l=10, r=10, b=10),
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TABLAS DE APOYO
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Ranking de Sectores")
    resumen_sectores = df.groupby('Sector')['Fuerza Relativa (RS)'].mean().reset_index()
    resumen_sectores = resumen_sectores.sort_values(by='Fuerza Relativa (RS)', ascending=False)
    st.dataframe(resumen_sectores, use_container_width=True, hide_index=True)

with col2:
    st.subheader("🚀 Top 10 Más Fuertes")
    top_fuertes = df.sort_values(by='Fuerza Relativa (RS)', ascending=False).head(10)
    st.dataframe(top_fuertes[['Ticker', 'Cambio %', 'Fuerza Relativa (RS)', 'Sector']], use_container_width=True, hide_index=True)
    
    st.subheader("🩸 Top 10 Más Débiles")
    top_debiles = df.sort_values(by='Fuerza Relativa (RS)', ascending=True).head(10)
    st.dataframe(top_debiles[['Ticker', 'Cambio %', 'Fuerza Relativa (RS)', 'Sector']], use_container_width=True, hide_index=True)
