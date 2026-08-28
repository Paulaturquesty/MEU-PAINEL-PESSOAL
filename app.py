import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai

# Configuração visual avançada para replicar o Juris Control
st.set_page_config(
    page_title="Painel de Controle Pessoal",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS customizada (Layout idêntico à imagem)
st.markdown("""
<style>
    /* Estilo do Menu Lateral */
    [data-testid="stSidebar"] {
        background-color: #0b132b;
        color: #ffffff;
    }
    
    /* Ajustes dos botões do menu */
    .stRadio > label {
        color: #8d99ae !important;
        font-weight: 600;
    }
    
    /* Cards de métricas estilo Topbar */
    div[data-testid="stMetricValue"] {
        font-size: 20px !important;
        color: #1c2541;
    }
    div[data-testid="stMetric"] {
        background-color: #f4f5f6;
        border-radius: 6px;
        padding: 10px 15px;
        border-left: 4px solid #3a86ff;
    }
</style>
""", unsafe_allow_html=True)

# --- BANCO DE DADOS EM SESSÃO ---
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

# --- BARRA LATERAL (ASSISTENTE E NAVEGAÇÃO CORPORATIVA) ---
with st.sidebar:
    st.markdown("### 🏛️ **Painel Pessoal**")
    st.caption("v1.0.0 | Usuário Administrador")
    st.divider()
    
    # Nomes fiéis às suas planilhas e à estrutura da imagem
    menu = st.radio("MÓDULOS DO SISTEMA", [
        "📌 Painel de Controle", 
        "💳 Financeiro & Gastos", 
        "⏳ Metas & Prazos", 
        "🎯 Lista de Desejos"
    ])
    
    st.divider()
    
    # Assistente IA Integrado Imediatamente
    st.markdown("### 🤖 **Assistente Gemini**")
    api_key = st.text_input("Chave API Gemini:", type="password", help="Insira sua API Key do Google AI Studio")
    
    # Leitor de Documentos Global
    uploaded_file = st.file_drop_target if hasattr(st, 'file_drop_target') else st.file_uploader("Enviar comprovante ou documento:", type=['pdf', 'png', 'jpg', 'txt'])
    
    pergunta_ia = st.text_area("O que deseja que o Gemini faça?", placeholder="Ex: Leia o documento acima e extraia o valor e vencimento.")
    
    if st.button("Executar com IA"):
        if not api_key:
            st.error("Insira a chave da API do Gemini acima.")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                contexto_dados = f"""
                Capital Atual: R$ {st.session_state.gastos[st.session_state.gastos['Categoria'] == 'Entrada']['Valor'].sum() - st.session_state.gastos[st.session_state.gastos['Categoria'] != 'Entrada']['Valor'].sum()}
                Tarefas: {st.session_state.tarefas.to_dict()}
                Financeiro: {st.session_state.gastos.to_dict()}
                """
                
                prompt_final = f"Contexto do Sistema:\n{contexto_dados}\n\nSolicitação: {pergunta_ia}"
                
                with st.spinner("Analisando dados..."):
                    resposta = model.generate_content(prompt_final)
                    st.info("### Resposta do Assistente:")
                    st.write(resposta.text)
            except Exception as e:
                st.error(f"Erro ao processar: {e}")

# Cálculos do Caixa
entradas = st.session_state.gastos[st.session_state.gastos['Categoria'] == 'Entrada']['Valor'].sum()
saidas = st.session_state.gastos[st.session_state.gastos['Categoria'] != 'Entrada']['Valor'].sum()
saldo_capital = entradas - saidas

# --- TOPBAR COM BUSCA E FILTROS (COMO NA IMAGEM) ---
st.markdown("## **Painel de Controle**")
col_search, col_btn = st.columns([4, 1])
with col_search:
    st.text_input("🔍 Buscar tarefa, gasto, meta ou compromisso...", label_visibility="collapsed")
with col_btn:
    st.button("🔍 Pesquisar", use_container_width=True)

# Indicadores em Banner (Topbar Visual)
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Capital Livre", f"R$ {saldo_capital:,.2f}")
m2.metric("Tarefas Hoje", len(st.session_state.tarefas))
m3.metric("Contas a Vencer", len(st.session_state.gastos[st.session_state.gastos['Status'] == 'Pendente']))
m4.metric("Prazos Mês", 3)
m5.metric("Desejos Ativos", len(st.session_state.desejos))

st.divider()

# --- MÓDULO 1: PAINEL DE CONTROLE (AGENDA + FORMULÁRIO RETRÁTIL) ---
if menu == "📌 Painel de Controle":
    col_agenda, col_form = st.columns([2, 1])
    
    with col_agenda:
        st.markdown("### 📅 Agenda & Prazos do Mês")
        # Visualização estilo tabela/calendário central
        st.dataframe(st.session_state.tarefas, use_container_width=True, height=400)
        
    with col_form:
        st.markdown("### **+ Adicionar Tarefa / Prazo**")
        with st.form("form_novo_item"):
            titulo = st.text_input("Título:")
            cat = st.selectbox("Categoria:", ["Prioridade", "Metas", "Rotina Diária"])
            prazo_item = st.date_input("Prazo Final:", datetime.date.today())
            status_item = st.selectbox("Situação:", ["Pendente", "Em Andamento", "Concluído"])
            
            if st.form_submit_button("Salvar no Sistema"):
                nova = pd.DataFrame([{"Título": titulo, "Categoria": cat, "Status": status_item, "Prazo": prazo_item}])
                st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova], ignore_index=True)
                st.success("Item salvo com sucesso!")

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

# --- MÓDULO 3: METAS ---
elif menu == "⏳ Metas & Prazos":
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
