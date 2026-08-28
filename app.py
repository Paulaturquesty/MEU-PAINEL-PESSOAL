import streamlit as st
import pandas as pd
import datetime
import calendar

# Configuração visual avançada (Design Corporativo)
st.set_page_config(
    page_title="Painel de Controle Pessoal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado - Fonte Plus Jakarta Sans e Tema Escuro Elegante no Menu
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, button, input, select, textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* BARRA LATERAL (Menu Escuro Corporativo #0B111E) */
    [data-testid="stSidebar"] {
        background-color: #0B111E !important;
    }
    
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #94A3B8 !important;
    }

    /* Item selecionado no menu */
    [data-testid="stSidebar"] label[data-baseweb="radio"] {
        background-color: transparent;
        padding: 8px 12px;
        border-radius: 6px;
    }

    /* Fundo da Área Principal */
    .main {
        background-color: #F8FAFC;
    }

    /* Estilo das caixas do Calendário */
    .cal-day-header {
        text-align: center;
        font-weight: 700;
        background-color: #E2E8F0;
        padding: 6px;
        border-radius: 4px;
        color: #1E293B;
        font-size: 12px;
    }
    
    .cal-day-box {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        min-height: 85px;
        padding: 6px;
        margin-bottom: 5px;
    }
    
    .cal-day-box-today {
        background-color: #EFF6FF;
        border: 2px solid #2563EB;
        border-radius: 6px;
        min-height: 85px;
        padding: 6px;
        margin-bottom: 5px;
    }

    .cal-date-num {
        font-weight: 700;
        font-size: 11px;
        color: #0F172A;
    }

    .task-badge {
        background-color: #1E293B;
        color: #FFFFFF !important;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 10px;
        margin-top: 3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DOS DADOS NA SESSÃO ---
if 'salario' not in st.session_state:
    st.session_state.salario = 5000.0

if 'reserva_guardada' not in st.session_state:
    st.session_state.reserva_guardada = 1200.0

if 'gastos' not in st.session_state:
    st.session_state.gastos = pd.DataFrame([
        {"Item": "Aluguel", "Categoria": "Fixo", "Valor Total": 1500.0, "Parcela Atual": 1, "Total Parcelas": 1, "Valor Pago": 1500.0, "Status": "Pago"},
        {"Item": "Cartão de Crédito", "Categoria": "Variável", "Valor Total": 1200.0, "Parcela Atual": 1, "Total Parcelas": 1, "Valor Pago": 0.0, "Status": "Pendente"},
        {"Item": "Financiamento TV", "Categoria": "Parcelamento", "Valor Total": 2400.0, "Parcela Atual": 6, "Total Parcelas": 12, "Valor Pago": 1200.0, "Status": "Pendente"}
    ])

if 'tarefas' not in st.session_state:
    st.session_state.tarefas = pd.DataFrame([
        {"Título": "Pagar fatura do cartão", "Categoria": "Financeiro", "Status": "Pendente", "Prazo": datetime.date.today()},
        {"Título": "Revisar relatório do mês", "Categoria": "Trabalho", "Status": "Concluído", "Prazo": datetime.date.today()}
    ])

if 'metas' not in st.session_state:
    st.session_state.metas = pd.DataFrame([
        {"Meta": "Reserva de Emergência", "Valor Alvo": 10000.0, "Valor Atual": 3500.0, "Prazo": datetime.date(2026, 12, 31)},
        {"Meta": "Viagem de Fim de Ano", "Valor Alvo": 5000.0, "Valor Atual": 1500.0, "Prazo": datetime.date(2026, 11, 30)}
    ])

# --- BARRA LATERAL (MENU LIMPO) ---
with st.sidebar:
    st.markdown("### 🏛️ **Painel Pessoal**")
    st.caption("v1.0.0 | Acesso Privado")
    st.divider()
    
    menu = st.radio("NAVEGAÇÃO", [
        "Painel de Controle", 
        "Financeiro & Gastos", 
        "Metas & Prazos", 
        "Reserva & Economias"
    ])

# --- CÁLCULOS FINANCEIROS GLOBAIS ---
total_despesas_pendentes = st.session_state.gastos[st.session_state.gastos['Status'] == 'Pendente']['Valor Total'].sum()
total_despesas_geral = st.session_state.gastos['Valor Total'].sum()
porcentagem_comprometida = (total_despesas_geral / st.session_state.salario) * 100 if st.session_state.salario > 0 else 0

# --- TOPBAR ---
st.markdown("## **Painel de Controle Pessoal**")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Renda/Salário Mensal", f"R$ {st.session_state.salario:,.2f}")
m2.metric("Despesas Comprometidas", f"R$ {total_despesas_geral:,.2f}", delta=f"{porcentagem_comprometida:.1f}% da Renda", delta_color="inverse")
m3.metric("Contas Pendentes", len(st.session_state.gastos[st.session_state.gastos['Status'] == 'Pendente']))
m4.metric("Reserva Guardada", f"R$ {st.session_state.reserva_guardada:,.2f}")

st.divider()

# --- ABA 1: PAINEL DE CONTROLE (AGENDA + FORMULÁRIO) ---
if menu == "Painel de Controle":
    col_cal, col_form = st.columns([2.2, 1])
    
    with col_cal:
        hoje = datetime.date.today()
        st.markdown(f"### 📅 **Agenda - {hoje.strftime('%B / %Y').capitalize()}**")
        
        dias_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"]
        cols_h = st.columns(7)
        for i, d in enumerate(dias_semana):
            cols_h[i].markdown(f"<div class='cal-day-header'>{d}</div>", unsafe_allow_html=True)
            
        cal = calendar.Calendar(firstweekday=6)
        dias_mes = cal.monthdatescalendar(hoje.year, hoje.month)
        
        for semana in dias_mes:
            cols_s = st.columns(7)
            for i, dia in enumerate(semana):
                with cols_s[i]:
                    box_class = "cal-day-box-today" if dia == hoje else "cal-day-box"
                    tarefas_dia = st.session_state.tarefas[st.session_state.tarefas['Prazo'] == dia]
                    
                    html_t = ""
                    for _, t in tarefas_dia.iterrows():
                        html_t += f"<div class='task-badge'>{t['Título']}</div>"
                    
                    cor_num = "#0F172A" if dia.month == hoje.month else "#94A3B8"
                    st.markdown(f"""
                        <div class='{box_class}'>
                            <div class='cal-date-num' style='color:{cor_num};'>{dia.day}</div>
                            {html_t}
                        </div>
                    """, unsafe_allow_html=True)
                    
    with col_form:
        st.markdown("### ➕ **Adicionar Tarefa**")
        with st.form("form_tarefa"):
            titulo_t = st.text_input("Título:")
            cat_t = st.selectbox("Categoria:", ["Geral", "Financeiro", "Trabalho", "Pessoal"])
            prazo_t = st.date_input("Data do Prazo:", datetime.date.today())
            if st.form_submit_button("Salvar Tarefa", use_container_width=True):
                nova_t = pd.DataFrame([{"Título": titulo_t, "Categoria": cat_t, "Status": "Pendente", "Prazo": prazo_t}])
                st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova_t], ignore_index=True)
                st.success("Tarefa adicionada!")
                st.rerun()

        st.markdown("---")
        st.markdown("### ✅ **Gerenciar Status**")
        for idx, row in st.session_state.tarefas.iterrows():
            c_check, c_text = st.columns([1, 4])
            is_done = row['Status'] == 'Concluído'
            if c_check.checkbox("", value=is_done, key=f"t_{idx}"):
                st.session_state.tarefas.at[idx, 'Status'] = 'Concluído'
            else:
                st.session_state.tarefas.at[idx, 'Status'] = 'Pendente'
            c_text.write(f"**{row['Título']}** ({row['Status']})")

# --- ABA 2: FINANCEIRO & GASTOS ---
elif menu == "Financeiro & Gastos":
    col_fin, col_add_fin = st.columns([2, 1])
    
    with col_fin:
        st.markdown("### 📋 **Controle Financeiro & Parcelamentos**")
        
        # Ajuste da Salário na Sessão
        novo_salario = st.number_input("Editar Renda/Salário Mensal (R$):", value=st.session_state.salario, step=100.0)
        st.session_state.salario = novo_salario
        
        st.markdown("---")
        st.dataframe(st.session_state.gastos, use_container_width=True)
        
        st.markdown("#### ⏳ **Progresso de Quitação das Dívidas/Parcelas**")
        for idx, row in st.session_state.gastos.iterrows():
            if row['Total Parcelas'] > 1:
                progresso = row['Parcela Atual'] / row['Total Parcelas']
                st.write(f"**{row['Item']}** (Parcela {row['Parcela Atual']}/{row['Total Parcelas']})")
                st.progress(progresso)
                
        st.markdown("---")
        st.markdown("### 💡 **Análise da Renda & Recomendações**")
        if porcentagem_comprometida > 70:
            st.error(f"⚠️ **Atenção:** Você tem **{porcentagem_comprometida:.1f}%** do seu salário comprometido com despesas. Recomendamos renegociar parcelamentos e cortar gastos variáveis.")
        elif porcentagem_comprometida > 50:
            st.warning(f"⚖️ **Moderado:** **{porcentagem_comprometida:.1f}%** da sua renda está comprometida. Mantenha o foco em quitar parcelas antigas antes de novas compras.")
        else:
            st.success(f"✅ **Saudável:** Apenas **{porcentagem_comprometida:.1f}%** do seu salário está comprometido. Bom momento para direcionar o excedente para sua Reserva.")

    with col_add_fin:
        st.markdown("### ➕ **Novo Lançamento**")
        with st.form("form_gasto"):
            item_g = st.text_input("Descrição do Gasto/Conta:")
            cat_g = st.selectbox("Categoria:", ["Fixo", "Variável", "Parcelamento"])
            val_total = st.number_input("Valor Total (R$):", min_value=0.0, step=50.0)
            parc_atual = st.number_input("Parcela Atual:", min_value=1, value=1)
            total_parc = st.number_input("Total de Parcelas:", min_value=1, value=1)
            status_g = st.selectbox("Status:", ["Pendente", "Pago"])
            
            if st.form_submit_button("Lançar no Financeiro", use_container_width=True):
                val_pago = (val_total / total_parc) * parc_atual if status_g == 'Pago' else 0.0
                novo_g = pd.DataFrame([{
                    "Item": item_g, "Categoria": cat_g, "Valor Total": val_total, 
                    "Parcela Atual": parc_atual, "Total Parcelas": total_parc, 
                    "Valor Pago": val_pago, "Status": status_g
                }])
                st.session_state.gastos = pd.concat([st.session_state.gastos, novo_g], ignore_index=True)
                st.success("Lançado com sucesso!")
                st.rerun()

# --- ABA 3: METAS & PRAZOS ---
elif menu == "Metas & Prazos":
    col_m1, col_m2 = st.columns([2, 1])
    
    with col_m1:
        st.markdown("### 🎯 **Progresso das Metas**")
        for idx, row in st.session_state.metas.iterrows():
            pct = (row['Valor Atual'] / row['Valor Alvo']) if row['Valor Alvo'] > 0 else 0
            st.write(f"**{row['Meta']}** — R$ {row['Valor Atual']:,.2f} de R$ {row['Valor Alvo']:,.2f}")
            st.progress(min(pct, 1.0))
            st.caption(f"Prazo: {row['Prazo']} | Falta guardar: R$ {(row['Valor Alvo'] - row['Valor Atual']):,.2f}")
            st.markdown("---")
            
    with col_m2:
        st.markdown("### ➕ **Criar Nova Meta**")
        with st.form("form_meta"):
            nome_m = st.text_input("Nome da Meta:")
            alvo_m = st.number_input("Valor Objetivo (R$):", min_value=100.0, step=100.0)
            atual_m = st.number_input("Valor Já Guardado (R$):", min_value=0.0, step=50.0)
            prazo_m = st.date_input("Data Limite:", datetime.date(2026, 12, 31))
            
            if st.form_submit_button("Salvar Meta", use_container_width=True):
                nova_m = pd.DataFrame([{"Meta": nome_m, "Valor Alvo": alvo_m, "Valor Atual": atual_m, "Prazo": prazo_m}])
                st.session_state.metas = pd.concat([st.session_state.metas, nova_m], ignore_index=True)
                st.success("Meta adicionada!")
                st.rerun()

# --- ABA 4: RESERVA & ECONOMIAS ---
elif menu == "Reserva & Economias":
    st.markdown("### 🏦 **Acompanhamento do Dinheiro Guardado**")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        nova_reserva = st.number_input("Atualizar Saldo Atual da Reserva (R$):", value=st.session_state.reserva_guardada, step=100.0)
        st.session_state.reserva_guardada = nova_reserva
        st.success(f"Saldo Guardado Atualizado: **R$ {st.session_state.reserva_guardada:,.2f}**")
        
    with col_r2:
        meta_reserva = st.session_state.salario * 6
        pct_reserva = (st.session_state.reserva_guardada / meta_reserva) if meta_reserva > 0 else 0
        st.markdown(f"**Meta Ideal (6 meses de salário):** R$ {meta_reserva:,.2f}")
        st.progress(min(pct_reserva, 1.0))
        st.caption(f"Você já construiu **{(pct_reserva * 100):.1f}%** da sua reserva ideal de segurança.")
