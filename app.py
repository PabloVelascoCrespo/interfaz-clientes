import streamlit as st
import streamlit.components.v1 as components
import datetime
import requests
import json
import requests
st.set_page_config(layout="wide")

st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 20px;
}
</style>
<style>
[data-testid="stMetricDelta"] svg {
    display: none;
}
</style>
""",
    unsafe_allow_html=True,
)

if "cliente_disabled" not in st.session_state:
    st.session_state.cliente_disabled = False
    st.session_state.tipo_cliente_disabled = False

def ColourWidgetText(wgt_txt, wch_colour = '#000000'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        elements[i].style.color = ' """ + wch_colour + """ '; } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

ColourWidgetText('Muy fria', '#83FFFD') 
ColourWidgetText('Fria', '#10EFFF') 
ColourWidgetText('Templada', '#42FF35') 
ColourWidgetText('Calurosa', '#FF0000') 
ColourWidgetText('Muy calurosa', '#B30000') 

def disable_selectbox(letra):
    if letra == "a":
        st.session_state.tipo_cliente_disabled = True
    elif letra == "b":
        st.session_state.cliente_disabled = True
#TODO
def buscar():
    respuesta = requests.post(url_alerta_consumo_energetico, headers={'accept': 'application/json', 'Content-Type': 'application/json'}, data='{"fecha": "'+str(fecha)+'"}')
    if( respuesta.status_code == requests.codes.ok ):
        diccionario_respuesta = json.loads(respuesta.text)
        st.subheader("Fecha: " + str(diccionario_respuesta["fecha"]))
        st.subheader("Consumo del día: " + str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]))
        st.subheader("Meteorología:")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Temperatura mínima", str(diccionario_respuesta["detalles"]["meteorologia"]["temperatura_minima"]["etiqueta"]), str(diccionario_respuesta["detalles"]["meteorologia"]["temperatura_minima"]["valor_numerico"]) + " ºC", delta_color="off")
        col2.metric("Temperatura media", str(diccionario_respuesta["detalles"]["meteorologia"]["temperatura media"]["etiqueta"]), str(diccionario_respuesta["detalles"]["meteorologia"]["temperatura media"]["valor_numerico"]) + " ºC", delta_color="off")
        col3.metric("Temperatura máxima", str(diccionario_respuesta["detalles"]["meteorologia"]["temperatura_maxima"]["etiqueta"]), str(diccionario_respuesta["detalles"]["meteorologia"]["temperatura_maxima"]["valor_numerico"]) + " ºC", delta_color="off")
        col4.metric("Precipitacion", str(diccionario_respuesta["detalles"]["meteorologia"]["precipitacion"]["etiqueta"]), str(diccionario_respuesta["detalles"]["meteorologia"]["precipitacion"]["valor_numerico"]), delta_color="off")
        col5.metric("Horas de sol", str(diccionario_respuesta["detalles"]["meteorologia"]["horas_de_sol"]["etiqueta"]), str(diccionario_respuesta["detalles"]["meteorologia"]["horas_de_sol"]["valor_numerico"]), delta_color="off")

        if diccionario_respuesta["detalles"]["fin de semana"]:
            col1.metric("Fin de semana", "Si")
        else:
            col1.metric("Fin de semana", "No")
        col2.metric("Estación", str(diccionario_respuesta["detalles"]["estacion"]))
        if diccionario_respuesta["detalles"]["eventos"] == []:
            col3.metric("Eventos", "No")
        else:
            for i in diccionario_respuesta["detalles"]["eventos"]:
                col3.metric("Eventos", str(i["Nombre"]), str(i["Clase"]), delta_color="off")
        if diccionario_respuesta["detalles"]["festivo"]:
            col4.metric("Fiesta", str(diccionario_respuesta["detalles"]["fiesta"]))
        else:
            col4.metric("Fiesta", "No")
    else:
        st.write("Día no encontrado")


def reiniciar():
    st.session_state.cliente_disabled = False
    st.session_state.tipo_cliente_disabled = False

url_clientes = "http://194.233.162.198/contadores"
url_tipo_clientes = "http://194.233.162.198/tipo_cliente" 
url_alerta_consumo_energetico = 'http://194.233.162.198/alerta_consumo_energetico'

json_clientes = requests.get(url_clientes).text
json_tipos_cliente = requests.get(url_tipo_clientes).text

lista_clientes = json.loads(json_clientes)["contadores"]
lista_tipos_cliente = json.loads(json_tipos_cliente)["tipo_cliente"]



col_fecha, col_cliente, col_tipo_cliente = st.columns(3)

with col_fecha:
    fecha = st.date_input("Fecha", datetime.datetime.today())

with col_cliente:
    cliente = st.selectbox(
        'Selecciona el cliente',
        lista_clientes,
        disabled=st.session_state.cliente_disabled,
        on_change=disable_selectbox,
        args="a"
    )
    st.button('BUSCAR', on_click=buscar)
    st.button('REINICIAR', on_click=reiniciar)


with col_tipo_cliente:
    tipo_cliente = st.selectbox(
        'Selecciona el tipo del cliente',
        lista_tipos_cliente,
        disabled=st.session_state.tipo_cliente_disabled,
        on_change=disable_selectbox,
        args="b"
    )

