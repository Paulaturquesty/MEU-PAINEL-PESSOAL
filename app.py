import streamlit as st
import pandas as pd
import datetime
import calendar
import google.generativeai as genai

# Configuração visual do sistema
st.set_page_config(
    page_title="Painel de Controle Pessoal",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS: Fonte Plus Jakarta Sans, Cores Customizadas e Calendário
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, button, input, select, textarea {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* BARRA LATERAL (#351c75 com texto branco) */
    [data-testid="stSidebar"] {
        background-color: #351c75 !important;
        color: #FFFFFF !important;
    }
    
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
    }

    /* ÁREA PRINCIPAL (Fundo claro com texto escuro) */
    .main {
        background-color: #F8F9FA;
        color: #1A1A1A;
    }

    /* Estilo das caixas do Calendário */
    .cal-day-header {
        text-align: center;
        font-weight: 700;
        background-color: #ECECF0;
        padding: 5px;
        border-radius: 4px;
        color: #351c75;
    }
    
    .cal-day-box {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        min-height: 90px;
        padding: 6px;
        margin-bottom: 5px;
    }
    
    .cal-day-box-today {
        background-color: #F0EBFB;
        border: 2px solid #351c75;
        border-radius: 6px;
        min-height: 90px;
        padding: 6px;
        margin-bottom: 5px;
    }

    .cal-date-num {
        font-weight: bold;
        font-size: 12px;
        color: #351c75;
        margin-bottom: 4px;
    }

    .task-badge {
        background-color: #351c75;
        color: white !important;
        padding: 2px 5px;
        border-radius: 3px;
        font-size: 10px;
        margin-top: 2px;
        display: block;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>
""", unsafe_allow_html=True)

# --- DADOS DA SESSÃO ---
if 'gastos' not in st.session_state:
    st.session_state.gastos = pd.DataFrame([
        {"Item": "Cartão de Crédito", "Categoria": "Fixo", "Valor": 1250.0, "Status": "Pendente", "Vencimento": datetime.date.today()},
        {"Item": "Consultoria Pessoal", "Categoria": "Entrada", "Valor": 3500.0, "Status": "Recebido", "Vencimento": datetime.date.today()}
    ])

if 'tarefas' not in st.session_state:
    st.session_state.tarefas = pd.DataFrame([
        {"Título": "Revisar Prazos do Mês", "Categoria": "Prioridade", "Status": "Pendente", "Prazo": datetime.date.today()},
        {"Título": "Planejamento Metas 2026", "Categoria": "Metas", "Status": "Em Andamento", "Prazo": datetime.date.today()}
    ])

if 'desejos' not in st.session_state:
    st.session_state.desejos = pd.DataFrame([
        {"Desejo": "Notebook Novo", "Valor Estimado": 4500.0, "Status": "Planejando"}
    ])

# --- BARRA LATERAL ROXA (#351c75) COM ÍCONES DE CONTORNO ---
with st.sidebar:
    st.markdown("### 🏛️ **Painel Pessoal**")
    st.caption("v1.0.0 | Acesso Privado")
    st.divider()
    
    # Nomes com ícones minimalistas de contorno
    menu = st.radio("MÓDULOS DO SISTEMA", [
        "📑 Painel de Controle", 
        "💳 Financeiro & Gastos", 
        "🗓️ Metas & Prazos", 
        "🎯 Lista de Desejos"
    ])
    
    st.divider()
    
    st.markdown("### 💬 **Assistente Gemini**")
    api_key = st.text_input("Chave API Gemini:", type="password", help="Insira sua chave do Google AI Studio")
    
    uploaded_file = st.file_uploader("Enviar documento/comprovante:", type=['pdf', 'png', 'jpg', 'txt'])
    
    pergunta_ia = st.text_area("Instruções para o Gemini:", placeholder="Ex: Leia a imagem e adicione o gasto no meu financeiro.")
    
    if st.button("Executar Assistente", use_container_width=True):
        if not api_key:
            st.error("Insira a chave da API Gemini.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                contexto_dados = f"""
                Capital Atual: R$ {st.session_state.gastos[st.session_state.gastos['Categoria'] == 'Entrada']['Valor'].sum() - st.session_state.gastos[st.session_state.gastos['Categoria'] != 'Entrada']['Valor'].sum()}
                Tarefas: {st.session_state.tarefas.to_dict()}
                Financeiro: {st.session_state.gastos.to_dict()}
                """
                
                prompt_final = f"Contexto:\n{contexto_dados}\n\nSolicitação: {pergunta_ia}"
                
                with st.spinner("Analisando..."):
                    resposta = model.generate_content(prompt_final)
                    st.info("### Resposta da IA:")
                    st.write(resposta.text)
            except Exception as e:
                st.error(f"Erro: {e}")

# Cálculos Financeiros
entradas = st.session_state.gastos[st.session_state.gastos['Categoria'] == 'Entrada']['Valor'].sum()
saidas = st.session_state.gastos[st.session_state.gastos['Categoria'] != 'Entrada']['Valor'].sum()
saldo_capital = entradas - saidas

# --- TOPBAR ---
st.markdown("## **Painel de Controle**")
col_search, col_btn = st.columns([4, 1])
with col_search:
    st.text_input("🔍 Buscar processo, cliente, tarefa...", label_visibility="collapsed")
with col_btn:
    st.button("🔍 Pesquisar", use_container_width=True)

# Indicadores
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Capital Livre", f"R$ {saldo_capital:,.2f}")
m2.metric("Tarefas Hoje", len(st.session_state.tarefas))
m3.metric("Contas a Vencer", len(st.session_state.gastos[st.session_state.gastos['Status'] == 'Pendente']))
m4.metric("Prazos Mês", len(st.session_state.tarefas[st.session_state.tarefas['Categoria'] == 'Prioridade']))
m5.metric("Desejos Ativos", len(st.session_state.desejos))

st.divider()

# --- MÓDULO 1: PAINEL DE CONTROLE COM CALENDÁRIO DINÂMICO ---
if menu == "📑 Painel de Controle":
    col_agenda, col_form = st.columns([2.2, 1])
    
    with col_agenda:
        # Lógica do Calendário Automático
        hoje = datetime.date.today()
        st.markdown(f"### 📅 **Agenda de {hoje.strftime('%B de %Y').capitalize()}**")
        
        # Estrutura de Dias da Semana
        dias_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"]
        cols_header = st.columns(7)
        for i, dia_nome in enumerate(dias_semana):
            cols_header[i].markdown(f"<div class='cal-day-header'>{dia_nome}</div>", unsafe_allow_html=True)
            
        # Matriz de Dias do Mês
        cal = calendar.Calendar(firstweekday=6) # 6 = Domingo
        dias_mes = cal.monthdatescalendar(hoje.year, hoje.month)
        
        for semana in dias_mes:
            cols_semana = st.columns(7)
            for i, dia in enumerate(semana):
                with cols_semana[i]:
                    # Destaca o dia de hoje
                    box_class = "cal-day-box-today" if dia == hoje else "cal-day-box"
                    
                    # Filtra tarefas pertencentes a este dia específico do calendário
                    tarefas_dia = st.session_state.tarefas[st.session_state.tarefas['Prazo'] == dia]
                    
                    html_tasks = ""
                    for _, t in tarefas_dia.iterrows():
                        html_tasks += f"<div class='task-badge' title='{t['Título']}'>{t['Título']}</div>"
                    
                    # Mostra os dias apenas do mês atual com cor normal
                    cor_num = "#351c75" if dia.month == hoje.month else "#A0A0A0"
                    
                    st.markdown(f"""
                        <div class='{box_class}'>
                            <div class='cal-date-num' style='color: {cor_num};'>{dia.day}</div>
                            {html_tasks}
                        </div>
                    """, unsafe_allow_html=True)
        
    with col_form:
        st.markdown("### **+ Adicionar Tarefa / Prazo**")
        with st.form("form_novo_item"):
            titulo = st.text_input("Título da Tarefa:")
            cat = st.selectbox("Categoria:", ["Prioridade", "Metas", "Rotina Diária"])
            prazo_item = st.date_input("Data do Prazo:", datetime.date.today())
            status_item = st.selectbox("Situação:", ["Pendente", "Em Andamento", "Concluído"])
            
            if st.form_submit_button("Salvar no Calendário"):
                nova = pd.DataFrame([{"Título": titulo, "Categoria": cat, "Status": status_item, "Prazo": prazo_item}])
                st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova], ignore_index=True)
                st.success("Salvo no calendário com sucesso!")
                st.rerun()

# --- MÓDULO 2: FINANCEIRO ---
elif menu == "💳 Financeiro & Gastos":
    col_fin1, col_fin2 = st.columns([2, 1])
    
    with col_fin1:
        st.markdown("### 📋 Planilha Financeira")
        st.dataframe(st.session_state.gastos, use_container_width=True, height=400)
        
    with col_fin2:
        st.markdown("### **+ Novo Lançamento**")
        with st.form("form_fin"):
            item_f = st.text_input("Descrição:")
            cat_f = st.selectbox("Tipo:", ["Fixo", "Variável", "Entrada", "Investimento"])
            val_f = st.number_input("Valor (R$):", min_value=0.0, format="%.2f")
            venc_f = st.date_input("Vencimento:", datetime.date.today())
            stat_f = st.selectbox("Status:", ["Pendente", "Pago", "Recebido"])
            
            if st.form_submit_button("Lançar Caixa"):
                novo_gasto = pd.DataFrame([{"Item": item_f, "Categoria": cat_f, "Valor": val_f, "Status": stat_f, "Vencimento": venc_f}])
                st.session_state.gastos = pd.concat([st.session_state.gastos, novo_gasto], ignore_index=True)
                st.success("Lançamento efetuado!")
                st.rerun()

# --- MÓDULO 3: METAS ---
elif menu == "🗓️ Metas & Prazos":
    st.markdown("### 🎯 Acompanhamento de Metas")
    st.dataframe(st.session_state.tarefas[st.session_state.tarefas['Categoria'] == 'Metas'], use_container_width=True)

# --- MÓDULO 4: LISTA DE DESEJOS ---
elif menu == "🎯 Lista de Desejos":
    st.markdown("### 🛒 Simulador de Compras e Investimento")
    st.dataframe(st.session_state.desejos, use_container_width=True)
    
    st.subheader("Análise de Viabilidade Financeira")
    desejo_sel = st.selectbox("Selecione o Desejo:", st.session_state.desejos['Desejo'].tolist() if not st.session_state.desejos.empty else ["Nenhum"])
    
    if desejo_sel != "Nenhum":
        val_desejo = st.session_state.desejos[st.session_state.desejos['Desejo'] == desejo_sel]['Valor Estimado'].values[0]
        if saldo_capital >= val_desejo:
            st.success(f"✅ Viável! Você possui saldo suficiente de R$ {saldo_capital:,.2f} para investir R$ {val_desejo:,.2f}.")
        else:
            st.error(f"❌ Inviável no momento. Faltam R$ {(val_desejo - saldo_capital):,.2f} para essa aquisição.")
