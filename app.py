import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Litoteca SEG UNAP - Privado",
    page_icon="🔒",
    layout="wide"
)

# Estilo CSS Avanzado SEG (Verde Institucional y Dorado)
st.markdown("""
    <style>
    .main-title {
        font-size:36px !important;
        font-weight: bold;
        color: #D4AF37; 
        text-align: center;
        background-color: #0B4F3A; 
        padding: 20px;
        border-radius: 10px 10px 0px 0px;
        margin-bottom: 0px;
        letter-spacing: 2px;
    }
    .sub-banner {
        background-color: #D4AF37; 
        color: #0B4F3A; 
        padding: 8px;
        text-align: center;
        font-weight: bold;
        border-radius: 0px 0px 10px 10px;
        font-size: 15px;
        margin-bottom: 30px;
    }
    .section-title {
        color: #0B4F3A;
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
        border: 2px solid #0B4F3A;
        max-width: 450px;
        margin: 0 auto;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Carga de Logo Institucional
c1, c2, c3 = st.columns([2, 1, 2])
with c2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)

st.markdown('<div class="main-title">LITOTECA SEG UNAP</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-banner">SOCIETY OF ECONOMIC GEOLOGISTS • CONTROL DE ACCESO</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SISTEMA DE SEGURIDAD (4 Usuarios Autorizados)
# ---------------------------------------------------------
USUARIOS_PERMITIDOS = {
    "seg_unap": "SegUnap2026",  # Usuario 1
    "mayersyerson17@gmail.com": "927685",        # Usuario 2
    "richardcoaquiraapaza@gmail.com": "925371",       # Usuario 3
    "carbajaljuancarlos194@gmail.com": "927700"    # Usuario 4
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
    st.markdown("<h3 style='text-align: center; color: #0B4F3A;'>🔐 Iniciar Sesión</h3>", unsafe_allow_html=True)
    st.caption("Plataforma restringida para personal autorizado.")
    st.write("")
    
    st.text_input("Usuario:", key="input_usuario")
    st.text_input("Contraseña:", type="password", key="input_password")
    st.write("")
    
    st.button("Ingresar al Sistema", on_click=verificar_credenciales, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state["intento_fallido"]:
        st.write("")
        st.error("❌ Credenciales incorrectas.")
    
    st.stop()
# ---------------------------------------------------------

# =========================================================
# CONTENIDO PRIVADO 
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
        df.columns = df.columns.astype(str).str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    return pd.DataFrame()

lista_hojas = obtener_nombres_hojas(ARCHIVO_EXCEL)

if lista_hojas:
    col_hoja, _ = st.columns([1, 3])
    with col_hoja:
        hoja_seleccionada = st.selectbox("📂 PESTAÑA ACTIVA:", lista_hojas)

    df = cargar_datos_hoja(ARCHIVO_EXCEL, hoja_seleccionada)

    if not df.empty:
        if 'CODIGO DE MUESTRA' in df.columns:
            df_filtrado = df.copy()

            st.markdown('<h3 class="section-title">🔍 FILTROS Y SEGMENTADORES</h3>', unsafe_allow_html=True)
            
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
                            sel_um = st.selectbox("⛏️ U.M. (Unidad Minera):", opciones)
                            if sel_um != "Todas":
                                df_filtrado = df_filtrado[df_filtrado['U.M.'] == sel_um]
                        elif col_name == 'Tipo de deposito':
                            opciones = ["Todos"] + list(df['Tipo de deposito'].dropna().unique())
                            sel_dep = st.selectbox("🌋 TIPO DE DEPÓSITO:", opciones)
                            if sel_dep != "Todos":
                                df_filtrado = df_filtrado[df_filtrado['Tipo de deposito'] == sel_dep]
                        elif col_name == 'NOMBRE DEL DONADOR':
                            opciones = ["Todos"] + list(df['NOMBRE DEL DONADOR'].dropna().unique())
                            sel_don = st.selectbox("🤝 DONADOR:", opciones)
                            if sel_don != "Todos":
                                df_filtrado = df_filtrado[df_filtrado['NOMBRE DEL DONADOR'] == sel_don]
                        elif col_name == 'ESTUDIANTE ENCARGADO':
                            opciones = ["Todos"] + list(df['ESTUDIANTE ENCARGADO'].dropna().unique())
                            sel_est = st.selectbox("🎓 ENCARGADO:", opciones)
                            if sel_est != "Todos":
                                df_filtrado = df_filtrado[df_filtrado['ESTUDIANTE ENCARGADO'] == sel_est]

            st.metric("TOTAL REGISTROS", len(df_filtrado))
            st.write("---")

            st.markdown('<h3 class="section-title">📊 DIAGRAMAS INTERACTIVOS</h3>', unsafe_allow_html=True)
            
            if not df_filtrado.empty:
                g1, g2 = st.columns(2)
                
                with g1:
                    if 'Tipo de deposito' in df_filtrado.columns and df_filtrado['Tipo de deposito'].dropna().any():
                        conteo = df_filtrado['Tipo de deposito'].value_counts().reset_index()
                        conteo.columns = ['Tipo de deposito', 'Cantidad']
                        fig_torta = px.pie(
                            conteo, values='Cantidad', names='Tipo de deposito', 
                            title="Distribución por Tipo de Depósito",
                            color_discrete_sequence=['#0B4F3A', '#D4AF37', '#1E7B58', '#E6C259', '#708090']
                        )
                        st.plotly_chart(fig_torta, use_container_width=True)
                        
                with g2:
                    if 'EMPRESA' in df_filtrado.columns and df_filtrado['EMPRESA'].dropna().any():
                        conteo = df_filtrado['EMPRESA'].value_counts().reset_index()
                        conteo.columns = ['EMPRESA', 'Cantidad']
                        fig_barras = px.bar(
                            conteo, x='EMPRESA', y='Cantidad', 
                            title="Muestras por Empresa",
                            text_auto=True, color_discrete_sequence=['#0B4F3A']
                        )
                        st.plotly_chart(fig_barras, use_container_width=True)

            st.write("---")

            col_tabla, col_foto = st.columns([2, 1])
            with col_tabla:
                st.markdown(f'<h4 class="section-title">📋 MATRIZ DE DATOS</h4>', unsafe_allow_html=True)
                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                
            with col_foto:
                st.markdown('<h4 class="section-title">📸 VISOR DE MUESTRA</h4>', unsafe_allow_html=True)
                codigos_disponibles = df_filtrado['CODIGO DE MUESTRA'].dropna().unique()
                if len(codigos_disponibles) > 0:
                    id_sel = st.selectbox("Seleccionar Código:", codigos_disponibles)
                    
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
            # =========================================================
            # 6. NUEVA VISTA DINÁMICA PARA LOGUEOS (CASAPALCA, SINA, ETC)
            # =========================================================
            st.markdown(f'<h4 class="section-title">📄 REPORTE DE LOGUEO: {hoja_seleccionada.upper()}</h4>', unsafe_allow_html=True)
            
            tab_tarjetas, tab_tabla = st.tabs(["🗂️ Vista Dinámica (Tarjetas)", "📊 Vista Original (Excel)"])
            
            with tab_tarjetas:
                st.info("💡 Exploración interactiva. Se han omitido los espacios vacíos para una lectura limpia de las descripciones.")
                
                for index, row in df.iterrows():
                    celdas_validas = [str(val) for val in row if pd.notna(val) and str(val).strip() != ""]
                    
                    if celdas_validas:
                        with st.expander(f"🔹 Registro de Datos (Fila {index + 1})", expanded=(index < 7)):
                            cols = st.columns(len(celdas_validas))
                            for i, texto in enumerate(celdas_validas):
                                with cols[i]:
                                    st.markdown(f"<div style='background-color:#ffffff; color:#111111; padding:15px; border-left: 4px solid #0B4F3A; border-radius:5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-size: 13px; font-family: monospace; white-space: pre-wrap;'>{texto}</div>", unsafe_allow_html=True)
                                    
            with tab_tabla:
                st.dataframe(df, use_container_width=True)
