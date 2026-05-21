import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE PÁGINA (Debe ser la primera línea)
st.set_page_config(
    page_title="Litoteca SEG UNAP - Privado",
    page_icon="🔒",
    layout="wide"
)

# Estilo CSS Avanzado SEG
st.markdown("""
    <style>
    .main-title {
        font-size:36px !important;
        font-weight: bold;
        color: #D4AF37; 
        text-align: center;
        background-color: #111111; 
        padding: 20px;
        border-radius: 10px 10px 0px 0px;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
    .sub-banner {
        background-color: #D4AF37; 
        color: #111111; 
        padding: 8px;
        text-align: center;
        font-weight: bold;
        border-radius: 0px 0px 10px 10px;
        font-size: 15px;
        margin-bottom: 30px;
    }
    .section-title {
        color: #111111;
        border-left: 5px solid #D4AF37;
        padding-left: 10px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .login-box {
        background-color: #f4f4f4;
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #D4AF37;
        text-align: center;
        max-width: 500px;
        margin: 0 auto;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">LITOTECA SEG UNAP</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-banner">SOCIETY OF ECONOMIC GEOLOGISTS • ACCESO RESTRINGIDO</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SISTEMA DE SEGURIDAD Y LOGIN
# ---------------------------------------------------------
# Aquí defines tu contraseña secreta
CONTRASENA_SECRETA = "SegUnap2026" 

def verificar_contrasena():
    """Devuelve True si el usuario ingresó la contraseña correcta."""
    if st.session_state.get("password", "") == CONTRASENA_SECRETA:
        st.session_state["autenticado"] = True
    else:
        st.session_state["autenticado"] = False

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.warning("🔒 **Plataforma Confidencial.** Por favor, ingrese la contraseña de acceso proporcionada por la directiva.")
    st.text_input("Contraseña:", type="password", key="password", on_change=verificar_contrasena)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.get("password", "") != "" and st.session_state.get("password", "") != CONTRASENA_SECRETA:
        st.error("❌ Contraseña incorrecta. Acceso denegado.")
    
    # st.stop() detiene el código aquí. Nada de lo que está abajo se ejecuta ni se envía al navegador.
    st.stop()
# ---------------------------------------------------------


# =========================================================
# A PARTIR DE AQUÍ SOLO LLEGAN LOS USUARIOS AUTENTICADOS
# =========================================================

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
        df.columns = df.columns.str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    return pd.DataFrame()

lista_hojas = obtener_nombres_hojas(ARCHIVO_EXCEL)

col_hoja, _ = st.columns([1, 3])
with col_hoja:
    hoja_seleccionada = st.selectbox("📂 PESTAÑA DEL EXCEL:", lista_hojas)

df = cargar_datos_hoja(ARCHIVO_EXCEL, hoja_seleccionada)

if df.empty:
    st.error(f"❌ No se pudo leer la hoja o está vacía.")
else:
    if 'CODIGO DE MUESTRA' in df.columns:
        df_filtrado = df.copy()

        st.markdown('<h3 class="section-title">🔍 FILTROS Y SEGMENTADORES</h3>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            if 'U.M.' in df.columns:
                opciones = ["Todas"] + list(df['U.M.'].dropna().unique())
                sel_um = st.selectbox("⛏️ U.M. (Unidad Minera):", opciones)
                if sel_um != "Todas":
                    df_filtrado = df_filtrado[df_filtrado['U.M.'] == sel_um]

        with c2:
            if 'Tipo de deposito' in df.columns:
                opciones = ["Todos"] + list(df['Tipo de deposito'].dropna().unique())
                sel_dep = st.selectbox("🌋 TIPO DE DEPÓSITO:", opciones)
                if sel_dep != "Todos":
                    df_filtrado = df_filtrado[df_filtrado['Tipo de deposito'] == sel_dep]

        with c3:
            if 'NOMBRE DEL DONADOR' in df.columns:
                opciones = ["Todos"] + list(df['NOMBRE DEL DONADOR'].dropna().unique())
                sel_don = st.selectbox("🤝 DONADOR:", opciones)
                if sel_don != "Todos":
                    df_filtrado = df_filtrado[df_filtrado['NOMBRE DEL DONADOR'] == sel_don]

        with c4:
            if 'ESTUDIANTE ENCARGADO' in df.columns:
                opciones = ["Todos"] + list(df['ESTUDIANTE ENCARGADO'].dropna().unique())
                sel_est = st.selectbox("🎓 ESTUDIANTE ENCARGADO:", opciones)
                if sel_est != "Todos":
                    df_filtrado = df_filtrado[df_filtrado['ESTUDIANTE ENCARGADO'] == sel_est]

        st.metric("TOTAL MUESTRAS FILTRADAS", len(df_filtrado))
        st.write("---")

        st.markdown('<h3 class="section-title">📊 DIAGRAMAS INTERACTIVOS</h3>', unsafe_allow_html=True)
        
        if not df_filtrado.empty:
            g1, g2 = st.columns(2)
            
            with g1:
                if 'Tipo de deposito' in df_filtrado.columns:
                    conteo = df_filtrado['Tipo de deposito'].value_counts().reset_index()
                    conteo.columns = ['Tipo de deposito', 'Cantidad']
                    fig_torta = px.pie(
                        conteo, values='Cantidad', names='Tipo de deposito', 
                        title="Distribución por Tipo de Depósito",
                        color_discrete_sequence=['#D4AF37', '#222222', '#555555', '#AA8822', '#CCCCCC']
                    )
                    st.plotly_chart(fig_torta, use_container_width=True)
                    
            with g2:
                if 'EMPRESA' in df_filtrado.columns:
                    conteo = df_filtrado['EMPRESA'].value_counts().reset_index()
                    conteo.columns = ['EMPRESA', 'Cantidad']
                    fig_barras = px.bar(
                        conteo, x='EMPRESA', y='Cantidad', 
                        title="Muestras por Empresa",
                        text_auto=True, color_discrete_sequence=['#D4AF37']
                    )
                    st.plotly_chart(fig_barras, use_container_width=True)

        st.write("---")

        col_tabla, col_foto = st.columns([2, 1])
        with col_tabla:
            st.markdown(f'<h4 class="section-title">📋 REGISTROS</h4>', unsafe_allow_html=True)
            st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
            
        with col_foto:
            st.markdown('<h4 class="section-title">📸 VISOR DE MUESTRA</h4>', unsafe_allow_html=True)
            codigos_disponibles = df_filtrado['CODIGO DE MUESTRA'].dropna().unique()
            if len(codigos_disponibles) > 0:
                id_sel = st.selectbox("Seleccionar CODIGO DE MUESTRA:", codigos_disponibles)
                
                fila = df_filtrado[df_filtrado['CODIGO DE MUESTRA'] == id_sel].iloc[0]
                um_text = fila['U.M.'] if 'U.M.' in df_filtrado.columns else "N/A"
                desc_text = fila['Descripcion'] if 'Descripcion' in df_filtrado.columns else "N/A"
                
                st.info(f"**U.M.:** {um_text} \n\n **Descripción:** {desc_text}")
                
                ruta_jpg = f"fotos/{id_sel}.jpg"
                ruta_png = f"fotos/{id_sel}.png"
                
                if os.path.exists(ruta_jpg):
                    st.image(ruta_jpg, caption=f"Muestra {id_sel}", use_container_width=True)
                elif os.path.exists(ruta_png):
                    st.image(ruta_png, caption=f"Muestra {id_sel}", use_container_width=True)
                else:
                    st.caption(f"ℹ️ Guarda la foto de esta roca como `{id_sel}.jpg` en tu carpeta 'fotos'.")
    else:
        st.warning("⚠️ Esta pestaña contiene un Formato de Reporte (Logueo) o Resumen, no una tabla estructurada de base de datos. Se mostrará en formato crudo a continuación.")
        st.dataframe(df, use_container_width=True)
