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
   (1880, -0.19, '#136ebc'), (1881, -0.107, '#2e81ba'), (1882, -0.139, '#237aba'), (1883, -0.201, '#0f6abd'), (1884, -0.318, '#214cb6'), (1885, -0.363, '#2942a2'), (1886, -0.331, '#2548b0'), (1887, -0.381, '#293f9a'), (1888, -0.187, '#136ebc'), (1889, -0.118, '#297dba'), (1890, -0.37, '#2942a2'), (1891, -0.232, '#0a62be'), (1892, -0.294, '#1952bc'), (1893, -0.331, '#2548b0'), (1894, -0.321, '#214cb6'), (1895, -0.24, '#0a60be'), (1896, -0.135, '#237aba'), (1897, -0.125, '#267bba'), (1898, -0.292, '#1952bc'), (1899, -0.193, '#116cbc'), (1900, -0.092, '#3083ba'), (1901, -0.162, '#1b74bb'), (1902, -0.3, '#1c50ba'), (1903, -0.386, '#293f9a'), (1904, -0.491, '#242e6c'), (1905, -0.271, '#1059be'), (1906, -0.238, '#0a62be'), (1907, -0.41, '#293b8f'), (1908, -0.438, '#283681'), (1909, -0.501, '#232d69'), (1910, -0.452, '#27347d'), (1911, -0.449, '#27347d'), (1912, -0.378, '#29409e'), (1913, -0.362, '#2843a5'), (1914, -0.174, '#1670bc'), (1915, -0.151, '#1e76bb'), (1916, -0.381, '#293f9a'), (1917, -0.485, '#252f6f'), (1918, -0.322, '#234ab3'), (1919, -0.291, '#1952bc'), (1920, -0.286, '#1655bd'), (1921, -0.197, '#116cbc'), (1922, -0.292, '#1952bc'), (1923, -0.27, '#1059be'), (1924, -0.269, '#1059be'), (1925, -0.221, '#0b66bd'), (1926, -0.098, '#3083ba'), (1927, -0.215, '#0b66bd'), (1928, -0.193, '#116cbc'), (1929, -0.357, '#2843a5'), (1930, -0.15, '#1e76bb'), (1931, -0.074, '#3888ba'), (1932, -0.152, '#1e76bb'), (1933, -0.284, '#1655bd'), (1934, -0.119, '#297dba'), (1935, -0.196, '#116cbc'), (1936, -0.138, '#237aba'), (1937, -0.012, '#4b94ba'), (1938, 0.001, '#5197ba'), (1939, -0.021, '#4892ba'), (1940, 0.136, '#81afc0'), (1941, 0.196, '#9bbbc6'), (1942, 0.069, '#68a4bc'), (1943, 0.091, '#71a8bd'), (1944, 0.204, '#9ebcc7'), (1945, 0.093, '#71a8bd'), (1946, -0.066, '#3b89ba'), (1947, -0.014, '#4b94ba'), (1948, -0.099, '#3083ba'), (1949, -0.107, '#2e81ba'), (1950, -0.175, '#1670bc'), (1951, -0.061, '#3b89ba'), (1952, 0.022, '#569abb'), (1953, 0.098, '#75aabe'), (1954, -0.128, '#267bba'), (1955, -0.135, '#237aba'), (1956, -0.187, '#136ebc'), (1957, 0.052, '#62a0bb'), (1958, 0.058, '#65a2bc'), (1959, 0.025, '#599cbb'), (1960, -0.03, '#4690ba'), (1961, 0.058, '#65a2bc'), (1962, 0.031, '#599cbb'), (1963, 0.058, '#65a2bc'), (1964, -0.199, '#0f6abd'), (1965, -0.112, '#2b7fba'), (1966, -0.06, '#3b89ba'), (1967, -0.019, '#4892ba'), (1968, -0.08, '#3686ba'), (1969, 0.049, '#62a0bb'), (1970, 0.025, '#599cbb'), (1971, -0.085, '#3384ba'), (1972, 0.003, '#5197ba'), (1973, 0.157, '#8bb4c2'), (1974, -0.066, '#3b89ba'), (1975, -0.022, '#4892ba'), (1976, -0.109, '#2b7fba'), (1977, 0.177, '#91b7c3'), (1978, 0.062, '#65a2bc'), (1979, 0.158, '#8bb4c2'), (1980, 0.255, '#b0c5cd'), (1981, 0.324, '#c7d2d7'), (1982, 0.127, '#7eaebf'), (1983, 0.313, '#c4d0d5'), (1984, 0.15, '#88b2c1'), (1985, 0.113, '#78abbe'), (1986, 0.179, '#94b8c4'), (1987, 0.313, '#c4d0d5'), (1988, 0.387, '#dee0e1'), (1989, 0.271, '#b6c9cf'), (1990, 0.444, '#f1ecec'), (1991, 0.411, '#e6e5e6'), (1992, 0.215, '#a1bec8'), (1993, 0.224, '#a4bfc9'), (1994, 0.315, '#c4d0d5'), (1995, 0.443, '#f1ecec'), (1996, 0.344, '#d0d7da'), (1997, 0.461, '#f0eae9'), (1998, 0.609, '#e0c0b5'), (1999, 0.375, '#d8dcde'), (2000, 0.397, '#e1e1e3'), (2001, 0.535, '#e7d5cf'), (2002, 0.633, '#deb9ad'), (2003, 0.623, '#dfbbb0'), (2004, 0.538, '#e7d5cf'), (2005, 0.683, '#daab9b'), (2006, 0.64, '#ddb6aa'), (2007, 0.673, '#daad9e'), (2008, 0.543, '#e6d2cd'), (2009, 0.665, '#dbafa1'), (2010, 0.731, '#d69d8a'), (2011, 0.612, '#e0c0b5'), (2012, 0.644, '#ddb6aa'), (2013, 0.685, '#daab9b'), (2014, 0.748, '#d49984'), (2015, 0.893, '#c87255'), (2016, 1.025, '#ba482e'), (2017, 0.921, '#c5684b'), (2018, 0.855, '#cb7b60'), (2019, 0.982, '#bf573a'), (2020, 1.011, '#bc4d32'), (2021, 0.856, '#cb7b60'), (2022, 0.902, '#c76d50'), (2023, 1.177, '#9f1b26'), (2024, 1.289, '#7e0e29')
]

YEARS  = [y for y, _, _ in STRIPES]
COLORS = [c for _, _, c in STRIPES]

# 2.  Sidebar controls  ------------------------------------------
st.sidebar.header("Stripe settings")

# Fixed overall canvas size for strict comparability
TOTAL_WIDTH_PX  = st.sidebar.number_input(
    "Overall bar width (px)", min_value=600, max_value=2000, value=1200, step=100
)
TOTAL_HEIGHT_PX = st.sidebar.number_input(
    "Bar height (px)", min_value=80,  max_value=400,  value=150,  step=10
)

st.sidebar.markdown("### Year range")
year_min, year_max = YEARS[0], YEARS[-1]

start_year = st.sidebar.number_input(
    "Start year", min_value=year_min, max_value=year_max,
    value=year_min, step=1, format="%d"
)
end_year = st.sidebar.number_input(
    "End year", min_value=year_min, max_value=year_max,
    value=year_max, step=1, format="%d"
)

if start_year > end_year:
    st.sidebar.error("Start year must be ≤ end year.")
    st.stop()

# 3.  Build the fixed-size image  ---------------------------------
idx0 = YEARS.index(int(start_year))
idx1 = YEARS.index(int(end_year)) + 1
sub_cols = COLORS[idx0:idx1]
n_years  = len(sub_cols)

# Stripe width is calculated so all stripes fill the canvas exactly
stripe_px = max(1, TOTAL_WIDTH_PX // n_years)          # integer px
img_w     = stripe_px * n_years                        # may be a few px < TOTAL_WIDTH_PX
img_h     = TOTAL_HEIGHT_PX

img  = Image.new("RGB", (img_w, img_h), "white")
draw = ImageDraw.Draw(img)

for i, color in enumerate(sub_cols):
    x0 = i * stripe_px
    draw.rectangle([x0, 0, x0 + stripe_px, img_h], fill=color)

# 4.  Display & download  -----------------------------------------
st.title("Personal Climate-Stripes")
st.caption("Source: NASA GISTEMP v4 (baseline 1951-1980)")

st.image(img, use_container_width=True)        # fills Streamlit column

st.download_button(
    label="Download PNG",
    data=img.tobytes(),
    file_name=f"stripes_{start_year}_{end_year}.png",
    mime="image/png"
)

