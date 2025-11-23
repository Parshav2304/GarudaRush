#!/usr/bin/env python3
"""
GarudaRush Prototype - Streamlit Dashboard
ML-Enhanced Agent-Based Intrusion Detection System
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json

# Page configuration
st.set_page_config(
    page_title="GarudaRush - DDoS Detection Prototype",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #3b82f6 0%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #06b6d4 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .footer {
        text-align: center;
        color: #94a3b8;
        padding: 2rem 0;
        margin-top: 2rem;
        border-top: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False
if 'total_packets' not in st.session_state:
    st.session_state.total_packets = 0
if 'attacks_detected' not in st.session_state:
    st.session_state.attacks_detected = 0
if 'normal_traffic' not in st.session_state:
    st.session_state.normal_traffic = 0
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'traffic_data' not in st.session_state:
    st.session_state.traffic_data = []
if 'attack_distribution' not in st.session_state:
    st.session_state.attack_distribution = {
        'SYN Flood': 0,
        'UDP Flood': 0,
        'HTTP Flood': 0,
        'Slowloris': 0,
        'DNS Amplification': 0
    }
if 'db_records' not in st.session_state:
    st.session_state.db_records = []

# Simulate database storage
def store_in_database(record_type, data):
    """Simulate storing data in database"""
    record = {
        'id': len(st.session_state.db_records) + 1,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'type': record_type,
        'data': data
    }
    st.session_state.db_records.append(record)
    return record

# Header
st.markdown('<h1 class="main-header">🛡️ GarudaRush</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">ML-Enhanced Agent-Based DDoS Detection System</p>', unsafe_allow_html=True)

# Main tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "📈 Analysis"])

# ==================== DASHBOARD TAB ====================
with tab1:
    # Monitoring Control
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ Start Monitoring" if not st.session_state.monitoring else "⏸️ Stop Monitoring"):
            st.session_state.monitoring = not st.session_state.monitoring
            if st.session_state.monitoring:
                st.success("✅ Monitoring started!")
            else:
                st.info("⏸️ Monitoring paused.")
    
    st.divider()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📦 Total Packets", f"{st.session_state.total_packets:,}")
    with col2:
        st.metric("🚨 Attacks Detected", st.session_state.attacks_detected)
    with col3:
        st.metric("✅ Normal Traffic", f"{st.session_state.normal_traffic:,}")
    with col4:
        st.metric("🎯 Accuracy", "96.5%")
    
    st.divider()
    
    # Real-Time Traffic
    st.subheader("📡 Real-Time Traffic Monitor")
    
    if st.session_state.monitoring:
        current_time = datetime.now().strftime("%H:%M:%S")
        normal = np.random.randint(50, 150)
        suspicious = np.random.randint(0, 30)
        attack = np.random.randint(0, 20)
        
        st.session_state.traffic_data.append({
            'time': current_time,
            'normal': normal,
            'suspicious': suspicious,
            'attack': attack
        })
        
        if len(st.session_state.traffic_data) > 30:
            st.session_state.traffic_data.pop(0)
        
        st.session_state.total_packets += (normal + suspicious + attack)
        st.session_state.normal_traffic += normal
        
        store_in_database('traffic', {
            'normal': normal,
            'suspicious': suspicious,
            'attack': attack
        })
        
        if np.random.random() > 0.85:
            st.session_state.attacks_detected += 1
            attack_type = np.random.choice(list(st.session_state.attack_distribution.keys()))
            st.session_state.attack_distribution[attack_type] += 1
            
            alert = {
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'type': attack_type,
                'severity': np.random.choice(['Critical', 'High', 'Medium']),
                'source': f"{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}",
                'destination': f"192.168.1.{np.random.randint(1,255)}",
                'confidence': round(np.random.uniform(85, 99), 1)
            }
            st.session_state.alerts.insert(0, alert)
            store_in_database('alert', alert)
            st.session_state.alerts = st.session_state.alerts[:15]
    
    if st.session_state.traffic_data:
        df = pd.DataFrame(st.session_state.traffic_data)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['time'], y=df['normal'], mode='lines+markers', name='Normal', line=dict(color='#10b981', width=3), fill='tozeroy'))
        fig.add_trace(go.Scatter(x=df['time'], y=df['suspicious'], mode='lines+markers', name='Suspicious', line=dict(color='#f59e0b', width=3), fill='tozeroy'))
        fig.add_trace(go.Scatter(x=df['time'], y=df['attack'], mode='lines+markers', name='Attack', line=dict(color='#ef4444', width=3), fill='tozeroy'))
        fig.update_layout(xaxis_title="Time", yaxis_title="Packets/Second", height=400, plot_bgcolor='rgba(15, 23, 42, 0.5)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Click 'Start Monitoring' to begin...")
    
    st.divider()
    
    # Alerts
    st.subheader("🚨 Recent Security Alerts")
    
    if st.session_state.alerts:
        for alert in st.session_state.alerts[:5]:
            severity_color = {'Critical': '#dc2626', 'High': '#f97316', 'Medium': '#eab308'}.get(alert.get('severity', 'Medium'), '#3b82f6')
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"### 🔴 {alert.get('type', 'Unknown')}")
                st.caption(f"🕐 {alert.get('time', 'N/A')}")
            with col2:
                st.markdown(f"**Source:** {alert.get('source', 'Unknown')}")
                st.markdown(f"**Destination:** {alert.get('destination', '192.168.1.1')}")
                st.caption(f"Confidence: {alert.get('confidence', 0)}%")
            with col3:
                st.markdown(f"<div style='background-color: {severity_color}; padding: 8px 16px; border-radius: 20px; text-align: center; font-weight: 600;'>{alert.get('severity', 'Medium')}</div>", unsafe_allow_html=True)
            st.divider()
    else:
        st.success("✅ No threats detected!")
    
    st.divider()
    
    # Database Status
    st.subheader("💾 Database Storage")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(st.session_state.db_records))
    with col2:
        st.metric("Alert Records", len([r for r in st.session_state.db_records if r['type'] == 'alert']))
    with col3:
        st.metric("Traffic Records", len([r for r in st.session_state.db_records if r['type'] == 'traffic']))
    
    if st.session_state.db_records:
        with st.expander("📋 View Recent Database Entries (Last 10)"):
            for record in st.session_state.db_records[-10:][::-1]:
                st.json({'ID': record['id'], 'Timestamp': record['timestamp'], 'Type': record['type'], 'Data': record['data']})
    
    st.divider()
    
    # Settings
    st.subheader("⚙️ Settings")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Reset Statistics"):
            st.session_state.total_packets = 0
            st.session_state.attacks_detected = 0
            st.session_state.normal_traffic = 0
            st.session_state.alerts = []
            st.session_state.traffic_data = []
            st.session_state.attack_distribution = {k: 0 for k in st.session_state.attack_distribution}
            st.success("✅ Reset!")
            st.rerun()
    with col2:
        if st.session_state.db_records and st.button("💾 Export Database"):
            export_data = {
                'export_time': datetime.now().isoformat(),
                'total_records': len(st.session_state.db_records),
                'records': st.session_state.db_records
            }
            st.download_button("⬇️ Download JSON", json.dumps(export_data, indent=2), f"garudarush_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "application/json")

# ==================== ANALYSIS TAB ====================
with tab2:
    st.subheader("📈 Analytics & Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Attack Distribution")
        if sum(st.session_state.attack_distribution.values()) > 0:
            fig = go.Figure(data=[go.Pie(labels=list(st.session_state.attack_distribution.keys()), values=list(st.session_state.attack_distribution.values()), hole=0.4, marker=dict(colors=['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']))])
            fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 No attacks yet")
    
    with col2:
        st.markdown("### 🏆 Model Performance")
        metrics = pd.DataFrame({'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'], 'Value': [96.5, 95.8, 97.2, 96.5]})
        fig = go.Figure(data=[go.Bar(x=metrics['Metric'], y=metrics['Value'], marker_color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'], text=metrics['Value'].apply(lambda x: f"{x}%"), textposition='outside')])
        fig.update_layout(height=400, yaxis_range=[0, 105], plot_bgcolor='rgba(15, 23, 42, 0.5)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.markdown("### 📊 Detection Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Detections", st.session_state.attacks_detected)
    with col2:
        rate = (st.session_state.attacks_detected / st.session_state.total_packets * 100) if st.session_state.total_packets > 0 else 0
        st.metric("Attack Rate", f"{rate:.2f}%")
    with col3:
        st.metric("False Positive", "3.2%")
    with col4:
        st.metric("Detection Time", "3.2s")

# Footer
st.markdown("""
<div class="footer">
    <p><strong>GarudaRush</strong> - ML-Enhanced DDoS Detection</p>
    <p>By <strong>Sourav Rinwa, Parshav Shah, Arvind Sharma</strong> • Guide: <strong>Mr. Utsav Dagar</strong></p>
</div>
""", unsafe_allow_html=True)

if st.session_state.monitoring:
    time.sleep(2)
    st.rerun()
