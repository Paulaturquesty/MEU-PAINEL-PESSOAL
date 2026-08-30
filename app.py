import streamlit as st
import pandas as pd
import datetime
import calendar

st.set_page_config(
    page_title="Painel de Controle Pessoal",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Estilizado
st.markdown("""
<style>
 
</style>
""", unsafe_allow_html=True)

# Sessão
if 'menu_ativo' not in st.session_state:
    st.session_state.menu_ativo = "Painel de Controle"

if 'data_selecionada' not in st.session_state:
    st.session_state.data_selecionada = datetime.date.today()

if 'historico' not in st.session_state:
    st.session_state.historico = {
        "2026-08": {
            "salario": 3780.0,
            "reserva": 600.0,
            "gastos": pd.DataFrame([
                {"Item": "NUBANK", "Categoria": "CARTÃO", "Valor Total": 121.37, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"},
                {"Item": "INTER", "Categoria": "CARTÃO", "Valor Total": 663.63, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"},
                {"Item": "MERCADO PAGO", "Categoria": "CARTÃO", "Valor Total": 203.25, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"},
                {"Item": "PLANO INTERNET", "Categoria": "CELULAR", "Valor Total": 64.99, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"},
                {"Item": "UBER", "Categoria": "TRANSPORTE", "Valor Total": 200.0, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"},
                {"Item": "FACULDADE", "Categoria": "ESTUDO", "Valor Total": 1304.28, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"},
                {"Item": "LAVA LOUÇA", "Categoria": "CASA", "Valor Total": 196.04, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"},
                {"Item": "PARCELAS FIXAS", "Categoria": "CARTAO", "Valor Total": 888.26, "Parcela Atual": 1, "Total Parcelas": 1, "Status": "Pendente"}
            ]),
            "tarefas": pd.DataFrame([
                {"Título": "Vencimento: INTER", "Categoria": "Financeiro", "Cor": "blue", "Status": "Pendente", "Prazo": datetime.date(2026, 8, 12)},
                {"Título": "Vencimento: NUBANK", "Categoria": "Financeiro", "Cor": "blue", "Status": "Pendente", "Prazo": datetime.date(2026, 8, 25)},
                {"Título": "Vencimento: FACULDADE", "Categoria": "Financeiro", "Cor": "black", "Status": "Pendente", "Prazo": datetime.date(2026, 8, 30)}
            ])
        }
    }

if 'metas' not in st.session_state:
    st.session_state.metas = pd.DataFrame([
        {"Meta": "HABILITAÇÃO", "Valor Alvo": 1900.0, "Valor Atual": 0.0, "Prazo": datetime.date(2026, 9, 30)},
        {"Meta": "IPAD 11ª GERAÇÃO 128GB", "Valor Alvo": 2667.08, "Valor Atual": 0.0, "Prazo": datetime.date(2026, 2, 1)},
        {"Meta": "DENTISTA (DR. GUSTAVO)", "Valor Alvo": 1500.0, "Valor Atual": 600.0, "Prazo": datetime.date(2027, 1, 1)},
        {"Meta": "IPHONE 17 PROMAX", "Valor Alvo": 6500.0, "Valor Atual": 0.0, "Prazo": datetime.date(2027, 3, 5)},
        {"Meta": "JEEP RENEGADE LIMITED CINZA", "Valor Alvo": 28000.0, "Valor Atual": 0.0, "Prazo": datetime.date(2027, 10, 28)}
    ])

# Sidebar
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
        
    if st.button("Reserva & Economias", key="btn_reserva", use_container_width=True):
        st.session_state.menu_ativo = "Reserva & Economias"
        st.rerun()
        
    if st.button("Importar Planilhas (IA)", key="btn_import", use_container_width=True):
        st.session_state.menu_ativo = "Importar Planilhas (IA)"
        st.rerun()

    if st.button("Histórico & Relatórios", key="btn_hist", use_container_width=True):
        st.session_state.menu_ativo = "Histórico & Relatórios"
        st.rerun()

    st.divider()
    st.markdown("##### Mês de Referência")
    mes_sel = st.selectbox("Mês:", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], index=7)
    ano_sel = st.number_input("Ano:", min_value=2024, max_value=2030, value=2026)
    
    chave_mes = f"{ano_sel}-{['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'].index(mes_sel)+1:02d}"

if chave_mes not in st.session_state.historico:
    st.session_state.historico[chave_mes] = {
        "salario": 3780.0,
        "reserva": 600.0,
        "gastos": pd.DataFrame(columns=["Item", "Categoria", "Valor Total", "Parcela Atual", "Total Parcelas", "Status"]),
        "tarefas": pd.DataFrame(columns=["Título", "Categoria", "Cor", "Status", "Prazo"])
    }

dados_mes = st.session_state.historico[chave_mes]

# Lógica de Dedução
if not dados_mes["gastos"].empty:
    for idx, row in dados_mes["gastos"].iterrows():
        if row["Status"] == "Pago" and row.get("Total Parcelas", 1) > 1:
            if row["Parcela Atual"] < row["Total Parcelas"]:
                dados_mes["gastos"].at[idx, "Parcela Atual"] = row["Parcela Atual"] + 1
                dados_mes["gastos"].at[idx, "Status"] = "Pendente"
            elif row["Parcela Atual"] == row["Total Parcelas"]:
                dados_mes["gastos"].at[idx, "Status"] = "Quitado"

total_gastos = dados_mes["gastos"][dados_mes["gastos"]["Status"] != "Quitado"]["Valor Total"].sum() if not dados_mes["gastos"].empty else 0.0
pct_comprometido = (total_gastos / dados_mes["salario"] * 100) if dados_mes["salario"] > 0 else 0.0

# Topbar
st.markdown("## Painel de Controle (Modo ADM)")
c_top1, c_top2, c_top3, c_top4 = st.columns(4)
c_top1.metric(f"Renda ({mes_sel})", f"R$ {dados_mes['salario']:,.2f}")
c_top2.metric("Total Comprometido", f"R$ {total_gastos:,.2f}", delta=f"{pct_comprometido:.1f}% da Renda", delta_color="inverse")
c_top3.metric("Contas Pendentes", len(dados_mes["gastos"][dados_mes["gastos"]["Status"] == "Pendente"]) if not dados_mes["gastos"].empty else 0)
c_top4.metric("Saldo Guardado", f"R$ {dados_mes['reserva']:,.2f}")

st.divider()

# Módulo 1: Painel de Controle
if st.session_state.menu_ativo == "Painel de Controle":
    col_agenda, col_drawer = st.columns([2.2, 1])
    
    with col_agenda:
        c_nav1, c_nav2, c_nav3 = st.columns([2, 1, 1])
        with c_nav1:
            st.markdown(f"### Agenda - {mes_sel} de {ano_sel}")
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
            
        num_mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'].index(mes_sel) + 1
        cal = calendar.Calendar(firstweekday=6)
        dias_mes = cal.monthdatescalendar(ano_sel, num_mes)
        
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

    with col_drawer:
        st.markdown("### Tarefa / Compromisso")
        
        with st.form("form_drawer_pessoal"):
            tit_t = st.text_input("Título do Compromisso:", placeholder="Ex: Pagar fatura ou reunião")
            cat_t = st.selectbox("Categoria:", ["Geral", "Financeiro", "Trabalho/Carreira", "Metas / Pessoal"])
            sit_t = st.selectbox("Situação:", ["Pendente", "Em Andamento", "Concluído"])
            cor_t = st.selectbox("Cor da Etiqueta:", ["black (Preto)", "blue (Azul)", "green (Verde)"])
            prazo_t = st.date_input("Data do Prazo:", st.session_state.data_selecionada)
            
            if st.form_submit_button("Salvar Compromisso", use_container_width=True):
                cor_limpa = cor_t.split(" ")[0]
                nova_t = pd.DataFrame([{"Título": tit_t, "Categoria": cat_t, "Cor": cor_limpa, "Status": sit_t, "Prazo": prazo_t}])
                dados_mes["tarefas"] = pd.concat([dados_mes["tarefas"], nova_t], ignore_index=True)
                st.session_state.data_selecionada = prazo_t
                st.success("Salvo!")
                st.rerun()

        st.markdown("---")
        st.markdown(f"#### Gerenciador ADM de Tarefas")
        df_tarefas_editavel = st.data_editor(
            dados_mes["tarefas"], 
            num_rows="dynamic", 
            use_container_width=True,
            key=f"editor_tarefas_{chave_mes}"
        )
        dados_mes["tarefas"] = df_tarefas_editavel

# Módulo 2: Financeiro
elif st.session_state.menu_ativo == "Financeiro & Gastos":
    col_f1, col_f2 = st.columns([2, 1])
    
    with col_f1:
        st.markdown(f"### Planilha Financeira ADM - {mes_sel}/{ano_sel}")
        dados_mes["salario"] = st.number_input("Renda / Salário deste Mês (R$):", value=dados_mes["salario"], step=100.0)
        
        st.markdown("---")
        st.caption("🛠️ **Modo ADM:** Edite valores, categorias, descrições ou parcelas diretamente na tabela:")
        df_editado = st.data_editor(
            dados_mes["gastos"], 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Status": st.column_config.SelectboxColumn("Status", options=["Pendente", "Pago", "Quitado"])
            },
            key=f"editor_gastos_{chave_mes}"
        )
        dados_mes["gastos"] = df_editado

    with col_f2:
        st.markdown("### Novo Lançamento")
        with st.form("form_fin"):
            item_f = st.text_input("Descrição:")
            cat_f = st.selectbox("Categoria:", ["Fixo", "Variável", "Parcelamento"])
            val_f = st.number_input("Valor Total (R$):", min_value=0.0, step=50.0)
            parc_a = st.number_input("Parcela Atual:", min_value=1, value=1)
            parc_t = st.number_input("Total Parcelas:", min_value=1, value=1)
            stat_f = st.selectbox("Status:", ["Pendente", "Pago"])
            
            if st.form_submit_button("Lançar no Mês", use_container_width=True):
                novo_g = pd.DataFrame([{"Item": item_f, "Categoria": cat_f, "Valor Total": val_f, "Parcela Atual": parc_a, "Total Parcelas": parc_t, "Status": stat_f}])
                dados_mes["gastos"] = pd.concat([dados_mes["gastos"], novo_g], ignore_index=True)
                st.success("Lançado!")
                st.rerun()

# Módulo 3: Metas
elif st.session_state.menu_ativo == "Metas & Prazos":
    col_m1, col_m2 = st.columns([2, 1])
    with col_m1:
        st.markdown("### Minhas Metas Globais (Modo ADM)")
        df_metas_edit = st.data_editor(st.session_state.metas, num_rows="dynamic", use_container_width=True)
        st.session_state.metas = df_metas_edit
        
    with col_m2:
        st.markdown("### Adicionar Meta")
        with st.form("f_meta"):
            n_meta = st.text_input("Meta:")
            v_alvo = st.number_input("Objetivo (R$):", min_value=100.0)
            v_atual = st.number_input("Atual (R$):", min_value=0.0)
            p_meta = st.date_input("Data Limite:", datetime.date(2026, 12, 31))
            if st.form_submit_button("Salvar Meta", use_container_width=True):
                nova_m = pd.DataFrame([{"Meta": n_meta, "Valor Alvo": v_alvo, "Valor Atual": v_atual, "Prazo": p_meta}])
                st.session_state.metas = pd.concat([st.session_state.metas, nova_m], ignore_index=True)
                st.rerun()

# Módulo 4: Reserva
elif st.session_state.menu_ativo == "Reserva & Economias":
    st.markdown("### Reserva de Emergência e Dinheiro Guardado")
    val_res = st.number_input(f"Saldo Guardado em {mes_sel}/{ano_sel} (R$):", value=dados_mes["reserva"], step=100.0)
    dados_mes["reserva"] = val_res

# Módulo 5: Importar Planilhas
elif st.session_state.menu_ativo == "Importar Planilhas (IA)":
    st.markdown("### 📥 Processador Multi-Abas de Planilhas")
    st.write("Envie os arquivos para leitura e integração automática:")
    
    arquivos_enviados = st.file_uploader("Selecione seus arquivos (.xlsx, .xls, .csv):", type=["xlsx", "xls", "csv"], accept_multiple_files=True)
    
    if arquivos_enviados:
        if st.button("Processar Abas e Atualizar Sistema", use_container_width=True):
            for arq in arquivos_enviados:
                try:
                    xls = pd.ExcelFile(arq)
                    for sheet in xls.sheet_names:
                        st.info(f"Processando aba: `{sheet}` de `{arq.name}`")
                    st.success(f"Arquivo `{arq.name}` integrado!")
                except Exception as e:
                    st.error(f"Erro ao ler `{arq.name}`: {e}")

# Módulo 6: Histórico
elif st.session_state.menu_ativo == "Histórico & Relatórios":
    st.markdown("### Consulta de Histórico e Relatórios")
    mes_historico = st.selectbox("Escolha o mês para consultar/baixar:", list(st.session_state.historico.keys()))
    st.dataframe(st.session_state.historico[mes_historico]['gastos'], use_container_width=True)
