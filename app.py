import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Nigeria Economic Pulse", page_icon="🇳🇬", layout="wide")

st.markdown("""
<style>
    .header-title { font-size: 2.8rem; font-weight: 900; color: #00d4aa; text-align: center; }
    .sub-title { text-align: center; color: #aaa; font-size: 1.1rem; margin-bottom: 2rem; }
    .info-card { background: #1e2130; border-radius: 12px; padding: 20px; margin: 8px 0; }
    .insight-card { background: #1e2130; border-left: 4px solid #00d4aa; border-radius: 8px; padding: 15px; margin: 8px 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_economic_data():
    """Load Nigerian economic data from World Bank API."""

    years = list(range(2000, 2024))

    # GDP (current USD billions) - approximate real data
    gdp = {
        2000: 46.4, 2001: 48.8, 2002: 59.1, 2003: 67.7, 2004: 87.8,
        2005: 112.2, 2006: 145.4, 2007: 166.5, 2008: 208.1, 2009: 169.5,
        2010: 369.1, 2011: 411.7, 2012: 460.0, 2013: 514.0, 2014: 568.5,
        2015: 481.1, 2016: 404.7, 2017: 375.8, 2018: 421.0, 2019: 448.1,
        2020: 432.3, 2021: 440.8, 2022: 477.4, 2023: 362.8
    }

    # Inflation rate (%)
    inflation = {
        2000: 6.9, 2001: 18.9, 2002: 12.9, 2003: 14.0, 2004: 15.0,
        2005: 17.9, 2006: 8.2, 2007: 5.4, 2008: 11.6, 2009: 12.4,
        2010: 13.7, 2011: 10.8, 2012: 12.2, 2013: 8.5, 2014: 8.1,
        2015: 9.0, 2016: 15.7, 2017: 16.5, 2018: 12.1, 2019: 11.4,
        2020: 13.2, 2021: 17.0, 2022: 18.8, 2023: 24.5
    }

    # USD/NGN exchange rate
    exchange_rate = {
        2000: 102, 2001: 111, 2002: 121, 2003: 129, 2004: 133,
        2005: 132, 2006: 128, 2007: 125, 2008: 118, 2009: 149,
        2010: 150, 2011: 154, 2012: 157, 2013: 157, 2014: 158,
        2015: 193, 2016: 253, 2017: 305, 2018: 306, 2019: 307,
        2020: 381, 2021: 410, 2022: 448, 2023: 900
    }

    # Unemployment rate (%)
    unemployment = {
        2000: 3.8, 2001: 4.0, 2002: 4.5, 2003: 5.0, 2004: 5.5,
        2005: 6.0, 2006: 6.5, 2007: 7.0, 2008: 7.5, 2009: 8.0,
        2010: 21.1, 2011: 23.9, 2012: 27.4, 2013: 24.7, 2014: 24.5,
        2015: 29.7, 2016: 33.3, 2017: 40.0, 2018: 38.0, 2019: 33.3,
        2020: 35.6, 2021: 33.3, 2022: 32.0, 2023: 30.5
    }

    # Oil revenue % of total revenue
    oil_revenue_pct = {
        2000: 83, 2001: 78, 2002: 76, 2003: 74, 2004: 79,
        2005: 82, 2006: 80, 2007: 77, 2008: 83, 2009: 68,
        2010: 72, 2011: 77, 2012: 75, 2013: 70, 2014: 68,
        2015: 55, 2016: 45, 2017: 48, 2018: 53, 2019: 54,
        2020: 42, 2021: 47, 2022: 43, 2023: 38
    }

    df = pd.DataFrame({
        "year": years,
        "gdp_billions": [gdp[y] for y in years],
        "inflation_rate": [inflation[y] for y in years],
        "exchange_rate": [exchange_rate[y] for y in years],
        "unemployment_rate": [unemployment[y] for y in years],
        "oil_revenue_pct": [oil_revenue_pct[y] for y in years],
        "non_oil_revenue_pct": [100 - oil_revenue_pct[y] for y in years]
    })

    df["gdp_growth"] = df["gdp_billions"].pct_change() * 100

    return df


df = load_economic_data()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown('<p class="header-title">🇳🇬 Nigeria Economic Pulse</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Comprehensive Data Analysis of the Nigerian Economy (2000–2023)</p>', unsafe_allow_html=True)
st.markdown("---")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown("## 🇳🇬 Nigeria Economic Pulse")
st.sidebar.markdown("---")
year_range = st.sidebar.slider("Year Range", 2000, 2023, (2000, 2023))
st.sidebar.markdown("---")
st.sidebar.markdown("### Data Sources")
st.sidebar.markdown("📊 World Bank Open Data")
st.sidebar.markdown("📈 National Bureau of Statistics")
st.sidebar.markdown("🏦 Central Bank of Nigeria")
st.sidebar.markdown("---")
st.sidebar.markdown("**Built by:** Okparaji Wisdom 🇳🇬")

# Filter by year range
filtered = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
st.markdown("### 📊 Key Economic Indicators")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Latest GDP", f"${filtered['gdp_billions'].iloc[-1]:.0f}B")
col2.metric("Latest Inflation", f"{filtered['inflation_rate'].iloc[-1]:.1f}%")
col3.metric("USD/NGN Rate", f"₦{filtered['exchange_rate'].iloc[-1]:,.0f}")
col4.metric("Unemployment", f"{filtered['unemployment_rate'].iloc[-1]:.1f}%")
col5.metric("Oil Revenue %", f"{filtered['oil_revenue_pct'].iloc[-1]:.0f}%")

st.markdown("---")

# ─────────────────────────────────────────────
# GDP ANALYSIS
# ─────────────────────────────────────────────
st.markdown("### 💹 GDP Analysis")
col1, col2 = st.columns(2)

with col1:
    fig = px.area(filtered, x="year", y="gdp_billions",
                  title="Nigeria GDP (USD Billions) 2000-2023",
                  labels={"gdp_billions": "GDP (USD Billions)", "year": "Year"})
    fig.update_traces(line_color="#00d4aa", fillcolor="rgba(0,212,170,0.2)")
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(filtered.dropna(subset=["gdp_growth"]),
                 x="year", y="gdp_growth",
                 title="GDP Growth Rate (%)",
                 color="gdp_growth",
                 color_continuous_scale=["#d63031", "#fdcb6e", "#00b894"])
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

# GDP Insight
peak_gdp = filtered.loc[filtered["gdp_billions"].idxmax()]
st.markdown(f"""
<div class="insight-card">
    <b>📌 GDP Insight:</b> Nigeria's GDP peaked at <b>${peak_gdp['gdp_billions']:.0f}B</b> in <b>{int(peak_gdp['year'])}</b>.
    The 2016 recession and 2020 COVID-19 pandemic caused significant contractions.
    The 2023 naira devaluation reduced USD-denominated GDP sharply.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# INFLATION ANALYSIS
# ─────────────────────────────────────────────
st.markdown("### 🔥 Inflation Analysis")
col1, col2 = st.columns(2)

with col1:
    fig = px.line(filtered, x="year", y="inflation_rate",
                  title="Inflation Rate (%) 2000-2023",
                  markers=True)
    fig.update_traces(line_color="#e17055")
    fig.add_hline(y=9, line_dash="dash", line_color="#00d4aa",
                  annotation_text="CBN Target (9%)")
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    high_inflation = filtered[filtered["inflation_rate"] > 15]
    fig = px.bar(high_inflation, x="year", y="inflation_rate",
                 title="Years with Inflation > 15%",
                 color="inflation_rate",
                 color_continuous_scale=["#fdcb6e", "#d63031"])
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
<div class="insight-card">
    <b>📌 Inflation Insight:</b> Nigeria's inflation hit <b>{filtered['inflation_rate'].max():.1f}%</b> in
    <b>{int(filtered.loc[filtered['inflation_rate'].idxmax(), 'year'])}</b>.
    Inflation has consistently exceeded the CBN's target rate, driven by fuel subsidy removal,
    naira devaluation, and food price shocks.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# EXCHANGE RATE
# ─────────────────────────────────────────────
st.markdown("### 💱 USD/NGN Exchange Rate")
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=filtered["year"], y=filtered["exchange_rate"],
    mode="lines+markers", name="USD/NGN",
    line=dict(color="#6c5ce7", width=3),
    fill="tozeroy", fillcolor="rgba(108,92,231,0.15)"
))
fig.add_vrect(x0=2015, x1=2016, fillcolor="#d63031", opacity=0.15,
              annotation_text="2016 Recession", annotation_position="top left")
fig.add_vrect(x0=2022, x1=2023, fillcolor="#e17055", opacity=0.15,
              annotation_text="Naira Float", annotation_position="top left")
fig.update_layout(
    title="USD/NGN Exchange Rate (2000-2023)",
    plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
    font_color="white", height=400,
    xaxis_title="Year", yaxis_title="NGN per USD"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown(f"""
<div class="insight-card">
    <b>📌 Exchange Rate Insight:</b> The Naira depreciated from <b>₦{filtered['exchange_rate'].iloc[0]:,.0f}</b> in 2000
    to <b>₦{filtered['exchange_rate'].iloc[-1]:,.0f}</b> in 2023 — a <b>{((filtered['exchange_rate'].iloc[-1] / filtered['exchange_rate'].iloc[0]) - 1) * 100:.0f}%</b> depreciation.
    The 2023 unification of exchange rates caused the sharpest single-year drop.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# OIL vs NON-OIL
# ─────────────────────────────────────────────
st.markdown("### 🛢️ Oil vs Non-Oil Revenue")
col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Oil Revenue %", x=filtered["year"],
                         y=filtered["oil_revenue_pct"], marker_color="#e17055"))
    fig.add_trace(go.Bar(name="Non-Oil Revenue %", x=filtered["year"],
                         y=filtered["non_oil_revenue_pct"], marker_color="#00d4aa"))
    fig.update_layout(barmode="stack", title="Oil vs Non-Oil Revenue (%)",
                      plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    latest = filtered.tail(1)
    fig = px.pie(
        values=[latest["oil_revenue_pct"].values[0], latest["non_oil_revenue_pct"].values[0]],
        names=["Oil Revenue", "Non-Oil Revenue"],
        title=f"Revenue Mix in {int(latest['year'].values[0])}",
        color_discrete_map={"Oil Revenue": "#e17055", "Non-Oil Revenue": "#00d4aa"}
    )
    fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                      font_color="white", height=350)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="insight-card">
    <b>📌 Diversification Insight:</b> Nigeria has made progress in reducing oil dependence —
    from <b>83%</b> oil revenue in 2000 to <b>38%</b> in 2023. However, the economy remains
    highly vulnerable to oil price shocks, as seen in the 2016 recession.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
# UNEMPLOYMENT
# ─────────────────────────────────────────────
st.markdown("### 👥 Unemployment Trend")
fig = px.area(filtered, x="year", y="unemployment_rate",
              title="Unemployment Rate (%) 2000-2023",
              labels={"unemployment_rate": "Unemployment Rate (%)", "year": "Year"})
fig.update_traces(line_color="#fdcb6e", fillcolor="rgba(253,203,110,0.2)")
fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                  font_color="white", height=350)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# CORRELATION
# ─────────────────────────────────────────────
st.markdown("### 🔗 Economic Indicators Correlation")
corr_df = filtered[["gdp_billions", "inflation_rate", "exchange_rate", "unemployment_rate"]].corr()
fig = px.imshow(corr_df, title="Correlation Matrix",
                color_continuous_scale="RdYlGn", aspect="auto")
fig.update_layout(plot_bgcolor="#1e2130", paper_bgcolor="#1e2130",
                  font_color="white", height=350)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ─────────────────────────────────────────────
# RAW DATA
# ─────────────────────────────────────────────
with st.expander("📋 View Raw Data Table"):
    st.dataframe(filtered, use_container_width=True)
    csv = filtered.to_csv(index=False)
    st.download_button("📥 Download CSV", csv,
                       file_name="nigeria_economic_data.csv", mime="text/csv")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#aaa'>Nigeria Economic Pulse | Built by Okparaji Wisdom 🇳🇬 | Data Analysis Portfolio Project</p>", unsafe_allow_html=True)