import { AlertTriangle, CheckCircle2, Download, Upload, X } from 'lucide-react';
import { useRef, useState } from 'react';
import api from '../services/api';

const BulkScanner = ({ user, onScanComplete }) => {
  const [urls, setUrls] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);
  const textAreaRef = useRef(null);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target.result;
      let extractedUrls = [];

      if (file.name.endsWith('.csv')) {
        // Parse CSV
        const lines = content.split('\n');
        extractedUrls = lines
          .map(line => line.split(',')[0].trim())
          .filter(url => url && url.includes('.'));
      } else if (file.name.endsWith('.txt')) {
        // Parse text file
        extractedUrls = content
          .split('\n')
          .map(url => url.trim())
          .filter(url => url && url.includes('.'));
      }

      setUrls(extractedUrls);
      setError('');
    };

    reader.onerror = () => {
      setError('Failed to read file');
    };

    reader.readAsText(file);
  };

  const handleTextInput = (e) => {
    const text = e.target.value;
    const extractedUrls = text
      .split('\n')
      .map(url => url.trim())
      .filter(url => url && url.includes('.'));
    setUrls(extractedUrls);
  };

  const formatUrl = (url) => {
    let formatted = url.trim().replace(/^(?:https?:\/\/)?(?:www\.)?/i, '');
    return 'https://' + formatted;
  };

  const handleBulkScan = async () => {
    if (urls.length === 0) {
      setError('Please add URLs to scan');
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);
    setProgress(0);

    try {
      const formattedUrls = urls.map(formatUrl);
      const response = await api.post('/api/predict/bulk', { urls: formattedUrls });
      
      setResults(response.data.results);
      setProgress(100);

      // Notify parent component if callback provided
      if (onScanComplete) {
        onScanComplete(response.data.results);
      }
    } catch (err) {
      console.error('Bulk scan error:', err);
      setError(err.response?.data?.error || 'Failed to scan URLs');
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setUrls([]);
    setResults([]);
    setError('');
    setProgress(0);
    if (fileInputRef.current) fileInputRef.current.value = '';
    if (textAreaRef.current) textAreaRef.current.value = '';
  };

  const exportResults = () => {
    if (results.length === 0) return;

    const csvContent = [
      ['URL', 'Result', 'Confidence', 'Status'],
      ...results.map(result => [
        result.url,
        result.is_phishing ? 'Phishing' : 'Safe',
        `${(result.confidence * 100).toFixed(1)}%`,
        result.error ? 'Error' : 'Success'
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', `bulk-scan-results-${Date.now()}.csv`);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold cyberpunk-text flex items-center gap-2">
          <Upload size={28} />
          Bulk URL Scanner
        </h2>
      </div>

      {/* Input Methods */}
      <div className="cyberpunk-card p-6 rounded-lg space-y-4">
        <div>
          <h3 className="text-lg font-semibold cyberpunk-text mb-2">Upload File</h3>
          <p className="text-sm text-muted-foreground mb-3">
            Upload a CSV or TXT file containing URLs (one per line)
          </p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.txt"
            onChange={handleFileUpload}
            className="cyberpunk-input w-full px-4 py-2 rounded"
          />
        </div>

        <div className="flex items-center gap-4">
          <div className="flex-1 border-t border-accent/20"></div>
          <span className="text-sm text-muted-foreground">OR</span>
          <div className="flex-1 border-t border-accent/20"></div>
        </div>

        <div>
          <h3 className="text-lg font-semibold cyberpunk-text mb-2">Paste URLs</h3>
          <p className="text-sm text-muted-foreground mb-3">
            Enter URLs manually (one per line)
          </p>
          <textarea
            ref={textAreaRef}
            onChange={handleTextInput}
            placeholder="example.com&#10;another-site.com&#10;test-website.net"
            rows={6}
            className="cyberpunk-input w-full px-4 py-2 rounded font-mono text-sm"
          />
        </div>

        {urls.length > 0 && (
          <div className="bg-accent/10 border border-accent/30 rounded p-3">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">
                {urls.length} URL{urls.length !== 1 ? 's' : ''} ready to scan
              </span>
              <button
                onClick={clearAll}
                className="text-destructive hover:text-destructive/80 flex items-center gap-1 text-sm"
              >
                <X size={16} />
                Clear
              </button>
            </div>
          </div>
        )}

        {error && (
          <div className="bg-destructive/10 text-destructive p-3 rounded flex items-center gap-2">
            <AlertTriangle size={18} />
            {error}
          </div>
        )}

        <div className="flex gap-4">
          <button
            onClick={handleBulkScan}
            disabled={loading || urls.length === 0}
            className="cyberpunk-button flex-1 px-6 py-3 rounded disabled:opacity-50 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Scanning... {progress}%
              </>
            ) : (
              <>
                <Upload size={18} />
                Scan {urls.length} URL{urls.length !== 1 ? 's' : ''}
              </>
            )}
          </button>
        </div>
      </div>

      {/* Results */}
      {results.length > 0 && (
        <div className="cyberpunk-card p-6 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xl font-semibold cyberpunk-text">Scan Results</h3>
            <button
              onClick={exportResults}
              className="cyberpunk-button px-4 py-2 rounded flex items-center gap-2"
            >
              <Download size={18} />
              Export Results
            </button>
          </div>

          {/* Summary */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-accent/10 border border-accent/30 rounded p-4">
              <p className="text-sm text-muted-foreground">Total Scanned</p>
              <p className="text-2xl font-bold cyberpunk-text mt-1">{results.length}</p>
            </div>
            <div className="bg-[#34c759]/10 border border-[#34c759]/30 rounded p-4">
              <p className="text-sm text-muted-foreground">Safe URLs</p>
              <p className="text-2xl font-bold text-[#34c759] mt-1">
                {results.filter(r => !r.is_phishing && !r.error).length}
              </p>
            </div>
            <div className="bg-destructive/10 border border-destructive/30 rounded p-4">
              <p className="text-sm text-muted-foreground">Phishing Detected</p>
              <p className="text-2xl font-bold text-destructive mt-1">
                {results.filter(r => r.is_phishing && !r.error).length}
              </p>
            </div>
          </div>

          {/* Detailed Results */}
          <div className="space-y-3 max-h-96 overflow-y-auto">
            {results.map((result, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-black/20 rounded border border-accent/20"
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-mono text-accent truncate">{result.url}</p>
                  {result.error && (
                    <p className="text-xs text-destructive mt-1">{result.error}</p>
                  )}
                </div>
                {!result.error && (
                  <div
                    className={`flex items-center gap-2 px-3 py-1 rounded ml-4 ${
                      result.is_phishing
                        ? 'bg-destructive/10 text-destructive'
                        : 'bg-[#34c759]/10 text-[#34c759]'
                    }`}
                  >
                    {result.is_phishing ? (
                      <AlertTriangle size={16} />
                    ) : (
                      <CheckCircle2 size={16} />
                    )}
                    <span className="text-sm font-medium">
                      {result.is_phishing ? 'Phishing' : 'Safe'}
                    </span>
                    <span className="text-sm font-mono">
                      {(result.confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default BulkScanner;
