import base64
import os
import re

import streamlit as st

# ════════════════════════════════════════════════════════════════════════════
#  Formulário de Avaliação de Funcionalidades — IGSA
#  Serve o formulario-avaliacao.html, embutindo a logo como data URI para
#  funcionar dentro do iframe do Streamlit (que não resolve caminhos relativos).
# ════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Formulário de Avaliação - IGSA", layout="wide")

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)


@st.cache_data(show_spinner=False)
def _load_form_html():
    html_path = os.path.join(_ROOT, "formulario-avaliacao.html")
    logo_path = os.path.join(_ROOT, "assets", "logo-ig.png")

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode("ascii")
        data_uri = "data:image/png;base64," + logo_b64
        html = re.sub(r'src="assets/logo-ig\.png"', f'src="{data_uri}"', html)

    return html


html = _load_form_html()
st.components.v1.html(html, height=2400, scrolling=True)
