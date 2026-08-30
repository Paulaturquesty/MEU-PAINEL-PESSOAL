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

# ESTILIZAÇÃO CSS (HYBRID DARK SIDEBAR / LIGHT CONTENT)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, button, input, select, textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* BARRA LATERAL TEMA ESCURO (#0B111E) */
    [data-testid="stSidebar"] {
        background-color: #0b111e !important;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #94a3b8 !important;
        font-weight: 500;
    }

    /* BOTÕES DO MENU LATERAL ALINHADOS À ESQUERDA */
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

    /* BADGES DE PRIORIDADE */
    .prio-alta { color: #ef4444; font-weight: 700; }
    .prio-media { color: #f59e0b; font-weight: 700; }
    .prio-baixa { color: #22c55e; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# INICIALIZAÇÃO DA SESSÃO E BANCO DE DADOS
if 'menu_ativo' not in st.session_state:
    st.session_state.menu_ativo = "Painel Geral (Tarefas)"

if 'historico' not in st.session_state:
    st.session_state.historico = {
        "08/2026": {
            "rendas": pd.DataFrame([
                {"Descrição": "Trabalho / Vínculo 1", "Valor Previsto": 2400.0, "Valor Recebido": 2400.0, "Data Recebimento": "06/08/2026"},
                {"Descrição": "Trabalho / Vínculo 2", "Valor Previsto": 1380.0, "Valor Recebido": 1380.0, "Data Recebimento": "28/08/2026"}
            ]),
            "gastos": pd.DataFrame([
                {"Descrição": "Faculdade", "Categoria": "Estudos", "Data Vencimento": "30/08/2026", "Valor": 1304.28, "Status": "Pendente"},
                {"Descrição": "Fatura Inter", "Categoria": "Cartões", "Data Vencimento": "12/08/2026", "Valor": 663.63, "Status": "Pendente"},
                {"Descrição": "Fatura Nubank", "Categoria": "Cartões", "Data Vencimento": "25/08/2026", "Valor": 121.37, "Status": "Pendente"}
            ])
        }
    }

if 'tarefas' not in st.session_state:
    st.session_state.tarefas = pd.DataFrame([
        {"Título": "Pagar Faculdade", "Data Vencimento": "30/08/2026", "Prioridade": "🔴 Alta", "Contexto": "Financeiro", "Status": "A Fazer"},
        {"Título": "Revisão de Relatório", "Data Vencimento": "28/08/2026", "Prioridade": "🟡 Média", "Contexto": "Trabalho 1", "Status": "Em Andamento"},
        {"Título": "Organizar Agenda Semanal", "Data Vencimento": "31/08/2026", "Prioridade": "🟢 Baixa", "Contexto": "Pessoal", "Status": "A Fazer"}
    ])

if 'metas' not in st.session_state:
    st.session_state.metas = pd.DataFrame([
        {"Nome da Meta": "Reserva de Emergência", "Valor Alvo (R$)": 10000.0, "Prazo": "31/12/2026", "Valor Já Guardado": 3500.0},
        {"Nome da Meta": "Habilitação", "Valor Alvo (R$)": 1900.0, "Prazo": "30/09/2026", "Valor Já Guardado": 600.0}
    ])

# BARRA LATERAL (FILTRO GLOBAL DE MÊS)
with st.sidebar:
    st.markdown("### Painel Pessoal")
    st.caption("v1.0.0 | System Admin")
    st.divider()
    
    if st.button("Painel Geral (Tarefas)", key="btn_geral", use_container_width=True):
        st.session_state.menu_ativo = "Painel Geral (Tarefas)"
        st.rerun()
        
    if st.button("Financeiro & Gastos", key="btn_fin", use_container_width=True):
        st.session_state.menu_ativo = "Financeiro & Gastos"
        st.rerun()
        
    if st.button("Metas & Prazos", key="btn_metas", use_container_width=True):
        st.session_state.menu_ativo = "Metas & Prazos"
        st.rerun()

    st.divider()
    st.markdown("##### Mês de Referência")
    mes_sel = st.selectbox("Selecione o Período:", ["06/2026", "07/2026", "08/2026", "09/2026", "10/2026"], index=2)

if mes_sel not in st.session_state.historico:
    st.session_state.historico[mes_sel] = {
        "rendas": pd.DataFrame(columns=["Descrição", "Valor Previsto", "Valor Recebido", "Data Recebimento"]),
        "gastos": pd.DataFrame(columns=["Descrição", "Categoria", "Data Vencimento", "Valor", "Status"])
    }

dados_mes = st.session_state.historico[mes_sel]

# MÓDULO 1: FINANCEIRO & GASTOS
if st.session_state.menu_ativo == "Financeiro & Gastos":
    st.markdown(f"## Painel Financeiro ({mes_sel})")
    
    # Resumo Geral do Mês
    total_entradas = dados_mes["rendas"]["Valor Recebido"].sum() if not dados_mes["rendas"].empty else 0.0
    total_saidas = dados_mes["gastos"]["Valor"].sum() if not dados_mes["gastos"].empty else 0.0
    saldo_restante = total_entradas - total_saidas
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Recebido", f"R$ {total_entradas:,.2f}")
    c2.metric("Total Gasto", f"R$ {total_saidas:,.2f}")
    c3.metric("Saldo Restante", f"R$ {saldo_restante:,.2f}", delta=f"{saldo_restante:,.2f}")
    st.divider()
    
    aba_rendas, aba_gastos = st.tabs(["💵 Rendas / Salários", "💸 Despesas & Gastos"])
    
    with aba_rendas:
        st.markdown("#### Entradas do Mês")
        df_rendas_edit = st.data_editor(dados_mes["rendas"], num_rows="dynamic", use_container_width=True, key=f"rendas_{mes_sel}")
        dados_mes["rendas"] = df_rendas_edit

    with aba_gastos:
        st.markdown("#### Despesas do Mês")
        df_gastos_edit = st.data_editor(
            dados_mes["gastos"], 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Status": st.column_config.SelectboxColumn("Status", options=["Pendente", "Pago"])
            },
            key=f"gastos_{mes_sel}"
        )
        dados_mes["gastos"] = df_gastos_edit

# MÓDULO 2: METAS E PRAZOS (ISOLADA)
elif st.session_state.menu_ativo == "Metas & Prazos":
    st.markdown("## Aba de Metas e Prazos")
    st.caption("ℹ️ Os valores desta aba são isolados e não alteram o cálculo de despesas mensais.")
    
    df_metas_edit = st.data_editor(st.session_state.metas, num_rows="dynamic", use_container_width=True, key="editor_metas")
    st.session_state.metas = df_metas_edit
    
    st.divider()
    st.markdown("### Acompanhamento de Progresso")
    
    for idx, row in st.session_state.metas.iterrows():
        val_alvo = row.get("Valor Alvo (R$)", 1.0)
        val_atual = row.get("Valor Já Guardado", 0.0)
        pct = min((val_atual / val_alvo) if val_alvo > 0 else 0.0, 1.0)
        
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.write(f"**{row['Nome da Meta']}** — R$ {val_atual:,.2f} de R$ {val_alvo:,.2f} (Prazo: {row['Prazo']})")
            st.progress(pct)
        with col_m2:
            st.caption(f"Atingido: **{(pct * 100):.1f}%**")

# MÓDULO 3: PAINEL GERAL (TAREFAS & ROTINA)
elif st.session_state.menu_ativo == "Painel Geral (Tarefas)":
    st.markdown("## Painel Geral de Tarefas e Rotina")
    
    col_t1, col_t2 = st.columns([2, 1])
    
    with col_t1:
        st.markdown("#### Minhas Tarefas Cadastradas")
        df_tarefas_edit = st.data_editor(
            st.session_state.tarefas,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Prioridade": st.column_config.SelectboxColumn("Prioridade", options=["🔴 Alta", "🟡 Média", "🟢 Baixa"]),
                "Status": st.column_config.SelectboxColumn("Status", options=["A Fazer", "Em Andamento", "Concluído"])
            },
            key="editor_tarefas_geral"
        )
        st.session_state.tarefas = df_tarefas_edit

    with col_t2:
        st.markdown("#### ➕ Nova Tarefa")
        with st.form("form_nova_tarefa"):
            tit = st.text_input("Título da Tarefa:")
            prio = st.selectbox("Prioridade:", ["🔴 Alta", "🟡 Média", "🟢 Baixa"])
            ctx = st.selectbox("Contexto / Área:", ["Trabalho 1", "Trabalho 2", "Estudos", "Financeiro", "Pessoal"])
            venc = st.date_input("Data de Vencimento:", datetime.date.today())
            
            if st.form_submit_button("Cadastrar Tarefa", use_container_width=True):
                nova_t = pd.DataFrame([{
                    "Título": tit, 
                    "Data Vencimento": venc.strftime("%d/%m/%Y"), 
                    "Prioridade": prio, 
                    "Contexto": ctx, 
                    "Status": "A Fazer"
                }])
                st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova_t], ignore_index=True)
                st.success("Tarefa adicionada!")
                st.rerun()
                
