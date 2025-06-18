# app.py
# ---------------------------------------------------------------
# Minimal Streamlit climate-stripes viewer with hard-coded data
# ---------------------------------------------------------------
# 
# ---------------------------------------------------------------

import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

# 1.  Hard-coded (year, anomaly, hex colour) list  ----------------
STRIPES = [
    (1913, -0.458, '#00356b'),
    (1914, -0.292, '#005595'),
    (1915, -0.190, '#006ba7'),
    (1916, -0.339, '#004f8e'),
    (1917, -0.446, '#003969'),
    # … paste all tuples here …
    (2020, 1.096, '#bf2320'),
    (2021, 0.854, '#e16c4e'),
    (2022, 0.886, '#db5e41'),
    (2023, 1.138, '#b80018'),
    (2024, 1.284, '#a20011'),
]

YEARS  = [y for y, _, _ in STRIPES]
COLORS = [c for _, _, c in STRIPES]

# 2.  Sidebar controls  ------------------------------------------
st.sidebar.header("Stripe settings")
width_px = st.sidebar.slider("Stripe width (pixels)", 8, 40, 20)
height_px = st.sidebar.slider("Stripe height (pixels)", 80, 300, 120)

# Year subset selector
yr_min, yr_max = st.sidebar.select_slider(
    "Select year range",
    options=YEARS,
    value=(YEARS[0], YEARS[-1])
)

# 3.  Build the image  -------------------------------------------
# Subset colours for chosen period
idx0 = YEARS.index(yr_min)
idx1 = YEARS.index(yr_max) + 1
sub_cols = COLORS[idx0:idx1]
n_stripes = len(sub_cols)

img_w = width_px * n_stripes
img_h = height_px
img   = Image.new("RGB", (img_w, img_h), "white")
draw  = ImageDraw.Draw(img)

for i, hex_color in enumerate(sub_cols):
    x0 = i * width_px
    draw.rectangle([x0, 0, x0 + width_px, img_h], fill=hex_color)

# 4.  Display  ----------------------------------------------------
st.title("Personal Climate-Stripes")
st.caption("Source: NASA GISTEMP v4  (baseline 1951-1980)")

st.image(img, use_column_width=True)

# 5.  Download button  -------------------------------------------
st.download_button(
    label="Download PNG",
    data=img.tobytes(),
    file_name=f"stripes_{yr_min}_{yr_max}.png",
    mime="image/png"
)
