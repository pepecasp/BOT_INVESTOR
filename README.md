# 📈 InvestQuant Pro — Cartera & Análisis Técnico Cuantitativo

Aplicación web profesional en **Python + Streamlit** con arquitectura **Mobile-First**, diseñada para desplegarse de inmediato en **Streamlit Community Cloud**. Permite gestionar la cartera de inversión en tiempo real, monitorizar activos clave (S&P 500, Oro, Plata y activos personalizados) y ejecutar un motor cuantitativo algorítmico que detecta tendencias, techos, suelos y alertas automáticas a Telegram.

---

## 🚀 Despliegue en Streamlit Community Cloud

### Paso 1: Subir el proyecto a GitHub
Sube este directorio a un repositorio de GitHub (público o privado):
```bash
git init
git add .
git commit -m "InvestQuant Pro inicial"
git remote add origin <URL_DE_TU_REPOSITORIO>
git push -u origin main
```

### Paso 2: Crear la App en Streamlit Cloud
1. Entra en [share.streamlit.io](https://share.streamlit.io).
2. Haz clic en **"New app"**.
3. Selecciona tu repositorio, rama (`main`) y archivo principal: `app.py`.

### Paso 3: Configurar Secretos (Telegram)
En la configuración de la app en Streamlit Cloud (**Settings > Secrets**), añade tus credenciales:
```toml
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrSTUvwxYZ"
TELEGRAM_CHAT_ID = "987654321"
```
*(Nota: Si no las configuras aquí, la app cuenta con campos manuales en la barra lateral con persistencia en sesión).*

---

## 📊 Arquitectura Cuantitativa Algorítmica

El motor analiza velas diarias (1D) de los últimos 24 meses y evalúa objetivamente:

### 1. Dirección de Tendencia
- **📈 Tendencia Alcista:** $SMA_{50} > SMA_{200}$, precio actual $> SMA_{50}$ y máximos locales crecientes.
- **📉 Tendencia Bajista:** $SMA_{50} < SMA_{200}$, precio actual $< SMA_{50}$ y máximos locales decrecientes.
- **↔️ Movimiento Lateral:** Oscilación estrecha ($< 4\%$ entre máx y mín de las últimas 20 sesiones) con pendiente de $SMA_{50}$ plana ($< 1.2\%$).

### 2. Detección de Niveles Clave
- **🛡️ Suelo Local (Soporte 30d):** $\min(Low_{30})$.
- **🧱 Techo Local (Resistencia 30d):** $\max(High_{30})$.
- **🏆 Máximo Anual (250d):** $\max(High_{250})$.

### 3. Patrones de Precio y Alertas a Telegram
- **🔴 Choque / Rechazo en Techo:** Precio a menos del 1% del techo local cerrando con vela roja o mecha superior pronunciada ($\ge 38\%$ del rango).
- **🚀 Ruptura de Techo (Nuevo Máximo):** Cierre sobre la resistencia local con volumen $\ge 1.3\times$ la media móvil de 20 sesiones.
- **🟢 Rebote en Soporte (Suelo Defendido):** Precio en soporte ($\le +1\%$), $RSI_{14} < 38$, vela verde alcista superando el máximo previo y volumen creciente.
- **📦 Movimiento Lateral / Rango:** Acumulación neutra entre el soporte y la resistencia.

---

## 💼 Gestión de Cartera (Wallet)
- Persistencia local en `portfolio.json`.
- Valoración automática en Euros (€), con conversión dinámica de divisas USD vía `EURUSD=X`.
- Métricas: Total Invertido, Valor Actual en Vivo, Ganancia/Pérdida Neta (€ y %) y Comisiones.
- Formulario de compras y gestor interactivo de transacciones.
