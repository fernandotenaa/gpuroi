import streamlit as st

# Función para calcular ROI de un conjunto de GPUs
def calcular_roi(gpu_counts, vast, gpu_specs):
    """
    Calcula el ROI anual de un conjunto de GPUs.

    Parámetros:
    gpu_counts : dict - {modelo: cantidad}
    vast       : float - Porcentaje de uso o eficiencia (entre 0 y 1)
    gpu_specs  : dict - Especificaciones de GPUs

    Retorna:
    tuple de floats - (roi_porcentaje, ingreso_mensual, costos_energia, costos_fijos, ingreso_anual, depreciacion_total, capex_total)
    """
    # Ingreso mensual total
    ingreso_mensual = sum(
        specs['rental'] * count * (24 * vast) * 28
        for model, count in gpu_counts.items()
        for specs in [gpu_specs[model]]
    )
    # Costos de energía mensual total
    costos_energia = sum(
        specs['consumo'] * (24 * vast) * 28 * count * 0.15
        for model, count in gpu_counts.items()
        for specs in [gpu_specs[model]]
    )
    # Costos fijos (suma de energía + gastos fijos mensuales)
    costos_fijos = costos_energia + 60 + 30
    # Ingreso anual neto
    ingreso_anual = (ingreso_mensual - costos_fijos) * 12
    # Depreciación anual total (4 años)
    depreciacion_total = sum(
        (gpu_specs[model]['price'] / 4) * count
        for model, count in gpu_counts.items()
    )
    # CAPEX total
    capex_total = sum(
        gpu_specs[model]['price'] * count
        for model, count in gpu_counts.items()
    )
    # Cálculo de ROI
    roi = (ingreso_anual - depreciacion_total) / capex_total * 100
    return roi, ingreso_mensual, costos_energia, costos_fijos, ingreso_anual, depreciacion_total, capex_total

# Título de la aplicación
st.title("Calculadora de ROI de GPUs alquiladas (Multi-GPU)")

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

# Sidebar: configuración
st.sidebar.header("Configuración del datacenter")

# Eficiencia de uso
dp_vast = st.sidebar.slider(
    "Eficiencia de uso (vast)",
    min_value=0.0,
    max_value=1.0,
    value=0.75,
    step=0.01
)

# Selección de múltiples modelos de GPU
gpu_modelos = st.sidebar.multiselect(
    "Modelos de GPU",
    options=list(gpu_specs.keys()),
    default=[list(gpu_specs.keys())[0]]
)

# Número de GPUs por modelo
gpu_counts = {}
for model in gpu_modelos:
    gpu_counts[model] = st.sidebar.number_input(
        f"Número de unidades de {model}",
        min_value=1,
        value=1,
        step=1
    )

# Validación: al menos un modelo
if not gpu_modelos:
    st.sidebar.error("Selecciona al menos un modelo de GPU para continuar.")
    st.stop()

# Cálculo de ROI y desgloses
roi, ingreso_mensual, costos_energia, costos_fijos, ingreso_anual, depreciacion_total, capex_total = \
    calcular_roi(gpu_counts, dp_vast, gpu_specs)

# Mostrar ROI estimado
st.metric("ROI estimado (%)", f"{roi:.2f}%")

# Desglose de cálculos
with st.expander("Ver desglose de cálculos"):
    st.write("**Configuración seleccionada:**")
    for model, count in gpu_counts.items():
        specs = gpu_specs[model]
        st.write(f"- {model}: {count} unidad(es) | Precio: ${specs['price']:,} | Alquiler h: ${specs['rental']:.2f}/h | Consumo: {specs['consumo']:.3f} kWh/h")
    st.write(f"\n**Ingreso mensual total:** ${ingreso_mensual:,.2f}")
    st.write(f"**Costos de energía mensuales:** ${costos_energia:,.2f}")
    st.write(f"**Costos fijos mensuales (energía + $60 + $30):** ${costos_fijos:,.2f}")
    st.write(f"**Ingreso anual neto:** ${ingreso_anual:,.2f}")
    st.write(f"**Depreciación anual total (4 años):** ${depreciacion_total:,.2f}")
    st.write(f"**Inversión total (CAPEX):** ${capex_total:,.2f}")


