# Dashboard Jurídico — IGSA

Gerador de dashboards jurídicos executivos para a Imaculada Gordiano Sociedade de Advogados.

## Arquivos do projeto

- `build_dashboard.py` — aplicativo Streamlit (serve o gerador + publica no Netlify)
- `index.html` — o gerador de dashboard (produto)
- `requirements.txt` — dependências (Streamlit)

## Como rodar no Streamlit Cloud

1. Suba estes arquivos no GitHub
2. Em share.streamlit.io: New app → aponte para `build_dashboard.py`
3. Configure o token do Netlify em Settings → Secrets:
   ```
   NETLIFY_TOKEN = "seu_token_aqui"
   ```

## Não versionar

- Token do Netlify (vai nos Secrets do Streamlit)
- Planilhas de clientes (.xlsx)
- HTMLs gerados
