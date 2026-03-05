# dashboard.py
# pip install streamlit pandas plotly openpyxl

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# --- Config ---
st.set_page_config(layout="wide", page_title="Infrastructure Constraints Dashboard")
NAVY = "#0A1F44"
ORANGE = "#FF6B00"



# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_excel("clean_data.xlsx")
    df = df[df["Country"] != "All Economies"].dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("🔧 Filters")
years = sorted(df["Year"].unique(), reverse=True)
selected_year = st.sidebar.selectbox("Survey Year", years)

year_df = df[df["Year"] == selected_year]
countries = sorted(year_df["Country"].unique())
selected_countries = st.sidebar.multiselect("Countries", countries, default=countries[:10])

# --- Filter data ---
filtered = year_df[year_df["Country"].isin(selected_countries)]

# --- Header ---
st.markdown(f"# Infrastructure Constraints Dashboard")
st.markdown(f"**Survey Year: {selected_year}** · {len(selected_countries)} countries selected")
st.divider()

# --- Category Rows ---
categories = sorted(filtered["Category"].unique())
icons = {"Climate": "🌍", "Electricity": "⚡", "Internet": "🌐", "Transport": "🚛", "Water": "💧"}

for cat in categories:
    cat_data = filtered[filtered["Category"] == cat]
    if cat_data.empty:
        continue

    indicators = cat_data["Indicator"].unique().tolist()
    st.markdown(f"### {icons.get(cat, '📊')} {cat}")

    # --- KPI Cards ---
    kpi_cols = st.columns(min(len(indicators), 4))
    for i, ind in enumerate(indicators[:4]):
        vals = cat_data[cat_data["Indicator"] == ind]["Value"].dropna()
        avg = vals.mean() if len(vals) > 0 else None
        with kpi_cols[i]:
            st.metric(
                label=ind[:60],
                value=f"{avg:.1f}" if avg is not None else "N/A",
                help="Average across selected countries"
            )

    # --- 3-Column Layout ---
    col1, col2, col3 = st.columns(3)
    #col1,  col3 = st.columns(2)

    # 1) Ranked Bar Chart
    with col1:
        st.markdown("**Ranked Comparison**")
        sel_ind = st.selectbox("Indicator", indicators, key=f"bar_{cat}")
        bar_data = (cat_data[cat_data["Indicator"] == sel_ind]
                    .dropna(subset=["Value"])
                    .sort_values("Value"))
        fig = px.bar(bar_data, x="Value", y="Country", orientation="h",
                     text=bar_data["Value"].round(1))
        fig.update_traces(marker_color=NAVY, textposition="outside",textfont=dict(color="black") )
        fig.update_layout(
            height=max(len(bar_data) * 28, 250),
            margin=dict(l=10, r=40, t=10, b=10),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False,title_font=dict(color="black"),tickfont=dict(color="black")), 
            yaxis=dict(showgrid=False,title_font=dict(color="black"),tickfont=dict(color="black"))
        )
        st.plotly_chart(fig, use_container_width=True)

    # 2) Indicator Table
    with col2:
        st.markdown("**Indicator Values**")
        pivot = cat_data.pivot_table(index="Country", columns="Indicator", values="Value")
        pivot = pivot.reindex(columns=indicators)

        st.dataframe(pivot.style.format("{:.2f}", na_rep="—"), height=max(len(pivot) * 35, 250))

    # 3) Heatmap
    with col3:
        st.markdown("**Relative Performance**")
        pivot_heat = cat_data.pivot_table(index="Country", columns="Indicator", values="Value")
        # Min-max normalize per column
        normalized = pivot_heat.apply(lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else 0.5)
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=normalized.values,
            x=[ind[:25] for ind in normalized.columns],
            y=normalized.index.tolist(),
            colorscale=[[0, NAVY], [0.5, "white"], [1, ORANGE]],
            zmin=0, zmax=1,
            text=normalized.round(2).values,
            texttemplate="%{text:.2f}",
            textfont={"size": 10,},
            #textfont=dict(size=10, color="black"),
            showscale=False
        ))
        fig_heat.update_layout(
            height=max(len(normalized) * 28, 250),
            margin=dict(l=10, r=10, t=10, b=10),

            paper_bgcolor="white", plot_bgcolor="white",
            xaxis=dict(
            tickfont=dict(color="black"),    # x-axis tick labels
            title_font=dict(color="black")   # x-axis title 
        ),
        yaxis=dict(
            tickfont=dict(color="black"),    # y-axis tick labels
            title_font=dict(color="black")   # y-axis title 
        )
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    st.divider()
    
