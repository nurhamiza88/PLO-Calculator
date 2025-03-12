import streamlit as st
import pandas as pd

def process_plo(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        
        # Pemetaan MQF ke PLO
        mqf_to_plo_mapping = {
            "KU": "PLO1", "CS": "PLO2", "PS": "PLO3", "IS": "PLO4", "COMS": "PLO5",
            "DS": "PLO6", "NS": "PLO7", "LAR": "PLO8", "KP": "PLO9", "ES": "PLO10", "EP": "PLO11"
        }
        
        # Kira purata % Attainment bagi setiap kategori MQF
        plo_achievement = df.groupby("MQF")["% Attainment"].mean().reset_index()
        plo_achievement["PLO"] = plo_achievement["MQF"].map(mqf_to_plo_mapping)
        
        # Susun mengikut urutan MQF yang betul
        mqf_order = ["KU", "CS", "PS", "IS", "COMS", "DS", "NS", "LAR", "KP", "ES", "EP"]
        plo_achievement["Order"] = plo_achievement["MQF"].apply(lambda x: mqf_order.index(x) if x in mqf_order else float("inf"))
        plo_achievement = plo_achievement.sort_values("Order").drop(columns=["Order"])
        
        # Susun semula lajur agar PLO menjadi lajur pertama
        plo_achievement = plo_achievement[["PLO", "MQF", "% Attainment"]]
        
        output_file = "PLO_Achievement.xlsx"
        plo_achievement.to_excel(output_file, index=False)
        
        return plo_achievement, output_file
    return None, None

st.title("PLO Calculation Tool")
st.write("Upload your Excel file to calculate PLO achievements and download the results.")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    results_df, output_file = process_plo(uploaded_file)
    
    if results_df is not None:
        st.write("### Processed PLO Data")
        st.dataframe(results_df)
        
        with open(output_file, "rb") as file:
            st.download_button(label="Download Processed PLO Data", data=file, file_name="PLO_Achievement.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
