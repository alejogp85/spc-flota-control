import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# 1. CONFIGURACIÓN DE LA APP 
st.set_page_config(page_title="Centro de Control Flota", layout="wide", page_icon="🚛")
st.title("🛰️ Centro de Control Operacional - Telemetría Diésel")
st.markdown("*(Proof of Concept - Detección de Anomalías SPC)*")

# 2. FILTRO OPERACIONAL (Nivel Head: Interactividad de piso)
col1, col2 = st.columns(2)
with col1:
    placa = st.selectbox("Seleccionar Unidad:", ["TRA-001 (Volvo FH)", "TRA-042 (Scania R)", "TRA-108 (Mercedes Actros)"])
with col2:
    st.metric(label="Consumo Actual Reportado por GPS", value="51.5 Lts/100km", delta="13.0 Lts sobre media", delta_color="inverse")

st.divider()

# Creamos 3 columnas para poner las métricas fuera del gráfico
col_metrica1, col_metrica2, col_metrica3 = st.columns(3)

with col_metrica1:
    st.error("⚠️ THRESHOLD ALERT: > 3σ")

with col_metrica2:
    st.success("✅ OPERATIONAL EFFICIENCY: 99.7% de viajes dentro del límite")

with col_metrica3:
    st.warning("💰 SAVINGS OPPORTUNITY: Reducción de variabilidad detectada (P&L Protection)")

st.divider()

# --- CÓDIGO DE PYTHON DE POWER BI ---
mu = 38.5
sigma = 2.2
ucl = mu + (3 * sigma)
lcl = mu - (3 * sigma)

x = np.linspace(mu - 4*sigma, mu + 5*sigma, 1000)
y = norm.pdf(x, mu, sigma)

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 7))

# Dibujar la campana principal
ax.plot(x, y, color='#00D4FF', linewidth=2.5, label='Distribución Normal')

# Rellenar el área de "Operational Efficiency" (99.7%)
ax.fill_between(x, y, where=(x >= lcl) & (x <= ucl), color='#00D4FF', alpha=0.2, label='Operational Efficiency: 99.7%')

# Rellenar las colas (Anomalías)
ax.fill_between(x, y, where=(x > ucl), color='#FF4C4C', alpha=0.4, label='Threshold Alert: > 3σ')
ax.fill_between(x, y, where=(x < lcl), color='#FF4C4C', alpha=0.4)

# 4. Dibujar las líneas de control
ax.axvline(mu, color='#00FF00', linestyle='--', linewidth=1.5, label=f'Media (μ): {mu} Lts/100km')
ax.axvline(ucl, color='#FF4C4C', linestyle='--', linewidth=1.5, label=f'UCL (+3σ): {ucl} Lts/100km')
ax.axvline(lcl, color='#FF4C4C', linestyle='--', linewidth=1.5, label=f'LCL (-3σ): {lcl} Lts/100km')

# 5. Colocar  Puntos Rojos (Anomalías)
anomalias = {
    48.2: "Punto A: 48.2\nDiagnóstico: Fuga o falla\nen sistema de inyección",
    51.5: "Punto B: 51.5\nDiagnóstico: ALERTA AUDITORÍA\n(Sospecha de 'ordeño')",
    31.0: "Punto C: 31.0\nDiagnóstico: Error sensor\ntelemetría / Carga incompleta"
}

for valor, texto in anomalias.items():
    y_val = norm.pdf(valor, mu, sigma)
    # Punto rojo brillante
    ax.scatter(valor, y_val, color='#FF0000', s=120, zorder=5, edgecolors='white', linewidth=1.5)
    # Línea punteada que conecta el punto con el eje X para darle énfasis
    ax.plot([valor, valor], [0, y_val], color='#FF0000', linestyle=':', linewidth=1)
    # Etiquetas de diagnóstico
    offset = 10 if valor > mu else -10
    ax.annotate(texto, (valor, y_val), textcoords="offset points", xytext=(offset, 15),
                ha='center', fontsize=8, color='white', weight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="#333333", ec="#FF4C4C", lw=1.5))

# 6. Etiquetas  (Texto fijo en el gráfico)
#fig.text(0.15, 0.88, "⚠️ THRESHOLD ALERT: > 3σ", fontsize=12, color='#FF4C4C', weight='bold')
#fig.text(0.15, 0.83, "✅ OPERATIONAL EFFICIENCY: 99.7% de viajes dentro del límite", fontsize=10, color='#00FF00')
#fig.text(0.15, 0.78, "💰 SAVINGS OPPORTUNITY: Reducción de variabilidad detectada (P&L Protection)", fontsize=10, color='#FFD700')

# 7. Formato final del gráfico
ax.set_title('Control Estadístico de Proceso (SPC) - Consumo Diésel Flota Pesada (Lts/100km)', fontsize=14, pad=20, color='white')
ax.set_xlabel('Consumo (Lts/100km)', fontsize=11, color='#CCCCCC')
ax.set_ylabel('Densidad de Probabilidad', fontsize=11, color='#CCCCCC')
ax.legend(loc='upper right', fontsize=8, framealpha=0.8)
ax.grid(axis='y', alpha=0.2)
ax.set_xlim(28, 55)

# Mostrar en Power BI
plt.tight_layout()
plt.show()

# --- CAMBIO CLAVE PARA STREAMLIT ---
# En Power BI plt.show()
# En Streamlit st.pyplot()
st.pyplot(fig)

# 4. PANEL DE DECISIÓN (Nivel Head: ¿Qué hacer con esta info?)
st.subheader("📋 Protocolo de Acción Automatizado")
st.error("🚨 ALERTA CRÍTICA DETECTADA: El vehículo supera el UCL (+3σ).")
st.code("""
IF Consumo > 45.1 Lts/100km:
    1. Enviar alerta al supervisor de flota.
    2. Bloquear dispensador de diésel en próxima estación.
    3. Generar ticket de auditoría interna (Sospecha de 'Ordeño').
""")




