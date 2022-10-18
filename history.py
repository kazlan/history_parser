from unicodedata import decimal
import streamlit as st
import pandas as pd

def calcular_megas(df):
    # Cambia la coma decimal por puntos
    df[0] = [x.replace(',', '.') for x in df[0]]
    #Convierte la columna a numérica
    df[0] = pd.to_numeric(df[0], downcast="float")
    # divide entre mil si son Kb para tenerlo todo en megas
    df[2] = df1[0] if df1[1].to_string == "MiB" else df1[0] /1000
    # devuelve la suma de megas con precision de 3 decimales
    return df[2].sum().round()

csv_file = st.file_uploader(label = "Archivo CSV", type = ['csv'], help = "Texto de ayuda")
if csv_file:
    dataframe = pd.read_csv(csv_file)
    st.write(dataframe)

    # Extrae cantidad y tipo de datos (Megas o Kbs)
    df1 = dataframe[' Uso'].str.extractall(r"(\d*,?\d*)\b ([KM]iB)\b\w*")
    df2 = df1.unstack()
    df2.columns = df2.columns.droplevel()
    df2.iloc[:,2:4]
    dataframe = dataframe.join(df2.iloc[:,2:4])
    dataframe.rename(columns={2: "cantidad", 0: "unidad"}, inplace=True)
    dataframe.columns
    st.metric("Total", f"{calcular_megas(df1)} Mb")
    st.bar_chart(dataframe,x="Fecha y hora", y=" Impacto")
    
else:
    st.info("Sube el archivo .csv obtenido al exportar el Histórico en Qvantel.")

