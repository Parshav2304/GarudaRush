#!/usr/bin/env python3
"""
GarudaRush Prototype - Streamlit Dashboard
ML-Enhanced Agent-Based Intrusion Detection System
Simplified version for demonstration
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
    .alert-box {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ef4444;
        margin-bottom: 0.5rem;
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
if 'detection_threshold' not in st.session_state:
    st.session_state.detection_threshold = 0.85
if 'update_interval' not in st.session_state:
    st.session_state.update_interval = 2

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
st.markdown('<p class="sub-header">ML-Enhanced Agent-Based DDoS Detection System - Prototype</p>', unsafe_allow_html=True)

# Main tabs
tab1, tab2 = st.tabs(["📊 Dashboard", "📈 Analysis"])

# ==================== DASHBOARD TAB ====================
with tab1:
    # Monitoring Control
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶️ Start Monitoring" if not st.session_state.monitoring else "⏸️ Stop Monitoring", 
                     key="monitor_btn",
                     use_container_width=True):
            st.session_state.monitoring = not st.session_state.monitoring
            if st.session_state.monitoring:
                st.success("✅ Monitoring started! System is now detecting attacks...")
            else:
                st.info("⏸️ Monitoring paused.")
    
    st.divider()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📦 Total Packets",
            value=f"{st.session_state.total_packets:,}",
            delta=f"+{np.random.randint(50, 150)}" if st.session_state.monitoring else None
        )
    
    with col2:
        st.metric(
            label="🚨 Attacks Detected",
            value=st.session_state.attacks_detected,
            delta=f"+{np.random.randint(0, 2)}" if st.session_state.monitoring else None,
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            label="✅ Normal Traffic",
            value=f"{st.session_state.normal_traffic:,}",
            delta=f"+{np.random.randint(40, 140)}" if st.session_state.monitoring else None
        )
    
    with col4:
        accuracy = 96.5 if st.session_state.total_packets > 0 else 0
        st.metric(
            label="🎯 Accuracy",
            value=f"{accuracy}%"
        )
    
    st.divider()
    
    # Real-Time Traffic Visualization
    st.subheader("📡 Real-Time Traffic Monitor")
    
    # Generate traffic data when monitoring
    if st.session_state.monitoring:
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # Generate packet data
        normal = np.random.randint(50, 150)
        suspicious = np.random.randint(0, 30)
        attack = np.random.randint(0, 20)
        
        st.session_state.traffic_data.append({
            'time': current_time,
            'normal': normal,
            'suspicious': suspicious,
            'attack': attack
        })
        
        # Keep only last 30 points
        if len(st.session_state.traffic_data) > 30:
            st.session_state.traffic_data.pop(0)
        
        # Update counters
        st.session_state.total_packets += (normal + suspicious + attack)
        st.session_state.normal_traffic += normal
        
        # Store packet data in simulated database
        store_in_database('traffic', {
            'normal': normal,
            'suspicious': suspicious,
            'attack': attack
        })
        
        # Randomly generate attacks
        if np.random.random() > 0.85:
            st.session_state.attacks_detected += 1
            attack_type = np.random.choice(list(st.session_state.attack_distribution.keys()))
            st.session_state.attack_distribution[attack_type] += 1
            
            # Create alert
            alert = {
                'id': len(st.session_state.alerts) + 1,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'type': attack_type,
                'severity': np.random.choice(['Critical', 'High', 'Medium'], p=[0.2, 0.5, 0.3]),
                'source': f"{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}",
                'destination': f"192.168.1.{np.random.randint(1,255)}",
                'confidence': round(np.random.uniform(85, 99), 1)
            }
            st.session_state.alerts.insert(0, alert)
            
            # Store alert in database
            store_in_database('alert', alert)
            
            # Keep only last 15 alerts
            st.session_state.alerts = st.session_state.alerts[:15]
    
    # Display traffic chart
    if st.session_state.traffic_data:
        df = pd.DataFrame(st.session_state.traffic_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['time'], y=df['normal'],
            mode='lines+markers',
            name='Normal',
            line=dict(color='#10b981', width=3),
            fill='tozeroy',
            fillcolor='rgba(16, 185, 129, 0.2)'
        ))
        fig.add_trace(go.Scatter(
            x=df['time'], y=df['suspicious'],
            mode='lines+markers',
            name='Suspicious',
            line=dict(color='#f59e0b', width=3),
            fill='tozeroy',
            fillcolor='rgba(245, 158, 11, 0.2)'
        ))
        fig.add_trace(go.Scatter(
            x=df['time'], y=df['attack'],
            mode='lines+markers',
            name='Attack',
            line=dict(color='#ef4444', width=3),
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.2)'
        ))
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Packets per Second",
            height=400,
            hovermode='x unified',
            plot_bgcolor='rgba(15, 23, 42, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("👆 Click 'Start Monitoring' to see real-time traffic data...")
    
    st.divider()
    
    # Alert Messages Section
    st.subheader("🚨 Recent Security Alerts")
    
    if st.session_state.alerts:
        for alert in st.session_state.alerts[:5]:  # Show only 5 most recent
            severity_colors = {
                'Critical': '#dc2626',
                'High': '#f97316',
                'Medium': '#eab308'
            }
            severity_color = severity_colors.get(alert.get('severity', 'Medium'), '#3b82f6')
            
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"### 🔴 {alert.get('type', 'Unknown Attack')}")
                    st.caption(f"🕐 {alert.get('time', 'N/A')}")
                
                with col2:
                    st.markdown(f"**Source:** {alert.get('source', 'Unknown')}")
                    st.markdown(f"**Destination:** {alert.get('destination', '192.168.1.1')}")
                    st.caption(f"Confidence: {alert.get('confidence', 0)}%")
                
                with col3:
                    st.markdown(
                        f"<div style='background-color: {severity_color}; padding: 8px 16px; "
                        f"border-radius: 20px; text-align: center; font-weight: 600;'>"
                        f"{alert.get('severity', 'Medium')}</div>",
                        unsafe_allow_html=True
                    )
                
                st.divider()
    else:
        st.success("✅ No threats detected. Your network is secure!")
    
    st.divider()
    
    # Database Storage Information
    st.subheader("💾 Database Storage Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_records = len(st.session_state.db_records)
        st.metric("Total Records Stored", total_records)
    
    with col2:
        alert_records = len([r for r in st.session_state.db_records if r['type'] == 'alert'])
        st.metric("Alert Records", alert_records)
    
    with col3:
        traffic_records = len([r for r in st.session_state.db_records if r['type'] == 'traffic'])
        st.metric("Traffic Records", traffic_records)
    
    # Show recent database entries
    if st.session_state.db_records:
        with st.expander("📋 View Recent Database Entries (Last 10)"):
            recent_records = st.session_state.db_records[-10:][::-1]
            for record in recent_records:
                st.json({
                    'ID': record['id'],
                    'Timestamp': record['timestamp'],
                    'Type': record['type'],
                    'Data': record['data']
                })
    
    st.divider()
    
    # Settings Section (at bottom)
    st.subheader("⚙️ System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        new_threshold = st.slider(
            "🎯 Detection Threshold",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.detection_threshold,
            step=0.05,
            help="Lower threshold = More sensitive (more detections, possibly more false positives)"
        )
        if new_threshold != st.session_state.detection_threshold:
            st.session_state.detection_threshold = new_threshold
            st.success(f"✅ Threshold updated to {new_threshold}")
    
    with col2:
        new_interval = st.slider(
            "⏱️ Update Interval (seconds)",
            min_value=1,
            max_value=10,
            value=st.session_state.update_interval,
            step=1,
            help="How often the dashboard refreshes"
        )
        if new_interval != st.session_state.update_interval:
            st.session_state.update_interval = new_interval
            st.success(f"✅ Interval updated to {new_interval}s")
    
    # Action Buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset Statistics", use_container_width=True):
            st.session_state.total_packets = 0
            st.session_state.attacks_detected = 0
            st.session_state.normal_traffic = 0
            st.session_state.alerts = []
            st.session_state.traffic_data = []
            st.session_state.attack_distribution = {k: 0 for k in st.session_state.attack_distribution}
            st.success("✅ Statistics reset successfully!")
            st.rerun()
    
    with col2:
        if st.button("💾 Export Database", use_container_width=True):
            if st.session_state.db_records:
                export_data = {
                    'export_time': datetime.now().isoformat(),
                    'total_records': len(st.session_state.db_records),
                    'records': st.session_state.db_records
                }
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"garudarush_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ No data to export yet. Start monitoring first!")

# ==================== ANALYSIS TAB ====================
with tab2:
    st.subheader("📈 System Analytics & Performance")
    
    # Attack Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Attack Type Distribution")
        
        if sum(st.session_state.attack_distribution.values()) > 0:
            fig = go.Figure(data=[go.Pie(
                labels=list(st.session_state.attack_distribution.keys()),
                values=list(st.session_state.attack_distribution.values()),
                hole=0.4,
                marker=dict(colors=['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6']),
                textinfo='label+percent',
                textfont=dict(size=14)
            )])
            
            fig.update_layout(
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 No attack data available. Start monitoring to see distribution.")
    
    with col2:
        st.markdown("### 🏆 Model Performance Metrics")
        
        metrics_data = pd.DataFrame({
            'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
            'Value': [96.5, 95.8, 97.2, 96.5]
        })
        
        fig = go.Figure(data=[go.Bar(
            x=metrics_data['Metric'],
            y=metrics_data['Value'],
            marker_color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'],
            text=metrics_data['Value'].apply(lambda x: f"{x}%"),
            textposition='outside',
            textfont=dict(size=14, color='white')
        )])
        
        fig.update_layout(
            height=400,
            yaxis_range=[0, 105],
            yaxis_title="Percentage (%)",
            plot_bgcolor='rgba(15, 23, 42, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Detection Statistics
    st.markdown("### 📊 Detection Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Detections", st.session_state.attacks_detected)
    
    with col2:
        detection_rate = (st.session_state.attacks_detected / st.session_state.total_packets * 100) if st.session_state.total_packets > 0 else 0
        st.metric("Attack Rate", f"{detection_rate:.2f}%")
    
    with col3:
        st.metric("False Positive Rate", "3.2%")
    
    with col4:
        st.metric("Avg Detection Time", "3.2s")
    
    st.divider()
    
    # System Performance
    st.markdown("### 💻 System Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        performance_data = pd.DataFrame({
            'Component': ['CPU Usage', 'Memory Usage', 'Network I/O', 'Disk I/O'],
            'Usage': [23, 45, 67, 12]
        })
        
        fig = go.Figure(data=[go.Bar(
            y=performance_data['Component'],
            x=performance_data['Usage'],
            orientation='h',
            marker=dict(
                color=performance_data['Usage'],
                colorscale='RdYlGn_r',
                showscale=False
            ),
            text=performance_data['Usage'].apply(lambda x: f"{x}%"),
            textposition='outside'
        )])
        
        fig.update_layout(
            title="Resource Utilization",
            xaxis_title="Usage (%)",
            xaxis_range=[0, 100],
            height=300,
            plot_bgcolor='rgba(15, 23, 42, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Processing statistics
        st.markdown("#### ⚡ Processing Statistics")
        
        stats_df = pd.DataFrame({
            'Metric': ['Packets/Second', 'Throughput', 'Latency', 'Memory Footprint'],
            'Value': ['15,000', '10 Gbps', '< 5s', '1.2 GB']
        })
        
        st.dataframe(
            stats_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("#### 🔧 System Info")
        system_info = {
            'ML Model': 'Random Forest',
            'Database': 'MongoDB (Simulated)',
            'Python Version': '3.8+',
            'Model Accuracy': '96.5%'
        }
        
        for key, value in system_info.items():
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.write(f"**{key}:**")
            with col_b:
                st.write(value)
    
    st.divider()
    
    # Database Analytics
    st.markdown("### 💾 Database Analytics")
    
    if st.session_state.db_records:
        col1, col2 = st.columns(2)
        
        with col1:
            # Records over time
            df_records = pd.DataFrame(st.session_state.db_records)
            df_records['timestamp'] = pd.to_datetime(df_records['timestamp'])
            df_records['minute'] = df_records['timestamp'].dt.strftime('%H:%M')
            
            records_count = df_records.groupby('minute').size().reset_index(name='count')
            
            fig = go.Figure(data=[go.Scatter(
                x=records_count['minute'],
                y=records_count['count'],
                mode='lines+markers',
                line=dict(color='#3b82f6', width=3),
                fill='tozeroy',
                fillcolor='rgba(59, 130, 246, 0.3)'
            )])
            
            fig.update_layout(
                title="Database Records Over Time",
                xaxis_title="Time",
                yaxis_title="Records Count",
                height=300,
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Record types distribution
            type_counts = df_records['type'].value_counts()
            
            fig = go.Figure(data=[go.Bar(
                x=type_counts.index,
                y=type_counts.values,
                marker_color=['#10b981', '#ef4444'],
                text=type_counts.values,
                textposition='outside'
            )])
            
            fig.update_layout(
                title="Database Record Types",
                xaxis_title="Record Type",
                yaxis_title="Count",
                height=300,
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📊 No database records yet. Start monitoring to collect data.")

# Footer
st.markdown("""
<div class="footer">
    <p><strong>GarudaRush Prototype</strong> - ML-Enhanced Agent-Based DDoS Detection System</p>
    <p>Developed by <strong>Sourav Rinwa</strong>, <strong>Parshav Shah</strong>, and <strong>Arvind Sharma</strong></p>
    <p>Guided by <strong>Mr. Utsav Dagar</strong></p>
    <p style="margin-top: 1rem; font-size: 0.875rem; color: #64748b;">
        💾 All data is simulated and stored in session memory for prototype demonstration
    </p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh when monitoring is active
if st.session_state.monitoring:
    time.sleep(st.session_state.update_interval)
    st.rerun()
