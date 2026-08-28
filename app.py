import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai

# Configuração da página
st.set_page_config(
    page_title="Meu Painel de Gestão",
    page_icon="📌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #1E1E2F;
        color: white;
    }
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #4E73DF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE DADOS NA SESSÃO ---
if 'gastos' not in st.session_state:
    st.session_state.gastos = pd.DataFrame([
        {"Item": "Salário / Entradas", "Tipo": "Entrada", "Valor": 5000.0, "Status": "Recebido", "Data": datetime.date.today()},
        {"Item": "Aluguel / Contas Fixas", "Tipo": "Despesa", "Valor": 1800.0, "Status": "Pago", "Data": datetime.date.today()},
        {"Item": "Mercado", "Tipo": "Despesa", "Valor": 600.0, "Status": "Pendente", "Data": datetime.date.today()}
    ])

if 'tarefas' not in st.session_state:
    st.session_state.tarefas = pd.DataFrame([
        {"Tarefa": "Revisar relatório financeiro", "Prioridade": "Alta", "Prazo": datetime.date.today(), "Status": "Pendente"},
        {"Tarefa": "Organizar metas do mês", "Prioridade": "Média", "Prazo": datetime.date.today(), "Status": "Em Andamento"}
    ])

if 'desejos' not in st.session_state:
    st.session_state.desejos = pd.DataFrame([
        {"Item Desejado": "Novo Monitor / Cadeira Ergonomica", "Valor Estimado": 1200.0, "Prioridade": "Média"}
    ])

# --- BARRA LATERAL (MENU PERSONALIZADO) ---
with st.sidebar:
    st.title("📌 Meu Painel Pessoal")
    st.caption("Sistema Unificado de Organização")
    
    menu = st.radio("Navegação", ["Dashboard (Hoje)", "Financeiro & Capital", "Afazeres & Prazos", "Lista de Desejos", "Assistente IA (Gemini)"])
    
    st.divider()
    api_key = st.text_input("Chave API Gemini (Opcional):", type="password", help="Insira sua chave gratuita do Google AI Studio")

# Cálculos Globais de Saldo
total_entradas = st.session_state.gastos[st.session_state.gastos['Tipo'] == 'Entrada']['Valor'].sum()
total_despesas = st.session_state.gastos[st.session_state.gastos['Tipo'] == 'Despesa']['Valor'].sum()
capital_disponivel = total_entradas - total_despesas

# --- PAINEL 1: DASHBOARD (HOJE) ---
if menu == "Dashboard (Hoje)":
    st.title("🗓️ Visão Geral de Hoje")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Capital Disponível", f"R$ {capital_disponivel:,.2f}")
    c2.metric("Tarefas Pendentes", len(st.session_state.tarefas[st.session_state.tarefas['Status'] != 'Concluído']))
    c3.metric("Contas Pendentes", len(st.session_state.gastos[st.session_state.gastos['Status'] == 'Pendente']))
    
    st.divider()
    
    col_esquerda, col_direita = st.columns([2, 1])
    
    with col_esquerda:
        st.subheader("📋 Prioridades do Dia")
        st.dataframe(st.session_state.tarefas, use_container_width=True)
        
    with col_direita:
        st.subheader("➕ Adicionar Rápido")
        with st.form("form_rapido"):
            nova_tarefa = st.text_input("Nova Tarefa:")
            prioridade = st.selectbox("Prioridade:", ["Baixa", "Média", "Alta"])
            prazo = st.date_input("Prazo:", datetime.date.today())
            
            if st.form_submit_button("Salvar Tarefa"):
                nova_linha = pd.DataFrame([{"Tarefa": nova_tarefa, "Prioridade": prioridade, "Prazo": prazo, "Status": "Pendente"}])
                st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova_linha], ignore_index=True)
                st.success("Adicionado com sucesso!")

# --- PAINEL 2: FINANCEIRO & CAPITAL ---
elif menu == "Financeiro & Capital":
    st.title("💰 Gestão Financeira")
    st.dataframe(st.session_state.gastos, use_container_width=True)
    
    st.subheader("Registrar Lançamento")
    with st.form("form_financeiro"):
        f_item = st.text_input("Descrição:")
        f_tipo = st.selectbox("Tipo:", ["Despesa", "Entrada"])
        f_valor = st.number_input("Valor (R$):", min_value=0.0, format="%.2f")
        f_status = st.selectbox("Status:", ["Pago", "Pendente", "Recebido"])
        f_data = st.date_input("Vencimento:")
        
        if st.form_submit_button("Salvar Financeiro"):
            novo_gasto = pd.DataFrame([{"Item": f_item, "Tipo": f_tipo, "Valor": f_valor, "Status": f_status, "Data": f_data}])
            st.session_state.gastos = pd.concat([st.session_state.gastos, novo_gasto], ignore_index=True)
            st.success("Lançado!")

# --- PAINEL 3: LISTA DE DESEJOS ---
elif menu == "Lista de Desejos":
    st.title("🎯 Lista de Desejos x Saldo Disponível")
    st.info(f"💡 **Capital Disponível:** R$ {capital_disponivel:,.2f}")
    
    st.dataframe(st.session_state.desejos, use_container_width=True)
    
    st.subheader("Simulador de Compra")
    item_simulado = st.selectbox("Selecione o item:", st.session_state.desejos['Item Desejado'].tolist() if not st.session_state.desejos.empty else ["Nenhum"])
    
    if item_simulado != "Nenhum":
        valor_item = st.session_state.desejos[st.session_state.desejos['Item Desejado'] == item_simulado]['Valor Estimado'].values[0]
        
        if capital_disponivel >= valor_item:
            st.success(f"✅ **Compra autorizada!** Saldo restante: R$ {(capital_disponivel - valor_item):,.2f}.")
        else:
            st.error(f"⚠️ **Atenção:** Faltam R$ {(valor_item - capital_disponivel):,.2f} para adquirir este item.")

# --- PAINEL 4: ASSISTENTE IA ---
elif menu == "Assistente IA (Gemini)":
    st.title("🤖 Consultor Pessoal Gemini")
    
    if not api_key:
        st.warning("Insira sua chave de API no menu lateral para ativar.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            pergunta = st.text_area("O que deseja analisar?")
            
            if st.button("Perguntar"):
                 contexto = f"Capital: R$ {capital_disponivel}. Gastos: {st.session_state.gastos.to_dict()}. Tarefas: {st.session_state.tarefas.to_dict()}."
                 resposta = model.generate_content(f"{contexto}\nPergunta: {pergunta}")
                 st.write("### Resposta da IA:")
                 st.write(resposta.text)
        except Exception as e:
            st.error(f"Erro: {e}")
