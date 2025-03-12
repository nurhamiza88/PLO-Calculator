import streamlit as st
import pandas as pd

def process_plo(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        
        mqf_to_plo_mapping = {
            "KU": "PLO1", "CS": "PLO2", "PS": "PLO3", "IS": "PLO4", "COMS": "PLO5",
            "DS": "PLO6", "NS": "PLO7", "LAR": "PLO8", "KP": "PLO9", "ES": "PLO10", "EP": "PLO11"
        }
        
        plo_achievement = df.groupby("MQF").apply(lambda x: (x["% Attainment"] * x["Weightage"]).sum() / x["Weightage"].sum())
        plo_achievement_df = plo_achievement.reset_index()
        plo_achievement_df.columns = ["MQF", "PLO Achievement (%)"]
        
        plo_achievement_df["PLO"] = plo_achievement_df["MQF"].map(mqf_to_plo_mapping)
        
        all_plo_df = pd.DataFrame(list(mqf_to_plo_mapping.items()), columns=["MQF", "PLO"])
        final_plo_df = all_plo_df.merge(plo_achievement_df, on=["MQF", "PLO"], how="left")
        
        mqf_order = ["KU", "CS", "PS", "IS", "COMS", "DS", "NS", "LAR", "KP", "ES", "EP"]
        final_plo_df["Order"] = final_plo_df["MQF"].apply(lambda x: mqf_order.index(x) if x in mqf_order else float("inf"))
        final_plo_df = final_plo_df.sort_values("Order").drop(columns=["Order"])
        
        output_file = "PLO_Achievement.xlsx"
        final_plo_df.to_excel(output_file, index=False)
        
        return final_plo_df, output_file
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
