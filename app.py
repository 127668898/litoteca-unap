import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE PÁGINA (Identidad Visual SEG UNAP)
st.set_page_config(
    page_title="Litoteca SEG UNAP - Privado",
    page_icon="🔒",
    layout="wide"
)

# Paleta de Colores Extraída del Logo (logo.jpg)
# Azul Principal: #1A3E62
# Dorado Acento: #DAA520 (Goldenrod académico)
# Fondo: #FFFFFF (Blanco Puro)

# Estilo CSS Avanzado (Limpieza, Contraste y Profesionalismo)
st.markdown("""
    <style>
    /* Fondo General Blanco Puro para limpieza absoluta */
    .stApp {
        background-color: #FFFFFF;
    }
    
    .main-title {
        font-size:36px !important;
        font-weight: bold;
        color: #DAA520; /* Dorado para el texto principal */
        text-align: center;
        background-color: #1A3E62; /* Azul Real Profundo del logo de fondo */
        padding: 20px;
        border-radius: 10px 10px 0px 0px;
        margin-bottom: 0px;
        letter-spacing: 2px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .sub-banner {
        background-color: #DAA520; /* Dorado del logo */
        color: #FFFFFF; /* Texto Blanco para contraste */
        padding: 8px;
        text-align: center;
        font-weight: bold;
        border-radius: 0px 0px 10px 10px;
        font-size: 15px;
        margin-bottom: 30px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }
    .section-title {
        color: #1A3E62; /* Azul del logo para títulos */
        border-left: 5px solid #DAA520; /* Acento Dorado */
        padding-left: 10px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .login-box {
        background-color: #FFFFFF; /* Caja Blanca */
        padding: 30px;
        border-radius: 12px;
        border: 2px solid #1A3E62; /* Borde Azul */
        max-width: 450px;
        margin: 0 auto;
        box-shadow: 0px 8px 20px rgba(26, 62, 98, 0.15); /* Sombra Azulada */
    }
    
    /* Estilo para inputs de login */
    .stTextInput>div>div>input {
        border-color: #1A3E62;
    }
    .stTextInput>div>div>input:focus {
        border-color: #DAA520;
        box-shadow: 0 0 0 0.2rem rgba(218, 165, 32, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

# Carga de Logo Institucional (Prioridad a logo.jpg)
c1, c2, c3 = st.columns([2, 1, 2])
with c2:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", use_container_width=True)
    elif os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

st.markdown('<div class="main-title">LITOTECA SEG UNAP</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-banner">SOCIETY OF ECONOMIC GEOLOGISTS • CONTROL DE ACCESO</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SISTEMA DE SEGURIDAD (Mantiene tus 4 Usuarios Activos)
# ---------------------------------------------------------
USUARIOS_PERMITIDOS = {
    "seg_unap": "SegUnap2026",  # Usuario General
    "mayersyerson17@gmail.com": "927685",        # Directiva 1
    "richardcoaquiraapaza@gmail.com": "925371",       # Directiva 2
    "carbajaljuancarlos194@gmail.com": "927700"    # Directiva 3
}

def verificar_credenciales():
    u_ingresado = st.session_state.get("input_usuario", "").strip()
    p_ingresada = st.session_state.get("input_password", "").strip()
    
    if u_ingresado in USUARIOS_PERMITIDOS and USUARIOS_PERMITIDOS[u_ingresado] == p_ingresada:
        st.session_state["autenticado"] = True
    else:
        st.session_state["autenticado"] = False
        st.session_state["intento_fallido"] = True

# Inicialización de estado de sesión
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "intento_fallido" not in st.session_state:
    st.session_state["intento_fallido"] = False

# Muro de Login (Estilizado)
if not st.session_state["autenticado"]:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #1A3E62; margin-top:0;'>🔐 Iniciar Sesión</h3>", unsafe_allow_html=True)
    st.caption("Plataforma restringida para miembros autorizados de la directiva SEG UNAP.")
    st.write("")
    
    st.text_input("Usuario (Email):", key="input_usuario")
    st.text_input("Contraseña (DNI):", type="password", key="input_password")
    st.write("")
    
    st.button("Ingresar al Sistema", on_click=verificar_credenciales, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state["intento_fallido"]:
        st.write("")
        st.error("❌ Credenciales incorrectas. Verifique su email o DNI.")
    
    st.stop() # Detiene la carga del resto de la página
# ---------------------------------------------------------

# =========================================================
# CONTENIDO PRIVADO (SOLO ACCESIBLE TRAS LOGIN)
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
        # Limpieza estándar
        df.columns = df.columns.astype(str).str.strip()
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    return pd.DataFrame()

lista_hojas = obtener_nombres_hojas(ARCHIVO_EXCEL)

if lista_hojas:
    # Selector de Pestaña Principal (Estilizado)
    col_hoja, _ = st.columns([1, 3])
    with col_hoja:
        hoja_seleccionada = st.selectbox("📂 PESTAÑA ACTIVA (Proyecto):", lista_hojas)

    df = cargar_datos_hoja(ARCHIVO_EXCEL, hoja_seleccionada)

    if not df.empty:
        # Validación: Si contiene datos tabulares estructurados (Base de Datos Principal)
        if 'CODIGO DE MUESTRA' in df.columns:
            df_filtrado = df.copy()

            # 3. FILTROS DINÁMICOS INTELIGENTES (Estilo Azul/Dorado)
            st.markdown('<h3 class="section-title">🔍 FILTROS Y SEGMENTADORES DE BASE DE DATOS</h3>', unsafe_allow_html=True)
            
            filtros_actuales = []
            # Detectar qué columnas de filtro existen en esta pestaña
            if 'U.M.' in df.columns: filtros_actuales.append('U.M.')
            if 'Tipo de deposito' in df.columns: filtros_actuales.append('Tipo de deposito')
            if 'NOMBRE DEL DONADOR' in df.columns: filtros_actuales.append('NOMBRE DEL DONADOR')
            if 'ESTUDIANTE ENCARGADO' in df.columns: filtros_actuales.append('ESTUDIANTE ENCARGADO')
            
            # Crear columnas de filtros dinámicamente
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

            st.metric("TOTAL REGISTROS FILTRADOS", len(df_filtrado))
            st.write("---")

            # 4. DIAGRAMAS ESTADÍSTICOS INTERACTIVOS (Nueva Paleta Azul/Oro)
            st.markdown('<h3 class="section-title">📊 DIAGRAMAS GEOLÓGICOS INTERACTIVOS</h3>', unsafe_allow_html=True)
            
            if not df_filtrado.empty:
                g1, g2 = st.columns(2)
                
                with g1:
                    if 'Tipo de deposito' in df_filtrado.columns and df_filtrado['Tipo de deposito'].dropna().any():
                        conteo = df_filtrado['Tipo de deposito'].value_counts().reset_index()
                        conteo.columns = ['Tipo de deposito', 'Cantidad']
                        # Gráfico de Donut Estilizado
                        fig_torta = px.pie(
                            conteo, values='Cantidad', names='Tipo de deposito', 
                            title="Distribución por Tipo de Depósito",
                            color_discrete_sequence=['#1A3E62', '#DAA520', '#4A6B8F', '#F0C96A', '#CCCCCC'],
                            hole=0.4
                        )
                        fig_torta.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(fig_torta, use_container_width=True)
                        
                with g2:
                    if 'EMPRESA' in df_filtrado.columns and df_filtrado['EMPRESA'].dropna().any():
                        conteo = df_filtrado['EMPRESA'].value_counts().reset_index()
                        conteo.columns = ['EMPRESA', 'Cantidad']
                        # Gráfico de Barras Estilizado
                        fig_barras = px.bar(
                            conteo, x='EMPRESA', y='Cantidad', 
                            title="Muestras por Empresa",
                            text_auto=True, color_discrete_sequence=['#1A3E62'] # Azul para barras
                        )
                        fig_barras.update_traces(marker_line_color='#DAA520', marker_line_width=1, opacity=0.9)
                        st.plotly_chart(fig_barras, use_container_width=True)

            st.write("---")

            # 5. MATRIZ DE REGISTROS Y VISOR MULTIMEDIA
            col_tabla, col_foto = st.columns([2, 1])
            with col_tabla:
                st.markdown(f'<h4 class="section-title">📋 MATRIZ DE DATOS (Filtrada)</h4>', unsafe_allow_html=True)
                # Ocultamos el índice para limpieza
                st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                
            with col_foto:
                st.markdown('<h4 class="section-title">📸 VISOR DE MUESTRA FISICA</h4>', unsafe_allow_html=True)
                # Obtenemos solo los códigos que sobrevivieron a los filtros
                codigos_disponibles = df_filtrado['CODIGO DE MUESTRA'].dropna().unique()
                if len(codigos_disponibles) > 0:
                    id_sel = st.selectbox("Seleccionar Código Analizado:", codigos_disponibles)
                    
                    # Extraer info de la fila seleccionada
                    fila = df_filtrado[df_filtrado['CODIGO DE MUESTRA'] == id_sel].iloc[0]
                    um_text = fila['U.M.'] if 'U.M.' in df_filtrado.columns else "N/A"
                    desc_text = fila['Descripcion'] if 'Descripcion' in df_filtrado.columns else "N/A"
                    
                    # Mostrar info descriptiva
                    st.info(f"**U.M.:** {um_text} \n\n **Descripción Visual:** {desc_text}")
                    
                    # Buscador de Fotos (soporta JPG o PNG con el nombre del código)
                    ruta_jpg = f"fotos/{id_sel}.jpg"
                    ruta_png = f"fotos/{id_sel}.png"
                    
                    if os.path.exists(ruta_jpg):
                        st.image(ruta_jpg, caption=f"Muestra de mano: {id_sel}", use_container_width=True)
                    elif os.path.exists(ruta_png):
                        st.image(ruta_png, caption=f"Muestra de mano: {id_sel}", use_container_width=True)
        else:
            # =========================================================
            # 6. NUEVA VISTA DINÁMICA PARA LOGUEOS (CASAPALCA, SINA, ETC)
            # =========================================================
            # Si entras a una pestaña tipo reporte de texto o formato de logueo
            st.markdown(f'<h4 class="section-title">📄 REPORTE GEOLÓGICO DE LOGUEO: {hoja_seleccionada.upper()}</h4>', unsafe_allow_html=True)
            
            # Pestañas interactivas para elegir visualización
            tab_tarjetas, tab_tabla = st.tabs(["🗂️ Vista Dinámica (Tarjetas Monospace)", "📊 Vista Original (Excel Tabla)"])
            
            with tab_tarjetas:
                st.info("💡 Exploración interactiva de logueos geológicos. Se han omitido los espacios vacíos y se usa fuente 'Monospace' para respetar la alineación original de descripciones técnicas.")
                
                # Recorremos cada fila del Excel (Logueo individual)
                for index, row in df.iterrows():
                    # Extraemos solo las celdas que realmente tienen texto (ignoramos los NaN)
                    celdas_validas = [str(val) for val in row if pd.notna(val) and str(val).strip() != ""]
                    
                    if celdas_validas:
                        # Creamos un menú desplegable (expander) por cada bloque de información
                        # expanded=(index < 7) abre los primeros registros por defecto
                        with st.expander(f"🔹 Bloque de Registro Técnicos (Fila Excel {index + 1})", expanded=(index < 7)):
                            # Distribuimos la información en columnas automáticas según la cantidad de datos
                            cols = st.columns(len(celdas_validas))
                            for i, texto in enumerate(celdas_validas):
                                with cols[i]:
                                    # Mantenemos los saltos de línea originales (\n) y aplicamos diseño Monospace SEG (Dorado/Azul)
                                    # Diseño Premium de Tarjeta
                                    st.markdown(f"""
                                    <div style='background-color:#ffffff; color:#111111; padding:15px; border-left: 4px solid #1A3E62; border-radius:5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-size: 13px; font-family: monospace; white-space: pre-wrap;'>
                                        {texto}
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
            with tab_tabla:
                # Muestra la hoja de cálculo cruda si el usuario prefiere
                st.dataframe(df, use_container_width=True)
