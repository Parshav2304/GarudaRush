import React, { useState, useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';
import {
  getDashboardOverview,
  getLiveTraffic,
  exportTrafficData,
  getRealtimeMetrics,
  getAgentStatus
} from '../../services/api';
import { toast } from 'react-toastify';
import Layout from '../Layout/Layout';
import './Dashboard.css';

const Dashboard = () => {
  const [isMonitoring, setIsMonitoring] = useState(true);
  const [dashboardData, setDashboardData] = useState(null);
  // eslint-disable-next-line no-unused-vars
  const [liveTraffic, setLiveTraffic] = useState({ normal: [], suspicious: [] });
  const [realtimeMetrics, setRealtimeMetrics] = useState(null);
  const [agentStatus, setAgentStatus] = useState(null);

  const trafficChartRef = useRef(null);
  const pieChartRef = useRef(null);
  const barChartRef = useRef(null);
  const trafficChart = useRef(null);
  const pieChart = useRef(null);
  const barChart = useRef(null);

  useEffect(() => {
    fetchDashboardData();
    fetchRealtimeMetrics();
    fetchAgentStatus();
    const interval = setInterval(() => {
      fetchDashboardData();
      fetchRealtimeMetrics();
      fetchAgentStatus();
    }, 10000); // Update every 10 seconds
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (isMonitoring) {
      fetchLiveTraffic();
      const interval = setInterval(fetchLiveTraffic, 2000); // Update every 2 seconds
      return () => clearInterval(interval);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isMonitoring]);

  useEffect(() => {
    if (dashboardData) {
      initializeCharts();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dashboardData]);

  const fetchDashboardData = async () => {
    try {
      const data = await getDashboardOverview(24);
      setDashboardData(data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    }
  };

  const fetchLiveTraffic = async () => {
    try {
      const data = await getLiveTraffic(20);
      setLiveTraffic(data);
      updateTrafficChart(data);
    } catch (error) {
      console.error('Failed to fetch live traffic:', error);
    }
  };

  const fetchRealtimeMetrics = async () => {
    try {
      const data = await getRealtimeMetrics();
      setRealtimeMetrics(data.metrics);
    } catch (error) {
      console.error('Failed to fetch real-time metrics:', error);
    }
  };

  const fetchAgentStatus = async () => {
    try {
      const data = await getAgentStatus();
      setAgentStatus(data);
    } catch (error) {
      console.error('Failed to fetch agent status:', error);
    }
  };

  const initializeCharts = () => {
    // Traffic Chart
    if (trafficChartRef.current) {
      const ctx = trafficChartRef.current.getContext('2d');
      // Create gradients
      const normalGradient = ctx.createLinearGradient(0, 0, 0, 400);
      normalGradient.addColorStop(0, 'rgba(0, 212, 255, 0.4)');
      normalGradient.addColorStop(1, 'rgba(0, 212, 255, 0.01)');

      const suspiciousGradient = ctx.createLinearGradient(0, 0, 0, 400);
      suspiciousGradient.addColorStop(0, 'rgba(255, 71, 87, 0.4)');
      suspiciousGradient.addColorStop(1, 'rgba(255, 71, 87, 0.01)');

      if (trafficChart.current) {
        trafficChart.current.destroy();
      }

      trafficChart.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Array.from({ length: 20 }, (_, i) => {
            const t = new Date(Date.now() - (19 - i) * 3000);
            return t.toLocaleTimeString();
          }),
          datasets: [
            {
              label: 'Normal Traffic',
              data: Array.from({ length: 20 }, () => Math.floor(Math.random() * 50 + 30)),
              borderColor: '#00d4ff',
              backgroundColor: normalGradient,
              borderWidth: 2,
              pointRadius: 0,
              pointHoverRadius: 6,
              tension: 0.4,
              fill: true
            },
            {
              label: 'Suspicious Traffic',
              data: Array.from({ length: 20 }, () => Math.floor(Math.random() * 10)),
              borderColor: '#ff4757',
              backgroundColor: suspiciousGradient,
              borderWidth: 2,
              pointRadius: 0,
              pointHoverRadius: 6,
              tension: 0.4,
              fill: true
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: {
              labels: { color: '#a4b0be', usePointStyle: true, boxWidth: 8, font: { family: 'Inter', size: 13 } }
            },
            tooltip: {
              backgroundColor: 'rgba(18, 20, 29, 0.9)',
              titleColor: '#fff',
              bodyColor: '#a4b0be',
              borderColor: 'rgba(255,255,255,0.1)',
              borderWidth: 1,
              padding: 12,
              callbacks: {
                title: function (context) {
                  return context[0].label; // Labels are already formatted
                }
              }
            }
          },
          scales: {
            x: {
              ticks: {
                color: '#747d8c',
                font: { family: 'Inter' },
                callback: function (val, index) {
                  return this.getLabelForValue(val); // Labels are already formatted
                }
              },
              grid: { color: 'rgba(255, 255, 255, 0.03)', drawBorder: false }
            },
            y: {
              beginAtZero: true,
              ticks: { color: '#747d8c', font: { family: 'Inter' } },
              grid: { color: 'rgba(255, 255, 255, 0.03)', drawBorder: false }
            }
          }
        }
      });
    }

    // Pie Chart
    if (pieChartRef.current && dashboardData?.attack_distribution) {
      const ctx = pieChartRef.current.getContext('2d');

      if (pieChart.current) {
        pieChart.current.destroy();
      }

      const attackDist = dashboardData.attack_distribution;
      pieChart.current = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: Object.keys(attackDist),
          datasets: [{
            data: Object.values(attackDist),
            backgroundColor: ['#00d4ff', '#4ecdc4', '#ff4757', '#ffa502', '#1e90ff', '#f368e0'],
            borderWidth: 0,
            hoverOffset: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '65%',
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                color: '#a4b0be',
                padding: 20,
                usePointStyle: true,
                pointStyle: 'circle',
                font: { family: 'Inter', size: 12 }
              }
            },
            tooltip: {
              backgroundColor: 'rgba(18, 20, 29, 0.9)',
              titleColor: '#fff',
              bodyColor: '#a4b0be',
              borderColor: 'rgba(255,255,255,0.1)',
              borderWidth: 1,
              padding: 12
            }
          }
        }
      });
    }

    // Bar Chart
    if (barChartRef.current && dashboardData?.model_performance) {
      const ctx = barChartRef.current.getContext('2d');

      if (barChart.current) {
        barChart.current.destroy();
      }

      const perf = dashboardData.model_performance;

      // Gradient for bars
      const barGradient = ctx.createLinearGradient(0, 0, 0, 400);
      barGradient.addColorStop(0, '#00d4ff');
      barGradient.addColorStop(1, '#1e90ff');

      barChart.current = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
          datasets: [{
            label: 'Performance (%)',
            data: [perf.accuracy, perf.precision, perf.recall, perf.f1_score],
            backgroundColor: barGradient,
            borderRadius: 6,
            barThickness: 32
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            },
            tooltip: {
              backgroundColor: 'rgba(18, 20, 29, 0.9)',
              titleColor: '#fff',
              bodyColor: '#a4b0be',
              borderColor: 'rgba(255,255,255,0.1)',
              borderWidth: 1,
              padding: 12
            }
          },
          scales: {
            x: {
              ticks: { color: '#a4b0be', font: { family: 'Inter' } },
              grid: { display: false }
            },
            y: {
              ticks: { color: '#747d8c', font: { family: 'Inter' } },
              grid: { color: 'rgba(255, 255, 255, 0.03)', drawBorder: false },
              min: 0,
              max: 100
            }
          }
        }
      });
    }
  };

  const formatTimeString = (timeStr) => {
    if (!timeStr) return '';
    // Handle old format HH:MM:SS
    if (/^\d{2}:\d{2}:\d{2}$/.test(timeStr)) {
      const [h, m, s] = timeStr.split(':');
      const now = new Date();
      now.setUTCHours(parseInt(h, 10), parseInt(m, 10), parseInt(s, 10), 0);
      return now.toLocaleTimeString();
    }
    // Handle ISO strings with Z
    const d = new Date(timeStr);
    if (!isNaN(d.getTime())) {
      return d.toLocaleTimeString();
    }
    return timeStr;
  };

  const updateTrafficChart = (data) => {
    if (trafficChart.current && (data.normal || data.suspicious)) {
      const chart = trafficChart.current;

      // Build a unified timeline from both normal and suspicious data
      const timeMap = new Map();
      (data.normal || []).forEach(d => {
        if (!timeMap.has(d.time)) timeMap.set(d.time, { normal: 0, suspicious: 0, formattedTime: formatTimeString(d.time) });
        timeMap.get(d.time).normal = d.value;
      });
      (data.suspicious || []).forEach(d => {
        if (!timeMap.has(d.time)) timeMap.set(d.time, { normal: 0, suspicious: 0, formattedTime: formatTimeString(d.time) });
        timeMap.get(d.time).suspicious = d.value;
      });

      // Sort by time string (ISO/HH:MM:SS are lexicographically sortable)
      const sorted = [...timeMap.entries()].sort((a, b) => a[0].localeCompare(b[0]));

      chart.data.labels = sorted.map(([, v]) => v.formattedTime);
      chart.data.datasets[0].data = sorted.map(([, v]) => v.normal);
      chart.data.datasets[1].data = sorted.map(([, v]) => v.suspicious);
      chart.update('none');
    }
  };

  const toggleMonitoring = () => {
    setIsMonitoring(!isMonitoring);
    toast.info(isMonitoring ? 'Monitoring stopped' : 'Monitoring started');
  };

  const handleResetStats = () => {
    toast.success('Statistics reset successfully!');
  };

  const handleExportDatabase = async () => {
    try {
      const data = await exportTrafficData();
      const blob = new Blob([data.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = data.filename;
      a.click();
      toast.success('Database exported successfully!');
    } catch (error) {
      toast.error('Failed to export database');
    }
  };

  if (!dashboardData) {
    return (
      <Layout>
        <div className="loading-container">Loading dashboard...</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="title-icon"><rect width="7" height="9" x="3" y="3" rx="1" /><rect width="7" height="5" x="14" y="3" rx="1" /><rect width="7" height="9" x="14" y="12" rx="1" /><rect width="7" height="5" x="3" y="16" rx="1" /></svg>
            Dashboard Overview
          </h1>
          <p className="subtitle">Real-time monitoring and analytics</p>
        </div>

        {/* Real-time Metrics */}
        {realtimeMetrics && (
          <div className="realtime-metrics">
            <div className="metric-card">
              <div className="metric-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" /></svg>
              </div>
              <div className="metric-content">
                <div className="metric-label">Packet Rate</div>
                <div className="metric-value">{realtimeMetrics.packet_rate} pkt/s</div>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" /><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71" /></svg>
              </div>
              <div className="metric-content">
                <div className="metric-label">Active Connections</div>
                <div className="metric-value">{realtimeMetrics.active_connections}</div>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2" /></svg>
              </div>
              <div className="metric-content">
                <div className="metric-label">Bandwidth</div>
                <div className="metric-value">{realtimeMetrics.bandwidth_mbps} MB/s</div>
              </div>
            </div>
            <div className="metric-card">
              <div className="metric-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" /><path d="M12 9v4" /><path d="M12 17h.01" /></svg>
              </div>
              <div className="metric-content">
                <div className="metric-label">Threat Level</div>
                <div className={`metric-value threat-${realtimeMetrics.threat_level}`}>
                  {realtimeMetrics.threat_level.toUpperCase()}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Agent Status */}
        {agentStatus && (
          <div className="agent-status-section">
            <h2>
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2" /><line x1="12" x2="12" y1="8" y2="12" /><line x1="8" x2="8" y1="12" y2="12" /><line x1="16" x2="16" y1="12" y2="12" /></svg>
              Monitoring Agents
            </h2>
            <div className="agent-grid">
              {agentStatus.agents.length > 0 ? (
                agentStatus.agents.map((agent) => (
                  <div key={agent.id} className="agent-card">
                    <div className="agent-header">
                      <span className={`agent-status-indicator ${agent.status}`}></span>
                      <span className="agent-id">{agent.id}</span>
                    </div>
                    <div className="agent-stats">
                      <div className="agent-stat">
                        <span className="stat-label">Status:</span>
                        <span className={`stat-value ${agent.status}`}>{agent.status}</span>
                      </div>
                      <div className="agent-stat">
                        <span className="stat-label">Packets:</span>
                        <span className="stat-value">{agent.packets_processed}</span>
                      </div>
                      <div className="agent-stat">
                        <span className="stat-label">Rate:</span>
                        <span className="stat-value">{agent.avg_packet_rate} pkt/s</span>
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-agents">No active agents</div>
              )}
            </div>
          </div>
        )}

        {/* Traffic Monitor */}
        <section className="section">
          <h2>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2 12h4l3-9 5 18 3-9h5" /></svg>
            Real-Time Traffic Monitor
          </h2>
          <div className="chart-box">
            <canvas ref={trafficChartRef}></canvas>
          </div>
          <button className={`btn ${!isMonitoring ? 'stopped' : ''}`} onClick={toggleMonitoring}>
            {isMonitoring ? (
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="6" y="4" width="4" height="16" /><rect x="14" y="4" width="4" height="16" /></svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="5 3 19 12 5 21 5 3" /></svg>
            )}
            <span>{isMonitoring ? 'Stop Monitoring' : 'Start Monitoring'}</span>
          </button>
        </section>

        {/* Database Storage */}
        <section className="section">
          <h2>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3" /><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" /><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" /></svg>
            Database Storage
          </h2>
          <div className="flex">
            <div className="card">
              <div className="stats-title">Total Records</div>
              <div className="stats-value">{dashboardData.overview.total_records}</div>
            </div>
            <div className="card">
              <div className="stats-title">Alert Records</div>
              <div className="stats-value">{dashboardData.overview.alert_records}</div>
            </div>
            <div className="card">
              <div className="stats-title">Traffic Records</div>
              <div className="stats-value">{dashboardData.overview.traffic_records}</div>
            </div>
          </div>
          <div>
            <button className="btn" onClick={handleResetStats}>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" /><path d="M3 3v5h5" /></svg>
              Reset Statistics
            </button>
            <button className="btn" onClick={handleExportDatabase}>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" x2="12" y1="15" y2="3" /></svg>
              Export Database
            </button>
          </div>
        </section>

        {/* Analytics & Performance */}
        <section className="section">
          <h2>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21.21 15.89A10 10 0 1 1 8 2.83" /><path d="M22 12A10 10 0 0 0 12 2v10z" /></svg>
            Analytics & Performance
          </h2>
          <div className="flex">
            <div className="chart-box pie-chart-container">
              <div className="chart-header">Attack Distribution</div>
              <canvas ref={pieChartRef}></canvas>
            </div>
            <div className="chart-box" style={{ flex: 1, minWidth: '400px' }}>
              <div className="chart-header">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: '#ffa502' }}><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" /><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" /><path d="M4 22h16" /><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22" /><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" /><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z" /></svg>
                Model Performance
              </div>
              <canvas ref={barChartRef}></canvas>
            </div>
          </div>
        </section>

        {/* Detection Statistics */}
        <section className="section">
          <h2>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17" /><polyline points="16 7 22 7 22 13" /></svg>
            Detection Statistics
          </h2>
          <div className="stats-grid">
            <div className="card">
              <div className="stats-title">Total Detections</div>
              <div className="stats-value">{dashboardData.detection_stats.total_detections}</div>
            </div>
            <div className="card">
              <div className="stats-title">Attack Rate</div>
              <div className="stats-value">{dashboardData.detection_stats.attack_rate}%</div>
            </div>
            <div className="card">
              <div className="stats-title">False Positive</div>
              <div className="stats-value">{dashboardData.detection_stats.false_positive_rate}%</div>
            </div>
            <div className="card">
              <div className="stats-title">Detection Time</div>
              <div className="stats-value">{dashboardData.detection_stats.avg_detection_time}s</div>
            </div>
          </div>
        </section>
      </div>
    </Layout>
  );
};

export default Dashboard;