import io
import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# -----------------------------
# SETTINGS
# -----------------------------
TEMPLATE = "billmemo.jpg"   # must be in the same folder / repo as this file
FONT_PATH = "arial.ttf"     # bundle a .ttf in the repo so it works on any server

st.set_page_config(page_title="Tempo Bill Generator", page_icon="🧾", layout="centered")
st.title("🧾 Raghav Tempo Service Bill Generator")

# -----------------------------
# Inputs
# -----------------------------
invoice = st.text_input("Invoice Number").strip()
date = st.text_input("Date").strip()
customer = st.text_input("Customer Name").strip()

generate = st.button("Generate Bill", type="primary")

# -----------------------------
# Generate Bill
# -----------------------------
if generate:
    if not os.path.exists(TEMPLATE):
        st.error(
            f"Template image '{TEMPLATE}' not found. "
            "Make sure it's uploaded to the same folder as app.py in your repo."
        )
        st.stop()

    img = Image.open(TEMPLATE).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(FONT_PATH, 24)
    except Exception:
        font = ImageFont.load_default()

    # Hardcoded positions (same as your original script)
    if invoice:
        draw.text((1263, 31), invoice, fill="black", font=font)
    if date:
        draw.text((1167, 58), date, fill="black", font=font)
    if customer:
        draw.text((128, 425), customer, fill="black", font=font)

    # Save to an in-memory buffer instead of disk
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    filename = f"{invoice}.png" if invoice else "Untitled.png"

    st.success("Bill generated!")

    # Preview
    preview = img.copy()
    preview.thumbnail((450, 650))
    st.image(preview, caption="Preview")

    # Download button
    st.download_button(
        label="⬇️ Download Bill",
        data=buf,
        file_name=filename,
        mime="image/png",
    )
