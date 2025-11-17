import streamlit as st
import pandas as pd
import io
from io import BytesIO

st.title("Barcode Translator")
data_df = pd.DataFrame(
    {
        "widget1": ["we"],
        "widget2": ["2"]
    }
)

edited_df = st.data_editor(
    data_df,
    column_config={
        "widget1": st.column_config.Column(
            "Input Barcode",
            required=True
        ),
        "widget2": st.column_config.Column(
            "Translated Barcode",
            required=True
        )
    },
    hide_index=True,
    num_rows="dynamic",
)

if "history_df" not in st.session_state:
    st.session_state.history_df = pd.DataFrame(columns=["Entered Barcode","Output"])
def add_to_history():
    text = st.session_state["user_input"]
    if text:  # only save non-blank input
        st.session_state.history_df.loc[len(st.session_state.history_df)] = [text,""]

title = st.text_input("Enter barcode",key="user_input",on_change=add_to_history)
    
index = 0
test = 1
for i in edited_df.iloc[:,0]:
    if i==str(title):
        st.write(edited_df.iloc[index,1])
        st.session_state.history_df.iloc[-1,1]=edited_df.iloc[index,1]
        break
    index += 1

st.write("Scan History")
st.dataframe(st.session_state.history_df)


def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    processed_data = output.getvalue()
    return processed_data  
excel_bytes = to_excel_bytes(st.session_state.history_df)
st.download_button(
    label="Download Excel file",
    data=excel_bytes,
    file_name="history.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
