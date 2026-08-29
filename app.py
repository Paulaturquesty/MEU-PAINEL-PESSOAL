# --- SUB-ROTINA DE LEITURA COMPLETA DAS SUAS PLANILHAS NO APP.PY ---
def carregar_planilhas_oficiais(arquivo_gastos, arquivo_metas):
    # 1. Carregar Metas
    xls_metas = pd.ExcelFile(arquivo_metas)
    if 'PLANEJAMENTO E METAS ANUAIS ' in xls_metas.sheet_names:
        df_m = pd.read_excel(xls_metas, sheet_name='PLANEJAMENTO E METAS ANUAIS ', skiprows=10)
        df_m_clean = df_m[['Meta | Item a Comprar', 'Valor Necessário', 'Valor Guardado', 'Data Alvo', 'Status']].dropna(subset=['Meta | Item a Comprar'])
        df_m_clean.columns = ['Meta', 'Valor Alvo', 'Valor Atual', 'Prazo', 'Status']
        st.session_state.metas = df_m_clean

    # 2. Carregar Gastos e Abas Mensais (062026, 072026, 082026, 092026)
    xls_gastos = pd.ExcelFile(arquivo_gastos)
    for sheet in xls_gastos.sheet_names:
        sheet_clean = sheet.strip()
        if sheet_clean in ['062026', '072026', '082026', '092026']:
            mes_fmt = f"2026-{sheet_clean[:2]}"
            df_g = pd.read_excel(xls_gastos, sheet_name=sheet, skiprows=2)
            
            # Extrair Tabela de Gastos (Colunas I a O)
            gastos_mes = df_g.iloc[:, 8:15].dropna(subset=[df_g.columns[8]])
            gastos_mes.columns = ['Item', 'Vencimento', 'Categoria', 'Valor Total', 'Detalhes', 'Método', 'Status_Pago']
            gastos_mes['Parcela Atual'] = 1
            gastos_mes['Total Parcelas'] = 1
            gastos_mes['Status'] = gastos_mes['Status_Pago'].apply(lambda x: 'Pago' if x == True else 'Pendente')
            
            # Atualiza no histórico global do app
            if mes_fmt in st.session_state.historico:
                st.session_state.historico[mes_fmt]['gastos'] = gastos_mes[['Item', 'Categoria', 'Valor Total', 'Parcela Atual', 'Total Parcelas', 'Status']]
