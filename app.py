import streamlit as st
import pandas as pd
from datetime import datetime, date
import calendar

# 1. Configuração da página
st.set_page_config(
    page_title="Meu Painel Pessoal",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injeção de CSS personalizado (Estilo escuro na barra lateral + visual limpo)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    /* Sidebar Escura */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    /* Faixa de Contadores Rápidos (KPIs) */
    .kpi-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: nowrap;
        overflow-x: auto;
    }
    
    .date-card {
        background-color: #0f172a;
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 700;
        display: flex;
        align-items: center;
        white-space: nowrap;
    }
    
    .badge-card {
        padding: 8px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        border: 1px solid rgba(0,0,0,0.06);
        white-space: nowrap;
    }
    
    .badge-tarefas { background-color: #e0f2fe; color: #0369a1; }
    .badge-estudos { background-color: #fef9c3; color: #a16207; }
    .badge-rotina  { background-color: #dcfce7; color: #15803d; }
    .badge-habitos { background-color: #f3e8ff; color: #7e22ce; }
    .badge-financas{ background-color: #d1fae5; color: #047857; }

    /* Botões arredondados */
    div.stButton > button {
        border-radius: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar (Navegação Pessoal)
with st.sidebar:
    st.markdown("### ✨ Minha Vida & Rotina")
    st.caption("Organizador Pessoal • v1.0")
    st.markdown("---")
    
    menu = [
        "📊 Visão Geral",
        "📅 Agenda & Compromissos",
        "🎯 Metas & Objetivos",
        "📚 Estudos & Cursos",
        "💪 Treino & Saúde",
        "💰 Controle Financeiro",
        "🛒 Listas & Compras",
        "💡 Ideias & Projetos",
        "⚙️ Configurações"
    ]
    st.radio("Navegação", menu, label_visibility="collapsed")

# 4. Cabeçalho Superior e Filtros
col_titulo, col_busca, col_perfil = st.columns([2, 4, 2])

with col_titulo:
    st.title("Painel Pessoal")

with col_busca:
    st.text_input("Busca", placeholder="🔍 Buscar tarefa, nota, compromisso...", label_visibility="collapsed")

with col_perfil:
    st.markdown("**👤 Meu Perfil**")
    st.caption("Foco do Dia: Produtividade")

# Linha de Filtros Rápidos / Modos de Visualização
filtro_cols = st.columns([1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 2.5])
with filtro_cols[0]: st.button("📅 Agenda", type="primary")
with filtro_cols[1]: st.button("📋 Lista")
with filtro_cols[2]: st.button("📌 Kanban")
with filtro_cols[3]: st.button("🌱 Hábitos")
with filtro_cols[4]: st.button("🔔 Lembretes (2)")
with filtro_cols[6]: st.button("+ Nova Atividade", type="primary", use_container_width=True)

st.markdown("---")

# 5. Faixa de Indicadores (Métricas do Dia)
st.markdown("""
<div class="kpi-container">
    <div class="date-card">📅 HOJE</div>
    <div class="badge-card badge-tarefas">📋 4 Tarefas</div>
    <div class="badge-card badge-estudos">📚 2h Estudos</div>
    <div class="badge-card badge-rotina">🌿 Rotina Matinal OK</div>
    <div class="badge-card badge-habitos">💧 2.5L Água</div>
    <div class="badge-card badge-financas">💳 Contas em Dia</div>
</div>
""", unsafe_allow_html=True)

# 6. Layout Principal: Calendário + Drawer Lateral de Cadastro
col_agenda, col_drawer = st.columns([7, 4])

with col_agenda:
    st.subheader("Planejamento do Mês")
    
    # Cabeçalho dos dias da semana
    dias_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"]
    cols_dias = st.columns(7)
    for i, dia in enumerate(dias_semana):
        cols_dias[i].markdown(f"**{dia}**")
    
    # Grid de calendário simplificado
    hoje = datetime.now()
    cal = calendar.monthcalendar(hoje.year, hoje.month)
    for semana in cal:
        cols_sem = st.columns(7)
        for i, d in enumerate(semana):
            if d != 0:
                with cols_sem[i]:
                    st.markdown(f"**{d}**")
                    if d == hoje.day:
                        st.info("📌 Foco Total")
                    elif d in (5, 12, 19, 26):
                        st.success("🏋️ Treino")
            else:
                cols_sem[i].write("")

with col_drawer:
    with st.container(border=True):
        st.subheader("Nova Atividade / Hábito")
        status = st.selectbox("Status", ["⏳ A Fazer", "🚀 Em Andamento", "✅ Concluído", "⏸️ Pausado"])
        
        titulo = st.text_input("Título da Atividade", placeholder="Ex: Organizar semana / Estudo do módulo 2")
        categoria = st.selectbox("Categoria", ["📚 Estudos", "💪 Saúde / Treino", "💼 Trabalho / Estágio", "🏠 Casa / Família", "💰 Finanças"])
        prioridade = st.select_slider("Prioridade", options=["Baixa", "Média", "Alta", "Urgente"], value="Média")
        data_limite = st.date_input("Data Planejada", date.today())
        notas = st.text_area("Observações / Checklist", placeholder="Detalhes ou passos para concluir...", height=80)
        
        c1, c2 = st.columns(2)
        with c1:
            st.button("Cancelar", use_container_width=True)
        with c2:
            st.button("Salvar Registro", type="primary", use_container_width=True)
