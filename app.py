import streamlit as st
import datetime
import requests
import json

if "cliente_disabled" not in st.session_state:
    st.session_state.cliente_disabled = False
    st.session_state.tipo_cliente_disabled = False

def disable_selectbox(letra):
    if letra == "a":
        st.session_state.tipo_cliente_disabled = True
    elif letra == "b":
        st.session_state.cliente_disabled = True

url_clientes = "http://194.233.162.198/contadores"
url_tipo_clientes = "http://194.233.162.198/tipo_cliente" 

json_clientes = requests.get(url_clientes).text
json_tipos_cliente = requests.get(url_tipo_clientes).text

lista_clientes = json.loads(json_clientes)["contadores"]
lista_tipos_cliente = json.loads(json_tipos_cliente)["tipo_cliente"]



col_fecha, col_cliente, col_tipo_cliente = st.columns(3)

with col_fecha:
    d = st.date_input("Fecha", datetime.datetime.today())
    st.write("La fecha elegida es: ", d)

with col_cliente:
    cliente = st.selectbox(
        'Selecciona el cliente',
        lista_clientes,
        disabled=st.session_state.cliente_disabled,
        on_change=disable_selectbox,
        args="a"
    )
    st.write("Has elegido a: "+cliente)

with col_tipo_cliente:
    tipo_cliente = st.selectbox(
        'Selecciona el tipo del cliente',
        lista_tipos_cliente,
        disabled=st.session_state.tipo_cliente_disabled,
        on_change=disable_selectbox,
        args="b"
    )
    st.write("Has elegido a: "+tipo_cliente)

def click_button():
    st.write("Se van a buscar los datos con los valores:")
    st.write("Fecha: "+str(d))
    if st.session_state.cliente_disabled == False:
        st.write("Cliente: "+cliente)
    else:
        st.write("Tipo Cliente: "+tipo_cliente)
st.button('BUSCAR', on_click=click_button)