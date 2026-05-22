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

# Paleta de Colores Oficial SEG
# Azul Marino SEG: #002855
# Dorado/Bronce SEG: #98793E
# Fondo: #FFFFFF (Blanco Puro)

st.markdown("""
    <style>
    /* Fondo General Blanco Puro */
    .stApp {
        background-color: #FFFFFF;
    }
    
    .block-container {
        padding-top: 3.5rem !important; 
    }
    
    .header-title {
        color: #002855;
        font-size: 30px;
        font-weight: 700;
        margin-top: 20px; 
        margin-bottom: 0px;
        padding-bottom: 0px;
        line-height: 1.2;
    }
    .header-subtitle {
        color: #98793E;
        font-size: 16px;
        font-style: italic;
        margin-top: 0px;
        padding-top: 0px;
    }
    
    /* ---------------------------------------------------
       BARRA DE NAVEGACIÓN PRINCIPAL (AZUL)
       --------------------------------------------------- */
    div[data-testid="stTabs"] {
        margin-top: 15px;
    }
    div[data-testid="stTabs"] > div[data-baseweb="tab-list"] {
        background-color: #002855;
        padding: 0;
        border-radius: 4px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        gap: 0px;
    }
    div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button {
        color: #FFFFFF !important;
        font-size: 15px;
        font-weight: 500;
        padding: 15px 25px;
        border: none;
    }
    div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button:hover {
        background-color: #001a38;
        color: #98793E !important;
    }
    div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #98793E !important;
        color: #002855 !important;
        font-weight: bold;
        border-radius: 4px;
    }
    
    /* ---------------------------------------------------
       SUB-MENÚ DESGLOSABLE (DORADO ESTILO SEG)
       --------------------------------------------------- */
    div[data-testid="stTabs"] div[data-testid="stTabs"] > div[data-baseweb="tab-list"] {
        background-color: #98793E; /* Color dorado extraído de tu imagen */
        margin-top: -15px;
        border-radius: 0px 0px 4px 4px;
        box-shadow: inset 0px 2px 4px rgba(0,0,0,0.1);
    }
    div[data-testid="stTabs"] div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button {
        color: #FFFFFF !important;
        font-size: 14px;
        padding: 10px 20px;
        font-weight: normal;
    }
    div[data-testid="stTabs"] div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button:hover {
        background-color: #7A6132 !important; /* Dorado más oscuro al pasar el ratón */
        color: #FFFFFF !important;
    }
    div[data-testid="stTabs"] div[data-testid="stTabs"] > div[data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #7A6132 !important;
        color: #FFFFFF !important;
        font-weight: bold;
        border-radius: 0px;
    }

    /* Ocultar las líneas inferiores feas de Streamlit */
    [data-baseweb="tab-border"] {
        display: none !important;
    }
    
    /* Estilos Generales */
    div[data-testid="stButton"] button {
        background-color: #98793E !important;
        color: #FFFFFF !important;
        border: none !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        border-radius: 4px !important;
        transition: 0.3s;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #7A6132 !important;
    }
    .stTextInput>div>div>input {
        background-color: #F8F9FA;
        border: 1px solid #CCCCCC;
    }
    .stTextInput>div>div>input:focus {
        border-color: #002855;
        box-shadow: 0 0 0 0.2rem rgba(0, 40, 85, 0.25);
    }
    .section-title {
        color: #002855; 
        border-left: 5px solid #98793E; 
        padding-left: 10px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .info-text {
        color: #333333;
        font-size: 16px;
        line-height: 1.6;
        text-align: justify;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. ENCABEZADO OFICIAL (SIEMPRE VISIBLE)
# ---------------------------------------------------------
col_logo, col_texto = st.columns([1, 6])
with col_logo:
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=120)
    elif os.path.exists("logo.png"):
        st.image("logo.png", width=120)

with col_texto:
    st.markdown("""
        <div class="header-title">LITOTECA SEG UNAP</div>
        <div class="header-subtitle">Society of Economic Geologists Student Chapter</div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. BARRA DE NAVEGACIÓN Y ESTRUCTURA DEL PORTAL
# ---------------------------------------------------------
tab_acerca, tab_litoteca, tab_equipo, tab_fundacion = st.tabs([
    "Acerca de", 
    "Litoteca", 
    "Participantes", 
    "Fundaciones"
])

# ==========================================
# PESTAÑA 1: ACERCA DE (CON SUB-MENÚ DORADO)
# ==========================================
with tab_acerca:
    # Sub-menú estilizado simulando el desglosable
    sub_sociedad, sub_eventos, sub_contacto = st.tabs(["Acerca de la Sociedad", "Actividades y Eventos", "Contáctanos"])
    
    with sub_sociedad:
        st.write("")
        st.markdown('<h3 class="section-title">Capítulo Estudiantil SEG UNAP - Puno</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-text">
            El Capítulo Estudiantil de la <b>Society of Economic Geologists (SEG)</b> de la Universidad Nacional del Altiplano (UNAP) en Puno, es una organización académica sin fines de lucro conformada por estudiantes, egresados y docentes de la Facultad de Ingeniería Geológica y Metalúrgica.<br><br>
            Nuestro principal objetivo es avanzar en el conocimiento de la geología de yacimientos minerales, sirviendo como un puente directo entre la excelencia académica y la industria minera. Situados estratégicamente en el sur del Perú, una de las regiones metalogenéticas más ricas y diversas de los Andes, enfocamos nuestros esfuerzos en el estudio de sistemas epitermales, pórfidos, skarn y depósitos polimetálicos.
        </div>
        """, unsafe_allow_html=True)

    with sub_eventos:
        st.write("")
        st.markdown('<h3 class="section-title">Calendario Académico y Eventos</h3>', unsafe_allow_html=True)
        st.info("📌 Próximamente: Aquí anunciaremos nuestros webinars técnicos, talleres de logueo, salidas de campo y certificaciones del capítulo.")
        
    with sub_contacto:
        st.write("")
        st.markdown('<h3 class="section-title">Únete al Capítulo</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-text">
            ¿Interesado en la geología económica? Síguenos en nuestras redes oficiales y entérate de las convocatorias para formar parte de la directiva o asistir a nuestros próximos eventos de terreno.<br><br>
            📧 <b>Correo Institucional:</b> [Añadir correo SEG UNAP]<br>
            📱 <b>Facebook/LinkedIn:</b> [Añadir links]
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PESTAÑA 2: LITOTECA (PROTEGIDA CON LOGIN)
# ==========================================
with tab_litoteca:
    st.write("")
    
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
        _, col_login, _ = st.columns([2, 2.5, 2])
        
        with col_login:
            st.text_input("Nombre de usuario", key="input_usuario", placeholder="Ingrese su correo o usuario")
            st.text_input("Contraseña", type="password", key="input_password", placeholder="••••••••")
            st.write("")
            
            st.button("Iniciar sesión", on_click=verificar_credenciales, use_container_width=True)
            
            if st.session_state["intento_fallido"]:
                st.error("❌ Credenciales incorrectas. Verifique su acceso.")
                
            st.markdown("""
                <div style="text-align: center; margin-top: 20px; font-size: 14px;">
                    <a href="#" style="color: #0056b3;">¿Olvidaste la contraseña?</a>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.success("✅ Autenticación exitosa. Bienvenido a la Base de Datos de la Litoteca.")
        
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
                hoja_seleccionada = st.selectbox("📂 SELECCIONAR PESTAÑA / PROYECTO:", lista_hojas)

            df = cargar_datos_hoja(ARCHIVO_EXCEL, hoja_seleccionada)

            if not df.empty:
                if 'CODIGO DE MUESTRA' in df.columns:
                    df_filtrado = df.copy()

                    st.markdown('<h3 class="section-title">🔍 FILTROS DE BÚSQUEDA</h3>', unsafe_allow_html=True)
                    
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

                    st.metric("TOTAL REGISTROS FILTRADOS", len(df_filtrado))
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
                                    color_discrete_sequence=['#002855', '#98793E', '#4A6B8F', '#F0C96A', '#CCCCCC'],
                                    hole=0.4
                                )
                                fig_torta.update_traces(textposition='inside', textinfo='percent+label')
                                st.plotly_chart(fig_torta, use_container_width=True)
                                
                        with g2:
                            if 'EMPRESA' in df_filtrado.columns and df_filtrado['EMPRESA'].dropna().any():
                                conteo = df_filtrado['EMPRESA'].value_counts().reset_index()
                                conteo.columns = ['EMPRESA', 'Cantidad']
                                fig_barras = px.bar(
                                    conteo, x='EMPRESA', y='Cantidad', 
                                    title="Muestras por Empresa",
                                    text_auto=True, color_discrete_sequence=['#002855'] 
                                )
                                fig_barras.update_traces(marker_line_color='#98793E', marker_line_width=1, opacity=0.9)
                                st.plotly_chart(fig_barras, use_container_width=True)

                    st.write("---")

                    col_tabla, col_foto = st.columns([2, 1])
                    with col_tabla:
                        st.markdown(f'<h4 class="section-title">📋 MATRIZ DE DATOS</h4>', unsafe_allow_html=True)
                        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
                        
                    with col_foto:
                        st.markdown('<h4 class="section-title">📸 VISOR DE MUESTRA FÍSICA</h4>', unsafe_allow_html=True)
                        codigos_disponibles = df_filtrado['CODIGO DE MUESTRA'].dropna().unique()
                        if len(codigos_disponibles) > 0:
                            id_sel = st.selectbox("Seleccionar Código Analizado:", codigos_disponibles)
                            
                            fila = df_filtrado[df_filtrado['CODIGO DE MUESTRA'] == id_sel].iloc[0]
                            um_text = fila['U.M.'] if 'U.M.' in df_filtrado.columns else "N/A"
                            desc_text = fila['Descripcion'] if 'Descripcion' in df_filtrado.columns else "N/A"
                            
                            st.info(f"📍 **U.M.:** {um_text} \n\n 🔬 **Descripción:** {desc_text}")
                            
                            ruta_jpg = f"fotos/{id_sel}.jpg"
                            ruta_png = f"fotos/{id_sel}.png"
                            
                            if os.path.exists(ruta_jpg):
                                st.image(ruta_jpg, caption=f"Muestra: {id_sel}", use_container_width=True)
                            elif os.path.exists(ruta_png):
                                st.image(ruta_png, caption=f"Muestra: {id_sel}", use_container_width=True)
                else:
                    st.markdown(f'<h4 class="section-title">📄 REPORTE DE LOGUEO: {hoja_seleccionada.upper()}</h4>', unsafe_allow_html=True)
                    
                    tab_tarjetas, tab_tabla = st.tabs(["🗂️ Vista Dinámica (Tarjetas)", "📊 Vista Original (Excel)"])
                    
                    with tab_tarjetas:
                        st.info("💡 Exploración interactiva. Formato estructurado para descripciones geológicas de campo.")
                        for index, row in df.iterrows():
                            celdas_validas = [str(val) for val in row if pd.notna(val) and str(val).strip() != ""]
                            
                            if celdas_validas:
                                with st.expander(f"🔹 Bloque de Registro Técnico (Fila {index + 1})", expanded=(index < 7)):
                                    cols = st.columns(len(celdas_validas))
                                    for i, texto in enumerate(celdas_validas):
                                        with cols[i]:
                                            st.markdown(f"<div style='background-color:#ffffff; color:#111111; padding:15px; border-left: 4px solid #002855; border-radius:5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); font-size: 13px; font-family: monospace; white-space: pre-wrap;'>{texto}</div>", unsafe_allow_html=True)
                    with tab_tabla:
                        st.dataframe(df, use_container_width=True)

# ==========================================
# PESTAÑA 3: PARTICIPANTES (CON SUB-MENÚ DORADO)
# ==========================================
with tab_equipo:
    sub_junta, sub_proyectos = st.tabs(["Junta Directiva", "Proyectos de Campo"])
    
    with sub_junta:
        st.write("")
        st.markdown('<h3 class="section-title">Junta Directiva SEG UNAP</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-text">
            El Capítulo Estudiantil SEG UNAP está liderado por un equipo de estudiantes comprometidos con la difusión del conocimiento en geología económica.<br><br>
            <ul>
                <li><b>Presidente(a):</b> [Nombre]</li>
                <li><b>Vicepresidente(a):</b> [Nombre]</li>
                <li><b>Secretario(a):</b> [Nombre]</li>
                <li><b>Tesorero(a):</b> [Nombre]</li>
                <li><b>Vocal de Litoteca:</b> Gary Bustinza</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with sub_proyectos:
        st.write("")
        st.markdown('<h3 class="section-title">Proyectos de Investigación y Mapeo</h3>', unsafe_allow_html=True)
        st.info("📌 Espacio reservado para documentar futuras salidas a terreno, recolección de muestras y análisis metalogenético en la región de Puno.")

# ==========================================
# PESTAÑA 4: FUNDACIONES
# ==========================================
with tab_fundacion:
    st.write("")
    st.markdown('<h3 class="section-title">Respaldo de la SEG Foundation</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-text">
        El Capítulo Estudiantil de la UNAP cuenta con el prestigioso aval y apoyo de la <b>Society of Economic Geologists Foundation (SEGF)</b>, pilar que sostiene el desarrollo de estudiantes de geología a nivel mundial.<br><br>
        A través de la membresía SEG, los estudiantes pueden postular a:
        <ul>
            <li><b>Subvenciones de Investigación (Student Research Grants):</b> Fondos para financiar trabajos de tesis y análisis de laboratorio.</li>
            <li><b>Apoyo para Viajes:</b> Becas para organizar excursiones a yacimientos y asistir a conferencias internacionales.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
