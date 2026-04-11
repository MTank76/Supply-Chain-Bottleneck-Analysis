import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="ChainPulse | SCBA", 
    layout="wide", 
    page_icon="📦",
    initial_sidebar_state="expanded"
)

# 2. MODERN DARK UI CUSTOM CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px; 
        border-radius: 15px;
    }
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DATA ENGINE
@st.cache_data
def load_data():
    try:
        # UPDATED FILE ID
        file_id = '16pTRmYdTNdWErHN4a0F9N_8mwva94bLE'
        url = f'https://drive.google.com/uc?export=download&id={file_id}'
        
        # Use latin1 encoding to handle special characters in the international data
        df = pd.read_csv(url, encoding='latin1')
        
        # Re-calculating the bottleneck logic in case it's the raw version
        if 'Is_Bottleneck' not in df.columns:
            df['Is_Bottleneck'] = df['Days for shipping (real)'] > df['Days for shipment (scheduled)']
        
        # Date and Metric Processing
        df['Order Date'] = pd.to_datetime(df['order date (DateOrders)'])
        df['Shipment_Delay'] = df['Days for shipping (real)'] - df['Days for shipment (scheduled)']
        df['Bottleneck_Status'] = df['Is_Bottleneck'].map({True: 'Bottleneck', False: 'On-Time'})
        
        return df
    except Exception as e:
        st.error(f"Cloud Data Feed Error: {e}")
        return None
        
df = load_data()

if df is not None:
    # 4. SIDEBAR INTELLIGENCE FILTERS
    with st.sidebar:
        st.title("⚡Quick Pulse")
        st.markdown("---")

        with st.expander("📅 Temporal Range", expanded=True):
            st.write("**Select Window**")
            date_range = st.date_input(
                "Date Selector",
                value=(df['Order Date'].min(), df['Order Date'].max()),
                label_visibility="collapsed"
            )

        with st.expander("🌐 Geographic Reach", expanded=True):
            st.write("**Market Hubs**")
            market_filter = st.multiselect(
                "Markets", 
                options=df['Market'].unique(), 
                default=df['Market'].unique()[:3],
                label_visibility="collapsed"
            )

        with st.expander("🚚 Logistics Flow", expanded=True):
            st.write("**Shipping Modes**")
            shipping_filter = st.multiselect(
                "Modes", 
                options=df['Shipping Mode'].unique(), 
                default=df['Shipping Mode'].unique(),
                label_visibility="collapsed"
            )

        st.markdown("---")
        if st.button("♻️ Reset Intelligence Hub", use_container_width=True):
            st.rerun()

    # Apply Filtering
    filtered_df = df[
        (df['Order Date'].dt.date >= date_range[0]) & 
        (df['Order Date'].dt.date <= date_range[1]) &
        (df['Market'].isin(market_filter)) &
        (df['Shipping Mode'].isin(shipping_filter))
    ]

    # 5. HEADER & KPI METRICS
    st.title("📦 Supply Chain Intelligence Hub")
    
    m1, m2, m3, m4 = st.columns(4)
    total_load = len(filtered_df)
    incidents = filtered_df['Is_Bottleneck'].sum()
    
    m1.metric("Total Load", f"{total_load:,}")
    m2.metric("Incident Count", f"{incidents:,}", delta_color="inverse")
    m3.metric("Failure Rate", f"{(incidents/total_load*100 if total_load > 0 else 0):.1f}%")
    m4.metric("Avg Latency", f"{filtered_df['Shipment_Delay'].mean():.1f} Days")

    st.markdown("---")

    # 6. TABBED ANALYTICS DASHBOARD
    tab_efficiency, tab_trends = st.tabs(["📊 Logistics Efficiency", "🎯 Trends & Correlation"])

    with tab_efficiency:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Mode Efficiency")
            fig_mode = px.histogram(filtered_df, x="Shipping Mode", color="Bottleneck_Status", 
                                    barmode="group", color_discrete_map={'Bottleneck': '#f43f5e', 'On-Time': '#38bdf8'},
                                    template="plotly_dark")
            st.plotly_chart(fig_mode, use_container_width=True)
        with col2:
            st.subheader("🌎 Regional Risk Heatmap")
            reg_df = filtered_df.groupby('Order Region')['Is_Bottleneck'].mean().reset_index()
            fig_reg = px.bar(reg_df.sort_values('Is_Bottleneck'), y='Order Region', x='Is_Bottleneck',
                             color='Is_Bottleneck', color_continuous_scale='Reds', template="plotly_dark")
            st.plotly_chart(fig_reg, use_container_width=True)

    with tab_trends:
        st.subheader("📈 Daily Bottleneck Trend")
        trend_df = filtered_df.groupby(filtered_df['Order Date'].dt.date)['Is_Bottleneck'].sum().reset_index()
        fig_trend = px.area(trend_df, x='Order Date', y='Is_Bottleneck', color_discrete_sequence=['#fb923c'], template="plotly_dark")
        fig_trend.update_xaxes(rangeslider_visible=True)
        st.plotly_chart(fig_trend, use_container_width=True)

        st.subheader("🎯 Value-Delay Correlation")
        # Sampled for high performance
        fig_scatter = px.scatter(filtered_df.sample(min(1500, len(filtered_df))), 
                                 x="Product Price", y="Shipment_Delay", color="Bottleneck_Status", 
                                 size="Order Item Quantity", template="plotly_dark")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # 7. RAW DATA ACCESS
    with st.expander("🔍 View Filtered Raw Data"):
        st.dataframe(filtered_df.head(100), use_container_width=True)
