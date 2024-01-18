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
json_clientes = requests.get(url_clientes).text
json_tipos_cliente = requests.get(url_tipo_clientes).text

lista_clientes = json.loads(json_clientes)["contadores"]
lista_tipos_cliente = json.loads(json_tipos_cliente)["tipo_cliente"]

st.set_page_config(layout="wide")

if "cliente_disabled" not in st.session_state:
    st.session_state.cliente_disabled = False
    st.session_state.tipo_cliente_disabled = False
    st.session_state.fecha_disabled = False
    st.session_state.disable_all = False

def reiniciar():
    st.session_state["current_page"] = "main_page"
    st.session_state.cliente_disabled = False
    st.session_state.tipo_cliente_disabled = False
    st.session_state.cnt_selectbox = '-------------------------'
    st.session_state.tipo_cliente_selectbox = '-------------------------'

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

def data_page():
    url_alerta_consumo_energetico = ""
    respuesta = ""
#    if st.session_state["cnt"] == '-------------------------' and st.session_state["tipo_cliente"] == '-------------------------':
#        st.title("Debes seleccionar un cliente o un tipo de cliente.")
#    elif st.session_state["cnt"] == '-------------------------':
#        url_alerta_consumo_energetico = 'http://194.233.162.198/early_warning?dia='+str(st.session_state["fecha"])+'&tipo_cliente='+str(st.session_state["tipo_cliente"])
#    else:
#        url_alerta_consumo_energetico = 'http://194.233.162.198/early_warning?dia='+str(st.session_state["fecha"])+'&cnt='+str(st.session_state["cnt"])
#    if url_alerta_consumo_energetico == "":
#        pass

    if st.session_state["tipo_cliente"] == '-------------------------':
        st.title("Debes seleccionar un cliente o un tipo de cliente.")
    else:
        url_alerta_consumo_energetico = 'http://194.233.162.198/early_warning?dia='+str(st.session_state["fecha"])+'&tipo_cliente='+str(st.session_state["tipo_cliente"])    
    if url_alerta_consumo_energetico == "":
        pass
    else:
        respuesta = requests.get(url_alerta_consumo_energetico, headers={'accept': 'application/json'})
        if( respuesta.status_code == requests.codes.ok ):
#            if st.session_state["cnt"] == '-------------------------':
#                st.title("Búsqueda por tipo de cliente")
#            else:
#                st.title("Búsqueda por cliente")
            st.title("Búsqueda por tipo de cliente")
            diccionario_respuesta = json.loads(respuesta.text)
            print(diccionario_respuesta)
            st.subheader("Fecha:")
            st.write( diccionario_respuesta["fecha"][8:10]+"/"+diccionario_respuesta["fecha"][5:7]+"/"+diccionario_respuesta["fecha"][0:4])
#            if st.session_state["tipo_cliente"] == '-------------------------':
#                st.subheader("Cliente:")
#                st.write(str(diccionario_respuesta["cnt"]))
            st.subheader("Tipo del Cliente:")
            st.write(str(diccionario_respuesta["tipo_cliente"]))

            st.subheader("Afectación de Consumo:")
            col1,col2,col3,col4,col5 = st.columns(5)

            flecha = ""

            col1.metric("Nivel", str(diccionario_respuesta["afectacion_de_consumo"]["nivel"]))

            if str(diccionario_respuesta["afectacion_de_consumo"]["sentido"]) == "Alza":
                flecha = "⬆"
            elif str(diccionario_respuesta["afectacion_de_consumo"]["sentido"]) == "Baja":
                flecha = "⬇"
            else:
                flecha = "→"

            col2.metric("Sentido", flecha+str(diccionario_respuesta["afectacion_de_consumo"]["sentido"]))

            col3.metric("Ajuste", "",str(diccionario_respuesta["afectacion_de_consumo"]["ajuste"])+" kWh")
            col4.metric("Desviación estándar", "",str(diccionario_respuesta["afectacion_de_consumo"]["desviacion"])+" kWh")

            color = ""
            if str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Muy bajo" or str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Bajo":
                color = "green"
            elif str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Muy alto" or str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Alto":
                color = "red"
            elif str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) == "Regular":
                color = "blue"
            else:
                color = "gray"

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
            if diccionario_respuesta["detalles_dia"]["vispera_festivo"]:
                col5.metric("Víspera de festivo", str(diccionario_respuesta["detalles_dia"]["vispera_fiesta"]))
            if diccionario_respuesta["detalles_dia"]["post_festivo"]:
                col5.metric("Post festivo", str(diccionario_respuesta["detalles_dia"]["post_fiesta"]))

            st.subheader("Consumo del día:")
            st.write(":"+color+"[" + str(diccionario_respuesta["tipo_de_dia_de_consumo"]["etiqueta"]) + "]")
        else:
            st.title("Día no encontrado")

    a,b,c,d,e = st.columns(5)

    c.button("REINICIAR", on_click=reiniciar)
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

    ColourWidgetText('Mucho', 'red')
    ColourWidgetText('Poco', 'green')
    ColourWidgetText('No afecta', 'blue')
    ColourWidgetText('⬆Alza', 'red')
    ColourWidgetText('⬇Baja', 'green')
    ColourWidgetText('→No afecta', 'blue')

def main_page():
    #col_fecha, col_cliente, col_tipo_cliente = st.columns(3)

    col_fecha, col_tipo_cliente = st.columns(2)

    with col_fecha:
        st.session_state["fecha"] = st.date_input("Fecha", value=datetime.date(2022, 10, 1),min_value=datetime.date(2022, 10, 1), max_value=datetime.date(2023, 10, 31), disabled=st.session_state.fecha_disabled, format="DD/MM/YYYY")
   # with col_cliente:
   #     opciones_cnt = ['-------------------------']+lista_clientes
   #     st.session_state["cnt"] = st.selectbox(
   #         'Selecciona el cliente',
   #         opciones_cnt,
   #         key="cnt_selectbox",
   #         on_change=disable_selectbox,
   #         args="a",
   #         disabled=st.session_state.cliente_disabled
   #     )
        

    with col_tipo_cliente:
        opciones_tipo_cliente = ['-------------------------']+lista_tipos_cliente
        st.session_state["tipo_cliente"] = st.selectbox( 
            'Selecciona el tipo del cliente',
            opciones_tipo_cliente,
            key="tipo_cliente_selectbox",
            on_change=disable_selectbox,
            args="b",
            disabled=st.session_state.tipo_cliente_disabled
        )

    a,b,c,d,e,f,g,h,i,j,k,l,m,n,ñ = st.columns(15)

    if h.button("BUSCAR"):
        st.session_state["current_page"] = "data_page"
        st.rerun()

    h.button("REINICIAR", on_click=reiniciar)

def main():
    st.session_state.setdefault("current_page", "main_page")
    if st.session_state["current_page"] == "main_page":
        main_page()
    elif st.session_state["current_page"] == "data_page":
        data_page()

if __name__ == '__main__':
    main()