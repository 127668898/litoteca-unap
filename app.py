import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. CONFIGURACIÓN DE PÁGINA DE ALTO IMPACTO
st.set_page_config(
    page_title="Litoteca SEG UNAP - Analytics Premium",
    page_icon="👑",
    layout="wide"
)

# Estilo CSS de Nivel Profesional (Paleta SEG: #D4AF37, #111111, #1E1E1E)
st.markdown("""
    <style>
    body {
        background-color: #F8F9FA;
    }
    .main-title {
        font-size:38px !important;
        font-weight: 800;
        color: #D4AF37; 
        text-align: center;
        background: linear-gradient(145deg, #111111, #222222);
        padding: 25px;
        border-radius: 12px 12px 0px 0px;
        margin-bottom: 0px;
        letter-spacing: 3px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    .sub-banner {
        background-color: #D4AF37; 
        color: #111111; 
        padding: 10px;
        text-align: center;
        font-weight: bold;
        border-radius: 0px 0px 12px 12px;
        font-size: 14px;
        margin-bottom: 35px;
        letter-spacing: 1px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .section-title {
        color: #111111;
        border-left: 6px solid #D4AF37;
        padding-left: 12px;
        font-weight: 700;
        font-size: 22px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    /* Tarjetas KPI de Diseñador */
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-top: 4px solid #D4AF37;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.3s;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 6px 18px rgba(212, 175, 55, 0.2);
    }
    .kpi-val {
        font-size: 32px;
        font-weight: 800;
        color: #111111;
        margin: 5px 0;
    }
    .kpi-lbl {
        font-size: 12px;
        text-transform: uppercase;
        color: #666666;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .login-box {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 12px;
        border: 2px solid #D4AF37;
        max-width: 450px;
        margin: 0 auto;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.15);
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado Visual
c1, c2, c3 = st.columns([2, 1, 2])
with c2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)

st.markdown('<div class="main-title">LITOTECA SEG UNAP</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-banner">CONTROL ANALÍTICO INTERACTIVO • REPOSITORIO DE INFORMACIÓN GEOLÓGICA</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SISTEMA DE SEGURIDAD
# ---------------------------------------------------------
USUARIOS_PERMITIDOS = {
    "seg_unap": "SegUnap2026",       
    "admin_litoteca": "UnapMuestras" 
}

def verificar_credenciales():
    u_ingresado = st.session_state.get("input_usuario", "").strip()
    p_ingresada = st.session_state.get("input_password", "").strip()
    if u_ingresado in USUARIOS_PERMITIDOS and USUARIOS_PERMITIDOS[u_ingresado] == p_ingresada:
        st.session_state["autenticado"] = True
    else:
        st.session_state["autenticado"] = False
        st.session_state["intento_fallido"] = True

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "intento_fallido" not in st.session_state:
    st.session_state["intento_fallido"] = False

if not st.session_state["autenticado"]:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #111111; margin-top:0;'>🔐 Panel Reservado</h3>", unsafe_allow_html=True)
    st.caption("Autenticación obligatoria para acceso a base de datos de yacimientos económicos.")
    st.write("")
    st.text_input("Usuario:", key="input_usuario")
    st.text_input("Contraseña:", type="password", key="input_password")
    st.write("")
    st.button("Acceder a la Litoteca", on_click=verificar_credenciales, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state["intento_fallido"]:
        st.write("")
        st.error("❌ Credenciales no válidas.")
    st.stop()

# ---------------------------------------------------------
# 3. PROCESAMIENTO Y CONFIGURACIÓN DE DATOS
# ---------------------------------------------------------
ARCHIVO_EXCEL = "datos_muestras.xlsx"

@st.cache_data
def obtener_nombres_hojas(ruta_excel):
    if os.path.exists(ruta_excel):
        return pd.ExcelFile(ruta_excel).sheet_names
    return []

@st.cache_data
def cargar_datos_hoja(ruta_excel, nombre_hoja):
    if os.path.exists(ruta_excel):
        df = pd.read_excel(ruta_excel, sheet_name=nombre_hoja)
        df.columns = df.columns.astype(str).str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    return pd.DataFrame()

lista_hojas = obtener_nombres_hojas(ARCHIVO_EXCEL)

if lista_hojas:
    col_hoja, _ = st.columns([1, 3])
    with col_hoja:
        hoja_seleccionada = st.selectbox("📂 SELECCIONAR PROYECTO O CAPA O pestaña:", lista_hojas)

    df = cargar_datos_hoja(ARCHIVO_EXCEL, hoja_seleccionada)

    if not df.empty:
        if 'CODIGO DE MUESTRA' in df.columns:
            df_filtrado = df.copy()

            # 4. FILTROS EN BARRA HORIZONTAL COMPACTA
            st.markdown('<h3 class="section-title">🔍 SEGMENTADORES AVANZADOS</h3>', unsafe_allow_html=True)
            
            filtros_actuales = []
            if 'U.M.' in df.columns: filtros_actuales.append('U.M.')
            if 'Tipo de deposito' in df.columns: filtros_actuales.append('Tipo de deposito')
            if 'NOMBRE DEL DONADOR' in df.columns: filtros_actuales.append('NOMBRE DEL DONADOR')
            if 'ESTUDIANTE ENCARGADO' in df.columns: filtros_actuales.append('ESTUDIANTE ENCARGADO')
            
            if filtros_actuales:
                columnas_filtros = st.columns(len(filtros_actuales))
                for idx, col_name in enumerate(filtros_actuales):
                    with columnas_filtros[idx]:
                        if col_name == 'U.M.':
                            opciones = ["Todas"] + list(df['U.M.'].dropna().unique())
                            sel_um = st.selectbox("⛏️ Unidad Minera", opciones)
                            if sel_um != "Todas":
                                df_filtrado = df_filtrado[df_filtrado['U.M.'] == sel_um]
                        elif col_name == 'Tipo de deposito':
                            opciones = ["Todos"] + list(df['Tipo de deposito'].dropna().unique())
                            sel_dep = st.selectbox("🌋 Tipo de Depósito", opciones)
                            if sel_dep != "Todos":
                                df_filtrado = df_filtrado[df_filtrado['Tipo de deposito'] == sel_dep]
                        elif col_name == 'NOMBRE DEL DONADOR':
                            opciones = ["Todos"] + list(df['NOMBRE DEL DONADOR'].dropna().unique())
                            sel_don = st.selectbox("🤝 Donante de Muestra", opciones)
                            if sel_don != "Todos":
                                df_filtrado = df_filtrado[df_filtrado['NOMBRE DEL DONADOR'] == sel_don]
                        elif col_name == 'ESTUDIANTE ENCARGADO':
                            opciones = ["Todos"] + list(df['ESTUDIANTE ENCARGADO'].dropna().unique())
                            sel_est = st.selectbox("🎓 Estudiante Responsable", opciones)
                            if sel_est != "Todos":
                                df_filtrado = df_filtrado[df_filtrado['ESTUDIANTE ENCARGADO'] == sel_est]

            # 5. BLOQUE DE TARJETAS DE MÉTRICAS (KPI CARDS) - ESTILO PREMIUM
            st.write("")
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            
            total_m = len(df_filtrado)
            minas_m = df_filtrado['U.M.'].nunique() if 'U.M.' in df_filtrado.columns else 0
            yac_m = df_filtrado['Tipo de deposito'].nunique() if 'Tipo de deposito' in df_filtrado.columns else 0
            cajas_m = df_filtrado['NRO DE CAJA'].nunique() if 'NRO DE CAJA' in df_filtrado.columns else 0

            with kpi_col1:
                st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Muestras Filtradas</div><div class="kpi-val">{total_m}</div></div>', unsafe_allow_html=True)
            with kpi_col2:
                st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Unidades Mineras</div><div class="kpi-val">{minas_m}</div></div>', unsafe_allow_html=True)
            with kpi_col3:
                st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Modelos de Depósito</div><div class="kpi-val">{yac_m}</div></div>', unsafe_allow_html=True)
            with kpi_col4:
                st.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Cajas en Litoteca</div><div class="kpi-val">{cajas_m}</div></div>', unsafe_allow_html=True)

            # 6. CONFIGURACIÓN GRÁFICA INTERACTIVA DE ALTO RENDIMIENTO
            st.markdown('<h3 class="section-title">📊 DIAGRAMAS Y DISTRIBUCIONES GEOLÓGICAS</h3>', unsafe_allow_html=True)
            
            if not df_filtrado.empty:
                g1, g2 = st.columns(2)
                
                with g1:
                    if 'Tipo de deposito' in df_filtrado.columns and df_filtrado['Tipo de deposito'].dropna().any():
                        conteo = df_filtrado['Tipo de deposito'].value_counts().reset_index()
                        conteo.columns = ['Tipo de deposito', 'Cantidad']
                        
                        # Gráfico de Donut Avanzado con diseño limpio
                        fig_torta = go.Figure(data=[go.Pie(
                            labels=conteo['Tipo de deposito'], 
                            values=conteo['Cantidad'], 
                            hole=.5,
                            hoverinfo="label+percent+value",
                            textinfo="value",
                            marker=dict(colors=['#D4AF37', '#1A1A1A', '#4A4A4A', '#8E761D', '#C0C0C0'], 
                                        line=dict(color='#FFFFFF', width=2))
                        )])
                        
                        fig_torta.update_layout(
                            title_text="Clasificación de Yacimientos e Alteraciones",
                            title_font=dict(size=16, font_family="Arial", color="#111111"),
                            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                            margin=dict(t=50, b=40, l=10, r=10),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig_torta, use_container_width=True)
                        
                with g2:
                    if 'EMPRESA' in df_filtrado.columns and df_filtrado['EMPRESA'].dropna().any():
                        conteo = df_filtrado['EMPRESA'].value_counts().reset_index()
                        conteo.columns = ['EMPRESA', 'Cantidad']
                        
                        # Gráfico de Barras Avanzado
                        fig_barras = go.Figure(data=[go.Bar(
                            x=conteo['EMPRESA'],
                            y=conteo['Cantidad'],
                            text=conteo['Cantidad'],
                            textposition='auto',
                            marker_color='#D4AF37',
                            hoverinfo="x+y",
                            marker_line=dict(color='#111111', width=1)
                        )])
                        
                        fig_barras.update_layout(
                            title_text="Muestras Aportadas por Compañías Mineras",
                            title_font=dict(size=16, font_family="Arial", color="#111111"),
                            margin=dict(t=50, b=40, l=20, r=20),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            xaxis=dict(showgrid=False, title="Compañía / Origen"),
                            yaxis=dict(showgrid=True, gridcolor='#EFEFEF', title="N° de Rocas")
                        )
                        st.plotly_chart(fig_barras, use_container_width=True)

            st.write("---")

            # 7. MATRIZ DE DATOS Y VISOR MULTIMEDIA
            col_tabla, col_foto = st.columns([2, 1])
            with col_tabla:
                st.markdown(f'<h4 class="section-title">📋 MATRIZ DE REGISTROS DE CAMPO</h4>', unsafe_allow_html=True)
                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                
            with col_foto:
                st.markdown('<h4 class="section-title">📸 VISOR MULTIMEDIA DE ROCAS</h4>', unsafe_allow_html=True)
                codigos_disponibles = df_filtrado['CODIGO DE MUESTRA'].dropna().unique()
                if len(codigos_disponibles) > 0:
                    id_sel = st.selectbox("Seleccionar Código Analizado:", codigos_disponibles)
                    
                    fila = df_filtrado[df_filtrado['CODIGO DE MUESTRA'] == id_sel].iloc[0]
                    um_text = fila['U.M.'] if 'U.M.' in df_filtrado.columns else "N/A"
                    desc_text = fila['Descripcion'] if 'Descripcion' in df_filtrado.columns else "N/A"
                    
                    st.info(f"📍 **U.M.:** {um_text} \n\n 🔬 **Descripción Visual:** {desc_text}")
                    
                    ruta_jpg = f"fotos/{id_sel}.jpg"
                    ruta_png = f"fotos/{id_sel}.png"
                    
                    if os.path.exists(ruta_jpg):
                        st.image(ruta_jpg, caption=f"Muestra de mano: {id_sel}", use_container_width=True)
                    elif os.path.exists(ruta_png):
                        st.image(ruta_png, caption=f"Muestra de mano: {id_sel}", use_container_width=True)
        else:
            # Vista Estilizada para Hojas de Texto (Logueos individuales como Casapalca)
            st.markdown(f'<h4 class="section-title">📄 REPORTE GEOLÓGICO DE DETALLE: {hoja_seleccionada.upper()}</h4>', unsafe_allow_html=True)
            
            tab_tarjetas, tab_tabla = st.tabs(["🗂️ Vista Dinámica Estructurada", "📊 Hoja de Cálculo Original"])
            
            with tab_tarjetas:
                for index, row in df.iterrows():
                    celdas_validas = [str(val) for val in row if pd.notna(val) and str(val).strip() != ""]
                    if celdas_validas:
                        with st.expander(f"🔹 Registro Descriptivo (Sección {index + 1})", expanded=(index < 5)):
                            cols = st.columns(len(celdas_validas))
                            for i, texto in enumerate(celdas_validas):
                                with cols[i]:
                                    st.markdown(f"<div style='background-color:#ffffff; color:#111111; padding:15px; border-left: 4px solid #D4AF37; border-radius:5px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); font-size: 13px; font-family: monospace; white-space: pre-wrap;'>{texto}</div>", unsafe_allow_html=True)
                                    
            with tab_tabla:
                st.dataframe(df, use_container_width=True)
