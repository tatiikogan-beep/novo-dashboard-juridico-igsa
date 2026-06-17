import base64
import os
import re
import time
import urllib.request
import streamlit as st

# ════════════════════════════════════════════════════════════════════════════
#  Gerador de Dashboard Jurídico — IGSA
#  Serve o index.html (produto), convertendo os CDNs em bibliotecas embutidas
#  (offline) para funcionar sem depender de internet no cliente.
# ════════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Dashboard Jurídico - IGSA", layout="wide")

# ── Baixa bibliotecas uma vez e embute inline (cache) ────────────────────────
@st.cache_data(show_spinner=False)
def _fetch_lib(url, fallback=""):
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.read().decode("utf-8")
    except Exception:
        return fallback

# ── Lê o index.html (na mesma pasta deste script) ────────────────────────────
@st.cache_data(show_spinner=False)
def _load_index_html():
    here = os.path.dirname(os.path.abspath(__file__))
    for name in ("index.html", "Dashboard_Juridico.html"):
        p = os.path.join(here, name)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return f.read()
    return None

# ── Converte os <script src="CDN"></script> em scripts embutidos (offline) ───
@st.cache_data(show_spinner=False)
def _make_offline(html):
    # captura cada <script src="URL"></script> e troca pelo conteúdo
    def repl(m):
        url = m.group(1)
        code = _fetch_lib(url, "")
        if not code:
            # se falhar o download, mantém o CDN como fallback
            return '<script src="%s"></script>' % url
        return "<script>%s</script>" % code
    return re.sub(r'<script src="([^"]+)"></script>', repl, html)

html = _load_index_html()

if html is None:
    st.error(
        "Arquivo **index.html** não encontrado na pasta do app. "
        "Suba o index.html para o repositório, junto deste script."
    )
else:
    with st.spinner("Preparando o gerador..."):
        html_offline = _make_offline(html)
    st.components.v1.html(html_offline, height=900, scrolling=True)


# ── Ferramenta: Corrigir HTML antigo (sem gráficos) ──────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🔧 Corrigir HTML existente")
    st.caption("Faça upload de um HTML gerado antes do fix para embutir as bibliotecas automaticamente.")
    uploaded_fix = st.file_uploader("Selecione o arquivo HTML", type=["html"], key="fix_uploader")
    if uploaded_fix is not None:
        with st.spinner("Baixando bibliotecas e corrigindo... (pode levar ~20s)"):
            import re as _re
            _html = uploaded_fix.read().decode("utf-8")
            _xlsx   = _fetch_lib("https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js")
            _chart  = _fetch_lib("https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js")
            _dlbl   = _fetch_lib("https://cdnjs.cloudflare.com/ajax/libs/chartjs-plugin-datalabels/2.2.0/chartjs-plugin-datalabels.min.js")
            _jszip  = _fetch_lib("https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js")
            _html = _re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/jszip/[^"]+"></script>',
                            f'<script>{_jszip}</script>', _html)
            _html = _re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/xlsx/[^"]+"></script>',
                            f'<script>{_xlsx}</script>', _html)
            _html = _re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/Chart\.js/[^"]+"></script>',
                            f'<script>{_chart}</script>', _html)
            _html = _re.sub(r'<script src="https://cdnjs\.cloudflare\.com/ajax/libs/chartjs-plugin-datalabels/[^"]+"></script>',
                            f'<script>{_dlbl}</script>', _html)
            _html = _re.sub(r'<link[^>]*fonts\.googleapis\.com[^>]*>', '', _html)
            _out_name = uploaded_fix.name.replace(".html", "_OFFLINE.html")
            st.success("✅ HTML corrigido com sucesso!")
            st.download_button(
                label="⬇️ Baixar HTML corrigido (funciona offline e no Teams)",
                data=_html.encode("utf-8"),
                file_name=_out_name,
                mime="text/html"
            )


# ── Ferramenta: Publicar dashboard no Netlify ────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🌐 Publicar no Netlify")
    st.caption("Publique o HTML gerado e receba um link para enviar por e-mail ou WhatsApp.")

    _netlify_token = ""
    try:
        _netlify_token = st.secrets.get("NETLIFY_TOKEN", "")
    except Exception:
        pass
    if not _netlify_token:
        _netlify_token = st.text_input("Token do Netlify (Personal Access Token)", type="password", key="netlify_token_input")
        st.caption("Crie seu token em: app.netlify.com")

    _html_to_publish = st.file_uploader("Selecione o HTML do dashboard", type=["html"], key="netlify_uploader")

    if _html_to_publish is not None and _netlify_token:
        if st.button("\U0001f4e4 Publicar e gerar link", key="netlify_publish_btn"):
            import urllib.request as _ur2
            import json as _json2
            import zipfile as _zf
            import io as _io2

            with st.spinner("Publicando no Netlify... aguarde"):
                try:
                    _html_bytes = _html_to_publish.read()

                    # netlify.toml para forçar Content-Type correto
                    _toml_lines = [
                        "[[headers]]",
                        '  for = "/*"',
                        "  [headers.values]",
                        '    Content-Type = "text/html; charset=utf-8"'
                    ]
                    _toml_bytes = "\n".join(_toml_lines).encode("utf-8")

                    # Cria ZIP com index.html + netlify.toml
                    _zip_buf = _io2.BytesIO()
                    with _zf.ZipFile(_zip_buf, "w", _zf.ZIP_DEFLATED) as _zobj:
                        _zobj.writestr("index.html", _html_bytes)
                        _zobj.writestr("netlify.toml", _toml_bytes)
                    _zip_data = _zip_buf.getvalue()

                    # Passo 1: Criar site
                    _req_site = _ur2.Request(
                        "https://api.netlify.com/api/v1/sites",
                        data=_json2.dumps({}).encode("utf-8"),
                        headers={
                            "Authorization": f"Bearer {_netlify_token}",
                            "Content-Type": "application/json"
                        },
                        method="POST"
                    )
                    with _ur2.urlopen(_req_site) as _r:
                        _site = _json2.loads(_r.read().decode("utf-8"))
                    _site_id = _site["id"]

                    # Passo 2: Deploy via ZIP
                    _req_deploy = _ur2.Request(
                        f"https://api.netlify.com/api/v1/sites/{_site_id}/deploys",
                        data=_zip_data,
                        headers={
                            "Authorization": f"Bearer {_netlify_token}",
                            "Content-Type": "application/zip"
                        },
                        method="POST"
                    )
                    with _ur2.urlopen(_req_deploy) as _r:
                        _deploy = _json2.loads(_r.read().decode("utf-8"))

                    # Polling até ficar pronto
                    import time as _time
                    _deploy_id = _deploy["id"]
                    _status = _deploy
                    for _ in range(15):
                        _time.sleep(2)
                        _req_check = _ur2.Request(
                            f"https://api.netlify.com/api/v1/deploys/{_deploy_id}",
                            headers={"Authorization": f"Bearer {_netlify_token}"}
                        )
                        with _ur2.urlopen(_req_check) as _r:
                            _status = _json2.loads(_r.read().decode("utf-8"))
                        if _status.get("state") in ("ready", "current"):
                            break

                    _link = _status.get("ssl_url") or _status.get("url") or _site.get("ssl_url") or _site.get("url", "")
                    st.success("\u2705 Dashboard publicado com sucesso!")
                    st.markdown("### \U0001f517 Link para enviar ao cliente:")
                    st.code(_link, language=None)
                    st.caption("Copie o link acima e envie por e-mail ou WhatsApp.")
                except Exception as _e:
                    st.error(f"Erro ao publicar: {str(_e)}")
    elif _html_to_publish is not None and not _netlify_token:
        st.warning("\u26a0\ufe0f Token do Netlify n\u00e3o encontrado nos secrets.")
