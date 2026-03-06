import React, { useState, useEffect, useRef } from 'react';
import { Chart } from 'chart.js/auto';
import { getTrafficStats, getLiveTraffic, exportTrafficData } from '../../services/api';
import { toast } from 'react-toastify';
import Layout from '../Layout/Layout';
import './Traffic.css';

const Traffic = () => {
  const [stats, setStats] = useState(null);
  const [liveData, setLiveData] = useState({ normal: [], suspicious: [] });
  const [timeRange, setTimeRange] = useState(1);
  const [isMonitoring, setIsMonitoring] = useState(true);

  const trafficChartRef = useRef(null);
  const protocolChartRef = useRef(null);
  const trafficChart = useRef(null);
  const protocolChart = useRef(null);

  useEffect(() => {
    fetchStats();
    if (isMonitoring) {
      fetchLiveData();
      const interval = setInterval(fetchLiveData, 3000);
      return () => clearInterval(interval);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [timeRange, isMonitoring]);

  useEffect(() => {
    if (liveData.normal.length > 0) {
      initializeCharts();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [liveData, stats]);

  const fetchStats = async () => {
    try {
      const data = await getTrafficStats(timeRange);
      setStats(data.stats);
    } catch (error) {
      toast.error('Failed to fetch traffic statistics');
    }
  };

  const fetchLiveData = async () => {
    try {
      const data = await getLiveTraffic(30);
      setLiveData(data);
      updateTrafficChart(data);
    } catch (error) {
      console.error('Failed to fetch live traffic:', error);
    }
  };

  const initializeCharts = () => {
    // Traffic Chart
    if (trafficChartRef.current && !trafficChart.current) {
      const ctx = trafficChartRef.current.getContext('2d');
      // Create gradients
      const normalGradient = ctx.createLinearGradient(0, 0, 0, 400);
      normalGradient.addColorStop(0, 'rgba(0, 212, 255, 0.4)');
      normalGradient.addColorStop(1, 'rgba(0, 212, 255, 0.01)');

      const suspiciousGradient = ctx.createLinearGradient(0, 0, 0, 400);
      suspiciousGradient.addColorStop(0, 'rgba(255, 71, 87, 0.4)');
      suspiciousGradient.addColorStop(1, 'rgba(255, 71, 87, 0.01)');

      trafficChart.current = new Chart(ctx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [
            {
              label: 'Normal Traffic',
              data: [],
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
              data: [],
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
              padding: 12
            }
          },
          scales: {
            x: {
              ticks: { color: '#747d8c', font: { family: 'Inter' } },
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

    // Protocol Distribution Chart
    if (protocolChartRef.current && stats?.protocol_distribution && !protocolChart.current) {
      const ctx = protocolChartRef.current.getContext('2d');
      const protocols = Object.keys(stats.protocol_distribution);
      const counts = Object.values(stats.protocol_distribution);

      protocolChart.current = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: protocols,
          datasets: [{
            data: counts,
            backgroundColor: [
              '#00d4ff', '#4ecdc4', '#ff4757', '#ffa502', '#1e90ff', '#f368e0'
            ],
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
              position: 'right',
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
  };

  const formatTimeString = (timeStr) => {
    if (!timeStr) return '';
    if (/^\d{2}:\d{2}:\d{2}$/.test(timeStr)) {
      const [h, m, s] = timeStr.split(':');
      const now = new Date();
      now.setUTCHours(parseInt(h, 10), parseInt(m, 10), parseInt(s, 10), 0);
      return now.toLocaleTimeString();
    }
    const d = new Date(timeStr);
    if (!isNaN(d.getTime())) {
      return d.toLocaleTimeString();
    }
    return timeStr;
  };

  const updateTrafficChart = (data) => {
    if (trafficChart.current && data.normal) {
      const chart = trafficChart.current;
      chart.data.labels = data.normal.map(d => formatTimeString(d.time));
      chart.data.datasets[0].data = data.normal.map(d => d.value);
      chart.data.datasets[1].data = data.suspicious.map(d => d.value);
      chart.update('none');
    }
  };

  const updateProtocolChart = () => {
    if (protocolChart.current && stats?.protocol_distribution) {
      const protocols = Object.keys(stats.protocol_distribution);
      const counts = Object.values(stats.protocol_distribution);

      protocolChart.current.data.labels = protocols;
      protocolChart.current.data.datasets[0].data = counts;
      protocolChart.current.update();
    }
  };

  useEffect(() => {
    if (stats?.protocol_distribution) {
      updateProtocolChart();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stats]);

  const handleExport = async () => {
    try {
      const data = await exportTrafficData();
      const blob = new Blob([data.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = data.filename;
      a.click();
      toast.success('Traffic data exported successfully!');
    } catch (error) {
      toast.error('Failed to export traffic data');
    }
  };

  return (
    <Layout>
      <div className="traffic-container">
        <div className="traffic-header">
          <h1>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="title-icon"><path d="M22 12h-4l-3 9L9 3l-3 9H2" /></svg>
            Network Traffic Monitor
          </h1>
          <p className="subtitle">Real-time network traffic analysis and monitoring</p>
        </div>

        <div className="traffic-controls">
          <div className="control-group">
            <label>Time Range:</label>
            <select
              value={timeRange}
              onChange={(e) => {
                setTimeRange(Number(e.target.value));
                fetchStats();
              }}
              className="control-select"
            >
              <option value={1}>Last Hour</option>
              <option value={6}>Last 6 Hours</option>
              <option value={24}>Last 24 Hours</option>
              <option value={168}>Last Week</option>
            </select>
          </div>

          <button
            className={`monitor-btn ${isMonitoring ? 'active' : ''}`}
            onClick={() => setIsMonitoring(!isMonitoring)}
          >
            {isMonitoring ? (
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="6" y="4" width="4" height="16" /><rect x="14" y="4" width="4" height="16" /></svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="5 3 19 12 5 21 5 3" /></svg>
            )}
            <span>{isMonitoring ? 'Pause Monitoring' : 'Resume Monitoring'}</span>
          </button>

          <button className="export-btn" onClick={handleExport}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="7 10 12 15 17 10" /><line x1="12" x2="12" y1="15" y2="3" /></svg>
            <span>Export Data</span>
          </button>
        </div>

        {stats && (
          <div className="traffic-stats-grid">
            <div className="stat-card">
              <div className="stat-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" /><polyline points="3.29 7 12 12 20.71 7" /><line x1="12" x2="12" y1="22" y2="12" /></svg>
              </div>
              <div className="stat-content">
                <div className="stat-label">Total Packets</div>
                <div className="stat-value">{stats.total_packets?.toLocaleString() || 0}</div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3" /><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3" /><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" /></svg>
              </div>
              <div className="stat-content">
                <div className="stat-label">Total Bytes</div>
                <div className="stat-value">
                  {(stats.total_bytes / (1024 * 1024)).toFixed(2)} MB
                </div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" /></svg>
              </div>
              <div className="stat-content">
                <div className="stat-label">Avg Packet Rate</div>
                <div className="stat-value">
                  {stats.avg_packet_rate?.toFixed(2) || 0} pkt/s
                </div>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" /><path d="M12 9v4" /><path d="M12 17h.01" /></svg>
              </div>
              <div className="stat-content">
                <div className="stat-label">Recent Attacks</div>
                <div className="stat-value danger">{stats.recent_attacks || 0}</div>
              </div>
            </div>
          </div>
        )}

        <div className="traffic-charts">
          <div className="chart-section">
            <h2>Real-Time Traffic Flow</h2>
            <div className="chart-box">
              <canvas ref={trafficChartRef}></canvas>
            </div>
          </div>

          <div className="chart-section">
            <h2>Protocol Distribution</h2>
            <div className="chart-box protocol-chart">
              {stats?.protocol_distribution ? (
                <canvas ref={protocolChartRef}></canvas>
              ) : (
                <div className="no-data">No protocol data available</div>
              )}
            </div>
          </div>
        </div>

        {stats?.protocol_distribution && (
          <div className="protocol-list">
            <h2>Protocol Details</h2>
            <div className="protocol-grid">
              {Object.entries(stats.protocol_distribution).map(([protocol, count]) => (
                <div key={protocol} className="protocol-item">
                  <span className="protocol-name">{protocol}</span>
                  <span className="protocol-count">{count}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Traffic;
