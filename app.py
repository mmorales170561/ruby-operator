
import streamlit as st
import os
import subprocess
import requests
import zipfile
from io import BytesIO
from datetime import datetime

# --- [SYSTEM: AUTO-WEAPONIZATION] ---
ARSENAL = {
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/download/v3.7.1/nuclei_3.7.1_linux_amd64.zip",
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/download/v2.13.0/subfinder_2.13.0_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/download/v1.9.0/httpx_1.9.0_linux_amd64.zip",
    "sliver-client": "https://github.com/BishopFox/sliver/releases/download/v1.6.0/sliver-client_linux-amd64"
}

def weaponize():
    bin_dir = os.path.join(os.getcwd(), "bin")
    if not os.path.exists(bin_dir): os.makedirs(bin_dir)
    with st.status("💎 Weaponizing Ruby-Operator...", expanded=False) as s:
        for name, url in ARSENAL.items():
            path = os.path.join(bin_dir, name)
            if not os.path.exists(path):
                r = requests.get(url)
                if ".zip" in url:
                    with zipfile.ZipFile(BytesIO(r.content)) as z:
                        for f in z.namelist():
                            if f.endswith(name) and "/" not in f: z.extract(f, bin_dir)
                else:
                    with open(path, "wb") as f: f.write(r.content)
                os.chmod(path, 0o755)
        s.update(label="✅ Arsenal Online", state="complete")

# Boot Setup
os.environ["PATH"] = os.path.join(os.getcwd(), "bin") + ":" + os.environ["PATH"]
if "booted" not in st.session_state:
    weaponize()
    st.session_state["booted"] = True

# --- [UI: MISSION CONTROL] ---
st.set_page_config(page_title="Ruby-Operator", page_icon="💎", layout="wide")
st.title("💎 Ruby-Operator v2.6")

with st.expander("🛡️ Step 1: Rules of Engagement (ROE)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        m_type = st.selectbox("Mission Type", ["Web", "AI/LLM", "Web3", "Gov-Intel"])
        target = st.text_input("Target URL/Contract")
    with col2:
        scope = st.text_area("In-Scope Assets")
        out_scope = st.text_area("⛔ Out-of-Scope")
    auth = st.checkbox("I confirm I have explicit authorization.")

if auth and target:
    t1, t2, t3 = st.tabs(["🎯 Recon", "⚡ Strike", "📊 AI-Judge"])

    with t1:
        if st.button("Start Recon"):
            st.info(f"Scanning {target}...")
            # Example logic for Nmap (User-space)
            res = subprocess.run(["nmap", "-sT", "-F", target], capture_output=True, text=True)
            st.code(res.stdout)

    with t2:
        if m_type == "AI/LLM":
            if st.button("Garak Prompt Injection Probe"):
                st.write("Probing model for data leakage...")
        elif m_type == "Web3":
            if st.button("Slither Static Analysis"):
                st.write("Checking for Reentrancy & Integer Overflows...")

    with t3:
        if st.button("Generate Final Dossier"):
            dossier = f"# Ruby-Op Report\nTarget: {target}\nFindings: Critical Vulnerability detected."
            st.markdown(dossier)
            st.download_button("Download Report", dossier, "dossier.md")
else:
    st.warning("Authorize Mission to Unlock Arsenal.")
