import json, io
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="JSON → XLS (curve1/2/3)", page_icon="📈")
st.title("JSON → XLSX: curve1/2/3 → s1/s2/s3")

uploaded = st.file_uploader("Upload JSON file", type=["json"])
if uploaded:
    data = json.load(uploaded)

    curve1 = data.get("curve1", [])
    curve2 = data.get("curve2", [])
    curve3 = data.get("curve3", [])

    max_len = max(len(curve1), len(curve2), len(curve3)) if any([curve1, curve2, curve3]) else 0
    pad = lambda lst, n: lst + [None] * (n - len(lst))

    df = pd.DataFrame({
        "s1": pad(curve1, max_len),
        "s2": pad(curve2, max_len),
        "s3": pad(curve3, max_len),
    })

    st.subheader("Preview (first 30 rows)")
    st.dataframe(df.head(30), use_container_width=True)

    # Excel in-memory
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="data")

    # use original JSON filename + "-converted.xlsx"
    base_name = os.path.splitext(uploaded.name)[0]
    file_name = f"{base_name}-converted.xlsx"

    st.download_button(
        "Preuzmi XLSX",
        data=buf.getvalue(),
        file_name=file_name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
    st.info("Učitaj .json fajl koji sadrži ključeve: curve1, curve2, curve3.")
