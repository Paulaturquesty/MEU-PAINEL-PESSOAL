import streamlit as st
import pandas as pd
import datetime
import calendar

# Configuração da página
st.set_page_config(
    page_title="Painel de Gestão Pessoal",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FORMATADOR DE MOEDA BRASILEIRA (R$ 1.000,00)
def formata_reais(valor):
    try:
        val = float(valor)
        return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"

# ESTILIZAÇÃO CSS (Inspirada na UI Juris Control)
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

# INICIALIZAÇÃO DA SESSÃO GLOBAL
if 'menu_ativo' not in st.session_state:
    st.session_state.menu_ativo = "Painel de Controle"

if 'data_selecionada' not in st.session_state:
    st.session_state.data_selecionada = datetime.date.today()

if 'historico' not in st.session_state:
    st.session_state.historico = {
        "08/2026": {
            "rendas": pd.DataFrame([
                {"Descrição": "Salário PCA", "Valor Previsto": 1700.0, "Valor Recebido": 1700.0, "Data Recebimento": "06/07/2026"},
                {"Descrição": "Salário Leandro", "Valor Previsto": 1000.0, "Valor Recebido": 1000.0, "Data Recebimento": "28/08/2026"},
                {"Descrição": "Salário Aider Box", "Valor Previsto": 1080.0, "Valor Recebido": 1080.0, "Data Recebimento": "28/08/2026"}
            ]),
            "gastos": pd.DataFrame([
                {"Descrição": "NUBANK", "Categoria": "CARTÃO", "Valor": 121.37, "Data Vencimento": "25/09/2026", "Status": "Pendente"},
                {"Descrição": "INTER", "Categoria": "CARTÃO", "Valor": 663.63, "Data Vencimento": "12/09/2026", "Status": "Pendente"},
                {"Descrição": "MERCADO PAGO", "Categoria": "CARTÃO", "Valor": 203.25, "Data Vencimento": "07/09/2026", "Status": "Pendente"},
                {"Descrição": "PLANO INTERNET", "Categoria": "CELULAR", "Valor": 64.99, "Data Vencimento": "15/09/2026", "Status": "Pendente"},
                {"Descrição": "UBER", "Categoria": "TRANSPORTE", "Valor": 200.0, "Data Vencimento": "01/09/2026", "Status": "Pendente"},
                {"Descrição": "FACULDADE", "Categoria": "ESTUDO", "Valor": 1304.28, "Data Vencimento": "30/09/2026", "Status": "Pendente"},
                {"Descrição": "LAVA LOUÇA", "Categoria": "CASA", "Valor": 196.04, "Data Vencimento": "08/09/2026", "Status": "Pendente"},
                {"Descrição": "ENERGIA", "Categoria": "CASA", "Valor": 200.0, "Data Vencimento": "14/09/2026", "Status": "Pendente"},
                {"Descrição": "PARCELAS FIXAS", "Categoria": "CARTAO", "Valor": 888.26, "Data Vencimento": "07/09/2026", "Status": "Pendente"}
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

if 'historico_aportes' not in st.session_state:
    st.session_state.historico_aportes = pd.DataFrame([
        {"Nome da Meta": "DENTISTA (DR. GUSTAVO)", "Mês / Referência": "07/2026", "Valor Aportado (R$)": 600.0, "Data do Lançamento": "01/07/2026"}
    ])

# NAVEGAÇÃO LATERAL (SIDEBAR)
with st.sidebar:
    st.markdown("### Painel Pessoal")
    st.caption("v5.2.0 | Acesso ADM")
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

if "tarefas" not in dados_mes:
    dados_mes["tarefas"] = pd.DataFrame(columns=["Título", "Contexto", "Prioridade", "Status", "Prazo"])

# CÁLCULOS DINÂMICOS
total_entradas = float(dados_mes["rendas"]["Valor Recebido"].sum()) if ("Valor Recebido" in dados_mes["rendas"].columns and not dados_mes["rendas"].empty) else 0.0
total_gastos = float(dados_mes["gastos"]["Valor"].sum()) if ("Valor" in dados_mes["gastos"].columns and not dados_mes["gastos"].empty) else 0.0
saldo_restante = total_entradas - total_gastos

# TOPBAR INSPIRADA NA UI (CARDS DE RESUMO)
st.markdown("## Painel de Controle")
c_top1, c_top2, c_top3, c_top4 = st.columns(4)
c_top1.metric(f"Total Recebido ({mes_sel})", formata_reais(total_entradas))
c_top2.metric("Total Gasto", formata_reais(total_gastos))
c_top3.metric("Saldo Restante", formata_reais(saldo_restante), delta=formata_reais(saldo_restante))
contas_pend = len(dados_mes["gastos"][dados_mes["gastos"]["Status"] == "Pendente"]) if ("Status" in dados_mes["gastos"].columns and not dados_mes["gastos"].empty) else 0
c_top4.metric("Contas Pendentes", contas_pend)

st.divider()

# MÓDULO 1: PAINEL DE CONTROLE (AGENDA + TAREFAS)
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
                    
                    tarefas_df = dados_mes.get("tarefas", pd.DataFrame())
                    tarefas_dia = pd.DataFrame()
                    if not tarefas_df.empty and "Prazo" in tarefas_df.columns:
                        tarefas_dia = tarefas_df[tarefas_df['Prazo'] == dia]
                    
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
                st.session_state.historico[mes_sel]["tarefas"] = pd.concat([dados_mes.get("tarefas", pd.DataFrame()), nova_t], ignore_index=True)
                st.session_state.data_selecionada = prazo_t
                st.success("Salvo!")
                st.rerun()

        st.markdown("---")
        st.markdown(f"#### Gerenciador ADM de Tarefas")
        
        tarefas_para_editar = dados_mes.get("tarefas", pd.DataFrame(columns=["Título", "Contexto", "Prioridade", "Status", "Prazo"]))
        
        res_tarefas = st.data_editor(
            tarefas_para_editar, 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Prioridade": st.column_config.SelectboxColumn("Prioridade", options=["🔴 Alta", "🟡 Média", "🟢 Baixa"]),
                "Status": st.column_config.SelectboxColumn("Status", options=["A Fazer", "Em Andamento", "Concluído"])
            }
        )
        st.session_state.historico[mes_sel]["tarefas"] = res_tarefas

# MÓDULO 2: FINANCEIRO & GASTOS
elif st.session_state.menu_ativo == "Financeiro & Gastos":
    st.markdown(f"### Painel Financeiro - Referência {mes_sel}")
    st.caption("💡 Edição instantânea célula a célula:")
    
    aba_rendas, aba_despesas = st.tabs(["💵 Rendas / Salários", "💸 Despesas & Gastos"])
    
    with aba_rendas:
        st.markdown("#### Entradas do Mês")
        res_rendas = st.data_editor(
            dados_mes["rendas"], 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Valor Previsto": st.column_config.NumberColumn("Valor Previsto", format="R$ %.2f"),
                "Valor Recebido": st.column_config.NumberColumn("Valor Recebido", format="R$ %.2f")
            }
        )
        st.session_state.historico[mes_sel]["rendas"] = res_rendas

    with aba_despesas:
        st.markdown("#### Despesas & Contas")
        res_gastos = st.data_editor(
            dados_mes["gastos"], 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
                "Status": st.column_config.SelectboxColumn("Status", options=["Pendente", "Pago"])
            }
        )
        st.session_state.historico[mes_sel]["gastos"] = res_gastos

# MÓDULO 3: METAS E PRAZOS (ISOLADA)
elif st.session_state.menu_ativo == "Metas & Prazos":
    st.markdown("### Aba de Metas e Prazos (Isolada)")
    st.caption("ℹ️ **Regra de Escopo:** Os valores cadastrados aqui ficam restritos a esta aba e não entram no cálculo de despesas mensais.")
    
    res_metas = st.data_editor(
        st.session_state.metas, 
        num_rows="dynamic", 
        use_container_width=True, 
        column_config={
            "Valor Alvo (R$)": st.column_config.NumberColumn("Valor Alvo (R$)", format="R$ %.2f"),
            "Valor Já Guardado": st.column_config.NumberColumn("Valor Já Guardado", format="R$ %.2f")
        }
    )
    st.session_state.metas = res_metas
    
    st.markdown("---")
    st.markdown("#### Progresso & Aporte Mensal Sugerido")
    
    for idx, row in st.session_state.metas.iterrows():
        val_alvo = float(row.get("Valor Alvo (R$)", 1.0))
        val_guardado = float(row.get("Valor Já Guardado", 0.0))
        falta = max(val_alvo - val_guardado, 0.0)
        pct = min((val_guardado / val_alvo) if val_alvo > 0 else 0.0, 1.0)
        
        aporte_sugerido = falta / 6.0
        
        col_m1, col_m2 = st.columns([3, 1])
        with col_m1:
            st.write(f"**{row['Nome da Meta']}** — Guardado: **{formata_reais(val_guardado)}** de **{formata_reais(val_alvo)}** | **Falta: {formata_reais(falta)}** | Prazo: {row['Prazo']}")
            st.progress(pct)
        with col_m2:
            st.caption(f"Aporte Sugerido: **{formata_reais(aporte_sugerido)} /mês**")

    st.markdown("---")
    st.markdown("### 💰 Histórico de Economia / Aportes Mensais por Meta")
    st.caption("Registre aqui quanto você conseguiu guardar em cada mês para cada meta específica:")
    
    col_ap1, col_ap2 = st.columns([1, 2])
    
    with col_ap1:
        st.markdown("##### ➕ Lançar Novo Aporte")
        with st.form("form_novo_aporte"):
            meta_escolhida = st.selectbox("Escolha a Meta:", st.session_state.metas["Nome da Meta"].unique())
            mes_ref_aporte = st.selectbox("Mês de Referência:", ["06/2026", "07/2026", "08/2026", "09/2026", "10/2026", "11/2026", "12/2026"], index=2)
            valor_aportado = st.number_input("Quanto guardou neste mês (R$):", min_value=0.0, step=50.0)
            data_reg = st.date_input("Data do Registro:", datetime.date.today())
            
            if st.form_submit_button("Salvar Aporte do Mês", use_container_width=True):
                novo_ap = pd.DataFrame([{
                    "Nome da Meta": meta_escolhida,
                    "Mês / Referência": mes_ref_aporte,
                    "Valor Aportado (R$)": valor_aportado,
                    "Data do Lançamento": data_reg.strftime("%d/%m/%Y")
                }])
                st.session_state.historico_aportes = pd.concat([st.session_state.historico_aportes, novo_ap], ignore_index=True)
                
                idx_meta = st.session_state.metas[st.session_state.metas["Nome da Meta"] == meta_escolhida].index
                if not idx_meta.empty:
                    val_antigo = float(st.session_state.metas.loc[idx_meta[0], "Valor Já Guardado"])
                    st.session_state.metas.loc[idx_meta[0], "Valor Já Guardado"] = val_antigo + valor_aportado
                
                st.success(f"Aporte de {formata_reais(valor_aportado)} adicionado à meta '{meta_escolhida}'!")
                st.rerun()

    with col_ap2:
        st.markdown("##### 📜 Extrato de Aportes Realizados no Tempo")
        res_aportes = st.data_editor(
            st.session_state.historico_aportes,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Valor Aportado (R$)": st.column_config.NumberColumn("Valor Aportado (R$)", format="R$ %.2f")
            }
        )
        st.session_state.historico_aportes = res_aportes

# MÓDULO 4: IMPORTAR PLANILHAS
elif st.session_state.menu_ativo == "Importar Planilhas (IA)":
    st.markdown("### 📥 Importador Minucioso de Planilhas Excel")
    st.write("Envie seus arquivos `.xlsx` para distribuição automática e estruturada:")
    
    arquivos_enviados = st.file_uploader("Selecione seus arquivos (.xlsx ou .csv):", type=["xlsx", "xls", "csv"], accept_multiple_files=True)
    
    if arquivos_enviados:
        if st.button("Processar e Distribuir Dados", use_container_width=True):
            for arq in arquivos_enviados:
                try:
                    if arq.name.endswith('.csv'):
                        df_imp = pd.read_csv(arq)
                        st.info(f"Arquivo CSV `{arq.name}` lido.")
                    else:
                        xls = pd.ExcelFile(arq)
                        for sheet in xls.sheet_names:
                            sheet_clean = sheet.strip()
                            
                            if sheet_clean in ['062026', '072026', '082026', '092026']:
                                mes_chave = f"{sheet_clean[:2]}/{sheet_clean[2:]}"
                                df_raw = pd.read_excel(xls, sheet_name=sheet)
                                
                                df_gastos_raw = df_raw.iloc[2:, 8:15].dropna(subset=[df_raw.columns[8]])
                                if not df_gastos_raw.empty:
                                    df_gastos_raw.columns = ['Descrição', 'Data Vencimento', 'Categoria', 'Valor', 'Detalhes', 'Método', 'Pago_Bool']
                                    df_gastos_raw['Status'] = df_gastos_raw['Pago_Bool'].apply(lambda x: 'Pago' if x == True else 'Pendente')
                                    df_gastos_raw['Valor'] = pd.to_numeric(df_gastos_raw['Valor'], errors='coerce').fillna(0.0)
                                    
                                    if mes_chave not in st.session_state.historico:
                                        st.session_state.historico[mes_chave] = {
                                            "rendas": pd.DataFrame(columns=["Descrição", "Valor Previsto", "Valor Recebido", "Data Recebimento"]),
                                            "gastos": pd.DataFrame(),
                                            "tarefas": pd.DataFrame(columns=["Título", "Contexto", "Prioridade", "Status", "Prazo"])
                                        }
                                    st.session_state.historico[mes_chave]["gastos"] = df_gastos_raw[['Descrição', 'Categoria', 'Valor', 'Data Vencimento', 'Status']]
                                
                                if len(df_raw.columns) >= 20:
                                    df_rendas_raw = df_raw.iloc[2:, 16:20].dropna(subset=[df_raw.columns[16]])
                                    if not df_rendas_raw.empty:
                                        df_rendas_raw.columns = ['Descrição', 'Data Recebimento', 'Categoria', 'Valor Recebido']
                                        df_rendas_raw['Valor Previsto'] = pd.to_numeric(df_rendas_raw['Valor Recebido'], errors='coerce').fillna(0.0)
                                        df_rendas_raw['Valor Recebido'] = pd.to_numeric(df_rendas_raw['Valor Recebido'], errors='coerce').fillna(0.0)
                                        st.session_state.historico[mes_chave]["rendas"] = df_rendas_raw[['Descrição', 'Valor Previsto', 'Valor Recebido', 'Data Recebimento']]

                            elif 'METAS' in sheet_clean.upper() or 'PLANEJAMENTO' in sheet_clean.upper():
                                df_metas_raw = pd.read_excel(xls, sheet_name=sheet, skiprows=10)
                                if 'Meta | Item a Comprar' in df_metas_raw.columns:
                                    df_m_clean = df_metas_raw[['Meta | Item a Comprar', 'Valor Necessário', 'Valor Guardado', 'Data Alvo']].dropna(subset=['Meta | Item a Comprar'])
                                    df_m_clean.columns = ['Nome da Meta', 'Valor Alvo (R$)', 'Valor Já Guardado', 'Prazo']
                                    df_m_clean['Valor Alvo (R$)'] = pd.to_numeric(df_m_clean['Valor Alvo (R$)'], errors='coerce').fillna(0.0)
                                    df_m_clean['Valor Já Guardado'] = pd.to_numeric(df_m_clean['Valor Já Guardado'], errors='coerce').fillna(0.0)
                                    st.session_state.metas = df_m_clean

                    st.success(f"✅ Arquivo `{arq.name}` integrado perfeitamente!")
                except Exception as e:
                    st.error(f"Erro ao processar `{arq.name}`: {e}")

# MÓDULO 5: HISTÓRICO
elif st.session_state.menu_ativo == "Histórico & Relatórios":
    st.markdown("### Relatórios do Mês")
    st.dataframe(dados_mes["gastos"], use_container_width=True)
