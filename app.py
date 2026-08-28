import streamlit as st
import pandas as pd
import datetime
import google.generativeai as genai

# Configuração da página (Layout Wide para parecer um Web App corporativo)
st.set_page_config(
    page_title="Sistema de Gestão Pessoal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS para aproximar do layout da imagem (Menu escuro + cards)
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

# --- BARRA LATERAL (MENU & APORTE DE CHAVE API) ---
with st.sidebar:
    st.title("📌 Juris Control / Painel")
    st.caption("Sistema Integrado de Gestão Pessoal")
    
    menu = st.radio("Navegação", ["Dashboard (Hoje)", "Financeiro & Capital", "Afazeres & Prazos", "Lista de Desejos", "Assistente IA (Gemini)"])
    
    st.divider()
    api_key = st.text_input("Chave API Gemini (Opcional):", type="password", help="Insira sua chave gratuita do Google AI Studio")

# Cálculos Globais de Saldo
total_entradas = st.session_state.gastos[st.session_state.gastos['Tipo'] == 'Entrada']['Valor'].sum()
total_despesas = st.session_state.gastos[st.session_state.gastos['Tipo'] == 'Despesa']['Valor'].sum()
capital_disponivel = total_entradas - total_despesas

# --- PAINEL 1: DASHBOARD (HOJE) ---
if menu == "Dashboard (Hoje)":
    st.title("🗓️ Painel de Controle Diario")
    
    # Resumo Superior em Métricas
    c1, c2, c3 = st.columns(3)
    c1.metric("Capital Atual Disponível", f"R$ {capital_disponivel:,.2f}")
    c2.metric("Tarefas Pendentes Hoje", len(st.session_state.tarefas[st.session_state.tarefas['Status'] != 'Concluído']))
    c3.metric("Contas a Vencer/Pendentes", len(st.session_state.gastos[st.session_state.gastos['Status'] == 'Pendente']))
    
    st.divider()
    
    col_esquerda, col_direita = st.columns([2, 1])
    
    with col_esquerda:
        st.subheader("📋 Compromissos & Prioridades de Hoje")
        st.dataframe(st.session_state.tarefas, use_container_width=True)
        
    with col_direita:
        st.subheader("➕ Adicionar Rápido")
        with st.form("form_rapido"):
            nova_tarefa = st.text_input("Nova Tarefa/Compromisso:")
            prioridade = st.selectbox("Prioridade:", ["Baixa", "Média", "Alta"])
            prazo = st.date_input("Prazo:", datetime.date.today())
            
            if st.form_submit_button("Salvar no Sistema"):
                nova_linha = pd.DataFrame([{"Tarefa": nova_tarefa, "Prioridade": prioridade, "Prazo": prazo, "Status": "Pendente"}])
                st.session_state.tarefas = pd.concat([st.session_state.tarefas, nova_linha], ignore_index=True)
                st.success("Adicionado com sucesso!")

# --- PAINEL 2: FINANCEIRO & CAPITAL ---
elif menu == "Financeiro & Capital":
    st.title("💰 Gestão Financeira Integrada")
    
    st.dataframe(st.session_state.gastos, use_container_width=True)
    
    st.subheader("Registrar Movimentação Financeira")
    with st.form("form_financeiro"):
        f_item = st.text_input("Descrição do Item/Lançamento:")
        f_tipo = st.selectbox("Tipo:", ["Despesa", "Entrada"])
        f_valor = st.number_input("Valor (R$):", min_value=0.0, format="%.2f")
        f_status = st.selectbox("Status:", ["Pago", "Pendente", "Recebido"])
        f_data = st.date_input("Data de Vencimento/Recebimento:")
        
        if st.form_submit_button("Lançar no Caixa"):
            novo_gasto = pd.DataFrame([{"Item": f_item, "Tipo": f_tipo, "Valor": f_valor, "Status": f_status, "Data": f_data}])
            st.session_state.gastos = pd.concat([st.session_state.gastos, novo_gasto], ignore_index=True)
            st.success("Lançamento efetuado!")

# --- PAINEL 3: LISTA DE DESEJOS & SIMULADOR DE INVESTIMENTO ---
elif menu == "Lista de Desejos":
    st.title("🎯 Lista de Desejos vs. Capital Atual")
    
    st.info(f"💡 **Seu Capital Atual é de R$ {capital_disponivel:,.2f}**")
    
    st.dataframe(st.session_state.desejos, use_container_width=True)
    
    st.subheader("Simulador de Compra / Investimento")
    item_simulado = st.selectbox("Selecione o item para simular:", st.session_state.desejos['Item Desejado'].tolist() if not st.session_state.desejos.empty else ["Nenhum"])
    
    if item_simulado != "Nenhum":
        valor_item = st.session_state.desejos[st.session_state.desejos['Item Desejado'] == item_simulado]['Valor Estimado'].values[0]
        
        if capital_disponivel >= valor_item:
            st.success(f"✅ **Você PODE comprar este item agora!** O saldo restante será de R$ {(capital_disponivel - valor_item):,.2f}.")
        else:
            st.error(f"⚠️ **Atenção:** Você precisa de mais R$ {(valor_item - capital_disponivel):,.2f} para realizar este desejo sem comprometer seu caixa atual.")

# --- PAINEL 4: ASSISTENTE IA (GEMINI) ---
elif menu == "Assistente IA (Gemini)":
    st.title("🤖 Consultor Pessoal Gemini")
    
    if not api_key:
        st.warning("Insira sua chave de API do Gemini no menu lateral para ativar a IA.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            pergunta = st.text_area("O que você gostaria que a IA analise do seu sistema hoje?")
            
            if st.button("Analisar com Gemini"):
                 contexto = f"""
                Dados Atuais do Usuário:
                - Capital Disponível: R$ {capital_disponivel}
                - Gastos/Entradas: {st.session_state.gastos.to_dict()}
                - Tarefas: {st.session_state.tarefas.to_dict()}
                - Lista de Desejos: {st.session_state.desejos.to_dict()}
                
                Pergunta do usuário: {pergunta}
                """
                 resposta = model.generate_content(contexto)
                 st.write("### Resposta da IA:")
                 st.write(resposta.text)
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")
