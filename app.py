#!/usr/bin/env python3
"""
GarudaRush Prototype - WITH VISIBLE DATABASE
Enhanced version showing database operations clearly
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
    page_title="GarudaRush - DDoS Detection with Database",
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
    .db-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 2px solid #3b82f6;
        margin: 1rem 0;
    }
    .alert-box {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ef4444;
        margin-bottom: 0.5rem;
    }
    .record-box {
        background: rgba(30, 41, 59, 0.8);
        padding: 0.75rem;
        border-radius: 0.5rem;
        border-left: 3px solid #10b981;
        margin-bottom: 0.5rem;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE MANAGER ====================
class SimpleDatabase:
    """Simple database that shows every operation"""
    
    def __init__(self):
        if 'db_records' not in st.session_state:
            st.session_state.db_records = []
        if 'db_logs' not in st.session_state:
            st.session_state.db_logs = []
    
    def insert(self, record_type, data):
        """Insert record and log the operation"""
        record = {
            'id': f"REC-{len(st.session_state.db_records) + 1:05d}",
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            'type': record_type,
            'data': data
        }
        
        st.session_state.db_records.append(record)
        
        # Log the operation
        log_entry = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'operation': 'INSERT',
            'collection': record_type,
            'record_id': record['id'],
            'status': '✅ SUCCESS'
        }
        st.session_state.db_logs.append(log_entry)
        
        return record
    
    def get_stats(self):
        """Get database statistics"""
        total = len(st.session_state.db_records)
        alerts = len([r for r in st.session_state.db_records if r['type'] == 'alert'])
        traffic = len([r for r in st.session_state.db_records if r['type'] == 'traffic'])
        
        return {
            'total': total,
            'alerts': alerts,
            'traffic': traffic,
            'size_kb': total * 0.5  # Approximate size
        }
    
    def get_recent(self, limit=10):
        """Get recent records"""
        return st.session_state.db_records[-limit:][::-1]
    
    def get_logs(self, limit=20):
        """Get recent database operation logs"""
        return st.session_state.db_logs[-limit:][::-1]

# Initialize database
if 'db' not in st.session_state:
    st.session_state.db = SimpleDatabase()

db = st.session_state.db

# Initialize other session state
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

# Header
st.markdown('<h1 class="main-header">🛡️ GarudaRush</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">ML-Enhanced DDoS Detection with Real-Time Database Operations</p>', unsafe_allow_html=True)

# Database Status Bar (Always Visible)
st.markdown('<div class="db-box">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
stats = db.get_stats()

with col1:
    st.markdown("### 💾 Database")
    st.markdown("**Type:** Session Storage")
with col2:
    st.metric("Total Records", stats['total'])
with col3:
    st.metric("Alert Records", stats['alerts'])
with col4:
    st.metric("Traffic Records", stats['traffic'])

st.markdown('</div>', unsafe_allow_html=True)

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
                st.success("✅ Monitoring started! Database operations will be logged below...")
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
    
    # Real-Time Traffic with Database Operations
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
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
            
            if len(st.session_state.traffic_data) > 30:
                st.session_state.traffic_data.pop(0)
            
            # Update counters
            st.session_state.total_packets += (normal + suspicious + attack)
            st.session_state.normal_traffic += normal
            
            # 🔥 STORE IN DATABASE - VISIBLE OPERATION
            db_record = db.insert('traffic', {
                'normal_packets': normal,
                'suspicious_packets': suspicious,
                'attack_packets': attack,
                'total': normal + suspicious + attack
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
                    'severity': np.random.choice(['Critical', 'High', 'Medium']),
                    'source': f"{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}.{np.random.randint(1,255)}",
                    'destination': f"192.168.1.{np.random.randint(1,255)}",
                    'confidence': round(np.random.uniform(85, 99), 1)
                }
                st.session_state.alerts.insert(0, alert)
                
                # 🔥 STORE ALERT IN DATABASE - VISIBLE OPERATION
                db_alert = db.insert('alert', alert)
                
                st.session_state.alerts = st.session_state.alerts[:15]
        
        # Display traffic chart
        if st.session_state.traffic_data:
            df = pd.DataFrame(st.session_state.traffic_data)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['time'], y=df['normal'],
                mode='lines+markers', name='Normal',
                line=dict(color='#10b981', width=3),
                fill='tozeroy'
            ))
            fig.add_trace(go.Scatter(
                x=df['time'], y=df['suspicious'],
                mode='lines+markers', name='Suspicious',
                line=dict(color='#f59e0b', width=3),
                fill='tozeroy'
            ))
            fig.add_trace(go.Scatter(
                x=df['time'], y=df['attack'],
                mode='lines+markers', name='Attack',
                line=dict(color='#ef4444', width=3),
                fill='tozeroy'
            ))
            
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Packets/Second",
                height=350,
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👆 Click 'Start Monitoring' to begin...")
    
    with col_right:
        st.subheader("🔍 Live Database Operations")
        
        # Show real-time database logs
        logs = db.get_logs(limit=10)
        
        if logs:
            for log in logs:
                st.markdown(
                    f'<div class="record-box">'
                    f'<strong>{log["time"]}</strong> - {log["operation"]}<br>'
                    f'Collection: <code>{log["collection"]}</code><br>'
                    f'ID: <code>{log["record_id"]}</code> {log["status"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No database operations yet")
    
    st.divider()
    
    # Alert Messages Section
    st.subheader("🚨 Recent Security Alerts")
    
    if st.session_state.alerts:
        for alert in st.session_state.alerts[:5]:
            severity_colors = {
                'Critical': '#dc2626',
                'High': '#f97316',
                'Medium': '#eab308'
            }
            severity_color = severity_colors.get(alert['severity'], '#3b82f6')
            
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"### 🔴 {alert['type']}")
                st.caption(f"🕐 {alert['time']}")
            
            with col2:
                st.markdown(f"**Source:** {alert['source']}")
                st.markdown(f"**Destination:** {alert['destination']}")
                st.caption(f"Confidence: {alert['confidence']}%")
            
            with col3:
                st.markdown(
                    f"<div style='background-color: {severity_color}; padding: 8px 16px; "
                    f"border-radius: 20px; text-align: center; font-weight: 600;'>"
                    f"{alert['severity']}</div>",
                    unsafe_allow_html=True
                )
            
            st.divider()
    else:
        st.success("✅ No threats detected!")
    
    st.divider()
    
    # Database Records Viewer
    st.subheader("💾 Database Records (Last 10 Entries)")
    
    records = db.get_recent(limit=10)
    
    if records:
        for record in records:
            record_color = '#10b981' if record['type'] == 'traffic' else '#ef4444'
            
            with st.expander(f"📝 {record['id']} - {record['type'].upper()} - {record['timestamp']}"):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.markdown("**Record Info:**")
                    st.write(f"ID: `{record['id']}`")
                    st.write(f"Type: `{record['type']}`")
                    st.write(f"Time: `{record['timestamp']}`")
                
                with col2:
                    st.markdown("**Stored Data:**")
                    st.json(record['data'])
    else:
        st.info("No records in database yet. Start monitoring to collect data.")
    
    st.divider()
    
    # Settings Section
    st.subheader("⚙️ System Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Reset All Data", use_container_width=True):
            st.session_state.db_records = []
            st.session_state.db_logs = []
            st.session_state.total_packets = 0
            st.session_state.attacks_detected = 0
            st.session_state.normal_traffic = 0
            st.session_state.alerts = []
            st.session_state.traffic_data = []
            st.success("✅ All data reset!")
            st.rerun()
    
    with col2:
        if st.button("💾 Export Database", use_container_width=True):
            export_data = {
                'export_time': datetime.now().isoformat(),
                'stats': stats,
                'records': st.session_state.db_records,
                'logs': st.session_state.db_logs
            }
            st.download_button(
                label="⬇️ Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"garudarush_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        st.metric("Database Size", f"{stats['size_kb']:.1f} KB")

# ==================== ANALYSIS TAB ====================
with tab2:
    st.subheader("📈 System Analytics & Database Performance")
    
    # Database Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Database Growth Over Time")
        
        if st.session_state.db_records:
            # Create time-based chart
            df_records = pd.DataFrame(st.session_state.db_records)
            df_records['timestamp'] = pd.to_datetime(df_records['timestamp'])
            df_records['minute'] = df_records['timestamp'].dt.strftime('%H:%M')
            
            growth = df_records.groupby('minute').size().cumsum().reset_index(name='total_records')
            
            fig = go.Figure(data=[go.Scatter(
                x=growth['minute'],
                y=growth['total_records'],
                mode='lines+markers',
                line=dict(color='#3b82f6', width=3),
                fill='tozeroy'
            )])
            
            fig.update_layout(
                xaxis_title="Time",
                yaxis_title="Total Records",
                height=300,
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    
    with col2:
        st.markdown("### 🗂️ Records by Type")
        
        if st.session_state.db_records:
            df_records = pd.DataFrame(st.session_state.db_records)
            type_counts = df_records['type'].value_counts()
            
            fig = go.Figure(data=[go.Bar(
                x=type_counts.index,
                y=type_counts.values,
                marker_color=['#10b981', '#ef4444'],
                text=type_counts.values,
                textposition='outside'
            )])
            
            fig.update_layout(
                xaxis_title="Record Type",
                yaxis_title="Count",
                height=300,
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    
    st.divider()
    
    # Attack Distribution
    st.markdown("### 🎯 Attack Type Distribution")
    
    if sum(st.session_state.attack_distribution.values()) > 0:
        fig = go.Figure(data=[go.Pie(
            labels=list(st.session_state.attack_distribution.keys()),
            values=list(st.session_state.attack_distribution.values()),
            hole=0.4,
            marker=dict(colors=['#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6'])
        )])
        
        fig.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No attacks detected yet")
    
    st.divider()
    
    # Database Operations Log
    st.markdown("### 📝 Database Operation Log (Last 20)")
    
    logs = db.get_logs(limit=20)
    
    if logs:
        df_logs = pd.DataFrame(logs)
        st.dataframe(
            df_logs,
            use_container_width=True,
            hide_index=True,
            column_config={
                "time": "Time",
                "operation": "Operation",
                "collection": "Collection",
                "record_id": "Record ID",
                "status": "Status"
            }
        )
    else:
        st.info("No operations logged yet")

# Footer
st.markdown("""
<div class="footer" style="text-align: center; color: #94a3b8; padding: 2rem 0; margin-top: 2rem; border-top: 1px solid #334155;">
    <p><strong>GarudaRush Prototype with Database Visibility</strong></p>
    <p>Developed by <strong>Sourav Rinwa</strong>, <strong>Parshav Shah</strong>, <strong>Arvind Sharma</strong></p>
    <p>Guided by <strong>Mr. Utsav Dagar</strong></p>
    <p style="margin-top: 1rem; font-size: 0.875rem;">
        💾 Using Session-Based Database (In-Memory Storage for Prototype)
    </p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh
if st.session_state.monitoring:
    time.sleep(2)
    st.rerun()
```

---

## **Now Your GitHub Repository Structure:**
```
GarudaRush-Prototype/
├── streamlit_app_with_db.py   ← NEW: Enhanced version with visible database
├── requirements.txt            ← Same as before
├── README.md                   ← Update this
├── .gitignore                  
└── .streamlit/
    └── config.toml
