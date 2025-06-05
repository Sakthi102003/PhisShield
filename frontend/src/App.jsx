import axios from 'axios'
import jsPDF from 'jspdf'
import { AlertTriangle, CheckCircle2, Download, Globe, LogOut, Shield } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import Auth from './components/Auth'
import History from './components/History'

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [user, setUser] = useState(null)
  const [showHistory, setShowHistory] = useState(false)
  const [urlInfo, setUrlInfo] = useState(null)
  const [loadingInfo, setLoadingInfo] = useState(false)

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token')
    const username = localStorage.getItem('username')
    if (token && username) {
      setUser({ token, username })
    }
  }, [])

  const handleLogin = (userData) => {
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    setUser(null)
    setShowHistory(false)
  }

  // Debounce function to limit API calls
  const debounce = (func, wait) => {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func(...args), wait);
    };
  };

  // URL validation and formatting function
  const formatAndValidateUrl = (input) => {
    if (!input) return null;
    
    // Remove leading/trailing whitespace and common prefixes
    let formattedUrl = input.trim()
      .replace(/^(?:https?:\/\/)?(?:www\.)?/i, '');
    
    // Add https:// if missing
    formattedUrl = 'https://' + formattedUrl;
    
    try {
      const url = new URL(formattedUrl);
      // Basic domain validation
      return url.hostname.includes('.') ? formattedUrl : null;
    } catch (e) {
      return null;
    }
  };

  // Debounced URL info fetcher
  const debouncedFetchUrlInfo = useCallback(
    debounce(async (inputUrl, token) => {
      if (!inputUrl) return;

      const formattedUrl = formatAndValidateUrl(inputUrl);
      if (!formattedUrl) return;

      setLoadingInfo(true);
      setUrlInfo(null);
      
      try {
        const response = await axios.get(`http://localhost:5000/api/url-info`, {
          params: { url: formattedUrl },
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        setUrlInfo(response.data);
      } catch (err) {
        console.error('Error fetching URL info:', err);
        // Set minimal URL info with error
        setUrlInfo({
          domain: new URL(formattedUrl).hostname,
          error: 'Could not fetch website information',
          title: null,
          description: null,
          type: null
        });
      } finally {
        setLoadingInfo(false);
      }
    }, 500),
    []
  );

  const handleUrlChange = (e) => {
    const newUrl = e.target.value;
    setUrl(newUrl);
    
    if (newUrl && user?.token) {
      debouncedFetchUrlInfo(newUrl, user.token);
    } else {
      setUrlInfo(null);
    }
  };

  const handleCheck = async () => {
    const formattedUrl = formatAndValidateUrl(url);
    if (!formattedUrl) {
      setError('Please enter a valid website address');
      return;
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('http://localhost:5000/api/predict', 
        { url: formattedUrl },
        {
          headers: {
            'Authorization': `Bearer ${user.token}`
          }
        }
      )
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const generatePDF = () => {
    if (!result) return

    const doc = new jsPDF()
    const pageWidth = doc.internal.pageSize.getWidth()
    
    // Title
    doc.setFontSize(20)
    doc.setTextColor(0, 120, 255)
    doc.text('PhishShield Analysis Report', pageWidth / 2, 20, { align: 'center' })
    
    // URL
    doc.setFontSize(12)
    doc.setTextColor(0, 0, 0)
    doc.text('Analyzed URL:', 20, 40)
    doc.setTextColor(0, 120, 255)
    doc.text(url, 20, 50)
    
    // Result
    doc.setTextColor(0, 0, 0)
    doc.text('Analysis Result:', 20, 70)
    doc.setTextColor(result.is_phishing ? '#ff3b30' : '#34c759')
    doc.text(
      result.is_phishing ? 'Potential Phishing Site Detected' : 'Legitimate Website',
      20,
      80
    )
    
    // Confidence
    doc.setTextColor(0, 0, 0)
    doc.text('Confidence:', 20, 100)
    doc.setTextColor(0, 120, 255)
    doc.text(`${(result.confidence * 100).toFixed(1)}%`, 20, 110)
    
    // Features
    doc.setTextColor(0, 0, 0)
    doc.text('URL Analysis Details:', 20, 130)
    
    let yPosition = 140
    Object.entries(result.features).forEach(([key, value]) => {
      const featureName = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
      doc.setTextColor(0, 180, 216)
      doc.text(`${featureName}:`, 20, yPosition)
      doc.setTextColor(0, 120, 255)
      doc.text(String(value), 20, yPosition + 10)
      yPosition += 20
    })
    
    // Footer
    doc.setFontSize(10)
    doc.setTextColor(100, 100, 100)
    doc.text(
      `Generated by PhishShield on ${new Date().toLocaleString()}`,
      pageWidth / 2,
      doc.internal.pageSize.getHeight() - 10,
      { align: 'center' }
    )
    
    // Save the PDF
    doc.save(`phishshield-report-${new Date().getTime()}.pdf`)
  }

  const exportHistory = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/history', {
        headers: {
          'Authorization': `Bearer ${user.token}`
        }
      });
      
      const rows = [
        ['PhishShield History Export'],
        ['Generated on:', new Date().toLocaleString()],
        [''],
        ['URL', 'Result', 'Confidence', 'Date Checked']
      ];

      response.data.forEach(item => {
        rows.push([
          item.url,
          item.is_phishing ? 'Potential Phishing' : 'Legitimate',
          `${(item.confidence * 100).toFixed(1)}%`,
          new Date(item.checked_at).toLocaleString()
        ]);
      });

      const csvContent = rows.map(row => row.join(',')).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('hidden', '');
      a.setAttribute('href', url);
      a.setAttribute('download', `phishshield-history-${Date.now()}.csv`);
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (err) {
      setError('Failed to export history');
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground">
      {!user ? (
        <Auth onLogin={handleLogin} />
      ) : (
        <div className="container mx-auto px-4 py-8">
          <div className="flex justify-between items-center mb-8">
            <h1 
              onClick={() => {
                setUrl('');
                setResult(null);
                setError(null);
                setUrlInfo(null);
                setShowHistory(false);
              }} 
              className="text-3xl font-bold cyberpunk-text cursor-pointer hover:text-accent transition-colors"
            >
              PhishShield
            </h1>
            <div className="flex gap-4">
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="cyberpunk-button px-4 py-2 rounded"
              >
                {showHistory ? 'Back to Scanner' : 'View History'}
              </button>
              <button
                onClick={handleLogout}
                className="cyberpunk-button px-4 py-2 rounded flex items-center gap-2"
              >
                <LogOut size={18} /> Logout
              </button>
            </div>
          </div>

          {showHistory ? (
            <History token={user.token} />
          ) : (
            <div className="cyberpunk-card rounded-lg p-6 max-w-2xl mx-auto">
              <div className="space-y-4">
                <div className="flex gap-4">
                  <div className="flex-1 relative">
                    <input
                      type="text"
                      value={url}
                      onChange={handleUrlChange}
                      placeholder="Enter website (e.g., example.com)"
                      className={`cyberpunk-input w-full px-4 py-2 rounded ${
                        url && !formatAndValidateUrl(url) ? 'border-destructive' : ''
                      }`}
                    />
                    {url && !formatAndValidateUrl(url) && (
                      <div className="absolute text-xs text-destructive mt-1">
                        Please enter a valid website address
                      </div>
                    )}
                  </div>
                  <button
                    onClick={handleCheck}
                    disabled={loading || !url || !formatAndValidateUrl(url)}
                    className="cyberpunk-button px-6 py-2 rounded disabled:opacity-50"
                  >
                    {loading ? 'Analyzing...' : 'Check URL'}
                  </button>
                </div>

                {loadingInfo && (
                  <div className="text-accent text-sm flex items-center gap-2 mt-2">
                    <Globe className="animate-spin" size={16} />
                    Fetching website information...
                  </div>
                )}

                {urlInfo && (
                  <div className="cyberpunk-border bg-black/20 p-3 rounded space-y-2">
                    <div className="flex items-center gap-2 text-accent">
                      <Globe size={16} />
                      <span className="font-semibold">URL Information</span>
                    </div>
                    <div className="grid gap-2">
                      {urlInfo.error ? (
                        <div className="text-sm text-destructive">
                          {urlInfo.error}
                        </div>
                      ) : null}
                      
                      {/* Always show domain */}
                      <div className="text-sm flex items-center gap-2">
                        <span className="text-muted-foreground min-w-[80px]">Domain:</span>
                        <span className="text-foreground font-mono">{urlInfo.domain || 'Unknown'}</span>
                      </div>

                      {/* Show status if available */}
                      {urlInfo.status && (
                        <div className="text-sm flex items-center gap-2">
                          <span className="text-muted-foreground min-w-[80px]">Status:</span>
                          <span className={`font-mono ${
                            urlInfo.status >= 200 && urlInfo.status < 300 
                              ? 'text-[#34c759]' 
                              : 'text-destructive'
                          }`}>
                            {urlInfo.status}
                          </span>
                        </div>
                      )}

                      {/* Title with proper wrapping */}
                      <div className="text-sm flex gap-2">
                        <span className="text-muted-foreground min-w-[80px]">Title:</span>
                        <span className="text-foreground break-words">
                          {urlInfo.title || 'No title available'}
                        </span>
                      </div>

                      {/* Description with proper wrapping */}
                      {urlInfo.description && (
                        <div className="text-sm flex gap-2">
                          <span className="text-muted-foreground min-w-[80px]">Description:</span>
                          <span className="text-foreground break-words">
                            {urlInfo.description}
                          </span>
                        </div>
                      )}

                      {/* Content type */}
                      <div className="text-sm flex items-center gap-2">
                        <span className="text-muted-foreground min-w-[80px]">Type:</span>
                        <span className="text-foreground font-mono">
                          {urlInfo.type || 'Unknown'}
                        </span>
                      </div>
                    </div>
                  </div>
                )}

                {error && (
                  <div className="bg-destructive/10 text-destructive p-4 rounded flex items-center gap-2">
                    <AlertTriangle size={18} />
                    {error}
                  </div>
                )}

                {result && (
                  <div className="space-y-4">
                    <div className={`p-4 rounded flex items-center gap-2 ${
                      result.is_phishing 
                        ? 'bg-destructive/10 text-destructive' 
                        : 'bg-[#34c759]/10 text-[#34c759]'
                    }`}>
                      {result.is_phishing ? (
                        <AlertTriangle size={18} />
                      ) : (
                        <CheckCircle2 size={18} />
                      )}
                      <span className="font-semibold">
                        {result.is_phishing
                          ? 'Potential Phishing Site Detected'
                          : 'Legitimate Website'}
                      </span>
                      <span className="ml-auto">
                        Confidence: {(result.confidence * 100).toFixed(1)}%
                      </span>
                    </div>

                    <div className="space-y-2">
                      <h3 className="text-lg font-semibold cyberpunk-text">URL Analysis Details</h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {Object.entries(result.features).map(([key, value]) => (
                          <div key={key} className="cyberpunk-border bg-black/20 p-3 rounded">
                            <div className="text-sm text-secondary-foreground">
                              {key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                            </div>
                            <div className="mt-1 font-mono text-accent">
                              {typeof value === 'boolean' ? (value ? 'Yes' : 'No') : value}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <button
                      onClick={generatePDF}
                      className="cyberpunk-button px-4 py-2 rounded flex items-center gap-2 w-full justify-center"
                    >
                      <Download size={18} />
                      Download Report
                    </button>
                  </div>
                )}

                {showHistory && (
                  <div className="mt-4 flex justify-end">
                    <button
                      onClick={exportHistory}
                      className="cyberpunk-button px-4 py-2 rounded flex items-center gap-2"
                    >
                      <Download size={18} />
                      Export History
                    </button>
                  </div>
                )}

                {urlInfo && !urlInfo.error && (
                  <div className="mt-4 cyberpunk-border bg-black/20 p-3 rounded">
                    <div className="flex items-center gap-2 text-accent mb-2">
                      <Shield size={16} />
                      <span className="font-semibold">Security Information</span>
                    </div>
                    <div className="grid gap-2">
                      <div className="text-sm flex items-center gap-2">
                        <span className="text-muted-foreground min-w-[100px]">HTTPS:</span>
                        <span className={`font-mono ${
                          url.startsWith('https://') ? 'text-[#34c759]' : 'text-destructive'
                        }`}>
                          {url.startsWith('https://') ? 'Secure' : 'Not Secure'}
                        </span>
                      </div>
                      {urlInfo.status && (
                        <div className="text-sm flex items-center gap-2">
                          <span className="text-muted-foreground min-w-[100px]">Connection:</span>
                          <span className={`font-mono ${
                            urlInfo.status >= 200 && urlInfo.status < 400 
                              ? 'text-[#34c759]' 
                              : 'text-destructive'
                          }`}>
                            {urlInfo.status >= 200 && urlInfo.status < 400 ? 'Successful' : 'Failed'}
                            {' '}(Status: {urlInfo.status})
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App