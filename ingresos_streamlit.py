import streamlit as st

def calcular_roi(alquiler_h, N, vast, precio_gpu, consumo):
    """
    Calcula el ROI de alquilar una GPU.

    Parámetros:
    alquiler_h : float - Ingreso por hora de alquiler
    N          : int   - Número de GPUs
    vast       : float - Porcentaje de uso o eficiencia (entre 0 y 1)
    precio_gpu : float - Precio de compra de una GPU
    consumo    : float - Consumo energético por hora en kWh

    Retorna:
    float - ROI calculado en porcentaje
    """
    ingreso_mensual = alquiler_h * N * (24 * vast) * 28
    costos_energia = consumo * (24 * vast) * 28 * N * 0.15
    costos_fijos = costos_energia + 60 + 30
    ingreso_anual = (ingreso_mensual - costos_fijos) * 12
    depreciacion = (precio_gpu / 4) * N  # Depreciación a 4 años
    roi = (ingreso_anual - depreciacion) / (precio_gpu * N)
    return roi * 100

# Título de la app
st.title("Calculadora de ROI de GPU alquiladas")

# Especificaciones de GPUs
gpu_specs = {
    "NVIDIA A100 (40 GB PCIe)": {"price": 15000.0, "rental": 0.94, "consumo": 0.40},
    "RTX 4070":               {"price": 599.0,   "rental": 0.11, "consumo": 0.20},
    "RTX 4070 Ti":            {"price": 799.0,   "rental": 0.12, "consumo": 0.285},
    "RTX 4080":               {"price": 1199.0,  "rental": 0.24, "consumo": 0.32},
    "RTX 4090":               {"price": 1599.0,  "rental": 0.39, "consumo": 0.45},
    "RTX 5070":               {"price": 549.0,   "rental": 0.09, "consumo": 0.25},
    "RTX 5070 Ti":            {"price": 749.0,   "rental": 0.17, "consumo": 0.30},
    "RTX 5080":               {"price": 999.0,   "rental": 0.20, "consumo": 0.36},
    "RTX 5090":               {"price": 1999.0,  "rental": 0.53, "consumo": 0.575},
    "RTX 6000 Ada":           {"price": 6799.0,  "rental": 0.68, "consumo": 0.30},
    "RTX A2000":              {"price": 449.0,   "rental": 0.03, "consumo": 0.07},
    "RTX A4000":              {"price": 1000.0,  "rental": 0.10, "consumo": 0.14},
    "RTX A4500":              {"price": 2250.0,  "rental": 0.18, "consumo": 0.20},
    "RTX A5000":              {"price": 2250.0,  "rental": 0.23, "consumo": 0.23},
    "RTX A6000":              {"price": 4650.0,  "rental": 0.48, "consumo": 0.30},
    "Titan RTX":              {"price": 2499.0,  "rental": 0.80, "consumo": 0.28},
    "Titan V":                {"price": 2999.0,  "rental": 0.70, "consumo": 0.25},
    "NVIDIA A10":             {"price": 3700.0,  "rental": 0.26, "consumo": 0.15},
    "NVIDIA A40":             {"price": 6650.0,  "rental": 0.51, "consumo": 0.30},
    "GTX 1060":               {"price": 249.0,   "rental": 0.09, "consumo": 0.12},
    "GTX 1070":               {"price": 379.0,   "rental": 0.08, "consumo": 0.15},
    "GTX 1080":               {"price": 599.0,   "rental": 0.08, "consumo": 0.18},
    "GTX TITAN X":            {"price": 999.0,   "rental": 0.08, "consumo": 0.25},
    "H100 NVL":               {"price": 30450.0, "rental": 2.27, "consumo": 0.70},
    "H100 SXM":               {"price": 30000.0, "rental": 2.20, "consumo": 0.70},
    "NVIDIA L40S":            {"price": 8351.99, "rental": 0.68, "consumo": 0.30},
    "Quadro RTX 8000":        {"price": 9999.0,  "rental": 0.29, "consumo": 0.26},
    "Tesla P100":             {"price": 5699.0,  "rental": 0.11, "consumo": 0.25},
    "Tesla P4":               {"price": 3997.99,"rental": 0.04, "consumo": 0.075},
    "Tesla P40":              {"price": 5699.0,  "rental": 0.11, "consumo": 0.25},
    "Tesla T4":               {"price": 1880.0,  "rental": 0.15, "consumo": 0.07},
    "Tesla V100":             {"price": 9900.0,  "rental": 0.14, "consumo": 0.30},
    "NVIDIA Titan Xp":        {"price": 1199.0,  "rental": 0.08, "consumo": 0.25},
}

# Sidebar: selección de GPU y parámetros
st.sidebar.header("Configuración")

gpu_seleccionada = st.sidebar.selectbox(
    "Modelo de GPU",
    options=list(gpu_specs.keys())
)

vast = st.sidebar.slider(
    "Eficiencia de uso (vast)",
    min_value=0.0,
    max_value=1.0,
    value=0.75,
    step=0.01
)

N = st.sidebar.number_input(
    "Número de GPUs",
    min_value=1,
    value=1,
    step=1
)

# Carga de especificaciones seleccionadas
specs = gpu_specs[gpu_seleccionada]
precio_gpu = specs["price"]
alquiler_h = specs["rental"]
consumo = specs["consumo"]

# Cálculo de ROI
roi = calcular_roi(alquiler_h, N, vast, precio_gpu, consumo)

# Mostrar resultado principal
st.metric("ROI estimado (%)", f"{roi:.2f}%")

# Desglose de cálculos
with st.expander("Ver desglose de cálculos"):
    ingreso_mensual = alquiler_h * N * (24 * vast) * 28
    costos_energia = consumo * (24 * vast) * 28 * N * 0.15
    costos_fijos = costos_energia + 60 + 30
    ingreso_anual = (ingreso_mensual - costos_fijos) * 12
    depreciacion = (precio_gpu / 4) * N

    st.write(f"**Modelo**: {gpu_seleccionada}")
    st.write(f"Ingreso por hora: ${alquiler_h:.2f}")
    st.write(f"Precio por GPU: ${precio_gpu:,.2f}")
    st.write(f"Consumo energético: {consumo:.3f} kWh/h")
    st.write(f"Ingreso mensual: ${ingreso_mensual:,.2f}")
    st.write(f"Costos de energía mensuales: ${costos_energia:,.2f}")
    st.write(f"Costos fijos mensuales (incluye $60 + $30): ${costos_fijos:,.2f}")
    st.write(f"Ingreso anual neto: ${ingreso_anual:,.2f}")
    st.write(f"Depreciación anual (4 años): ${depreciacion:,.2f}")


