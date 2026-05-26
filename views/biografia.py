"""Vista de Biografia - Informacion personal del autor."""

import streamlit as st
import base64
from core import hero,RUTA_PERFIL


def render():
    hero("Sobre el Autor",
         "Informacion personal del desarrollador del proyecto.",
         badges=["Biografia"])

    col_avatar, col_info = st.columns([1, 2])

    with col_avatar:
        img_bytes = RUTA_PERFIL.read_bytes()     
        img_b64 = base64.b64encode(img_bytes).decode("ascii")
     
        st.markdown(f"""
            <div style="text-align: center;">
               <img id="foto-perfil"  src="data:image/jpeg;base64,{img_b64}"
         style="width:15em; height:15em;  border-radius: 50%; object-fit:cover; border:4px solid #1C69D4;">
         <br/><br/>
                <div style="margin-top: 16px; font-size: 1.3rem;
                            font-weight: 700; color: #0F172A;">
                    Luis Alexander Suarez Colimba
                </div>
                <div style="color: #1C69D4; margin-top: 4px;">
                    Estudiante de Maestria
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("### Quien Soy")
        st.markdown("""
            <p style="text-align: justify">
            Luis A. Suárez C. Nacido en Guayaquil, Ecuador. 
            Ingeniero en Sistemas Computacionales y Maestrante en Ciencia de Datos e Inteligencia Artificial
            por la Universidad Casa Grande Actualmente se desempeña 
            como Arquitecto de Software, Ingeniero de Software y Líder Técnico en proyectos de desarrollo empresarial a la medida, 
            combinando su formación en ingeniería con su experiencia en entornos productivos del sector financiero y de instituciones públicas y privadas. Cuenta con más de seis años de experiencia liderando equipos técnicos en la construcción de soluciones escalables, con énfasis en sistemas de planificación y presupuesto para Gobiernos Autónomos Descentralizados municipales del Ecuador, así como en plataformas que optimizan la operatividad y los procesos institucionales de empresas privadas. Se caracteriza por un enfoque orientado a la mejora continua de procesos institucionales y por su interés en la aplicación de la Ciencia de Datos al sector público, particularmente en la automatización de tareas administrativas y en la integración de modelos de aprendizaje automático dentro de aplicaciones empresariales reales.
                    </p>
                 """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Contacto")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
            <div class="card">
                <div style="color: #64748B; font-size: 0.85rem;">CORREO</div>
                <div style="font-weight: 600; margin-top: 6px;">
                    ✅luissuarez2t@gmail.com <br/>
                    ✅luis.suarez2@casagrande.edu.ec
                </div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
            <div class="card">
                <div style="color: #64748B; font-size: 0.85rem;">UNIVERSIDAD</div>
                <div style="font-weight: 600; margin-top: 6px;">
                    Universidad Casa Grande
                </div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
            <div class="card">
                <div style="color: #64748B; font-size: 0.85rem;">UBICACION</div>
                <div style="font-weight: 600; margin-top: 6px;">
                    Guayaquil, Ecuador
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Formacion Academica")
    formaciones = [
        ("Maestria en IA y Ciencia de Datos",
         "Universidad Casa Grande", "2026 - En curso"),
        ("Ingeniería en Sistemas Computacionales",
         "Universidad de Guayaquil", "2015 - 2020"),
    ]
    for titulo, inst, periodo in formaciones:
        st.markdown(f"""
            <div class="card">
                <div style="font-weight: 700; color: #0F172A; font-size: 1.1rem;">
                    {titulo}
                </div>
                <div style="color: #1C69D4; margin-top: 4px;">
                    {inst} · {periodo}
                </div>
            </div>
        """, unsafe_allow_html=True)

    
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Portaflio")
    st.markdown("""
                <a href='https://profile-dun-two.vercel.app'>Portafolio Link 🌐</a>
                """,unsafe_allow_html=True)
    
    

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("### Habilidades Tecnicas")
    habs = {
    "Lenguajes": [
        "Java", "Python", "SQL",
        "JavaScript", "TypeScript"
    ],

    "Frameworks": [
        "Spring Boot", "Spring Cloud",
        "Angular", "FastAPI", "React"
    ],

    "Bases de Datos": [
        "SQL Server", "Oracle",
        "PostgreSQL", "MongoDB", 
        "PineCode", "Pg_Vector"
    ],

    "DevOps y Cloud": [
        "Docker", "Kubernetes",
        "Jenkins", "AWS"
    ],

    "Arquitectura e Integración": [
        "Microservicios",
        "REST APIs",
        "Spring Cloud Gateway",
        "Eureka Server",
        "BPM Activiti","Kafka",
        "IA Regenerativa", "RAG"
    ],

    "Herramientas": [
        "Git", "GitHub",
        "Pentaho", "Linux","Metabse","Power BI"
    ]
}
    for cat, items in habs.items():
        badges = "".join([f'<span class="badge">{i}</span>' for i in items])
        st.markdown(f"""
            <div style="margin-bottom: 14px;">
                <div style="color: #64748B; font-size: 0.9rem; margin-bottom: 6px;">
                    {cat}
                </div>
                <div>{badges}</div>
            </div>
        """, unsafe_allow_html=True)
