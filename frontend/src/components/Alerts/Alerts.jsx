import React, { useState, useEffect } from 'react';
import { getAlerts, acknowledgeAlert, resolveAlert, getAlertsSummary } from '../../services/api';
import { toast } from 'react-toastify';
import Layout from '../Layout/Layout';
import './Alerts.css';

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    severity: '',
    status: '',
    attack_type: ''
  });
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetchAlerts();
    fetchSummary();
    const interval = setInterval(() => {
      fetchAlerts();
      fetchSummary();
    }, 10000);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters, page]);

  const fetchAlerts = async () => {
    try {
      const params = {
        ...filters,
        page,
        limit: 20
      };
      const response = await getAlerts(params);
      setAlerts(response.alerts);
      setTotalPages(response.pagination.total_pages);
      setLoading(false);
    } catch (error) {
      toast.error('Failed to fetch alerts');
      setLoading(false);
    }
  };

  const fetchSummary = async () => {
    try {
      const data = await getAlertsSummary(24);
      setSummary(data);
    } catch (error) {
      console.error('Failed to fetch summary:', error);
    }
  };

  const handleAcknowledge = async (alertId) => {
    try {
      await acknowledgeAlert(alertId, 'Acknowledged by user');
      toast.success('Alert acknowledged');
      fetchAlerts();
      fetchSummary();
    } catch (error) {
      toast.error('Failed to acknowledge alert');
    }
  };

  const handleResolve = async (alertId) => {
    try {
      await resolveAlert(alertId, 'Resolved by user');
      toast.success('Alert resolved');
      fetchAlerts();
      fetchSummary();
    } catch (error) {
      toast.error('Failed to resolve alert');
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      low: '#4ecdc4',
      medium: '#ffa07a',
      high: '#ff6b6b',
      critical: '#ff1744'
    };
    return colors[severity] || '#9fa3ad';
  };

  const getStatusBadge = (status) => {
    const badges = {
      active: { text: 'Active', class: 'status-active' },
      acknowledged: { text: 'Acknowledged', class: 'status-acknowledged' },
      resolved: { text: 'Resolved', class: 'status-resolved' }
    };
    return badges[status] || { text: status, class: '' };
  };

  if (loading && !alerts.length) {
    return (
      <Layout>
        <div className="loading-container">Loading alerts...</div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="alerts-container">
        <div className="alerts-header">
          <h1>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="title-icon"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /><path d="M12 8v4" /><path d="M12 16h.01" /></svg>
            Security Alerts
          </h1>
          <p className="subtitle">Monitor and manage security threats</p>
        </div>

        {summary && (
          <div className="alerts-summary">
            <div className="summary-card">
              <div className="summary-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" /><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" /></svg>
              </div>
              <div className="summary-content">
                <div className="summary-label">Total Alerts</div>
                <div className="summary-value">{summary.summary.total}</div>
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-icon critical">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10" /><line x1="12" x2="12" y1="8" y2="12" /><line x1="12" x2="12.01" y1="16" y2="16" /></svg>
              </div>
              <div className="summary-content">
                <div className="summary-label">Critical</div>
                <div className="summary-value critical">{summary.summary.by_severity.critical}</div>
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-icon high">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" /><path d="M12 9v4" /><path d="M12 17h.01" /></svg>
              </div>
              <div className="summary-content">
                <div className="summary-label">High</div>
                <div className="summary-value high">{summary.summary.by_severity.high}</div>
              </div>
            </div>
            <div className="summary-card">
              <div className="summary-icon active">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12" /></svg>
              </div>
              <div className="summary-content">
                <div className="summary-label">Active</div>
                <div className="summary-value">{summary.summary.by_status.active}</div>
              </div>
            </div>
          </div>
        )}

        <div className="alerts-filters">
          <select
            value={filters.severity}
            onChange={(e) => {
              setFilters({ ...filters, severity: e.target.value });
              setPage(1);
            }}
            className="filter-select"
          >
            <option value="">All Severities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>

          <select
            value={filters.status}
            onChange={(e) => {
              setFilters({ ...filters, status: e.target.value });
              setPage(1);
            }}
            className="filter-select"
          >
            <option value="">All Statuses</option>
            <option value="active">Active</option>
            <option value="acknowledged">Acknowledged</option>
            <option value="resolved">Resolved</option>
          </select>

          <select
            value={filters.attack_type}
            onChange={(e) => {
              setFilters({ ...filters, attack_type: e.target.value });
              setPage(1);
            }}
            className="filter-select"
          >
            <option value="">All Attack Types</option>
            <option value="SYN Flood">SYN Flood</option>
            <option value="UDP Flood">UDP Flood</option>
            <option value="HTTP Flood">HTTP Flood</option>
            <option value="DNS Amplification">DNS Amplification</option>
            <option value="Slowloris">Slowloris</option>
          </select>
        </div>

        <div className="alerts-list">
          {alerts.length === 0 ? (
            <div className="empty-state">
              <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="empty-icon-svg"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /><path d="m9 12 2 2 4-4" /></svg>
              <h3>No alerts found</h3>
              <p>All clear! No security threats detected.</p>
            </div>
          ) : (
            alerts.map((alert) => {
              const statusBadge = getStatusBadge(alert.status);
              return (
                <div key={alert.id} className="alert-card">
                  <div className="alert-header">
                    <div className="alert-title-section">
                      <span
                        className="severity-indicator"
                        style={{ backgroundColor: getSeverityColor(alert.severity) }}
                      ></span>
                      <div>
                        <h3 className="alert-title">{alert.attack_type}</h3>
                        <div className="alert-meta">
                          <span className={`status-badge ${statusBadge.class}`}>
                            {statusBadge.text}
                          </span>
                          <span className="alert-time">
                            {new Date(alert.timestamp).toLocaleString()}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="alert-confidence">
                      <span className="confidence-label">Confidence</span>
                      <span className="confidence-value">
                        {(alert.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  <div className="alert-details">
                    <div className="detail-item">
                      <span className="detail-label">Source IP:</span>
                      <span className="detail-value">{alert.source_ip || 'N/A'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Destination IP:</span>
                      <span className="detail-value">{alert.destination_ip || 'N/A'}</span>
                    </div>
                    <div className="detail-item">
                      <span className="detail-label">Packets:</span>
                      <span className="detail-value">{alert.packet_count || 0}</span>
                    </div>
                    {alert.description && (
                      <div className="detail-item full-width">
                        <span className="detail-label">Description:</span>
                        <span className="detail-value">{alert.description}</span>
                      </div>
                    )}
                  </div>

                  {alert.status === 'active' && (
                    <div className="alert-actions">
                      <button
                        className="action-btn acknowledge-btn"
                        onClick={() => handleAcknowledge(alert.id)}
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12" /></svg> Acknowledge
                      </button>
                      <button
                        className="action-btn resolve-btn"
                        onClick={() => handleResolve(alert.id)}
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12" /></svg> Resolve
                      </button>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        {totalPages > 1 && (
          <div className="pagination">
            <button
              className="page-btn"
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
            >
              ← Previous
            </button>
            <span className="page-info">
              Page {page} of {totalPages}
            </span>
            <button
              className="page-btn"
              onClick={() => setPage(Math.min(totalPages, page + 1))}
              disabled={page === totalPages}
            >
              Next →
            </button>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default Alerts;
