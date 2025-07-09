import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from io import StringIO
from datetime import datetime

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="📱 PhonePe Pulse Dashboard",
    page_icon="📊",
    layout="wide"
)

# Enhanced Custom CSS for better styling with more vibrant colors
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    .critical-insight {
        background: linear-gradient(135deg, #ff4757 0%, #ff3742 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #ff1744;
        box-shadow: 0 8px 25px rgba(255,71,87,0.3);
        animation: pulse 2s infinite;
    }
    
    .high-insight {
        background: linear-gradient(135deg, #ff9f43 0%, #ff6348 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #ff6348;
        box-shadow: 0 8px 25px rgba(255,159,67,0.3);
    }
    
    .medium-insight {
        background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #feca57;
        box-shadow: 0 8px 25px rgba(254,202,87,0.3);
    }
    
    .positive-insight {
        background: linear-gradient(135deg, #5f27cd 0%, #00d2d3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #5f27cd;
        box-shadow: 0 8px 25px rgba(95,39,205,0.3);
    }
    
    .growth-insight {
        background: linear-gradient(135deg, #00d2d3 0%, #1dd1a1 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #1dd1a1;
        box-shadow: 0 8px 25px rgba(29,209,161,0.3);
    }
    
    .strategic-inference {
        background: linear-gradient(135deg, #2c2c54 0%, #40407a 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border: 3px solid #706fd3;
        box-shadow: 0 10px 30px rgba(112,111,211,0.4);
    }
    
    .market-inference {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #6c5ce7;
        box-shadow: 0 8px 25px rgba(108,92,231,0.3);
    }
    
    .business-inference {
        background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #fd79a8;
        box-shadow: 0 8px 25px rgba(253,121,168,0.3);
    }
    
    .trend-analysis {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #00b894;
        box-shadow: 0 8px 25px rgba(0,184,148,0.3);
    }
    
    .warning-insight {
        background: linear-gradient(135deg, #e17055 0%, #d63031 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border-left: 6px solid #e17055;
        box-shadow: 0 8px 25px rgba(225,112,85,0.3);
    }
    
    .performance-metric {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        color: white;
        border: 2px solid #74b9ff;
        box-shadow: 0 8px 25px rgba(116,185,255,0.3);
    }
    
    .insight-header {
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
    }
    
    .insight-body {
        font-size: 1.1em;
        line-height: 1.6;
        margin-bottom: 0.5rem;
    }
    
    .insight-details {
        font-size: 0.95em;
        opacity: 0.9;
        font-style: italic;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .stTabs > div[data-baseweb="tab-list"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    .stTabs > div[data-baseweb="tab-list"] > div {
        color: white;
        font-weight: bold;
    }
    
    .chart-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .section-header {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 1.4em;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .metric-card:hover {
    transform: scale(1.02);
    transition: all 0.2s ease-in-out;
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
}

</style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown("""
<div class="main-header">
    <h1>📊 PhonePe Pulse Dashboard - Advanced Analytics</h1>
    <p>Comprehensive analysis of transactions, user engagement, and insurance trends across Indian states and quarters</p>
    <p><strong>Real-time insights • Strategic intelligence • Market analysis</strong></p>
</div>
""", unsafe_allow_html=True)

# ---------------- Load and Clean Data ----------------
@st.cache_data
def load_data():
    data = {
        "aggregated_insurance": pd.read_csv("aggregated_insurance.csv").sort_values(by=["state", "year", "quarter"]),
        "map_transaction": pd.read_csv("map_transaction.csv").sort_values(by=["state", "year", "quarter"]),
        "top_insurance": pd.read_csv("top_insurance.csv").sort_values(by=["state", "year", "quarter"]),
        "aggregated_transaction_data": pd.read_csv("aggregated_transaction.csv").sort_values(by=["state", "year", "quarter"]),
        "map_user": pd.read_csv("map_user.csv").sort_values(by=["state", "year", "quarter"]),
        "top_transaction": pd.read_csv("top_transaction.csv").sort_values(by=["state", "year", "quarter"]),
        "aggregated_transaction": pd.read_csv("aggregated_transaction.csv").sort_values(by=["state", "year", "quarter"]),
        "aggregated_user_data": pd.read_csv("aggregated_user_data.csv").sort_values(by=["state", "year", "quarter"]),
        "map_insurance": pd.read_csv("map_insurance.csv").sort_values(by=["state", "year", "quarter"]),
        "top_user": pd.read_csv("top_user.csv").sort_values(by=["state", "year", "quarter"])
    }

    for name, df in data.items():
        df.columns = df.columns.str.strip()
        if 'state' in df.columns:
            df['state'] = df.state.str.strip()
        if 'type' in df.columns:
            df['type'] = df['type'].str.strip()
        data[name] = df

    return data

data = load_data()

# ---------------- Enhanced Helper Functions for Deep Insights ----------------
def generate_comprehensive_transaction_insights(df):
    insights = []
    
    if df.empty:
        insights.append(("warning", "⚠️ DATA UNAVAILABLE", "No transaction data available for the selected filters.", "Consider expanding your filter criteria or checking data availability."))
        return insights
    
    # Basic metrics
    total_amount = df['amount'].sum()
    total_count = df['count'].sum()
    avg_transaction = total_amount / total_count if total_count > 0 else 0
    
    # Volume Analysis
    if total_amount > 100000000:  # 10 Crore
        insights.append(("critical", "💰 HIGH VOLUME MARKET", 
                        f"Exceptional transaction volume of ₹{total_amount:,.0f} across {total_count:,} transactions",
                        f"Average transaction value: ₹{avg_transaction:,.0f} | This indicates a mature, high-value market segment"))
    elif total_amount > 10000000:  # 1 Crore
        insights.append(("high", "💵 SIGNIFICANT VOLUME", 
                        f"Strong transaction volume of ₹{total_amount:,.0f} with {total_count:,} transactions",
                        f"Average transaction value: ₹{avg_transaction:,.0f} | Growing market with good potential"))
    else:
        insights.append(("medium", "📊 MODERATE VOLUME", 
                        f"Transaction volume of ₹{total_amount:,.0f} across {total_count:,} transactions",
                        f"Average transaction value: ₹{avg_transaction:,.0f} | Emerging market opportunity"))
    
    # State-wise performance analysis
    if 'state' in df.columns:
        state_stats = df.groupby('state').agg({
            'amount': ['sum', 'mean', 'std'],
            'count': ['sum', 'mean', 'std']
        }).reset_index()
        
        state_stats.columns = ['state', 'total_amount', 'avg_amount', 'amount_std', 'total_count', 'avg_count', 'count_std']
        
        # Top performing state
        top_state = state_stats.loc[state_stats['total_amount'].idxmax()]
        state_dominance = (top_state['total_amount'] / state_stats['total_amount'].sum()) * 100
        
        if state_dominance > 40:
            insights.append(("critical", "🏆 MARKET DOMINANCE", 
                           f"{top_state['state']} dominates with {state_dominance:.1f}% market share (₹{top_state['total_amount']:,.0f})",
                           f"High concentration risk - consider diversification strategies"))
        else:
            insights.append(("positive", "🌟 BALANCED LEADERSHIP", 
                           f"{top_state['state']} leads with {state_dominance:.1f}% market share (₹{top_state['total_amount']:,.0f})",
                           f"Healthy market distribution across states"))
        
        # Market concentration analysis
        top_3_states = state_stats.nlargest(3, 'total_amount')
        top_3_share = (top_3_states['total_amount'].sum() / state_stats['total_amount'].sum()) * 100
        
        insights.append(("performance", "📈 MARKET CONCENTRATION", 
                        f"Top 3 states control {top_3_share:.1f}% of total volume",
                        f"States: {', '.join(top_3_states['state'].tolist())} | Concentration level: {'High' if top_3_share > 70 else 'Moderate'}"))
    
    # Transaction type analysis
    if 'type' in df.columns:
        type_stats = df.groupby('type').agg({
            'amount': ['sum', 'mean', 'count'],
            'count': ['sum', 'mean']
        }).reset_index()
        
        type_stats.columns = ['type', 'total_amount', 'avg_amount', 'txn_frequency', 'total_count', 'avg_count']
        
        # Most valuable transaction type
        top_type = type_stats.loc[type_stats['total_amount'].idxmax()]
        type_dominance = (top_type['total_amount'] / type_stats['total_amount'].sum()) * 100
        
        insights.append(("high", "💳 PRIMARY TRANSACTION TYPE", 
                        f"{top_type['type']} generates {type_dominance:.1f}% of total revenue (₹{top_type['total_amount']:,.0f})",
                        f"Average value: ₹{top_type['avg_amount']:,.0f} | Transaction frequency: {top_type['total_count']:,}"))
        
        # Transaction diversity analysis
        type_count = len(type_stats)
        if type_count > 5:
            insights.append(("positive", "🔄 DIVERSE PORTFOLIO", 
                           f"Strong diversification with {type_count} active transaction types",
                           f"Reduces dependency risk and provides multiple revenue streams"))
        else:
            insights.append(("medium", "🎯 FOCUSED APPROACH", 
                           f"Concentrated portfolio with {type_count} transaction types",
                           f"Opportunity for expansion into new transaction categories"))
    
    # Temporal analysis
    if 'quarter' in df.columns and 'year' in df.columns:
        temporal_stats = df.groupby(['year', 'quarter']).agg({
            'amount': 'sum',
            'count': 'sum'
        }).reset_index()
        
        if len(temporal_stats) > 1:
            # Growth calculation
            temporal_stats = temporal_stats.sort_values(['year', 'quarter'])
            temporal_stats['amount_growth'] = temporal_stats['amount'].pct_change()
            temporal_stats['count_growth'] = temporal_stats['count'].pct_change()
            
            avg_amount_growth = temporal_stats['amount_growth'].mean()
            avg_count_growth = temporal_stats['count_growth'].mean()
            
            if avg_amount_growth > 0.1:  # 10% growth
                insights.append(("growth", "📈 STRONG GROWTH TRAJECTORY", 
                               f"Exceptional growth rate of {avg_amount_growth:.1%} in transaction value",
                               f"Volume growth: {avg_count_growth:.1%} | Indicates expanding market adoption"))
            elif avg_amount_growth > 0:
                insights.append(("positive", "📊 STEADY GROWTH", 
                               f"Consistent growth rate of {avg_amount_growth:.1%} in transaction value",
                               f"Volume growth: {avg_count_growth:.1%} | Stable market expansion"))
            else:
                insights.append(("warning", "📉 DECLINING TREND", 
                               f"Market contraction of {abs(avg_amount_growth):.1%} in transaction value",
                               f"Volume change: {avg_count_growth:.1%} | Requires immediate strategic intervention"))
    
    # Performance benchmarking
    if 'state' in df.columns and len(df['state'].unique()) > 1:
        state_performance = df.groupby('state').agg({
            'amount': ['sum', 'mean'],
            'count': ['sum', 'mean']
        }).reset_index()
        
        state_performance.columns = ['state', 'total_amount', 'avg_amount', 'total_count', 'avg_count']
        state_performance['efficiency'] = state_performance['total_amount'] / state_performance['total_count']
        
        most_efficient = state_performance.loc[state_performance['efficiency'].idxmax()]
        least_efficient = state_performance.loc[state_performance['efficiency'].idxmin()]
        
        efficiency_gap = ((most_efficient['efficiency'] - least_efficient['efficiency']) / least_efficient['efficiency']) * 100
        
        insights.append(("performance", "⚡ EFFICIENCY ANALYSIS", 
                        f"Efficiency gap of {efficiency_gap:.1f}% between best ({most_efficient['state']}) and worst ({least_efficient['state']}) performing states",
                        f"Best: ₹{most_efficient['efficiency']:,.0f} per transaction | Worst: ₹{least_efficient['efficiency']:,.0f} per transaction"))
    
    return insights

def generate_deep_geographic_insights(df):
    insights = []
    
    if df.empty:
        insights.append(("warning", "⚠️ NO GEOGRAPHIC DATA", "No district-level data available for analysis.", "Check data availability for selected regions."))
        return insights
    
    # District-wise analysis
    if 'district' in df.columns:
        district_stats = df.groupby('district').agg({
            'amount': ['sum', 'mean', 'count'],
            'count': ['sum', 'mean']
        }).reset_index()
        
        district_stats.columns = ['district', 'total_amount', 'avg_amount', 'frequency', 'total_count', 'avg_count']
        
        # Geographic concentration
        total_districts = len(district_stats)
        total_volume = district_stats['total_amount'].sum()
        
        # Top performing district
        top_district = district_stats.loc[district_stats['total_amount'].idxmax()]
        district_dominance = (top_district['total_amount'] / total_volume) * 100
        
        insights.append(("critical", "🏙️ TOP PERFORMING DISTRICT", 
                        f"{top_district['district']} leads with {district_dominance:.1f}% of total volume (₹{top_district['total_amount']:,.0f})",
                        f"Total transactions: {top_district['total_count']:,} | Average value: ₹{top_district['avg_amount']:,.0f}"))
        
        # Geographic distribution analysis
        if total_districts > 10:
            top_10_share = (district_stats.nlargest(10, 'total_amount')['total_amount'].sum() / total_volume) * 100
            insights.append(("high", "🗺️ GEOGRAPHIC DISTRIBUTION", 
                           f"Top 10 districts control {top_10_share:.1f}% of volume across {total_districts} districts",
                           f"Distribution level: {'Concentrated' if top_10_share > 80 else 'Balanced'} | Urban vs Rural penetration analysis needed"))
        
        # Performance variance analysis
        district_variance = district_stats['total_amount'].std() / district_stats['total_amount'].mean()
        if district_variance > 1:
            insights.append(("medium", "📊 HIGH PERFORMANCE VARIANCE", 
                           f"Significant performance variation across districts (CV: {district_variance:.2f})",
                           f"Indicates uneven market development - opportunity for targeted growth strategies"))
        
        # Emerging districts identification
        if len(district_stats) > 5:
            median_performance = district_stats['total_amount'].median()
            emerging_districts = district_stats[
                (district_stats['total_amount'] > median_performance * 0.5) & 
                (district_stats['total_amount'] < median_performance * 1.5)
            ]
            
            if len(emerging_districts) > 0:
                insights.append(("positive", "🌱 EMERGING MARKETS", 
                               f"Identified {len(emerging_districts)} emerging districts with growth potential",
                               f"These districts show moderate performance and could benefit from focused investment"))
    
    return insights

def generate_advanced_user_insights(df):
    insights = []
    
    if df.empty:
        insights.append(("warning", "⚠️ NO USER DATA", "No user behavior data available for analysis.", "User engagement metrics unavailable."))
        return insights
    
    # Brand analysis
    if 'brand' in df.columns:
        brand_stats = df.groupby('brand').agg({
            'count': ['sum', 'mean']
        }).reset_index()
        
        brand_stats.columns = ['brand', 'total_users', 'avg_users']
        total_users = brand_stats['total_users'].sum()
        
        # Market leader analysis
        top_brand = brand_stats.loc[brand_stats['total_users'].idxmax()]
        brand_dominance = (top_brand['total_users'] / total_users) * 100
        
        if brand_dominance > 40:
            insights.append(("critical", "📱 BRAND DOMINANCE", 
                           f"{top_brand['brand']} dominates with {brand_dominance:.1f}% market share ({top_brand['total_users']:,} users)",
                           f"High dependency on single brand - consider diversification strategies"))
        else:
            insights.append(("positive", "🏷️ BRAND DIVERSITY", 
                           f"{top_brand['brand']} leads with {brand_dominance:.1f}% market share ({top_brand['total_users']:,} users)",
                           f"Healthy brand distribution reduces platform dependency risks"))
        
        # Brand portfolio analysis
        brand_count = len(brand_stats)
        if brand_count > 15:
            insights.append(("high", "🌐 EXTENSIVE BRAND COVERAGE", 
                           f"Supporting {brand_count} different device brands",
                           f"Comprehensive device compatibility ensures broad user accessibility"))
        
        # Top brands concentration
        top_3_brands = brand_stats.nlargest(3, 'total_users')
        top_3_share = (top_3_brands['total_users'].sum() / total_users) * 100
        
        insights.append(("performance", "📈 TOP BRANDS ANALYSIS", 
                        f"Top 3 brands capture {top_3_share:.1f}% of user base",
                        f"Brands: {', '.join(top_3_brands['brand'].tolist())} | Focus area for optimization"))
    
    return insights

def generate_strategic_inference(transaction_df, geographic_df, user_df):
    inferences = []
    
    # Market maturity analysis
    if not transaction_df.empty:
        total_states = len(transaction_df['state'].unique()) if 'state' in transaction_df.columns else 0
        total_volume = transaction_df['amount'].sum()
        
        if total_states > 20 and total_volume > 1000000000:  # 100 Crore
            inferences.append(("strategic", "🌍 MARKET MATURITY", 
                             f"Mature market presence across {total_states} states with ₹{total_volume:,.0f} volume",
                             f"Focus on optimization, efficiency improvements, and premium services"))
        elif total_states > 10:
            inferences.append(("market", "🚀 GROWTH PHASE", 
                             f"Expanding market across {total_states} states with strong growth indicators",
                             f"Opportunity for aggressive expansion and market share capture"))
        else:
            inferences.append(("business", "🎯 EMERGING MARKET", 
                             f"Early-stage market with presence in {total_states} states",
                             f"Focus on user acquisition and market penetration strategies"))
    
    # Competitive positioning
    if not transaction_df.empty and 'type' in transaction_df.columns:
        type_diversity = len(transaction_df['type'].unique())
        type_stats = transaction_df.groupby('type')['amount'].sum()
        type_concentration = (type_stats.max() / type_stats.sum()) * 100
        
        if type_diversity > 6 and type_concentration < 40:
            inferences.append(("strategic", "💼 DIVERSIFIED PORTFOLIO", 
                             f"Strong diversification with {type_diversity} transaction types, low concentration risk ({type_concentration:.1f}%)",
                             f"Resilient business model with multiple revenue streams"))
        elif type_concentration > 60:
            inferences.append(("business", "⚠️ CONCENTRATION RISK", 
                             f"High dependency on single transaction type ({type_concentration:.1f}% concentration)",
                             f"Strategic priority: Diversify transaction portfolio to reduce risk"))
    
    # User engagement strategy
    if not user_df.empty and 'brand' in user_df.columns:
        brand_stats = user_df.groupby('brand')['count'].sum()
        brand_concentration = (brand_stats.max() / brand_stats.sum()) * 100
        
        if brand_concentration < 30:
            inferences.append(("trend", "📱 DEVICE AGNOSTIC STRATEGY", 
                             f"Balanced device distribution ({brand_concentration:.1f}% top brand) indicates successful cross-platform adoption",
                             f"Continue platform-agnostic development for broader reach"))
        else:
            inferences.append(("market", "🎯 FOCUSED DEVICE STRATEGY", 
                             f"Strong concentration in top device brand ({brand_concentration:.1f}%) suggests targeted optimization opportunity",
                             f"Consider deeper integration with dominant platforms while expanding others"))
    
    # Geographic expansion insights
    if not geographic_df.empty and 'district' in geographic_df.columns:
        district_count = len(geographic_df['district'].unique())
        district_stats = geographic_df.groupby('district')['amount'].sum()
        geographic_concentration = (district_stats.max() / district_stats.sum()) * 100
        
        if district_count > 50 and geographic_concentration < 15:
            inferences.append(("strategic", "🗺️ BALANCED GEOGRAPHIC PRESENCE", 
                             f"Excellent geographic distribution across {district_count} districts with balanced penetration",
                             f"Model for sustainable growth - maintain balanced expansion strategy"))
        elif geographic_concentration > 30:
            inferences.append(("business", "🏙️ URBAN CONCENTRATION", 
                             f"High concentration in top district ({geographic_concentration:.1f}%) indicates urban-centric growth",
                             f"Strategic opportunity: Rural market penetration and tier-2/3 city expansion"))
    
    # Growth trajectory inference
    if not transaction_df.empty and 'year' in transaction_df.columns and 'quarter' in transaction_df.columns:
        temporal_data = transaction_df.groupby(['year', 'quarter'])['amount'].sum().reset_index()
        if len(temporal_data) > 2:
            temporal_data = temporal_data.sort_values(['year', 'quarter'])
            growth_rate = temporal_data['amount'].pct_change().mean()
            
            if growth_rate > 0.2:  # 20% growth
                inferences.append(("trend", "🚀 EXPONENTIAL GROWTH", 
                                 f"Exceptional growth trajectory with {growth_rate:.1%} average quarterly growth",
                                 f"Scale infrastructure and operations to support continued expansion"))
            elif growth_rate > 0.05:  # 5% growth
                inferences.append(("trend", "📈 STEADY EXPANSION", 
                                 f"Consistent growth pattern with {growth_rate:.1%} quarterly growth",
                                 f"Sustainable growth model - focus on efficiency and user experience"))
            else:
                inferences.append(("trend", "📊 MARKET STABILIZATION", 
                                 f"Growth rate of {growth_rate:.1%} indicates market maturation",
                                 f"Focus on retention, premium services, and operational efficiency"))
    
    return inferences
CATEGORY_CLASS_MAP = {
    "critical": "critical-insight",
    "high": "high-insight",
    "medium": "medium-insight",
    "positive": "positive-insight",
    "growth": "growth-insight",
    "strategic": "strategic-inference",
    "market": "market-inference",
    "business": "business-inference",
    "trend": "trend-analysis",
    "warning": "warning-insight",
    "performance": "performance-metric"
}

# ✅ 3. Renderer function for Insights & Inferences
def render_insights(insights):
    for category, header, body, details in insights:
        css_class = CATEGORY_CLASS_MAP.get(category, "positive-insight")
        st.markdown(f"""
        <div class="{css_class}">
            <div class="insight-header">{header}</div>
            <div class="insight-body">{body}</div>
            <div class="insight-details">{details}</div>
        </div>
        """, unsafe_allow_html=True)
# ---------------- Sidebar with Enhanced Filters ----------------
with st.sidebar:
    st.markdown("## 🔍 Advanced Filter Dashboard")
    
    # State selection with search
    states = sorted(data["aggregated_transaction"]["state"].unique())
    selected_states = st.multiselect(
        "🏛️ Select States", 
        states, 
        default=["Karnataka"],
        help="Choose one or more states to analyze"
    )
    
    # Year range with better styling
    years = sorted(data["aggregated_transaction"]["year"].unique())
    selected_year_range = st.select_slider(
        "📅 Select Year Range", 
        options=years, 
        value=(years[0], years[-1]),
        help="Select the time period for analysis"
    )
    
    # Quarter selection
    quarters = [1, 2, 3, 4]
    selected_quarters = st.multiselect(
        "📊 Select Quarters", 
        quarters, 
        default=quarters,
        help="Choose which quarters to include"
    )
    
    # Transaction type filter
    if 'type' in data["aggregated_transaction"].columns:
        txn_types = sorted(data["aggregated_transaction"]["type"].unique())
        selected_txn_types = st.multiselect(
            "💳 Transaction Types",
            txn_types,
            default=txn_types,
            help="Filter by transaction type"
        )
    else:
        selected_txn_types = []

# ---------------- Filter Function ----------------
def filter_df(df, states, year_range, quarters, txn_types=None):
    filtered = df[
        (df["state"].isin(states)) &
        (df["year"].between(year_range[0], year_range[1])) &
        (df["quarter"].isin(quarters))
    ]
    if txn_types and 'type' in df.columns:
        filtered = filtered[filtered["type"].isin(txn_types)]
    return filtered

# ---------------- Key Metrics Dashboard ----------------
if selected_states:
    st.markdown("## 📈 Key Metrics")
    
    # Calculate key metrics
    df_agg_txn = filter_df(data["aggregated_transaction"], selected_states, selected_year_range, selected_quarters, selected_txn_types)
    
    if not df_agg_txn.empty:

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_amount = df_agg_txn["amount"].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="insight-header">💰 Total Transaction Amount</div>
                <div class="insight-body">₹{total_amount:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            total_count = df_agg_txn["count"].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="insight-header">📊 Total Transactions</div>
                <div class="insight-body">{total_count:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            avg_amount = df_agg_txn["amount"].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="insight-header">📈 Average Transaction</div>
                <div class="insight-body">₹{avg_amount:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            unique_states = len(selected_states)
            st.markdown(f"""
            <div class="metric-card">
                <div class="insight-header">🏛️ States Analyzed</div>
                <div class="insight-body">{unique_states}</div>
            </div>
            """, unsafe_allow_html=True)



# ---------------- Enhanced Dashboard Tabs ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📦 Transaction Analysis", "🗺️ Geographic Analysis", "⭐ Top Performers", "🔍 Deep Insights"])

# ---------------- Tab 1: Enhanced Transaction Analysis ----------------
with tab1:
    df_agg_txn = filter_df(data["aggregated_transaction"], selected_states, selected_year_range, selected_quarters, selected_txn_types)
    df_agg_user = filter_df(data["aggregated_user_data"], selected_states, selected_year_range, selected_quarters)
    
    if not df_agg_txn.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💳 Transaction Amount by Type")
            grouped = df_agg_txn.groupby(["state", "type"]).agg({"amount": "sum"}).reset_index()
            fig1 = px.bar(grouped, x="type", y="amount", color="state", 
                         barmode="group", title="Transaction Amount by Type",
                         color_discrete_sequence=px.colors.qualitative.Set3)
            fig1.update_layout(xaxis_title="Transaction Type", yaxis_title="Amount (₹)")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Transaction Count by Type")
            grouped_count = df_agg_txn.groupby(["state", "type"]).agg({"count": "sum"}).reset_index()
            fig2 = px.bar(grouped_count, x="type", y="count", color="state", 
                        barmode="group", title="Transaction Count by Type",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
            fig2.update_layout(xaxis_title="Transaction Type", yaxis_title="Number of Transactions")
            st.plotly_chart(fig2, use_container_width=True)

        # Time series analysis
        st.markdown("### 📈 Transaction Trends Over Time")
        time_series = df_agg_txn.groupby(["year", "quarter"]).agg({"amount": "sum", "count": "sum"}).reset_index()
        time_series["period"] = time_series["year"].astype(str) + "-Q" + time_series["quarter"].astype(str)
        
        fig3 = make_subplots(specs=[[{"secondary_y": True}]])
        fig3.add_trace(
            go.Scatter(x=time_series["period"], y=time_series["amount"], 
                    mode='lines+markers', name="Amount (₹)", line=dict(color='blue')),
            secondary_y=False,
        )
        fig3.add_trace(
            go.Scatter(x=time_series["period"], y=time_series["count"], 
                    mode='lines+markers', name="Count", line=dict(color='red')),
            secondary_y=True,
        )

        fig3.update_layout(title="Transaction Trends Over Time", xaxis_title="Time Period")
        fig3.update_yaxes(title_text="Amount (₹)", secondary_y=False)
        fig3.update_yaxes(title_text="Number of Transactions", secondary_y=True)
        st.plotly_chart(fig3, use_container_width=True)

        # State-wise comparison
        st.markdown("### 🏛️ State-wise Performance")
        state_comparison = df_agg_txn.groupby("state").agg({"amount": "sum", "count": "sum"}).reset_index()
        state_comparison["avg_txn_amount"] = state_comparison["amount"] / state_comparison["count"]
        
        fig4 = px.scatter(state_comparison, x="count", y="amount", size="avg_txn_amount",
                         hover_name="state", title="State Performance Analysis",
                         labels={"count": "Number of Transactions", "amount": "Total Amount (₹)"})
        st.plotly_chart(fig4, use_container_width=True)
    
    # User Device Analysis
    st.markdown("### 📱 User Device Analysis")
    
    if not df_agg_user.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            grouped_user = df_agg_user.groupby("brand").agg({"count": "sum"}).reset_index()
            fig5 = px.pie(grouped_user, names="brand", values="count", 
                         title="Device Brand Distribution",
                         color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig5, use_container_width=True)
        
        with col2:
            # Brand performance over time
            brand_time = df_agg_user.groupby(["year", "brand"]).agg({"count": "sum"}).reset_index()
            fig6 = px.line(brand_time, x="year", y="count", color="brand",
                          title="Brand Usage Trends Over Time")
            st.plotly_chart(fig6, use_container_width=True)

    # Transaction Analysis Insights
    st.markdown("## 💡 Transaction Analysis Insights")
    transaction_insights = generate_comprehensive_transaction_insights(df_agg_txn)
    user_insights = generate_advanced_user_insights(df_agg_user)
    
    render_insights(transaction_insights)

    render_insights(user_insights)


# ---------------- Tab 2: Enhanced Geographic Analysis ----------------
with tab2:
    df_map_txn = filter_df(data["map_transaction"], selected_states, selected_year_range, selected_quarters)
    df_map_ins = filter_df(data["map_insurance"], selected_states, selected_year_range, selected_quarters)
    
    if not df_map_txn.empty:
        st.markdown("### 🗺️ District-wise Analysis")
        
        # Top performing districts
        district_summary = df_map_txn.groupby("district").agg({"amount": "sum", "count": "sum"}).reset_index()
        district_summary = district_summary.sort_values("amount", ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏆 Top 10 Districts by Amount")
            top_districts = district_summary.head(10)
            fig7 = px.bar(top_districts, x="amount", y="district", orientation='h',
                         title="Top 10 Districts by Transaction Amount",
                         color="amount", color_continuous_scale="viridis")
            st.plotly_chart(fig7, use_container_width=True)
        
        with col2:
            st.markdown("#### 🏆 Top 10 Districts by Count")
            top_districts_count = district_summary.sort_values("count", ascending=False).head(10)
            fig8 = px.bar(top_districts_count, x="count", y="district", orientation='h',
                         title="Top 10 Districts by Transaction Count",
                         color="count", color_continuous_scale="plasma")
            st.plotly_chart(fig8, use_container_width=True)
        
        # District distribution
        st.markdown("#### 📊 District Performance Distribution")
        fig9 = px.scatter(district_summary, x="count", y="amount", 
                         hover_name="district", title="District Performance Analysis",
                         labels={"count": "Number of Transactions", "amount": "Total Amount (₹)"},
                         color="amount", size="count")
        st.plotly_chart(fig9, use_container_width=True)
    
    # Insurance geographic analysis
    if not df_map_ins.empty:
        st.markdown("### 🛡️ Insurance Distribution")
        insurance_district = df_map_ins.groupby("district").agg({"amount": "sum", "count": "sum"}).reset_index()
        
        fig10 = px.treemap(insurance_district, path=["district"], values="amount",
                          title="Insurance Distribution by District")
        st.plotly_chart(fig10, use_container_width=True)

    # Geographic Analysis Insights
    st.markdown("## 💡 Geographic Analysis Insights")
    geographic_insights = generate_deep_geographic_insights(df_map_txn)
    render_insights(geographic_insights)

# ---------------- Tab 3: Enhanced Top Performers ----------------
with tab3:
    st.markdown("### 🏆 Top Performers Analysis")
    
    # Top transactions
    df_top_txn = filter_df(data["top_transaction"], selected_states, selected_year_range, selected_quarters)
    
    if not df_top_txn.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Top Transaction by Amount")
            top_amount = df_top_txn.nlargest(10, "amount")
            fig11 = px.bar(top_amount, x="amount", y="district", orientation='h',
              title="Top 10 Districts by Transaction Amount",
              color="amount", color_continuous_scale="viridis")
            st.plotly_chart(fig11, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Top Transaction by Count")
            top_count = df_top_txn.nlargest(10, "count")
            fig12 = px.bar(top_count, x="count", y="district", orientation='h',
              title="Top 10 Districts by Transaction Count",
              color="count", color_continuous_scale="plasma")
            st.plotly_chart(fig12, use_container_width=True)
    
    # Performance comparison
    if not df_top_txn.empty:
        st.markdown("#### 📈 Performance Comparison")
        fig13 = px.scatter(df_top_txn, x="count", y="amount", 
                  hover_name="district", color="state",
                  title="District Performance Analysis",
                  labels={"count": "Number of Transactions", "amount": "Total Amount (₹)"})
        st.plotly_chart(fig13, use_container_width=True)

    # Top Performers Insights
    st.markdown("## 💡 Top Performers Insights")
    top_insights = generate_deep_geographic_insights(df_top_txn)
    render_insights(top_insights)
    

# ---------------- Tab 4: Deep Insights ----------------
with tab4:
    st.markdown("### 🔍 Deep Insights & Analytics")
    
    # Correlation analysis
    if not df_agg_txn.empty:
        st.markdown("#### 📊 Correlation Analysis")
        
        # State-wise correlation between amount and count
        state_stats = df_agg_txn.groupby("state").agg({
            "amount": ["sum", "mean"],
            "count": ["sum", "mean"]
        }).reset_index()
        
        state_stats.columns = ["state", "total_amount", "avg_amount", "total_count", "avg_count"]
        
        fig14 = px.scatter(state_stats, x="total_count", y="total_amount", 
                          size="avg_amount", hover_name="state",
                          title="State-wise Transaction Volume vs Amount",
                          labels={"total_count": "Total Transactions", "total_amount": "Total Amount (₹)"})
        st.plotly_chart(fig14, use_container_width=True)
        
        # Quarter-wise performance
        st.markdown("#### 📈 Quarterly Performance Analysis")
        quarter_stats = df_agg_txn.groupby("quarter").agg({
            "amount": ["sum", "mean"],
            "count": ["sum", "mean"]
        }).reset_index()
        
        quarter_stats.columns = ["quarter", "total_amount", "avg_amount", "total_count", "avg_count"]
        
        fig15 = px.bar(quarter_stats, x="quarter", y=["total_amount", "total_count"],
                      title="Quarterly Performance Comparison",
                      barmode="group")
        st.plotly_chart(fig15, use_container_width=True)
        
        # Type-wise analysis
        st.markdown("#### 💳 Transaction Type Analysis")
        type_stats = df_agg_txn.groupby("type").agg({
            "amount": ["sum", "mean"],
            "count": ["sum", "mean"]
        }).reset_index()
        
        type_stats.columns = ["type", "total_amount", "avg_amount", "total_count", "avg_count"]
        
        fig16 = px.sunburst(df_agg_txn, path=["type", "state"], values="amount",
                           title="Transaction Type Distribution by State")
        st.plotly_chart(fig16, use_container_width=True)

    # Strategic Inference Section
    st.markdown("## 🎯 Strategic Inference")
    
    # Generate comprehensive inference
    df_map_txn = filter_df(data["map_transaction"], selected_states, selected_year_range, selected_quarters)
    df_agg_user = filter_df(data["aggregated_user_data"], selected_states, selected_year_range, selected_quarters)
    
    inferences = generate_strategic_inference(df_agg_txn, df_map_txn, df_agg_user)
    render_insights(inferences)
    

# ---------------- Data Export Feature ----------------
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Data")
if st.sidebar.button("Export Filtered Data"):
    with st.spinner("Preparing data for export..."):
        # Create a summary report
        summary_data = {
            "Total States": len(selected_states),
            "Year Range": f"{selected_year_range[0]} - {selected_year_range[1]}",
            "Quarters": selected_quarters,
            "Total Amount": f"₹{df_agg_txn['amount'].sum():,.0f}" if not df_agg_txn.empty else "N/A",
            "Total Transactions": f"{df_agg_txn['count'].sum():,}" if not df_agg_txn.empty else "N/A"
        }
        
        st.sidebar.json(summary_data)
        st.sidebar.success("Summary generated!")
        if not df_agg_txn.empty:
            export_payload = {
                "summary": summary_data,
                "filtered_transactions": df_agg_txn.to_dict(orient="records"),
            }
            
            # Convert to JSON string
            json_str = json.dumps(export_payload, indent=2)
            
            # Create a download button
            st.sidebar.download_button(
                label="⬇️ Download JSON",
                data=json_str,
                file_name="filtered_data.json",
                mime="application/json"
            )
            csv_buffer = StringIO()
            df_agg_txn.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            st.sidebar.download_button(
                label="⬇️ Download CSV",
                data=csv_data,
                file_name="filtered_transactions.csv",
                mime="text/csv"
            )

# Footer
st.markdown("---")
st.markdown("📊 PhonePe Pulse Dashboard - Enhanced with Advanced Analytics & Strategic Insights")
st.markdown("Built with Streamlit and Plotly for comprehensive data visualization and business intelligence")