import streamlit as st
import requests
from datetime import datetime
import pandas as pd

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''

# Solicitar fecha y hora de recogida
pickup_date = st.date_input("Select the pickup date")
pickup_time = st.time_input("Select the pickup time")

# Combinar fecha y hora en un solo objeto datetime
pickup_datetime = datetime.combine(pickup_date, pickup_time)


# Ask the user to select the parameters of the ride
pickup_longitude = st.number_input("Pickup longitude")
pickup_latitude = st.number_input("Pickup latitude")
dropoff_longitude = st.number_input("Dropoff longitude")
dropoff_latitude = st.number_input("Dropoff latitude")
passenger_count = st.number_input("Passenger count", min_value=1, max_value=8)

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

if url == 'https://taxifare.lewagon.ai/predict':

    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

"""

2. Let's build a dictionary containing the parameters for our API...
"""

params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}
"""
3. Let's call our API using the `requests` package...
"""
""""
4. Let's retrieve the prediction from the **JSON** returned by the API...
"""

# Botón para hacer la solicitud
if st.button("Get Fare Prediction"):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        prediction = response.json()
        fare = prediction['fare']
        st.success(f"💰 Tarifa estimada: **${fare:.2f}**")

        # Historial de predicciones
        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append(params | {"fare": fare})

    else:
        st.error("❌ Error al obtener la predicción.")
"""
## Finally, we can display the prediction to the user
"""

"""
EXTRA
"""
# Mostrar historial de predicciones
if "history" in st.session_state and len(st.session_state.history) > 0:
    st.markdown("### Historial de Predicciones:")
    df_history = pd.DataFrame(st.session_state.history)
    st.dataframe(df_history)
