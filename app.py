import streamlit as st
import pandas as pd
import datetime
import calendar

# Configuração da página - Layout Wide
st.set_page_config(
    page_title="Painel de Controle Pessoal",
    page_icon=":material/calendar_today:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DESIGN SYSTEM & CSS (SAAS FLAT DESIGN 2.0 / PLUS JAKARTA SANS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, button, input, select, textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* DARK SIDEBAR (#0B111E) */
    [data-testid="stSidebar"] {
        background-color: #0b111e !important;
        border-right: 1px solid #1e293b;
    }

    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #94a3b8 !important;
        font-weight: 500;
    }

    /* BOTÕES DO MENU LATERAL */
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

    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] div.stButton > button > div {
        text-align: left !important;
        width: 100% !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        gap: 10px !important;
    }

    /* AREA PRINCIPAL */
    .main {
        background-color: #f8fafc;
    }

    /* CARDS KPI / TOPBAR */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 18px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }

    /* CABEÇALHO DO CALENDÁRIO & NAVEGAÇÃO */
    .cal-nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .cal-header-day {
        text-align: center;
        font-weight: 600;
        color: #64748b;
        padding: 6px;
        font-size: 12px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    /* CÉLULAS DOS DIAS DO GRID */
    .cal-cell {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        min-height: 92px;
        padding: 6px;
        margin-bottom: 4px;
        transition: border-color 0.15s ease-in-out;
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

    /* MARCADOR CIRCULAR PARA DIA ATUAL/SELECIONADO (EX: DIA 28) */
    .cal-date-selected {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 50%;
        font-weight: 600;
    }

    /* EVENT BADGES (PILL CHIPS) */
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

    .badge-black { background-color: #0f172a; }
    .badge-blue { background-color: #2563eb; }
    .badge-green { background-color: #16a34a; }
</style>
""", unsafe_allow_html=True)

# --- GERENCIAMENTO DE ESTADO DE NAVEGAÇÃO ---
if 'menu_ativo' not in st.session_state:
    st.session_state.menu_ativo = "Painel de Controle"

if 'data_selecionada' not in st.session_state:
    st.session_state.data_selecionada = datetime.date.today()

# --- BANCO DE DADOS EM SESSÃO ---
if 'historico' not in st.session_state:
    st.session_state.historico = {
        "2026-08": {
            "salario": 5000.0,
            "reserva": 1500.0,
            "gastos": pd.DataFrame([
                {"Item": "Aluguel", "Categoria": "Fixo", "Valor Total": 1500.0, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pago"},
                {"Item": "Cartão de Crédito", "Categoria": "Variável", "Valor Total": 1200.0, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"},
                {"Item": "Financiamento TV", "Categoria": "Parcelamento", "Valor Total": 2400.0, "Parcela Atual": 6, "Total Parcelas": 12, "Status": "Pendente"}
            ]),
            "tarefas": pd.DataFrame([
                {"Título": "Revisão Geral do Mês", "Categoria": "Geral", "Cor": "black", "Status": "Pendente", "Prazo": datetime.date(2026, 8, 28)},
                {"Título": "Pagar Fatura Cartão", "Categoria": "Financeiro", "Cor": "blue", "Status": "Pendente", "Prazo": datetime.date(2026, 8, 28)},
                {"Título": "Comprovação de Pagamento", "Categoria": "Financeiro", "Cor": "green", "Status": "Concluído", "Prazo": datetime.date(2026, 8, 27)}
            ])
        }
    }

if 'metas' not in st.session_state:
    st.session_state.metas = pd.DataFrame([
        {"Meta": "Reserva de Emergência", "Valor Alvo": 10000.0, "Valor Atual": 3500.0, "Prazo": datetime.date(2026, 12, 31)}
    ])

# --- BARRA LATERAL (SIDEBAR DARK THEME) ---
with st.sidebar:
    st.markdown("### Painel Pessoal")
    st.caption("v1.0.0 | Acesso Privado")
    st.divider()
    
    if st.button("Painel de Controle", icon=":material/dashboard:", key="btn_painel", use_container_width=True):
        st.session_state.menu_ativo = "Painel de Controle"
        st.rerun()
        
    if st.button("Financeiro & Gastos", icon=":material/credit_card:", key="btn_fin", use_container_width=True):
        st.session_state.menu_ativo = "Financeiro & Gastos"
        st.rerun()
        
    if st.button("Metas & Prazos", icon=":material/hourglass_empty:", key="btn_metas", use_container_width=True):
        st.session_state.menu_ativo = "Metas & Prazos"
        st.rerun()
        
    if st.button("Reserva & Economias", icon=":material/account_balance:", key="btn_reserva", use_container_width=True):
        st.session_state.menu_ativo = "Reserva & Economias"
        st.rerun()
        
    if st.button("Histórico & Relatórios", icon=":material/description:", key="btn_hist", use_container_width=True):
        st.session_state.menu_ativo = "Histórico & Relatórios"
        st.rerun()

    st.divider()
    st.markdown("##### Mês de Referência")
    mes_sel = st.selectbox("Mês:", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], index=7)
    ano_sel = st.number_input("Ano:", min_value=2024, max_value=2030, value=2026)
    
    chave_mes = f"{ano_sel}-{['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'].index(mes_sel)+1:02d}"

if chave_mes not in st.session_state.historico:
    st.session_state.historico[chave_mes] = {
        "salario": 5000.0,
        "reserva": 0.0,
        "gastos": pd.DataFrame(columns=["Item", "Categoria", "Valor Total", "Parcela Atual", "Total Parcelas", "Status"]),
        "tarefas": pd.DataFrame(columns=["Título", "Categoria", "Cor", "Status", "Prazo"])
    }

dados_mes = st.session_state.historico[chave_mes]

# LÓGICA AUTOMÁTICA DE PARCELAMENTO
if not dados_mes["gastos"].empty:
    for idx, row in dados_mes["gastos"].iterrows():
        if row["Status"] == "Pago" and row["Total Parcelas"] > 1:
            if row["Parcela Atual"] < row["Total Parcelas"]:
                dados_mes["gastos"].at[idx, "Parcela Atual"] = row["Parcela Atual"] + 1
                dados_mes["gastos"].at[idx, "Status"] = "Pendente"
            elif row["Parcela Atual"] == row["Total Parcelas"]:
                dados_mes["gastos"].at[idx, "Status"] = "Quitado"

total_gastos = dados_mes["gastos"][dados_mes["gastos"]["Status"] != "Quitado"]["Valor Total"].sum() if not dados_mes["gastos"].empty else 0.0
pct_comprometido = (total_gastos / dados_mes["salario"] * 100) if dados_mes["salario"] > 0 else 0.0

# --- TOPBAR DA PÁGINA ---
st.markdown("## Painel de Controle")
c_top1, c_top2, c_top3, c_top4 = st.columns(4)
c_top1.metric(f"Renda ({mes_sel})", f"R$ {dados_mes['salario']:,.2f}")
c_top2.metric("Total Comprometido", f"R$ {total_gastos:,.2f}", delta=f"{pct_comprometido:.1f}% da Renda", delta_color="inverse")
c_top3.metric("Contas Pendentes", len(dados_mes["gastos"][dados_mes["gastos"]["Status"] == "Pendente"]) if not dados_mes["gastos"].empty else 0)
c_top4.metric("Saldo Guardado", f"R$ {dados_mes['reserva']:,.2f}")

st.divider()

# --- MÓDULO 1: PAINEL DE CONTROLE (GRID MENSUAL COMPACTO + DRAWER) ---
if st.session_state.menu_ativo == "Painel de Controle":
    
    col_agenda, col_drawer = st.columns([2.2, 1])
    
    # CONTROLE CENTRAL: GRID DO CALENDÁRIO
    with col_agenda:
        # Cabeçalho de Controle e Navegação do Período
        c_nav1, c_nav2, c_nav3 = st.columns([2, 1, 1])
        with c_nav1:
            st.markdown(f"### Agenda - {mes_sel} de {ano_sel}")
        with c_nav2:
            if st.button("Hoje", icon=":material/today:", use_container_width=True):
                st.session_state.data_selecionada = datetime.date.today()
                st.rerun()
        with c_nav3:
            st.caption(f"Data Ativa: {st.session_state.data_selecionada.strftime('%d/%m/%Y')}")

        # Dias da Semana
        dias_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"]
        cols_h = st.columns(7)
        for i, d in enumerate(dias_semana):
            cols_h[i].markdown(f"<div class='cal-header-day'>{d}</div>", unsafe_allow_html=True)
            
        num_mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'].index(mes_sel) + 1
        cal = calendar.Calendar(firstweekday=6)
        dias_mes = cal.monthdatescalendar(ano_sel, num_mes)
        
        # Grid Mensal (Linhas x Colunas)
        for semana in dias_mes:
            cols_s = st.columns(7)
            for i, dia in enumerate(semana):
                with cols_s[i]:
                    is_in_month = (dia.month == num_mes)
                    is_selected = (dia == st.session_state.data_selecionada)
                    
                    cell_class = "cal-cell" if is_in_month else "cal-cell-out"
                    num_class = "cal-date-number cal-date-selected" if is_selected else "cal-date-number"
                    
                    tarefas_dia = dados_mes["tarefas"][dados_mes["tarefas"]['Prazo'] == dia] if not dados_mes["tarefas"].empty else pd.DataFrame()
                    
                    html_badges = ""
                    if not tarefas_dia.empty:
                        for _, t in tarefas_dia.iterrows():
                            cor_badge = t.get("Cor", "black")
                            html_badges += f"<div class='badge-pill badge-{cor_badge}'>{t['Título']}</div>"
                    
                    st.markdown(f"""
                        <div class='{cell_class}'>
                            <span class='{num_class}'>{dia.day}</span>
                            {html_badges}
                        </div>
                    """, unsafe_allow_html=True)

    # DRAWER LATERAL DIREITO (PAINEL DE CRIAÇÃO E STATUS)
    with col_drawer:
        st.markdown("### Tarefa / Compromisso")
        
        with st.form("form_drawer_pessoal"):
            tit_t = st.text_input("Título do Compromisso:", placeholder="Ex: Pagar fatura ou reunião")
            cat_t = st.selectbox("Categoria:", ["Geral", "Financeiro", "Trabalho/Carreira", "Metas / Pessoal"])
            sit_t = st.selectbox("Situação:", ["Pendente", "Em Andamento", "Concluído"])
            cor_t = st.selectbox("Cor da Etiqueta:", ["black (Preto)", "blue (Azul)", "green (Verde)"])
            prazo_t = st.date_input("Data do Prazo:", st.session_state.data_selecionada)
            
            if st.form_submit_button("Salvar Compromisso", icon=":material/save:", use_container_width=True):
                cor_limpa = cor_t.split(" ")[0]
                nova_t = pd.DataFrame([{"Título": tit_t, "Categoria": cat_t, "Cor": cor_limpa, "Status": sit_t, "Prazo": prazo_t}])
                dados_mes["tarefas"] = pd.concat([dados_mes["tarefas"], nova_t], ignore_index=True)
                st.session_state.data_selecionada = prazo_t
                st.success("Salvo!")
                st.rerun()

        st.markdown("---")
        st.markdown(f"#### Compromissos em {st.session_state.data_selecionada.strftime('%d/%m/%Y')}")
        tarefas_filtradas = dados_mes["tarefas"][dados_mes["tarefas"]['Prazo'] == st.session_state.data_selecionada] if not dados_mes["tarefas"].empty else pd.DataFrame()
        
        if not tarefas_filtradas.empty:
            for idx, row in tarefas_filtradas.iterrows():
                c_chk, c_txt = st.columns([0.2, 0.8])
                chk = c_chk.checkbox("", value=(row['Status'] == 'Concluído'), key=f"t_draw_p_{chave_mes}_{idx}")
                dados_mes["tarefas"].loc[dados_mes["tarefas"]['Título'] == row['Título'], 'Status'] = 'Concluído' if chk else 'Pendente'
                c_txt.write(f"**{row['Título']}** ({row['Categoria']})")
        else:
            st.caption("Nenhum compromisso cadastrado nesta data.")

# --- MÓDULO 2: FINANCEIRO & GASTOS ---
elif st.session_state.menu_ativo == "Financeiro & Gastos":
    col_f1, col_f2 = st.columns([2, 1])
    
    with col_f1:
        st.markdown(f"### Planilha Financeira de {mes_sel}/{ano_sel}")
        dados_mes["salario"] = st.number_input("Renda / Salário deste Mês (R$):", value=dados_mes["salario"], step=100.0)
        
        st.markdown("---")
        st.caption("Marque o Status como 'Pago' para decrementar automaticamente a parcela:")
        df_editado = st.data_editor(
            dados_mes["gastos"], 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Status": st.column_config.SelectboxColumn("Status", options=["Pendente", "Pago", "Quitado"])
            }
        )
        dados_mes["gastos"] = df_editado
        
        st.markdown("#### Progresso Geral de Quitação")
        if not dados_mes["gastos"].empty:
            for _, row in dados_mes["gastos"].iterrows():
                if row.get('Total Parcelas', 1) > 1:
                    prog = row['Parcela Atual'] / row['Total Parcelas']
                    status_txt = "QUITADO" if row["Status"] == "Quitado" else f"Parcela {row['Parcela Atual']}/{row['Total Parcelas']}"
                    st.write(f"**{row['Item']}** — {status_txt}")
                    st.progress(min(prog, 1.0))

    with col_f2:
        st.markdown("### Novo Lançamento")
        with st.form("form_fin"):
            item_f = st.text_input("Descrição:")
            cat_f = st.selectbox("Categoria:", ["Fixo", "Variável", "Parcelamento"])
            val_f = st.number_input("Valor Total (R$):", min_value=0.0, step=50.0)
            parc_a = st.number_input("Parcela Atual:", min_value=1, value=1)
            parc_t = st.number_input("Total Parcelas:", min_value=1, value=1)
            stat_f = st.selectbox("Status:", ["Pendente", "Pago"])
            
            if st.form_submit_button("Lançar no Mês", icon=":material/post_add:", use_container_width=True):
                novo_g = pd.DataFrame([{"Item": item_f, "Categoria": cat_f, "Valor Total": val_f, "Parcela Atual": parc_a, "Total Parcelas": parc_t, "Status": stat_f}])
                dados_mes["gastos"] = pd.concat([dados_mes["gastos"], novo_g], ignore_index=True)
                st.success("Lançado!")
                st.rerun()

# --- MÓDULO 3: METAS ---
elif st.session_state.menu_ativo == "Metas & Prazos":
    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
        st.markdown("### Minhas Metas Globais")
        for idx, row in st.session_state.metas.iterrows():
            pct = (row['Valor Atual'] / row['Valor Alvo']) if row['Valor Alvo'] > 0 else 0
            st.write(f"**{row['Meta']}** — R$ {row['Valor Atual']:,.2f} de R$ {row['Valor Alvo']:,.2f}")
            st.progress(min(pct, 1.0))
            st.caption(f"Falta guardar: R$ {(row['Valor Alvo'] - row['Valor Atual']):,.2f} | Prazo: {row['Prazo']}")
            st.markdown("---")
            
    with col_m2:
        st.markdown("### Adicionar Meta")
        with st.form("f_meta"):
            n_meta = st.text_input("Meta:")
            v_alvo = st.number_input("Objetivo (R$):", min_value=100.0)
            v_atual = st.number_input("Atual (R$):", min_value=0.0)
            p_meta = st.date_input("Data Limite:", datetime.date(2026, 12, 31))
            if st.form_submit_button("Salvar Meta", icon=":material/flag:", use_container_width=True):
                nova_m = pd.DataFrame([{"Meta": n_meta, "Valor Alvo": v_alvo, "Valor Atual": v_atual, "Prazo": p_meta}])
                st.session_state.metas = pd.concat([st.session_state.metas, nova_m], ignore_index=True)
                st.rerun()

# --- MÓDULO 4: RESERVA & ECONOMIAS ---
elif st.session_state.menu_ativo == "Reserva & Economias":
    st.markdown("### Reserva de Emergência e Dinheiro Guardado")
    val_res = st.number_input(f"Saldo Guardado em {mes_sel}/{ano_sel} (R$):", value=dados_mes["reserva"], step=100.0)
    dados_mes["reserva"] = val_res
    
    st.markdown("---")
    alvo_reserva = dados_mes["salario"] * 6
    pct_r = (dados_mes["reserva"] / alvo_reserva) if alvo_reserva > 0 else 0
    st.markdown(f"**Meta Recomendada (6 meses de renda):** R$ {alvo_reserva:,.2f}")
    st.progress(min(pct_r, 1.0))
    st.caption(f"Você já acumulou **{(pct_r * 100):.1f}%** da sua reserva ideal de segurança.")

# --- MÓDULO 5: HISTÓRICO & RELATÓRIOS ---
elif st.session_state.menu_ativo == "Histórico & Relatórios":
    st.markdown("### Consulta de Histórico e Baixar Relatórios")
    mes_historico = st.selectbox("Escolha o mês para consultar/baixar:", list(st.session_state.historico.keys()))
    dados_h = st.session_state.historico[mes_historico]
    
    st.markdown(f"#### Resumo do Mês ({mes_historico})")
    st.write(f"- **Renda do Mês:** R$ {dados_h['salario']:,.2f}")
    st.write(f"- **Total Gastos:** R$ {dados_h['gastos']['Valor Total'].sum() if not dados_h['gastos'].empty else 0.0:,.2f}")
    st.write(f"- **Reserva no Mês:** R$ {dados_h['reserva']:,.2f}")
    
    st.markdown("#### Gastos do Mês Selecionado:")
    st.dataframe(dados_h['gastos'], use_container_width=True)
    
    if not dados_h['gastos'].empty:
        csv_data = dados_h['gastos'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Baixar Relatório de {mes_historico} (CSV)",
            icon=":material/download:",
            data=csv_data,
            file_name=f"relatorio_financeiro_{mes_historico}.csv",
            mime="text/csv"
        )
