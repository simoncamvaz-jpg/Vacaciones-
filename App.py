import streamlit as st
import pandas as pd
import os
from datetime import date

# --- CONFIGURACIÓN DE EQUIPOS (Extraído de tus fotos) ---
EQUIPOS = {
    "Eugenio": "Roberto", "Roberto": "Eugenio",
    "Diego": "J. Nielfa", "J. Nielfa": "Diego",
    "Rafa": "Quique", "Quique": "Rafa",
    "Simón": "Fernando", "Fernando": "Simón",
    "Antonio": "José Ramón", "José Ramón": "Antonio"
}

ARCHIVO_DATOS = 'vacaciones.csv'

# --- FUNCIONES ---
def cargar_datos():
    if not os.path.exists(ARCHIVO_DATOS):
        return pd.DataFrame(columns=["Empleado", "Fecha", "Compañero"])
    return pd.read_csv(ARCHIVO_DATOS)

def guardar_datos(df):
    df.to_csv(ARCHIVO_DATOS, index=False)

# --- INTERFAZ GRÁFICA ---
st.title("🏖️ Gestor de Vacaciones - Turnos 2026")

# 1. Selección de Usuario
usuario = st.selectbox("¿Quién eres?", list(EQUIPOS.keys()))
compañero = EQUIPOS[usuario]

st.info(f"👋 Hola **{usuario}**. Tu compañero de equipo es **{compañero}**.")

# 2. Cargar vacaciones existentes
df = cargar_datos()

# Ver vacaciones de tu compañero para que sepas qué días NO puedes coger
if not df.empty:
    vacaciones_compi = df[df["Empleado"] == compañero]["Fecha"].tolist()
    if vacaciones_compi:
        st.warning(f"⚠️ {compañero} ya tiene vacaciones: {', '.join(vacaciones_compi)}")
    else:
        st.success(f"{compañero} aún no ha pedido vacaciones.")

# 3. Selector de nuevas vacaciones
fecha_elegida = st.date_input("Elige una fecha para pedir libre", min_value=date(2026, 1, 1))
fecha_str = str(fecha_elegida)

col1, col2 = st.columns(2)

with col1:
    if st.button("Solicitar Vacaciones"):
        # VALIDACIÓN: Regla de oro
        if not df.empty and ((df["Empleado"] == compañero) & (df["Fecha"] == fecha_str)).any():
            st.error(f"⛔ ERROR: No puedes pedir el {fecha_str}. {compañero} ya lo tiene asignado.")
        
        # VALIDACIÓN: No duplicar
        elif not df.empty and ((df["Empleado"] == usuario) & (df["Fecha"] == fecha_str)).any():
            st.warning("Ya tienes ese día pedido.")
            
        else:
            # Guardar
            nuevo_registro = pd.DataFrame([{"Empleado": usuario, "Fecha": fecha_str, "Compañero": compañero}])
            df = pd.concat([df, nuevo_registro], ignore_index=True)
            guardar_datos(df)
            st.success(f"✅ Vacaciones confirmadas para el {fecha_str}")
            st.rerun()

with col2:
    if st.button("Borrar fecha seleccionada"):
        # Borrar mis vacaciones
        df = df[~((df["Empleado"] == usuario) & (df["Fecha"] == fecha_str))]
        guardar_datos(df)
        st.success("Día eliminado.")
        st.rerun()

# 4. Tabla Resumen
st.divider()
st.subheader("📅 Calendario Global")
st.dataframe(df.sort_values(by="Fecha"), use_container_width=True)
