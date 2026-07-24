# Dashboard Jurídico — IGSA

Gerador de dashboards jurídicos executivos para a Imaculada Gordiano Sociedade de Advogados.

## Arquivos do projeto

- `build_dashboard.py` — aplicativo Streamlit principal (serve o gerador de dashboard + publica no Netlify)
- `index.html` — o gerador de dashboard (produto)
- `pages/1_Formulario_de_Avaliacao.py` — página Streamlit que serve o formulário de avaliação de fornecedores
- `formulario-avaliacao.html` — formulário de avaliação de funcionalidades (produto)
- `assets/logo-ig.png` — logo usada no formulário de avaliação
- `requirements.txt` — dependências (Streamlit)

## Como rodar no Streamlit Cloud

1. Suba estes arquivos no GitHub (mantendo a pasta `pages/` e `assets/`)
2. Em share.streamlit.io: New app → aponte para `build_dashboard.py`
3. O formulário de avaliação aparece automaticamente como uma segunda página, na barra
   lateral do app ("Formulario de Avaliacao"), graças à convenção de multipage do Streamlit
4. Configure o token do Netlify em Settings → Secrets:
   ```
   NETLIFY_TOKEN = "seu_token_aqui"
   ```

## Formulário de Avaliação de Funcionalidades

Formulário interno da Controladoria para avaliar soluções de gestão jurídica oferecidas por
fornecedores: identificação do fornecedor, 15 funcionalidades classificadas em 5 níveis de
disponibilidade (Nativo, Via parceiro, Módulo adicional, Em desenvolvimento, Não possui) e 5
campos descritivos (IA, Integrações, Diferenciais, Roadmap, Observações gerais). As respostas
ficam salvas no `localStorage` do navegador — nenhum dado é enviado a servidores — e o formulário
pode ser impresso/exportado em PDF ou ter as respostas copiadas em texto.

## Não versionar

- Token do Netlify (vai nos Secrets do Streamlit)
- Planilhas de clientes (.xlsx)
- HTMLs gerados
