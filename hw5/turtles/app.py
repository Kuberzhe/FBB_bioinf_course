import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from collections import Counter

st.set_page_config(
    page_title="pi",
    page_icon="pi",
    layout="wide"
)


def count_overlapping(text, pattern):
    if not pattern:
        return 0
    cnt = 0
    start = 0
    while True:
        start = text.find(pattern, start)
        if start == -1:
            break
        cnt += 1
        start += 1  
    return cnt

def most_frequent_enclosing_substring(text, pat, k):
    if (len(pat) > k) or (k < 1):
        return None, 0
    counter = Counter()
    for i in range(len(text) - k + 1):
        subst = text[i:i + k]
        if pat in subst:
            counter[subst] += 1
    if counter:
        return counter.most_common(1)[0]
    return None,0


st.title("Миллион знаков пи")

df = pd.read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2026/2026-03-24/pi_digits.csv")
pi_str = "".join(df["digit"].astype(str).tolist())
col1,col2= st.columns(2)
query = col1.text_input("Число:", value="67")
query = "".join(ch for ch in query if ch.isdigit())
k = col2.text_input("Длина подстроки k:", value="67")
k = int(k)

kega = count_overlapping(pi_str, query)
freq_sub, freq_cnt = most_frequent_enclosing_substring(pi_str, query, k)

col1, col2= st.columns(2)
col1.metric("Сколько раз встречается число в первом миллионе знаков:", f"{kega:,}")
col2.metric(f"Самая частая подстрока длины {k}: {freq_sub if len(freq_sub) <= 10 else f'{freq_sub[:5]}...{freq_sub[-5:]}'} - встречается", f"{freq_cnt:,}")

window_size = st.slider("Длина окна для графиков", min_value=100, max_value=100000, value=67000, step=100)
window_size = int(window_size)  

pos = np.arange(0, len(pi_str), window_size)
densities = []


for start in pos:
    end = min(start + window_size, len(pi_str))
    densities.append(count_overlapping(pi_str[start:end], query))

df_density = pd.DataFrame({"Позиция в пи": pos, "Количество вхождений": densities})
fig_density = px.line(df_density, x="Позиция в пи", y="Количество вхождений",
                      title=f"Плотность вхождений {query}")

fig_dist = px.histogram(x=densities, nbins=min(20, max(densities)+1), title=f"Распределение числа вхождений {query} в окнах", labels={"x": "Число вхождений", "y": "Число окон"})
fig_dist.update_layout(bargap=0.1)
st.plotly_chart(fig_dist, use_container_width=True)

st.plotly_chart(fig_density, use_container_width=True)


