
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math

st.set_page_config(page_title="SACS Joint Load Generator", layout="centered")

# Inject Plausible script
plausible_script = """
<script defer data-domain='sacs-joint-load-generator.onrender.com' src='https://plausible.io/js/script.js'></script>
"""  # noqa
components.html(plausible_script, height=0)

# Sidebar About Me
with st.sidebar:
    st.markdown("### About Me")
    st.markdown("""
👨‍💻 **Sajjad Babamohammadi**  
Structural Engineer | Offshore | FEM  
[LinkedIn](https://www.linkedin.com/in/sajjad-b-7aab1b172/)
    """)

st.title("SACS Joint Load Generator")
st.caption("Created by Sajjad Babamohammadi")

# Quick Guide
with st.expander("📘 Quick Start Guide"):
    st.markdown("""
**What this app does**  
Converts Excel joint load definitions into `.txt` output for SACS Datagen.

**Excel format (Header row required):**  
- Load Condition  
- Load ID  
- Joint Name  
- FORCE(X), FORCE(Y), FORCE(Z)  
- MOMENT(X), MOMENT(Y), MOMENT(Z)

**How to use:**  
1. Download the sample Excel below
2. Replace with your actual values
3. Upload the Excel file
4. Download the SACS-ready `.txt` output

📝 *Each load condition can include multiple joints below it until an empty row appears.*
    """)

with open("SACS_Load_Sample.xlsx", "rb") as sample_file:
    st.download_button("📎 Download Sample Excel File", sample_file, file_name="SACS_Load_Sample.xlsx")

uploaded_file = st.file_uploader("Upload Your Excel File", type=["xlsx"])
rounded_values_log = []

if uploaded_file:
    components.html("""
        <script>
            if (typeof plausible === "function") {
                plausible("Upload File");
            }
        </script>
    """, height=0)

def round_to_seven_chars(value_str: str) -> str:
    try:
        num = float(value_str)
        for precision in range(6, -1, -1):
            rounded = round(num, precision)
            as_str = f"{rounded:.{precision}f}".rstrip('0').rstrip('.') if '.' in f"{rounded:.{precision}f}" else f"{rounded:.{precision}f}"
            if len(as_str) <= 7:
                return as_str.rjust(7)
        rough = f"{round(num)}"
        return rough[:7].rjust(7)
    except:
        return "   0.0"

def format_number(value: str) -> str:
    raw = value
    value = "0" if str(value).strip().lower() in ("", "nan") else str(value)
    if len(value) <= 7:
        return value.rjust(7)
    rounded_str = round_to_seven_chars(value)
    if rounded_str.strip() != value:
        rounded_values_log.append(f"'{raw}' was rounded to '{rounded_str.strip()}'")
    return rounded_str

def format_load_line(joint_name, fx, fy, fz, mx, my, mz, load_id):
    return (
        "LOAD" + " " * 3 +
        joint_name + " " * 5 +
        format_number(fx) +
        format_number(fy) +
        format_number(fz) +
        format_number(mx) + " " +
        format_number(my) +
        format_number(mz) + " " +
        "GLOB JOIN" + " " * 3 +
        load_id.ljust(8)
    ).ljust(81)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    header = [str(h).strip().lower().replace(" ", "") for h in df.columns]

    def smart_col(*keywords):
        keywords = [k.lower().replace(" ", "") for k in keywords]
        for i, h in enumerate(header):
            h_clean = h.lower().replace(" ", "")
            if all(k in h_clean for k in keywords):
                return i
        raise ValueError(f"Column not found matching: {' + '.join(keywords)}")

    try:
        load_cond_col = smart_col("Load", "Condition")
        load_id_col   = smart_col("Load", "ID")
        joint_col     = smart_col("Joint", "Name")
        fx_col        = smart_col("FORCE(X)")
        fy_col        = smart_col("FORCE(Y)")
        fz_col        = smart_col("FORCE(Z)")
        mx_col        = smart_col("MOMENT(X)")
        my_col        = smart_col("MOMENT(Y)")
        mz_col        = smart_col("MOMENT(Z)")

        output_lines = []
        current_condition = None
        rounded_values_log.clear()

        for _, row in df.iterrows():
            load_condition = str(row[load_cond_col]).strip() if not pd.isna(row[load_cond_col]) else ""
            load_id = str(row[load_id_col]).strip() if not pd.isna(row[load_id_col]) else ""
            joint = str(row[joint_col]).strip() if not pd.isna(row[joint_col]) else ""

            if load_condition:
                current_condition = load_condition
                output_lines.append(f"LOADCN{current_condition}")

            if not load_id or not joint:
                continue

            line = format_load_line(
                joint_name=joint,
                fx=row[fx_col], fy=row[fy_col], fz=row[fz_col],
                mx=row[mx_col], my=row[my_col], mz=row[mz_col],
                load_id=load_id
            )
            output_lines.append(line)

        result_txt = "\n".join(output_lines)
        if st.download_button("Download SACS File", result_txt, file_name="sacs_output.txt"):
            components.html("""
                <script>
                    if (typeof plausible === "function") {
                        plausible("Download SACS File");
                    }
                </script>
            """, height=0)

        if rounded_values_log:
            log_text = "Rounded Values:\n" + "\n".join(rounded_values_log)
            if st.download_button("Download Rounding Log", log_text, file_name="rounding_log.txt"):
                components.html("""
                    <script>
                        if (typeof plausible === "function") {
                            plausible("Download Log");
                        }
                    </script>
                """, height=0)

    except Exception as e:
        st.error(f"Error: {e}")

# Legal disclaimer footer
st.markdown(
    "<div style='text-align: center; font-size: 0.75rem; color: gray; margin-top: 2rem;'>"
    "⚠️ Although this tool has been carefully designed and tested, the responsibility for validating results and ensuring compliance with engineering standards lies with the user."
    "</div>",
    unsafe_allow_html=True
)
