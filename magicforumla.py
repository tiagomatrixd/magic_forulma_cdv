#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from numpy import int64
import bin.set_path_fundamentus
from fundamentus import get_setor_data
from fundamentus import get_setor_id
import fundamentus
import pandas as pd
import sys


def filter_out(data):
    """
    filter out: Finance and Securities

    Input/Output: DataFrame()
    """

    df = data
    lst = []
    lst = lst + get_setor_data( get_setor_id('financeiro') )
    lst = lst + get_setor_data( get_setor_id('seguros'   ) )
    lst = lst + get_setor_data( get_setor_id('previdencia'   ) )
    lst = lst + get_setor_data( get_setor_id('finandiversos'))
    for idx in lst:
        try:
            df = df.drop(idx)
            # print('idx: ',idx, 'dropped.')
        except:
            # print('idx: ',idx, 'NOT FOUND.')
            pass

    return df

df = fundamentus.get_resultado_raw()

df = filter_out(df)

df = df[df['Liq.2meses'] > int(sys.argv[1])]
df = df[df['Mrg Ebit'] > 0]
df = df.sort_values('EV/EBIT',ascending=True)
ok = df.rename_axis('index').reset_index()
df['R. EV/EBit'] = ok.index + 1
df = df.sort_values('ROIC',ascending=False)
df['R. ROIC'] = ok.index + 1

df['magicFormula'] = df['R. ROIC'] + df['R. EV/EBit']
df = df.sort_values(['magicFormula'], ascending=[True])
df =  df.drop(columns=['P/Ativ Circ.Liq', 'P/Cap.Giro', 'Patrim. Líq'])
df1 = df.sort_values(['R. EV/EBit'], ascending=[True])
with pd.ExcelWriter('MagicFormulaCV.xlsx') as writer:  
    df.to_excel(writer, sheet_name='MagicFormula')
    df1.to_excel(writer, sheet_name='MagicFormula Clube do Valor')