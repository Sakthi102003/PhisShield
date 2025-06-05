import axios from 'axios';
import { AlertTriangle, CheckCircle2, Clock } from 'lucide-react';
import { useEffect, useState } from 'react';
import { config } from '../config';

const History = () => {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        setError('Please login to view history');
        return;
      }

      const response = await axios.get(`${config.apiUrl}/api/history`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      setHistory(response.data);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch history');
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

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold cyberpunk-text flex items-center gap-2">
        <Clock size={24} />
        Scan History
      </h2>

      <div className="grid gap-4">
        {history.length === 0 ? (
          <div className="cyberpunk-card p-6 rounded-lg text-center text-muted-foreground">
            No scan history found
          </div>
        ) : (
          history.map((item) => (
            <div key={item.id} className="cyberpunk-card p-4 rounded-lg">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <div className="font-mono text-sm text-accent break-all">
                    {item.url}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {new Date(item.timestamp).toLocaleString()}
                  </div>
                </div>
                <div className={`flex items-center gap-2 px-3 py-1 rounded ${
                  item.is_phishing
                    ? 'bg-destructive/10 text-destructive'
                    : 'bg-[#34c759]/10 text-[#34c759]'
                }`}>
                  {item.is_phishing ? (
                    <AlertTriangle size={16} />
                  ) : (
                    <CheckCircle2 size={16} />
                  )}
                  <span className="text-sm font-medium">
                    {item.is_phishing ? 'Phishing' : 'Safe'}
                  </span>
                  <span className="text-sm font-mono">
                    {(item.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default History;
