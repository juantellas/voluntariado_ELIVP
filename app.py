import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import unicodedata

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="ELIVP 2026 · Inscritos",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Forzar sidebar abierto en entornos deployed
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] { transform: none !important; min-width: 280px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# ESTILOS GLOBALES
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #0f1923 !important;
    color: #D9DDDC !important;
}

.main .block-container {
    background-color: #0f1923;
    padding-top: 0 !important;
    padding-bottom: 3rem;
    max-width: 100% !important;
}
.main { background-color: #0f1923; }

/* ── Cabecera ── */
.dashboard-header {
    background: #ffffff;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px 30px;
    margin: 20px auto 30px auto;
    max-width: 900px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
}
.dashboard-header h1 {
    font-size: 32px;
    font-weight: 600;
    color: #0f1923;
    margin: 0 0 2px 0;
    line-height: 1.3;
}
.dashboard-header p {
    font-size: 12px;
    color: #7a8fa0;
    margin: 0;
}

/* ── Toggle de filtro ── */
.toggle-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #131e2b;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 12px 20px;
    margin-bottom: 24px;
}
.toggle-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
}
.toggle-active {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(74,222,128,0.1);
    border: 1px solid rgba(74,222,128,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    color: #4ade80;
    text-transform: uppercase;
}
.toggle-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #4ade80;
    display: inline-block;
}
.toggle-inactive {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 4px 14px;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    color: rgba(255,255,255,0.3);
    text-transform: uppercase;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #0f1923 !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSelectbox label {
    color: rgba(255,255,255,0.45) !important;
    font-size: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.5px !important;
}
[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #1a5cff !important;
    border-radius: 20px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.06) !important;
    border-color: rgba(255,255,255,0.12) !important;
    border-radius: 8px !important;
}

/* ── Toggle nativo de Streamlit ── */
[data-testid="stToggle"] label {
    color: rgba(255,255,255,0.6) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── Cards de gráfica ── */
.chart-card {
    background: #ffffff;
    border: 1px solid #e0e5ec;
    border-radius: 14px;
    padding: 18px 18px 10px 18px;
    margin-bottom: 4px;
}
.chart-card-title {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    color: #7a8fa0;
    margin: 0 0 12px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid #f0f2f6;
}

/* ── KPI cards ── */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e0e5ec;
    border-radius: 14px;
    padding: 18px 20px 16px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.kpi-blue::before  { background: #1a5cff; }
.kpi-amber::before { background: #e8900a; }
.kpi-green::before { background: #0f8c5c; }
.kpi-violet::before { background: #7c3aed; }
.kpi-label {
    font-size: 9px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.8px;
    color: #7a8fa0;
    margin: 0 0 6px 0;
}
.kpi-value {
    font-family: 'DM Mono', monospace;
    font-size: 32px;
    font-weight: 500;
    color: #0f1923;
    line-height: 1;
    margin: 0 0 8px 0;
}
.kpi-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 500;
    padding: 3px 9px;
    border-radius: 20px;
}
.kpi-blue   .kpi-badge { background: #dce8ff; color: #1a5cff; }
.kpi-amber  .kpi-badge { background: #fff3d6; color: #9a5e00; }
.kpi-green  .kpi-badge { background: #d6f5e9; color: #0f8c5c; }
.kpi-violet .kpi-badge { background: #ede9fe; color: #7c3aed; }

/* ── Banner seleccionados ── */
.banner-seleccionados {
    background: linear-gradient(135deg, #052e16 0%, #0a1a0f 100%);
    border: 1px solid rgba(74,222,128,0.2);
    border-radius: 12px;
    padding: 14px 22px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.banner-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #4ade80;
    flex-shrink: 0;
    box-shadow: 0 0 8px rgba(74,222,128,0.5);
}
.banner-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    color: #4ade80;
    text-transform: uppercase;
}
.banner-count {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 1.1rem;
    color: #4ade80;
    font-weight: 500;
}

/* ── Divisores de sección ── */
.section-header {
    font-size: 9px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #7a8fa0;
    margin: 22px 0 10px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e0e5ec;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: #ffffff !important;
    border-bottom: 1px solid #e0e5ec !important;
    border-radius: 12px 12px 0 0 !important;
    gap: 0 !important;
    padding: 0 8px !important;
}
[data-baseweb="tab"] {
    font-size: 12px !important;
    font-weight: 500 !important;
    padding: 12px 20px !important;
    color: #7a8fa0 !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: #1a5cff !important;
    border-bottom: 2px solid #1a5cff !important;
}

[data-testid="metric-container"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────
def limpiar_texto(s):
    if pd.isna(s):
        return s
    s = str(s).strip().upper()
    s = unicodedata.normalize("NFKD", s).encode("ascii", errors="ignore").decode("utf-8")
    s = s.replace("-", " ")
    s = " ".join(s.split())
    return s

def limpiar_objetivo(x):
    if pd.isna(x):
        return "N/A"
    return str(x).split(":")[0].strip()

ACCENT     = "#1a5cff"
AMBER      = "#e8900a"
GREEN      = "#0f8c5c"
SLATE      = "#94a3b8"
INK        = "#ffffff"
INK_MID    = "rgba(255,255,255,0.75)"
INK_LIGHT  = "rgba(255,255,255,0.5)"
BORDER     = "rgba(255,255,255,0.08)"
SURFACE    = "#1a1a2e"
COLORS_PIE = [ACCENT, "#5e8af5", "#93b4fc", SLATE, AMBER, GREEN]
COLOR_SEQ  = ["#1a5cff", "#5e8af5", "#93b4fc", "#c7d8ff", "#e2e8f0"]

PLOTLY_BASE = dict(
    paper_bgcolor="#1a1a2e",
    plot_bgcolor="#1a1a2e",
    font_family="DM Sans",
    font_color=INK_MID,
)

def section(label):
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)

def card_open(title):
    st.markdown(
        f'<div class="chart-card"><p class="chart-card-title">{title}</p>',
        unsafe_allow_html=True,
    )

def card_close():
    st.markdown("</div>", unsafe_allow_html=True)

def kpi_html(valor, label, badge_text, css_class):
    return (
        f'<div class="kpi-card {css_class}">'
        f'<p class="kpi-label">{label}</p>'
        f'<p class="kpi-value">{valor}</p>'
        f'<span class="kpi-badge">{badge_text}</span>'
        f'</div>'
    )

def make_donut(labels, values, colors, height=240):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.68,
        marker_colors=colors, textinfo="none",
        hovertemplate="<b>%{label}</b>: %{value:,} (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_BASE, showlegend=True, height=height,
        margin=dict(l=8, r=8, t=8, b=56),
        legend=dict(orientation="h", x=0.5, xanchor="center",
                    y=-0.05, yanchor="top", font_size=10, font_color=INK_MID),
    )
    return fig

def make_bar_h(data, col_y, col_x, color, height=None, margin=None):
    h = height or max(220, len(data) * 38)
    m = margin or dict(l=4, r=36, t=8, b=8)
    fig = go.Figure(go.Bar(
        x=data[col_x], y=data[col_y], orientation="h",
        marker_color=color, marker_line_width=0,
        hovertemplate="<b>%{y}</b>: %{x:,}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_BASE, showlegend=False, height=h, margin=m,
        yaxis=dict(autorange="reversed", tickfont_size=11,
                   gridcolor=SURFACE, showgrid=True),
        xaxis=dict(gridcolor=BORDER, tickfont_size=10, showgrid=True),
    )
    return fig


# ─────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────
@st.cache_data
def cargar_datos():
    df = pd.read_excel(
        "Postulación+ELIVP+2026_May+4,+2026_13.59_filtradotrue_CLEAN_MAPPED.xlsx"
    )
    df["FechaNacimiento"] = pd.to_datetime(df["FechaNacimiento"], errors="coerce")
    hoy = pd.Timestamp.today()
    df["Edad"] = (hoy - df["FechaNacimiento"]).dt.days // 365
    df["RangoEdad"] = df["Edad"].apply(
        lambda x: "18–28" if pd.notna(x) and 18 <= x <= 28 else "Fuera de rango"
    )
    for col in ["Barrio", "Localidad", "Genero", "NivelEducativo",
                "GruposPoblacionales", "MiembroOrganizacionJuvenil"]:
        if col in df.columns:
            df[col] = df[col].apply(limpiar_texto)

    # Normalizar columna Seleccionado
    if "Seleccionado" in df.columns:
        def normalizar_seleccionado(x):
            if pd.isna(x):
                return "No"
            s = str(x).strip()
            sl = s.lower()
            if "opcion 1" in sl or "opción 1" in sl:
                return "Si (Opcion 1)"
            if "opcion 2" in sl or "opción 2" in sl:
                return "Si (Opcion 2)"
            if sl in ["si", "sí"]:
                return "Si"
            return "No"
        df["Seleccionado"] = df["Seleccionado"].apply(normalizar_seleccionado)
    else:
        df["Seleccionado"] = "No"

    return df

@st.cache_data
def cargar_geo():
    try:
        gdf = gpd.read_file("barrios.geojson").to_crs(epsg=4326)
        for col in ["Barrio", "Localidad"]:
            if col in gdf.columns:
                gdf[col] = gdf[col].apply(limpiar_texto)
        return gdf
    except Exception:
        return None

df  = cargar_datos()
gdf = cargar_geo()


# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0 0 20px 0;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:20px">
        <p style="font-size:9px;letter-spacing:2px;color:rgba(255,255,255,0.3);
                  text-transform:uppercase;margin:0 0 4px 0">Uninorte x NuestraBarranquilla</p>
        <p style="font-size:17px;font-weight:600;color:#fff;margin:0">ELIVP 2026</p>
        <p style="font-size:11px;color:rgba(255,255,255,0.4);margin:2px 0 0 0">Panel de Inscritos</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size:9px;font-weight:600;letter-spacing:2px;'
        'text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:14px">Filtros</p>',
        unsafe_allow_html=True,
    )

    # ── Toggle seleccionados ──────────────────────
    solo_seleccionados = st.toggle(
        "Solo seleccionados",
        value=False,
        help="Muestra únicamente candidatos seleccionados (Opción 1 y/o Opción 2)"
    )

    # ── Filtro de opción (solo visible si toggle activo) ──
    f_opcion = []
    if solo_seleccionados:
        st.markdown(
            '<p style="font-size:9px;font-weight:600;letter-spacing:2px;'
            'text-transform:uppercase;color:rgba(74,222,128,0.5);'
            'margin:10px 0 6px 0">Horario asignado</p>',
            unsafe_allow_html=True,
        )
        f_opcion = st.multiselect(
            "Opción de horario",
            ["Si (Opcion 1)", "Si (Opcion 2)"],
            placeholder="Todas las opciones",
            label_visibility="collapsed",
        )

        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 8px;
            padding: 10px 14px;
            margin-top: 8px;
        ">
            <p style="
                font-family:'DM Mono',monospace;
                font-size:0.68rem;
                letter-spacing:0.1em;
                color:rgba(129,140,248,0.9);
                text-transform:uppercase;
                margin:0 0 6px 0;
            ">● Opción 1</p>
            <p style="
                font-family:'DM Sans',sans-serif;
                font-size:0.78rem;
                color:rgba(255,255,255,0.35);
                margin:0 0 10px 0;
                line-height:1.5;
            ">Martes y Jueves<br>2:00 PM – 6:00 PM</p>
            <p style="
                font-family:'DM Mono',monospace;
                font-size:0.68rem;
                letter-spacing:0.1em;
                color:rgba(52,211,153,0.9);
                text-transform:uppercase;
                margin:0 0 6px 0;
            ">● Opción 2</p>
            <p style="
                font-family:'DM Sans',sans-serif;
                font-size:0.78rem;
                color:rgba(255,255,255,0.35);
                margin:0;
                line-height:1.5;
            ">Viernes 2:00 PM – 6:00 PM<br>Sábados 9:00 AM – 1:00 PM</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    genero_opts    = sorted(df["Genero"].dropna().unique().tolist())
    localidad_opts = sorted(df["Localidad"].dropna().unique().tolist())
    estrato_opts   = sorted(df["Estrato"].dropna().unique().tolist())

    f_genero    = st.multiselect("Género",         genero_opts,                 placeholder="Todos")
    f_localidad = st.multiselect("Localidad",      localidad_opts,              placeholder="Todas")
    f_estrato   = st.multiselect("Estrato",        estrato_opts,                placeholder="Todos")
    f_rango     = st.multiselect("Rango de edad",  ["18–28", "Fuera de rango"], placeholder="Todos")

    # ── Aplicar filtros ──
    df_f = df.copy()

    if solo_seleccionados:
        opciones_seleccionadas = f_opcion if f_opcion else ["Si (Opcion 1)", "Si (Opcion 2)"]
        df_f = df_f[df_f["Seleccionado"].isin(opciones_seleccionadas)]

    if f_genero:    df_f = df_f[df_f["Genero"].isin(f_genero)]
    if f_localidad: df_f = df_f[df_f["Localidad"].isin(f_localidad)]
    if f_estrato:   df_f = df_f[df_f["Estrato"].isin(f_estrato)]
    if f_rango:     df_f = df_f[df_f["RangoEdad"].isin(f_rango)]

    pct_rango = (df_f["RangoEdad"] == "18–28").sum() / max(len(df_f), 1) * 100

    st.markdown(f"""
    <div style="border-top:1px solid rgba(255,255,255,0.08);padding-top:20px;margin-top:28px">
        <p style="font-size:9px;letter-spacing:1.5px;text-transform:uppercase;
                  color:rgba(255,255,255,0.3);margin-bottom:4px">Total filtrado</p>
        <p style="font-family:'DM Mono',monospace;font-size:34px;font-weight:500;
                  color:#fff;margin:0;line-height:1">{len(df_f):,}</p>
        <p style="font-size:11px;color:rgba(255,255,255,0.35);margin:6px 0 0 0">
            {pct_rango:.1f}% en rango 18–28
        </p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# CABECERA
# ─────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
    <h1>Caracterización de Inscritos - Prueba Final</h1>
    <p>Escuela de Liderazgo e Innovación Pública &nbsp;·&nbsp; Mayo 2026 &nbsp;·&nbsp; Barranquilla &nbsp;·&nbsp; Universidad Del Norte x NuestraBarranquilla</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# BANNER SELECCIONADOS (visible solo si toggle activo)
# ─────────────────────────────────────────
total_op1 = int((df["Seleccionado"] == "Si (Opcion 1)").sum())
total_op2 = int((df["Seleccionado"] == "Si (Opcion 2)").sum())
total_seleccionados = total_op1 + total_op2

if solo_seleccionados:
    if f_opcion and len(f_opcion) == 1:
        opcion_label = f_opcion[0]
        color_opcion = "#818cf8" if "1" in f_opcion[0] else "#34d399"
    else:
        opcion_label = "Opción 1 + Opción 2"
        color_opcion = "#4ade80"

    st.markdown(f"""
    <div class="banner-seleccionados" style="border-color:rgba(74,222,128,0.2);">
        <div class="banner-dot" style="background:{color_opcion};box-shadow:0 0 8px {color_opcion}66;"></div>
        <span class="banner-text">Seleccionados · {opcion_label}</span>
        <span class="banner-count" style="color:{color_opcion};">{len(df_f):,} / {total_seleccionados:,}</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────
total    = len(df_f)
en_rango = int((df_f["RangoEdad"] == "18–28").sum())
fuera    = int((df_f["RangoEdad"] != "18–28").sum())

if solo_seleccionados:
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(kpi_html(
            f"{total:,}", "Seleccionados", "Vista filtrada", "kpi-violet"
        ), unsafe_allow_html=True)
    with k2:
        op1_count = int((df_f["Seleccionado"] == "Si (Opcion 1)").sum())
        st.markdown(kpi_html(
            f"{op1_count:,}", "Opción 1",
            f"{op1_count / max(total, 1) * 100:.1f}% del filtrado", "kpi-blue"
        ), unsafe_allow_html=True)
    with k3:
        op2_count = int((df_f["Seleccionado"] == "Si (Opcion 2)").sum())
        st.markdown(kpi_html(
            f"{op2_count:,}", "Opción 2",
            f"{op2_count / max(total, 1) * 100:.1f}% del filtrado", "kpi-green"
        ), unsafe_allow_html=True)
    with k4:
        st.markdown(kpi_html(
            f"{en_rango:,}", "En rango 18–28",
            f"{en_rango / max(total, 1) * 100:.1f}% del filtrado", "kpi-amber"
        ), unsafe_allow_html=True)
else:
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(kpi_html(
            f"{total:,}", "Total inscritos", "Todos los registros", "kpi-blue"
        ), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_html(
            f"{en_rango:,}", "En rango 18–28",
            f"{en_rango / max(total, 1) * 100:.1f}% del total", "kpi-amber"
        ), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_html(
            f"{fuera:,}", "Fuera de rango",
            f"{fuera / max(total, 1) * 100:.1f}% del total", "kpi-green"
        ), unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  Caracterización  ",
    "  Socioeconómico  ",
    "  Mapa  ",
    "  Datos  ",
])


# ════════════════════════════════════════
# TAB 1 — CARACTERIZACIÓN
# ════════════════════════════════════════
with tab1:

    section("Género y edad")
    c1, c2 = st.columns(2)

    with c1:
        gen_data = df_f["Genero"].value_counts().reset_index()
        gen_data.columns = ["Género", "Cantidad"]
        card_open("Género")
        st.plotly_chart(
            make_donut(gen_data["Género"], gen_data["Cantidad"], COLORS_PIE),
            use_container_width=True,
        )
        card_close()

    with c2:
        edad_data = df_f["RangoEdad"].value_counts().reset_index()
        edad_data.columns = ["Rango", "Cantidad"]
        card_open("Rango de edad")
        st.plotly_chart(
            make_donut(edad_data["Rango"], edad_data["Cantidad"], [ACCENT, AMBER]),
            use_container_width=True,
        )
        card_close()

    df_f["Objetivo_limpio"] = df_f["ObjetivoOrganizacionJuvenil"].apply(limpiar_objetivo)

    section("Participación juvenil y territorio")

    o1, o2 = st.columns([1, 2])

    with o1:
        org = df_f["MiembroOrganizacionJuvenil"].value_counts().reset_index()
        org.columns = ["Miembro", "Cantidad"]
        card_open("Organización juvenil")
        st.plotly_chart(
            make_donut(org["Miembro"], org["Cantidad"], [GREEN, "#e0e5ec"], height=250),
            use_container_width=True,
        )
        card_close()

    with o2:
        loc_top = df_f["DisponibilidadHorario"].value_counts().reset_index()
        loc_top.columns = ["Disponibilidad", "Inscritos"]
        card_open("Horarios por Inscritos")
        st.plotly_chart(
            make_bar_h(loc_top, "Disponibilidad", "Inscritos", "#93b4fc", height=200),
            use_container_width=True,
        )
        card_close()

    c1, c2 = st.columns(2)

    with c1:
        exp = df_f["ExperienciaVoluntariado"].value_counts().reset_index()
        exp.columns = ["Experiencia", "Inscritos"]
        exp = exp.sort_values("Inscritos", ascending=False)
        card_open("Experiencia en Voluntariado")
        fig_exp = px.bar(exp, x="Experiencia", y="Inscritos",
                         color_discrete_sequence=["#1a5cff"])
        fig_exp.update_layout(**PLOTLY_BASE, height=320,
                               xaxis_title="", yaxis_title="Inscritos")
        st.plotly_chart(fig_exp, use_container_width=True)
        card_close()

    with c2:
        obj_org = df_f["Objetivo_limpio"].value_counts().reset_index()
        obj_org.columns = ["Objetivo", "Inscritos"]
        obj_org = obj_org.sort_values("Inscritos", ascending=True)
        card_open("Objetivo de la Organización Juvenil")
        st.plotly_chart(
            make_bar_h(obj_org, "Objetivo", "Inscritos", "#e8900a", height=260),
            use_container_width=True,
        )
        card_close()


# ════════════════════════════════════════
# TAB 2 — SOCIOECONÓMICO
# ════════════════════════════════════════
with tab2:

    section("Distribución socioeconómica")
    s1, s2 = st.columns([1, 2])

    with s1:
        estrato_data = (
            df_f["Estrato"].value_counts()
            .sort_index()
            .reset_index()
            .rename(columns={"Estrato": "Estrato", "count": "Cantidad"})
        )
        estrato_data["Estrato"] = estrato_data["Estrato"].astype(str)

        fig_estrato = go.Figure(go.Bar(
            x=estrato_data["Estrato"],
            y=estrato_data["Cantidad"],
            marker_color=COLOR_SEQ[:len(estrato_data)],
            marker_line_width=0,
            text=estrato_data["Cantidad"],
            textposition="outside",
            textfont=dict(size=10, family="DM Mono", color=INK_MID),
            hovertemplate="Estrato %{x}: %{y:,}<extra></extra>",
        ))
        fig_estrato.update_layout(
            **PLOTLY_BASE, showlegend=False, height=290,
            margin=dict(l=4, r=12, t=24, b=8),
            xaxis=dict(title=None, tickfont_size=12, gridcolor=SURFACE),
            yaxis=dict(gridcolor=BORDER, tickfont_size=10),
        )
        card_open("Estrato socioeconómico")
        st.plotly_chart(fig_estrato, use_container_width=True)
        card_close()

    with s2:
        loc_data = (
            df_f["Localidad"].value_counts()
            .reset_index()
            .rename(columns={"Localidad": "Localidad", "count": "Cantidad"})
            .head(12)
        )
        card_open("Localidades")
        st.plotly_chart(
            make_bar_h(loc_data, "Localidad", "Cantidad", ACCENT,
                       height=max(290, len(loc_data) * 36),
                       margin=dict(l=4, r=40, t=8, b=8)),
            use_container_width=True,
        )
        card_close()

    section("Cruce y proporción")
    cr1, cr2 = st.columns([2, 1])

    with cr1:
        if df_f["Genero"].nunique() > 0 and df_f["Estrato"].nunique() > 0:
            cross = (
                df_f.groupby(["Estrato", "Genero"])
                .size()
                .reset_index(name="Cantidad")
            )
            cross["Estrato"] = cross["Estrato"].astype(str)
            fig_cross = px.bar(
                cross, x="Estrato", y="Cantidad", color="Genero",
                barmode="group",
                color_discrete_sequence=[ACCENT, "#93b4fc", SLATE, "#c7d8ff"],
            )
            fig_cross.update_layout(
                **PLOTLY_BASE, showlegend=True, height=290,
                margin=dict(l=4, r=12, t=40, b=8),
                legend=dict(orientation="h", x=0.5, xanchor="center",
                            y=1.22, yanchor="top", font_size=10,
                            font_color=INK_MID, bgcolor="rgba(0,0,0,0)"),
                xaxis=dict(title="Estrato", tickfont_size=12),
                yaxis=dict(gridcolor=BORDER, tickfont_size=10),
            )
            fig_cross.update_traces(marker_line_width=0)
            card_open("Estrato × Género")
            st.plotly_chart(fig_cross, use_container_width=True)
            card_close()

    with cr2:
        card_open("Proporción por estrato")
        st.plotly_chart(
            make_donut(estrato_data["Estrato"].tolist(),
                       estrato_data["Cantidad"].tolist(),
                       COLOR_SEQ[:len(estrato_data)], height=290),
            use_container_width=True,
        )
        card_close()

    # ── Nivel educativo ───────────────────────────────────────────────────
    section("Nivel educativo")

    edu_data = (
        df_f["NivelEducativo"]
        .value_counts()
        .reset_index()
        .rename(columns={"NivelEducativo": "Nivel", "count": "Cantidad"})
    )

    # Orden jerárquico educativo
    orden_edu = [
        "PRIMARIA", "BACHILLERATO", "TECNICO", "TECNOLOGO",
        "UNIVERSITARIO", "ESPECIALIZACION", "MAESTRIA", "DOCTORADO"
    ]
    edu_data["_orden"] = edu_data["Nivel"].apply(
        lambda x: orden_edu.index(x) if x in orden_edu else 99
    )
    edu_data = edu_data.sort_values("_orden").drop(columns="_orden")

    e1, e2 = st.columns([1, 2])

    with e1:
        # Donut de distribución educativa
        card_open("Distribución por nivel educativo")
        st.plotly_chart(
            make_donut(
                edu_data["Nivel"].tolist(),
                edu_data["Cantidad"].tolist(),
                [ACCENT, "#5e8af5", "#93b4fc", "#c7d8ff",
                 AMBER, "#f5b942", GREEN, "#2dd4a0"],
                height=300,
            ),
            use_container_width=True,
        )
        card_close()

    with e2:
        # Barras horizontales ordenadas jerárquicamente
        card_open("Inscritos por nivel educativo")
        fig_edu = go.Figure()

        colores_edu = [
            "#c7d8ff", "#93b4fc", "#5e8af5", "#1a5cff",
            "#f5b942", "#e8900a", "#2dd4a0", "#0f8c5c",
        ]

        for i, row in edu_data.iterrows():
            color_idx = edu_data.index.tolist().index(i) % len(colores_edu)
            fig_edu.add_trace(go.Bar(
                x=[row["Cantidad"]],
                y=[row["Nivel"]],
                orientation="h",
                marker_color=colores_edu[color_idx],
                marker_line_width=0,
                text=[f"  {row['Cantidad']:,}"],
                textposition="outside",
                textfont=dict(size=10, family="DM Mono", color=INK_MID),
                hovertemplate=f"<b>{row['Nivel']}</b>: {row['Cantidad']:,}<extra></extra>",
                showlegend=False,
            ))

        fig_edu.update_layout(
            **PLOTLY_BASE,
            showlegend=False,
            height=max(260, len(edu_data) * 42),
            margin=dict(l=4, r=60, t=8, b=8),
            barmode="overlay",
            yaxis=dict(
                categoryorder="array",
                categoryarray=edu_data["Nivel"].tolist()[::-1],
                tickfont_size=11,
                gridcolor=SURFACE,
            ),
            xaxis=dict(gridcolor=BORDER, tickfont_size=10, showgrid=True),
        )
        st.plotly_chart(fig_edu, use_container_width=True)
        card_close()

    # Cruce NivelEducativo × Género (ancho completo)
    if df_f["Genero"].nunique() > 0 and df_f["NivelEducativo"].nunique() > 0:
        cross_edu = (
            df_f.groupby(["NivelEducativo", "Genero"])
            .size()
            .reset_index(name="Cantidad")
        )
        # Aplicar orden jerárquico
        cross_edu["_orden"] = cross_edu["NivelEducativo"].apply(
            lambda x: orden_edu.index(x) if x in orden_edu else 99
        )
        cross_edu = cross_edu.sort_values("_orden").drop(columns="_orden")

        fig_cross_edu = px.bar(
            cross_edu,
            x="NivelEducativo",
            y="Cantidad",
            color="Genero",
            barmode="group",
            color_discrete_sequence=[ACCENT, "#93b4fc", SLATE, "#c7d8ff"],
            category_orders={"NivelEducativo": edu_data["Nivel"].tolist()},
        )
        fig_cross_edu.update_layout(
            **PLOTLY_BASE,
            showlegend=True,
            height=300,
            margin=dict(l=4, r=12, t=40, b=8),
            legend=dict(
                orientation="h", x=0.5, xanchor="center",
                y=1.18, yanchor="top", font_size=10,
                font_color=INK_MID, bgcolor="rgba(0,0,0,0)",
            ),
            xaxis=dict(title=None, tickfont_size=11, tickangle=-20),
            yaxis=dict(gridcolor=BORDER, tickfont_size=10),
        )
        fig_cross_edu.update_traces(marker_line_width=0)
        card_open("Nivel educativo × Género")
        st.plotly_chart(fig_cross_edu, use_container_width=True)
        card_close()


# ════════════════════════════════════════
# TAB 3 — MAPA
# ════════════════════════════════════════
with tab3:
    modo = st.radio("Modo de visualización", ["Por Barrio", "Por Localidad"], horizontal=True)

    if gdf is not None:
        label_col = "Barrio" if modo == "Por Barrio" else "Localidad"
        conteo = df_f[label_col].value_counts().reset_index()
        conteo.columns = [label_col, "Cantidad"]
        gdf_merge = gdf.merge(conteo, on=label_col, how="left")
        gdf_plot  = gdf_merge[gdf_merge["Cantidad"].notna()]

        fig_map = px.choropleth_mapbox(
            gdf_plot,
            geojson=gdf_plot.__geo_interface__,
            locations=gdf_plot.index,
            color="Cantidad",
            hover_name=label_col,
            hover_data={"Cantidad": True},
            mapbox_style="carto-positron",
            zoom=10,
            center={"lat": 10.98, "lon": -74.80},
            opacity=0.75,
            color_continuous_scale=[[0, "#dce8ff"], [0.5, ACCENT], [1, "#08206c"]],
        )
        fig_map.update_layout(
            paper_bgcolor="#ffffff",
            font_family="DM Sans",
            font_color=INK_MID,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            height=520,
            coloraxis_colorbar=dict(
                thickness=10, len=0.6,
                title=dict(text="Inscritos", font_size=10),
                tickfont_size=10,
            ),
        )
        card_open(f"Distribución geográfica — {modo}")
        st.plotly_chart(fig_map, use_container_width=True)
        card_close()

        if st.checkbox("Mostrar zonas sin coincidencia (debug)"):
            diff = set(df_f[label_col].dropna()) - set(gdf[label_col].dropna())
            if diff:
                st.warning(f"Sin coincidencia en GeoJSON: {', '.join(sorted(diff))}")
            else:
                st.success("Todas las zonas coinciden.")
    else:
        st.info(
            "No se encontró el archivo `barrios.geojson`. "
            "Colócalo en la misma carpeta que este script para activar el mapa."
        )


# ════════════════════════════════════════
# TAB 4 — DATOS
# ════════════════════════════════════════
with tab4:
    section(f"Registros filtrados — {len(df_f):,} filas")

    cols_show = [c for c in [
        "Genero", "Localidad", "Barrio", "Estrato",
        "NivelEducativo", "GruposPoblacionales",
        "MiembroOrganizacionJuvenil", "Edad", "RangoEdad", "Seleccionado",
    ] if c in df_f.columns]

    card_open("Tabla de datos")
    st.dataframe(
        df_f[cols_show].reset_index(drop=True),
        use_container_width=True,
        height=460,
    )
    card_close()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    csv = df_f.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Descargar CSV filtrado",
        data=csv,
        file_name="inscritos_filtrado.csv",
        mime="text/csv",
    )
