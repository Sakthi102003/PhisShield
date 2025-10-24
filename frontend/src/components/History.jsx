import { AlertTriangle, CheckCircle2, Clock, Download, Filter, Search, X } from 'lucide-react';
import { useEffect, useState } from 'react';
import api from '../services/api';

const History = ({ user }) => {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all'); // all, safe, phishing
  const [sortBy, setSortBy] = useState('date-desc'); // date-desc, date-asc, confidence-desc, confidence-asc
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [history, searchTerm, filterType, sortBy, dateFrom, dateTo]);

  const fetchHistory = async () => {
    try {
      if (!user?.token) {
        setError('Please login to view history');
        setLoading(false);
        return;
      }

      const response = await api.get('/api/history');
      setHistory(response.data);
    } catch (err) {
      console.error('History fetch error:', err);
      setError(err.response?.data?.error || 'Failed to fetch history');
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...history];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(item =>
        item.url.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Type filter
    if (filterType === 'safe') {
      filtered = filtered.filter(item => !item.is_phishing);
    } else if (filterType === 'phishing') {
      filtered = filtered.filter(item => item.is_phishing);
    }

    // Date range filter
    if (dateFrom) {
      filtered = filtered.filter(item =>
        new Date(item.checked_at) >= new Date(dateFrom)
      );
    }
    if (dateTo) {
      filtered = filtered.filter(item =>
        new Date(item.checked_at) <= new Date(dateTo + 'T23:59:59')
      );
    }

    // Sort
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'date-desc':
          return new Date(b.checked_at) - new Date(a.checked_at);
        case 'date-asc':
          return new Date(a.checked_at) - new Date(b.checked_at);
        case 'confidence-desc':
          return b.confidence - a.confidence;
        case 'confidence-asc':
          return a.confidence - b.confidence;
        default:
          return 0;
      }
    });

    setFilteredHistory(filtered);
  };

  const clearFilters = () => {
    setSearchTerm('');
    setFilterType('all');
    setSortBy('date-desc');
    setDateFrom('');
    setDateTo('');
  };

  const exportHistory = () => {
    const csvContent = [
      ['URL', 'Result', 'Confidence', 'Date'],
      ...filteredHistory.map(item => [
        item.url,
        item.is_phishing ? 'Phishing' : 'Safe',
        `${(item.confidence * 100).toFixed(1)}%`,
        new Date(item.checked_at).toLocaleString()
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', `phishshield-history-${Date.now()}.csv`);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
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

  const hasActiveFilters = searchTerm || filterType !== 'all' || sortBy !== 'date-desc' || dateFrom || dateTo;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold cyberpunk-text flex items-center gap-2">
          <Clock size={24} />
          Scan History
        </h2>
        {filteredHistory.length > 0 && (
          <button
            onClick={exportHistory}
            className="cyberpunk-button px-4 py-2 rounded flex items-center gap-2"
          >
            <Download size={18} />
            Export
          </button>
        )}
      </div>

      {/* Filters Section */}
      <div className="cyberpunk-card p-4 rounded-lg space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold cyberpunk-text flex items-center gap-2">
            <Filter size={18} />
            Filters
          </h3>
          {hasActiveFilters && (
            <button
              onClick={clearFilters}
              className="text-sm text-destructive hover:text-destructive/80 flex items-center gap-1"
            >
              <X size={16} />
              Clear All
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* Search */}
          <div>
            <label className="text-sm text-muted-foreground block mb-2">Search URL</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" size={18} />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search..."
                className="cyberpunk-input w-full pl-10 pr-4 py-2 rounded"
              />
            </div>
          </div>

          {/* Result Type Filter */}
          <div>
            <label className="text-sm text-muted-foreground block mb-2">Result Type</label>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="cyberpunk-input w-full px-4 py-2 rounded"
            >
              <option value="all">All Results</option>
              <option value="safe">Safe Only</option>
              <option value="phishing">Phishing Only</option>
            </select>
          </div>

          {/* Sort By */}
          <div>
            <label className="text-sm text-muted-foreground block mb-2">Sort By</label>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="cyberpunk-input w-full px-4 py-2 rounded"
            >
              <option value="date-desc">Date (Newest First)</option>
              <option value="date-asc">Date (Oldest First)</option>
              <option value="confidence-desc">Confidence (High to Low)</option>
              <option value="confidence-asc">Confidence (Low to High)</option>
            </select>
          </div>

          {/* Date Range */}
          <div>
            <label className="text-sm text-muted-foreground block mb-2">Date Range</label>
            <div className="flex gap-2">
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="cyberpunk-input flex-1 px-2 py-2 rounded text-sm"
                placeholder="From"
              />
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="cyberpunk-input flex-1 px-2 py-2 rounded text-sm"
                placeholder="To"
              />
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="text-sm text-muted-foreground">
          Showing {filteredHistory.length} of {history.length} results
        </div>
      </div>

      {/* History List */}
      <div className="grid gap-4">
        {filteredHistory.length === 0 ? (
          <div className="cyberpunk-card p-6 rounded-lg text-center text-muted-foreground">
            {history.length === 0 ? 'No scan history found' : 'No results match your filters'}
          </div>
        ) : (
          filteredHistory.map((item, index) => (
            <div key={index} className="cyberpunk-card p-4 rounded-lg">
              <div className="flex items-start justify-between">
                <div className="space-y-1 flex-1 min-w-0">
                  <div className="font-mono text-sm text-accent break-all">
                    {item.url}
                  </div>
                  <div className="text-sm text-muted-foreground">
                    {new Date(item.checked_at).toLocaleString()}
                  </div>
                </div>
                <div className={`flex items-center gap-2 px-3 py-1 rounded ml-4 ${
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
