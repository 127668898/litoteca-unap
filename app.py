import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Portal SEG UNAP",
    page_icon="⚒️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. MOTOR CSS AVANZADO (Minimalismo y Animaciones)
st.markdown("""
    <style>
    /* Fondo General Blanco Puro y fuente limpia */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Animación de entrada suave (Fade In Up) */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Aplicar animación a los contenedores principales */
    .block-container {
        padding-top: 2.5rem !important;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* ---------------------------------------------------
       ENCABEZADO MINIMALISTA
       --------------------------------------------------- */
    .header-title {
        color: #002855;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-top: 25px; 
        margin-bottom: 0px;
        padding-bottom: 0px;
        line-height: 1.1;
    }
    .header-subtitle {
        color: #98793E;
        font-size: 15px;
        font-weight: 500;
        margin-top: 5px;
    }
    
    /* ---------------------------------------------------
       PESTAÑAS (TABS) ELEGANTES Y ANIMADAS
       --------------------------------------------------- */
    div[data-testid="stTabs"] {
        margin-top: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 1px solid #E0E0E0;
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #666666 !important;
        font-size: 16px;
        font-weight: 500;
        padding: 10px 5px;
        border: none;
        background-color: transparent !important;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #002855 !important;
        transform: translateY(-2px);
    }
    .stTabs [aria-selected="true"] {
        color: #002855 !important;
        font-weight: 700;
        border-bottom: 3px solid #98793E !important;
    }
    .stTabs [data-baseweb="tab-border"] {
        display: none !important;
    }

    /* ---------------------------------------------------
       CAJAS, BOTONES E INPUTS (Efecto Levitación/Hover)
       --------------------------------------------------- */
    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 12px;
        transition: all 0.3s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #98793E;
        box-shadow: 0px 4px 12px rgba(152, 121, 62, 0.15);
        transform: translateY(-1px);
    }
    
    /* Botones */
    div[data-testid="stButton"] button {
        background-color: #98793E !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 8px 24px !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #002855 !important;
        box-shadow: 0px 6px 15px rgba(0, 40, 85, 0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Títulos de sección */
    .section-title {
        color: #002855; 
        font-size: 20px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 20px;
        display: inline-block;
        border-bottom: 2px solid #98793E;
        padding-bottom: 5px;
    }
    
    /* Sombra suave para imágenes de muestra */
    img {
        border-radius: 8px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    img:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. ENCABEZADO MINIMALISTA
# ---------------------------------------------------------
col_logo, col_texto = st.columns([1, 8])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=90)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=90)

with col_texto:
    st.markdown("""
        <div class="header-title">LITOTECA SEG UNAP</div>
        <div class="header-subtitle">Society of Economic Geologists Student Chapter</div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. ESTRUCTURA DE NAVEGACIÓN
# ---------------------------------------------------------
tab_acerca, tab_litoteca, tab_equipo, tab_fundacion = st.tabs([
    "Acerca de", 
    "Litoteca", 
    "Participantes", 
    "Fundaciones"
])

# ==========================================
# PESTAÑA 1: ACERCA DE
# ==========================================
with tab_acerca:
    st.markdown('<div class="section-title">Capítulo Estudiantil SEG UNAP</div>', unsafe_allow_html=True)
    st.write("""
    El Capítulo Estudiantil de la **Society of Economic Geologists (SEG)** de la Universidad Nacional del Altiplano en Puno, es una organización académica sin fines de lucro conformada por estudiantes y docentes de la Facultad de Ingeniería Geológica y Metalúrgica.
    
    Nuestro principal objetivo es avanzar en el conocimiento de la geología de yacimientos minerales. Situados estratégicamente en el sur del Perú, enfocamos nuestros esfuerzos en el estudio de sistemas epitermales, pórfidos, skarn y depósitos polimetálicos.
    """)

# ==========================================
# PESTAÑA 2: LITOTECA (PROTEGIDA CON LOGIN)
# ==========================================
with tab_litoteca:
    USUARIOS_PERMITIDOS = {
        "seg_unap": "SegUnap2026",  
        "mayersyerson17@gmail.com": "927685",        
        "richardcoaquiraapaza@gmail.com": "925371",       
        "carbajaljuancarlos194@gmail.com": "927700"    
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
        st.write("")
        st.write("")
        _, col_login, _ = st.columns([1, 1.5, 1])
        
        with col_login:
            st.markdown("<h4 style='text-align:center; color:#002855; font-weight:700;'>Control de Acceso</h4>", unsafe_allow_html=True)
            st.write("")
            st.text_input("Usuario", key="input_usuario", placeholder="Ingrese su correo institucional")
            st.text_input("Contraseña", type="password", key="input_password", placeholder="••••••••")
            st.write("")
            st.button("Iniciar Sesión", on_click=verificar_credenciales, use_container_width=True)
            
            if st.session_state["intento_fallido"]:
                st.error("Credenciales incorrectas. Verifique su acceso.")
    else:
        st.success("Autenticación exitosa.")
        st.write("---")
        
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
            col_hoja, _ = st.columns([1.5, 2.5])
            with col_hoja:
                hoja_seleccionada = st.selectbox("📁 Proyecto Geológico:", lista_hojas, label_visibility="collapsed")

            df = cargar_datos_hoja(ARCHIVO_EXCEL, hoja_seleccionada)

            if not df.empty:
                if 'CODIGO DE MUESTRA' in df.columns:
                    df_filtrado = df.copy()

                    st.markdown('<div class="section-title">Filtros Activos</div>', unsafe_allow_html=True)
                    
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
                                    sel_um = st.selectbox("Unidad Minera", opciones)
                                    if sel_um != "Todas":
                                        df_filtrado = df_filtrado[df_filtrado['U.M.'] == sel_um]
                                elif col_name == 'Tipo de deposito':
                                    opciones = ["Todos"] + list(df['Tipo de deposito'].dropna().unique())
                                    sel_dep = st.selectbox("Tipo de Depósito", opciones)
                                    if sel_dep != "Todos":
                                        df_filtrado = df_filtrado[df_filtrado['Tipo de deposito'] == sel_dep]
                                elif col_name == 'NOMBRE DEL DONADOR':
                                    opciones = ["Todos"] + list(df['NOMBRE DEL DONADOR'].dropna().unique())
                                    sel_don = st.selectbox("Donador", opciones)
                                    if sel_don != "Todos":
                                        df_filtrado = df_filtrado[df_filtrado['NOMBRE DEL DONADOR'] == sel_don]
                                elif col_name == 'ESTUDIANTE ENCARGADO':
                                    opciones = ["Todos"] + list(df['ESTUDIANTE ENCARGADO'].dropna().unique())
                                    sel_est = st.selectbox("Encargado", opciones)
                                    if sel_est != "Todos":
                                        df_filtrado = df_filtrado[df_filtrado['ESTUDIANTE ENCARGADO'] == sel_est]

                    st.write("---")
                    
                    # Gráficos de Plotly con diseño minimalista (Fondo transparente)
                    st.markdown('<div class="section-title">Análisis de Datos</div>', unsafe_allow_html=True)
                    if not df_filtrado.empty:
                        g1, g2 = st.columns(2)
                        
                        with g1:
                            if 'Tipo de deposito' in df_filtrado.columns and df_filtrado['Tipo de deposito'].dropna().any():
                                conteo = df_filtrado['Tipo de deposito'].value_counts().reset_index()
                                conteo.columns = ['Tipo', 'Total']
                                fig_torta = px.pie(
                                    conteo, values='Total', names='Tipo', 
                                    hole=0.5,
                                    color_discrete_sequence=['#002855', '#98793E', '#4A6B8F', '#F0C96A', '#CCCCCC']
                                )
                                fig_torta.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)', 
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    margin=dict(t=30, b=10, l=10, r=10),
                                    title=dict(text="Distribución de Depósitos", font=dict(size=14, color='#002855'))
                                )
                                st.plotly_chart(fig_torta, use_container_width=True)
                                
                        with g2:
                            if 'EMPRESA' in df_filtrado.columns and df_filtrado['EMPRESA'].dropna().any():
                                conteo = df_filtrado['EMPRESA'].value_counts().reset_index()
                                conteo.columns = ['Empresa', 'Total']
                                fig_barras = px.bar(
                                    conteo, x='Empresa', y='Total', 
                                    text_auto=True, color_discrete_sequence=['#002855'] 
                                )
                                fig_barras.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)', 
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    margin=dict(t=30, b=10, l=10, r=10),
                                    title=dict(text="Muestras por Empresa", font=dict(size=14, color='#002855')),
                                    xaxis=dict(showgrid=False),
                                    yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
                                )
                                st.plotly_chart(fig_barras, use_container_width=True)

                    st.write("---")

                    col_tabla, col_foto = st.columns([2, 1.2])
                    with col_tabla:
                        st.markdown('<div class="section-title">Matriz de Inventario</div>', unsafe_allow_html=True)
                        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                        
                    with col_foto:
                        st.markdown('<div class="section-title">Visor Digital</div>', unsafe_allow_html=True)
                        codigos_disponibles = df_filtrado['CODIGO DE MUESTRA'].dropna().unique()
                        if len(codigos_disponibles) > 0:
                            id_sel = st.selectbox("Seleccionar Muestra:", codigos_disponibles, label_visibility="collapsed")
                            
                            fila = df_filtrado[df_filtrado['CODIGO DE MUESTRA'] == id_sel].iloc[0]
                            um_text = fila['U.M.'] if 'U.M.' in df_filtrado.columns else "N/A"
                            desc_text = fila['Descripcion'] if 'Descripcion' in df_filtrado.columns else "N/A"
                            
                            st.markdown(f"**U.M.:** {um_text}  \n**Detalle:** {desc_text}")
                            
                            ruta_jpg = f"fotos/{id_sel}.jpg"
                            ruta_png = f"fotos/{id_sel}.png"
                            
                            if os.path.exists(ruta_jpg):
                                st.image(ruta_jpg, use_container_width=True)
                            elif os.path.exists(ruta_png):
                                st.image(ruta_png, use_container_width=True)
                else:
                    st.markdown(f'<div class="section-title">Reporte Estructural: {hoja_seleccionada.upper()}</div>', unsafe_allow_html=True)
                    
                    for index, row in df.iterrows():
                        celdas_validas = [str(val) for val in row if pd.notna(val) and str(val).strip() != ""]
                        if celdas_validas:
                            with st.expander(f"Registro Técnico (Fila {index + 1})", expanded=(index < 5)):
                                cols = st.columns(len(celdas_validas))
                                for i, texto in enumerate(celdas_validas):
                                    with cols[i]:
                                        st.markdown(f"<div style='background-color:#F5F7FA; color:#333; padding:15px; border-radius:8px; font-size: 13px; font-family: monospace; white-space: pre-wrap;'>{texto}</div>", unsafe_allow_html=True)

# ==========================================
# PESTAÑA 3: PARTICIPANTES
# ==========================================
with tab_equipo:
    st.markdown('<div class="section-title">Junta Directiva</div>', unsafe_allow_html=True)
    st.write("""
    Nuestra directiva planifica, organiza y ejecuta todas las actividades académicas, de campo y la gestión técnica de nuestra Litoteca.
    
    * **Presidente(a):** [Nombre]
    * **Vicepresidente(a):** [Nombre]
    * **Secretario(a):** [Nombre]
    * **Tesorero(a):** [Nombre]
    * **Vocal de Litoteca:** Gary Bustinza
    """)

# ==========================================
# PESTAÑA 4: FUNDACIONES
# ==========================================
with tab_fundacion:
    st.markdown('<div class="section-title">Respaldo SEG Foundation</div>', unsafe_allow_html=True)
    st.write("""
    El Capítulo Estudiantil de la UNAP cuenta con el aval de la **Society of Economic Geologists Foundation (SEGF)**. A través de la membresía SEG, los estudiantes pueden postular a:
    
    * **Subvenciones de Investigación:** Fondos para financiar trabajos de tesis y análisis.
    * **Apoyo para Viajes:** Becas para organizar excursiones a yacimientos y asistir a conferencias internacionales.
    """)
