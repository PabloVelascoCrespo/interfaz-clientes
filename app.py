import streamlit as st
import streamlit.components.v1 as components
from datetime import timedelta
import datetime
import requests
import json
import requests

url_clientes = "http://194.233.162.198/contadores"
url_tipo_clientes = "http://194.233.162.198/tipo_cliente" 
fecha = ""
tipo_cliente=""
cliente=""

st.set_page_config(layout="wide")

st.markdown(
    """
<style>
[data-testid="stMetricValue"] {
    font-size: 18px;
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
    st.session_state.fecha_disabled = False
    st.session_state.disable_all = False


def ColourWidgetText(wgt_txt, wch_colour = '#000000'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        elements[i].style.color = ' """ + wch_colour + """ '; } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)

def disable_selectbox(letra):
    if letra == "a":
        st.session_state.tipo_cliente_disabled = True
    elif letra == "b":
        st.session_state.cliente_disabled = True

def disable_all():
    st.session_state.disable_all = True

def buscar():
    disable_all()
    if  st.session_state.cliente_disabled:
        url_alerta_consumo_energetico = 'http://194.233.162.198/early_warning?dia='+str(fecha)+'&tipo_cliente='+str(tipo_cliente)
        st.title("Búsqueda del tipo de cliente")
    else:
        url_alerta_consumo_energetico = 'http://194.233.162.198/early_warning?dia='+str(fecha)+'&cnt='+str(cliente)
        st.title("Búsqueda del cliente")
    respuesta = requests.get(url_alerta_consumo_energetico, headers={'accept': 'application/json'})
    print(url_alerta_consumo_energetico)
    if( respuesta.status_code == requests.codes.ok ):
        diccionario_respuesta = json.loads(respuesta.text)
        st.subheader("Fecha:")
        st.write(str(diccionario_respuesta["fecha"]))
        if  not st.session_state.cliente_disabled:
            st.subheader("Cliente:")
            st.write(str(diccionario_respuesta["cnt"]))
        st.subheader("Tipo del Cliente:")
        st.write(str(diccionario_respuesta["tipo_cliente"]))

        st.subheader("Afectación de Consumo: Nivel:")
        
        col1,col2,col3,col4,col5 = st.columns(5)
        col1.metric("Nivel", str(diccionario_respuesta["afectacion_de_consumo"]["nivel"]))
        col2.metric("Sentido", str(diccionario_respuesta["afectacion_de_consumo"]["sentido"]))
        
        color = ""
        if str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Muy bajo" or str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Bajo":
            color = "green"
        elif str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Muy alto" or str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Alto":
            color = "red"
        elif str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Regular":
            color = "blue"
        else:
            color = "gray"
        st.subheader("Consumo del día:")
        st.write(":"+color+"[" + str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) + "]")

        st.subheader("Meteorología")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Temperatura mínima", str(diccionario_respuesta["detalles_dia"]["meteorologia"]["temperatura_minima"]["etiqueta"]), str(diccionario_respuesta["detalles_dia"]["meteorologia"]["temperatura_minima"]["valor_numerico"]) + " ºC", delta_color="off")
        col2.metric("Temperatura media", str(diccionario_respuesta["detalles_dia"]["meteorologia"]["temperatura media"]["etiqueta"]), str(diccionario_respuesta["detalles_dia"]["meteorologia"]["temperatura media"]["valor_numerico"]) + " ºC", delta_color="off")
        col3.metric("Temperatura máxima", str(diccionario_respuesta["detalles_dia"]["meteorologia"]["temperatura_maxima"]["etiqueta"]), str(diccionario_respuesta["detalles_dia"]["meteorologia"]["temperatura_maxima"]["valor_numerico"]) + " ºC", delta_color="off")
        col4.metric("Precipitacion", str(diccionario_respuesta["detalles_dia"]["meteorologia"]["precipitacion"]["etiqueta"]), str(diccionario_respuesta["detalles_dia"]["meteorologia"]["precipitacion"]["valor_numerico"]), delta_color="off")
        col5.metric("Horas de sol", str(diccionario_respuesta["detalles_dia"]["meteorologia"]["horas_de_sol"]["etiqueta"]), str(diccionario_respuesta["detalles_dia"]["meteorologia"]["horas_de_sol"]["valor_numerico"]), delta_color="off")

        if diccionario_respuesta["detalles_dia"]["fin de semana"]:
            col1.metric("Fin de semana", "Si")
        else:
            col1.metric("Fin de semana", "No")
        col2.metric("Estación", str(diccionario_respuesta["detalles_dia"]["estacion"]))
        if diccionario_respuesta["detalles_dia"]["eventos"] == []:
            col3.metric("Eventos", "No")
        else:
            for i in diccionario_respuesta["detalles_dia"]["eventos"]:
                col3.metric("Eventos", str(i["Nombre"]), str(i["Clase"]), delta_color="off")
        if diccionario_respuesta["detalles_dia"]["incidencias"] == []:
            col4.metric("Incidencias", "No")
        else:
            for i in diccionario_respuesta["detalles_dia"]["incidencias"]:
                col4.metric("Incidencias", i)
        if diccionario_respuesta["detalles_dia"]["festivo"]:
            col5.metric("Fiesta", str(diccionario_respuesta["detalles_dia"]["fiesta"]))
        else:
            col5.metric("Fiesta", "No")
        respuesta1 = requests.post(url_alerta_consumo_energetico, headers={'accept': 'application/json', 'Content-Type': 'application/json'}, data='{"fecha": "'+str(fecha+timedelta(days=-1))+'"}')
        respuesta2 = requests.post(url_alerta_consumo_energetico, headers={'accept': 'application/json', 'Content-Type': 'application/json'}, data='{"fecha": "'+str(fecha+timedelta(days=-2))+'"}')
        if( respuesta1.status_code == requests.codes.ok ):
            diccionario_respuesta1 = json.loads(respuesta1.text)
            col4.metric("Día "+str(fecha+timedelta(days=-1))+":", "Consumo:", str(diccionario_respuesta1["tipo_de_dia_de_consumo"]["etiqueta"]), delta_color="off")
        if( respuesta2.status_code == requests.codes.ok ):
            diccionario_respuesta2 = json.loads(respuesta2.text)
            col2.metric("Día "+str(fecha+timedelta(days=-2))+":", "Consumo:", str(diccionario_respuesta2["tipo_de_dia_de_consumo"]["etiqueta"]), delta_color="off")

    else:
        st.write("Día no encontrado")

    a,b,c = st.columns(3)

    b.button('REINICIAR', on_click=reiniciar)


def reiniciar():
    st.session_state.cliente_disabled = False
    st.session_state.tipo_cliente_disabled = False
    st.session_state.fecha_disabled = False
    st.session_state.disable_all = False

json_clientes = requests.get(url_clientes).text
json_tipos_cliente = requests.get(url_tipo_clientes).text

lista_clientes = json.loads(json_clientes)["contadores"]
lista_tipos_cliente = json.loads(json_tipos_cliente)["tipo_cliente"]

col_fecha, col_cliente, col_tipo_cliente = st.columns(3)

col_fecha, col_cliente, col_tipo_cliente = st.columns(3)

ColourWidgetText('Primavera', '#F586E3')
ColourWidgetText('Verano', '#FF7B21')
ColourWidgetText('Otoño', '#B74E0D')
ColourWidgetText('Invierno', '#AEEDE6')

ColourWidgetText('Muy fria', '#83FFFD') 
ColourWidgetText('Fria', '#10EFFF') 
ColourWidgetText('Templada', '#42FF35') 
ColourWidgetText('Calurosa', '#FF0000') 
ColourWidgetText('Muy calurosa', '#B30000')

ColourWidgetText('Bajo', 'green') 
ColourWidgetText('Muy bajo', 'green') 
ColourWidgetText('Regular', 'blue') 
ColourWidgetText('Alto', 'red') 
ColourWidgetText('Muy alto', 'red') 

if not st.session_state.disable_all:
    with col_fecha:
        fecha = st.date_input("Fecha", datetime.datetime.today(), disabled=st.session_state.fecha_disabled)
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

