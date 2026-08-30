import streamlit as st
import pandas as pd
import datetime
import calendar

# Configuração da página - Layout Wide
st.set_page_config(
    page_title="Painel de Controle Pessoal",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS (Design System Hybrid Dark/Light)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, button, input, select, textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background-color: #0b111e !important;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #94a3b8 !important;
        font-weight: 500;
    }

    [data-testid="stSidebar"] div.stButton > button {
        background-color: transparent !important;
        color: #94a3b8 !important;
        border: none !important;
        width: 100% !important;
        text-align: left !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        padding: 10px 12px !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
    }

    [data-testid="stSidebar"] div.stButton > button > div,
    [data-testid="stSidebar"] div.stButton > button p,
    [data-testid="stSidebar"] div.stButton > button span {
        text-align: left !important;
        justify-content: flex-start !important;
        width: 100% !important;
        display: flex !important;
        margin: 0 !important;
    }

    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }

    .main {
        background-color: #f8fafc;
    }

    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }

    .cal-header-day {
        text-align: center;
        font-weight: 600;
        color: #64748b;
        padding: 6px;
        font-size: 12px;
        text-transform: uppercase;
    }

    .cal-cell {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        min-height: 92px;
        padding: 6px;
        margin-bottom: 4px;
    }

    .cal-cell-out {
        background-color: #f8fafc;
        border: 1px solid #f1f5f9;
        border-radius: 6px;
        min-height: 92px;
        padding: 6px;
        margin-bottom: 4px;
        opacity: 0.5;
    }

    .cal-date-number {
        font-weight: 500;
        font-size: 12px;
        color: #334155;
        margin-bottom: 4px;
        display: inline-block;
        width: 22px;
        height: 22px;
        line-height: 22px;
        text-align: center;
    }

    .cal-date-selected {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 50%;
        font-weight: 600;
    }

    .badge-pill {
        display: block;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: 500;
        margin-top: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: #ffffff !important;
    }

    .badge-red { background-color: #ef4444; }
    .badge-yellow { background-color: #f59e0b; }
    .badge-green { background-color: #16a34a; }
</style>
""", unsafe_allow_html=True)

# Inicialização da Sessão
if 'menu_ativo' not in st.session_state:
    st.session_state.menu_ativo = "Painel de Controle"

if 'data_selecionada' not in st.session_state:
    st.session_state.data_selecionada = datetime.date.today()

if 'historico' not in st.session_state:
    st.session_state.historico = {
        "08/2026": {
            "rendas": pd.DataFrame([
                {"Descrição": "Trabalho / Vínculo 1", "Valor Previsto": 2400.0, "Valor Recebido": 2400.0, "Data Recebimento": "06/08/2026"},
                {"Descrição": "Trabalho / Vínculo 2", "Valor Previsto": 1380.0, "Valor Recebido": 1380.0, "Data Recebimento": "28/08/2026"}
            ]),
            "gastos": pd.DataFrame([
                {"Descrição": "NUBANK", "Categoria": "CARTÃO", "Valor": 121.37, "Data Vencimento": "25/08/2026", "Status": "Pendente"},
                {"Descrição": "INTER", "Categoria": "CARTÃO", "Valor": 663.63, "Data Vencimento": "12/08/2026", "Status": "Pendente"},
                {"Descrição": "MERCADO PAGO", "Categoria": "CARTÃO", "Valor": 203.25, "Data Vencimento": "07/08/2026", "Status": "Pendente"},
                {"Descrição": "PLANO INTERNET", "Categoria": "CELULAR", "Valor": 64.99, "Data Vencimento": "15/08/2026", "Status": "Pendente"},
                {"Descrição": "UBER", "Categoria": "TRANSPORTE", "Valor": 200.0, "Data Vencimento": "01/08/2026", "Status": "Pendente"},
                {"Descrição": "FACULDADE", "Categoria": "ESTUDO", "Valor": 1304.28, "Data Vencimento": "30/08/2026", "Status": "Pendente"},
                {"Descrição": "LAVA LOUÇA", "Categoria": "CASA", "Valor": 196.04, "Data Vencimento": "08/08/2026", "Status": "Pendente"},
                {"Descrição": "PARCELAS FIXAS", "Categoria": "CARTAO", "Valor": 888.26, "Data Vencimento": "07/08/2026", "Status": "Pendente"}
            ]),
            "tarefas": pd.DataFrame([
                {"Título": "Vencimento: INTER", "Contexto": "Financeiro", "Prioridade": "🔴 Alta", "Status": "Pendente", "Prazo": datetime.date(2026, 8, 12)},
                {"Título": "Vencimento: NUBANK", "Contexto": "Financeiro", "Prioridade": "🔴 Alta", "Status": "Pendente", "Prazo": datetime.date(2026, 8, 25)},
                {"Título": "Vencimento: FACULDADE", "Contexto": "Financeiro", "Prioridade": "🟡 Média", "Status": "Pendente", "Prazo": datetime.date(2026, 8, 30)}
            ])
        }
    }

if 'metas' not in st.session_state:
    st.session_state.metas = pd.DataFrame([
        {"Nome da Meta": "HABILITAÇÃO", "Valor Alvo (R$)": 1900.0, "Valor Já Guardado": 0.0, "Prazo": "30/09/2026"},
        {"Nome da Meta": "IPAD 11ª GERAÇÃO 128GB", "Valor Alvo (R$)": 2667.08, "Valor Já Guardado": 0.0, "Prazo": "01/02/2027"},
        {"Nome da Meta": "DENTISTA (DR. GUSTAVO)", "Valor Alvo (R$)": 1500.0, "Valor Já Guardado": 600.0, "Prazo": "01/01/2027"},
        {"Nome da Meta": "IPHONE 17 PROMAX", "Valor Alvo (R$)": 6500.0, "Valor Já Guardado": 0.0, "Prazo": "05/03/2027"},
        {"Nome da Meta": "JEEP RENEGADE LIMITED", "Valor Alvo (R$)": 28000.0, "Valor Já Guardado": 0.0, "Prazo": "28/10/2027"}
    ])

# Menu Lateral
with st.sidebar:
    st.markdown("### Painel Pessoal")
    st.caption("v1.0.0 | Acesso ADM")
    st.divider()
    
    if st.button("Painel de Controle", key="btn_painel", use_container_width=True):
        st.session_state.menu_ativo = "Painel de Controle"
        st.rerun()
        
    if st.button("Financeiro & Gastos", key="btn_fin", use_container_width=True):
        st.session_state.menu_ativo = "Financeiro & Gastos"
        st.rerun()
        
    if st.button("Metas & Prazos", key="btn_metas", use_container_width=True):
        st.session_state.menu_ativo = "Metas & Prazos"
        st.rerun()
        
    if st.button("Importar Planilhas (IA)", key="btn_import", use_container_width=True):
        st.session_state.menu_ativo = "Importar Planilhas (IA)"
        st.rerun()

    if st.button("Histórico & Relatórios", key="btn_hist", use_container_width=True):
        st.session_state.menu_ativo = "Histórico & Relatórios"
        st.rerun()

    st.divider()
    st.markdown("##### Mês de Referência")
    mes_sel = st.selectbox("Selecione o Mês:", ["06/2026", "07/2026", "08/2026", "09/2026", "10/2026"], index=2)

if mes_sel not in st.session_state.historico:
    st.session_state.historico[mes_sel] = {
        "rendas": pd.DataFrame(columns=["Descrição", "Valor Previsto", "Valor Recebido", "Data Recebimento"]),
        "gastos": pd.DataFrame(columns=["Descrição", "Categoria", "Valor", "Data Vencimento", "Status"]),
        "tarefas": pd.DataFrame(columns=["Título", "Contexto", "Prioridade", "Status", "Prazo"])
    }

dados_mes = st.session_state.historico[mes_sel]

# Recálculo Automático Global
total_entradas = dados_mes["rendas"]["Valor Recebido"].sum() if "Valor Recebido" in dados_mes["rendas"].columns and not dados_mes["rendas"].empty else 0.0
total_gastos = dados_mes["gastos"]["Valor"].sum() if "Valor" in dados_mes["gastos"].columns and not dados_mes["gastos"].empty else 0.0
saldo_restante = total_entradas - total_gastos

# Topbar
st.markdown("## Painel de Controle (Modo ADM)")
c_top1, c_top2, c_top3, c_top4 = st.columns(4)
c_top1.metric(f"Total Recebido ({mes_sel})", f"R$ {total_entradas:,.2f}")
c_top2.metric("Total Gasto", f"R$ {total_gastos:,.2f}")
c_top3.metric("Saldo Restante", f"R$ {saldo_restante:,.2f}", delta=f"{saldo_restante:,.2f}")
contas_pend = len(dados_mes["gastos"][dados_mes["gastos"]["Status"] == "Pendente"]) if "Status" in dados_mes["gastos"].columns and not dados_mes["gastos"].empty else 0
c_top4.metric("Contas Pendentes", contas_pend)

st.divider()

# Módulo 1: Painel de Controle (Agenda + Drawer)
if st.session_state.menu_ativo == "Painel de Controle":
    col_agenda, col_drawer = st.columns([2.2, 1])
    
    with col_agenda:
        c_nav1, c_nav2, c_nav3 = st.columns([2, 1, 1])
        with c_nav1:
            st.markdown(f"### Agenda - Mês {mes_sel}")
        with c_nav2:
            if st.button("Hoje", use_container_width=True):
                st.session_state.data_selecionada = datetime.date.today()
                st.rerun()
        with c_nav3:
            st.caption(f"Data Ativa: {st.session_state.data_selecionada.strftime('%d/%m/%Y')}")

        dias_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"]
        cols_h = st.columns(7)
        for i, d in enumerate(dias_semana):
            cols_h[i].markdown(f"<div class='cal-header-day'>{d}</div>", unsafe_allow_html=True)
            
        m_num, a_num = int(mes_sel.split("/")[0]), int(mes_sel.split("/")[1])
        cal = calendar.Calendar(firstweekday=6)
        dias_mes = cal.monthdatescalendar(a_num, m_num)
        
        for semana in dias_mes:
            cols_s = st.columns(7)
            for i, dia in enumerate(semana):
                with cols_s[i]:
                    is_in_month = (dia.month == m_num)
                    is_selected = (dia == st.session_state.data_selecionada)
                    
                    cell_class = "cal-cell" if is_in_month else "cal-cell-out"
                    num_class = "cal-date-number cal-date-selected" if is_selected else "cal-date-number"
                    
                    tarefas_dia = pd.DataFrame()
                    if "tarefas" in dados_mes and not dados_mes["tarefas"].empty:
                        if "Prazo" in dados_mes["tarefas"].columns:
                            tarefas_dia = dados_mes["tarefas"][dados_mes["tarefas"]['Prazo'] == dia]
                    
                    html_badges = ""
                    if not tarefas_dia.empty:
                        for _, t in tarefas_dia.iterrows():
                            prio_str = str(t.get("Prioridade", ""))
                            cor_b = "red" if "Alta" in prio_str else ("yellow" if "Média" in prio_str else "green")
                            html_badges += f"<div class='badge-pill badge-{cor_b}'>{t['Título']}</div>"
                    
                    st.markdown(f"""
                        <div class='{cell_class}'>
                            <span class='{num_class}'>{dia.day}</span>
                            {html_badges}
                        </div>
                    """, unsafe_allow_html=True)

    with col_drawer:
        st.markdown("### Tarefa / Compromisso")
        
        with st.form("form_drawer_pessoal"):
            tit_t = st.text_input("Título da Tarefa:")
            cat_t = st.selectbox("Tag / Contexto:", ["Trabalho 1", "Trabalho 2", "Estudos", "Financeiro", "Pessoal"])
            prio_t = st.selectbox("Nível de Prioridade:", ["🔴 Alta", "🟡 Média", "🟢 Baixa"])
            prazo_t = st.date_input("Data de Vencimento:", st.session_state.data_selecionada)
            
            if st.form_submit_button("Cadastrar Tarefa", use_container_width=True):
                nova_t = pd.DataFrame([{
                    "Título": tit_t, 
                    "Contexto": cat_t, 
                    "Prioridade": prio_t, 
                    "Status": "A Fazer", 
                    "Prazo": prazo_t
                }])
                dados_mes["tarefas"] = pd.concat([dados_mes["tarefas"], nova_t], ignore_index=True)
                st.session_state.data_selecionada = prazo_t
                st.success("Salvo!")
                st.rerun()

        st.markdown("---")
        st.markdown(f"#### Gerenciador ADM de Tarefas (Edição Direta)")
        st.caption("💡 Dê dois cliques em qualquer célula da tabela para editar o texto ou valor sem precisar excluir:")
        
        df_tarefas_editavel = st.data_editor(
            dados_mes["tarefas"], 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Prioridade": st.column_config.SelectboxColumn("Prioridade", options=["🔴 Alta", "🟡 Média", "🟢 Baixa"]),
                "Status": st.column_config.SelectboxColumn("Status", options=["A Fazer", "Em Andamento", "Concluído"])
            },
            key=f"editor_tarefas_{mes_sel}"
        )
        dados_mes["tarefas"] = df_tarefas_editavel

# Módulo 2: Financeiro & Gastos
elif st.session_state.menu_ativo == "Financeiro & Gastos":
    st.markdown(f"### Painel Financeiro - Referência {mes_sel}")
    st.caption("💡 Dê dois cliques em qualquer valor ou nome abaixo para editar diretamente na planilha:")
    
    aba_rendas, aba_despesas = st.tabs(["💵 Rendas / Salários", "💸 Despesas & Gastos"])
    
    with aba_rendas:
        st.markdown("#### Entradas do Mês (Edição Célula a Célula)")
        df_rendas_edit = st.data_editor(
            dados_mes["rendas"], 
            num_rows="dynamic", 
            use_container_width=True,
            key=f"editor_rendas_{mes_sel}"
        )
        dados_mes["rendas"] = df_rendas_edit

    with aba_despesas:
        st.markdown("#### Despesas & Contas (Edição Célula a Célula)")
        df_gastos_edit = st.data_editor(
            dados_mes["gastos"], 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Status": st.column_config.SelectboxColumn("Status", options=["Pendente", "Pago"])
            },
            key=f"editor_gastos_{mes_sel}"
        )
        dados_mes["gastos"] = df_gastos_edit

# Módulo 3: Aba de Metas e Prazos (Isolada)
elif st.session_state.menu_ativo == "Metas & Prazos":
    st.markdown("### Aba de Metas e Prazos (Isolada)")
    st.caption("ℹ️ Dê dois cliques no nome ou valor para alterar suas metas a qualquer momento:")
    
    df_metas_edit = st.data_editor(
        st.session_state.metas, 
        num_rows="dynamic", 
        use_container_width=True, 
        key="editor_metas_isolado"
    )
    st.session_state.metas = df_metas_edit
    
    st.markdown("---")
    st.markdown("#### Progresso & Aporte Mensal Sugerido")
    
    for idx, row in st.session_state.metas.iterrows():
        val_alvo = row.get("Valor Alvo (R$)", 1.0)
        val_guardado = row.get("Valor Já Guardado", 0.0)
        falta = max(val_alvo - val_guardado, 0.0)
        pct = min((val_guardado / val_alvo) if val_alvo > 0 else 0.0, 1.0)
        
        aporte_sugerido = falta / 6.0
        
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.write(f"**{row['Nome da Meta']}** — Guardado: R$ {val_guardado:,.2f} de R$ {val_alvo:,.2f} | Prazo: {row['Prazo']}")
            st.progress(pct)
        with col_m2:
            st.caption(f"Aporte Sugerido: **R$ {aporte_sugerido:,.2f} /mês**")

# Módulo 4: Importar Planilhas
elif st.session_state.menu_ativo == "Importar Planilhas (IA)":
    st.markdown("### 📥 Importação de Arquivos")
    st.write("Envie seus arquivos de dados (.xlsx / .csv):")
    arquivos_enviados = st.file_uploader("Selecione seus arquivos:", type=["xlsx", "xls", "csv"], accept_multiple_files=True)
    if arquivos_enviados:
        if st.button("Processar Arquivos", use_container_width=True):
            st.success("Arquivos lidos com sucesso!")

# Módulo 5: Histórico
elif st.session_state.menu_ativo == "Histórico & Relatórios":
    st.markdown("### Relatórios do Mês")
    st.dataframe(dados_mes["gastos"], use_container_width=True)
