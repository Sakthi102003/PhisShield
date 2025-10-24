import { AlertTriangle, CheckCircle2, Clock, Shield, TrendingUp } from 'lucide-react';
import { useEffect, useState } from 'react';
import { Cell, Legend, Line, LineChart, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import api from '../services/api';

const COLORS = {
  safe: '#34c759',
  phishing: '#ff3b30',
  accent: '#0db8d8'
};

const Dashboard = ({ user }) => {
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      const response = await api.get('/api/statistics');
      setStatistics(response.data);
    } catch (err) {
      console.error('Statistics fetch error:', err);
      setError(err.response?.data?.error || 'Failed to fetch statistics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="cyberpunk-card p-4 rounded-lg text-destructive flex items-center justify-center gap-2">
        <AlertTriangle size={18} />
        <span>{error}</span>
      </div>
    );
  }

  if (!statistics) {
    return (
      <div className="cyberpunk-card p-6 rounded-lg text-center text-muted-foreground">
        No statistics available
      </div>
    );
  }

  const pieData = [
    { name: 'Safe', value: statistics.safe_count, color: COLORS.safe },
    { name: 'Phishing', value: statistics.phishing_count, color: COLORS.phishing }
  ];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="cyberpunk-card p-2 rounded shadow-lg">
          <p className="text-sm text-foreground">{`${payload[0].name}: ${payload[0].value}`}</p>
          <p className="text-xs text-muted-foreground">{`${((payload[0].value / statistics.total_scans) * 100).toFixed(1)}%`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold cyberpunk-text flex items-center gap-2">
          <TrendingUp size={28} />
          Dashboard
        </h2>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="cyberpunk-card p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Total Scans</p>
              <p className="text-3xl font-bold cyberpunk-text mt-1">{statistics.total_scans}</p>
            </div>
            <div className="bg-accent/10 p-3 rounded-full">
              <Shield size={24} className="text-accent" />
            </div>
          </div>
        </div>

        <div className="cyberpunk-card p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Safe URLs</p>
              <p className="text-3xl font-bold text-[#34c759] mt-1">{statistics.safe_count}</p>
            </div>
            <div className="bg-[#34c759]/10 p-3 rounded-full">
              <CheckCircle2 size={24} className="text-[#34c759]" />
            </div>
          </div>
        </div>

        <div className="cyberpunk-card p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Phishing Detected</p>
              <p className="text-3xl font-bold text-destructive mt-1">{statistics.phishing_count}</p>
            </div>
            <div className="bg-destructive/10 p-3 rounded-full">
              <AlertTriangle size={24} className="text-destructive" />
            </div>
          </div>
        </div>

        <div className="cyberpunk-card p-6 rounded-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-muted-foreground">Avg Confidence</p>
              <p className="text-3xl font-bold cyberpunk-text mt-1">
                {statistics.average_confidence ? `${statistics.average_confidence.toFixed(1)}%` : 'N/A'}
              </p>
            </div>
            <div className="bg-accent/10 p-3 rounded-full">
              <TrendingUp size={24} className="text-accent" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pie Chart */}
        <div className="cyberpunk-card p-6 rounded-lg">
          <h3 className="text-xl font-semibold cyberpunk-text mb-4">Scan Results Distribution</h3>
          {statistics.total_scans > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(1)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[300px] text-muted-foreground">
              No data available
            </div>
          )}
        </div>

        {/* Activity Timeline */}
        <div className="cyberpunk-card p-6 rounded-lg">
          <h3 className="text-xl font-semibold cyberpunk-text mb-4">Recent Activity</h3>
          {statistics.recent_activity && statistics.recent_activity.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={statistics.recent_activity}>
                <XAxis 
                  dataKey="date" 
                  stroke="#6b7280"
                  tick={{ fill: '#9ca3af', fontSize: 12 }}
                />
                <YAxis 
                  stroke="#6b7280"
                  tick={{ fill: '#9ca3af', fontSize: 12 }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(0, 0, 0, 0.8)', 
                    border: '1px solid #0db8d8',
                    borderRadius: '4px'
                  }}
                  labelStyle={{ color: '#0db8d8' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="scans" 
                  stroke={COLORS.accent} 
                  strokeWidth={2}
                  name="Scans"
                  dot={{ fill: COLORS.accent, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-[300px] text-muted-foreground">
              No recent activity
            </div>
          )}
        </div>
      </div>

      {/* Recent Scans */}
      <div className="cyberpunk-card p-6 rounded-lg">
        <h3 className="text-xl font-semibold cyberpunk-text mb-4 flex items-center gap-2">
          <Clock size={20} />
          Latest Scans
        </h3>
        {statistics.latest_scans && statistics.latest_scans.length > 0 ? (
          <div className="space-y-3">
            {statistics.latest_scans.map((scan, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-black/20 rounded border border-accent/20">
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-mono text-accent truncate">{scan.url}</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    {new Date(scan.checked_at).toLocaleString()}
                  </p>
                </div>
                <div className={`flex items-center gap-2 px-3 py-1 rounded ml-4 ${
                  scan.is_phishing
                    ? 'bg-destructive/10 text-destructive'
                    : 'bg-[#34c759]/10 text-[#34c759]'
                }`}>
                  {scan.is_phishing ? (
                    <AlertTriangle size={16} />
                  ) : (
                    <CheckCircle2 size={16} />
                  )}
                  <span className="text-sm font-medium">
                    {scan.is_phishing ? 'Phishing' : 'Safe'}
                  </span>
                  <span className="text-sm font-mono">
                    {(scan.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center text-muted-foreground py-8">
            No recent scans available
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
