import streamlit as st
import pandas as pd
import numpy as np

def calcular_megas(row):
    if row['unidad'] == "MiB": return row['cantidad']
    elif row['unidad'] == 'GiB': return row['cantidad'] * 1000
    elif row['unidad'] == 'KiB': return row['cantidad'] / 1000
    else: return 0

csv_file = st.file_uploader(label = "Archivo CSV", type = ['csv'], help = "Texto de ayuda")
if csv_file:
    dataframe = pd.read_csv(csv_file)

    # Extrae cantidad y tipo de datos (Megas o Kbs)
    df1 = dataframe[' Uso'].str.extractall(r"(\d*,?\d*)\b ([KGM]iB)\b\w*")
    df2 = df1.unstack()
    df2.columns = df2.columns.droplevel()
    df2 = df2.iloc[:,[2,4]]
    df2.rename(columns={2: 'cantidad', 1: 'unidad'}, inplace=True)
    df2['cantidad'] = [ x.replace(',', '.') if type(x) is str else x for x in df2['cantidad']]
    df2['cantidad'] = df2['cantidad'].astype(float)
    df2['Megas'] = df2.apply(lambda row: calcular_megas(row), axis=1)
    dataframe = dataframe.join(df2)
    st.dataframe(dataframe)
    met1, met2, met3 = st.columns(3)
    met2.metric('Mb Total', f"{dataframe['Megas'].sum().round()} Mb")
    met3.metric('Mb Roaming', f"{dataframe.loc[dataframe[' Roaming'] == 'Y']['Megas'].sum().round()} Mb")
    #met3.metric('Recargas en periodo', f"{dataframe.loc[dataframe[' Tipo'] == 'Recargar'][' Impacto en el saldo'].astype(float).sum()}")
    st.bar_chart(dataframe,x="Fecha y hora", y="Megas")
else:
    st.info("Sube el archivo .csv obtenido al exportar el Histórico en Qvantel.")

