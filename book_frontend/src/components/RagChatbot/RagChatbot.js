import React, { useState, useRef } from 'react';
import ragAPIService from '../../services/api.js';

// CSS styles for the component
const styles = {
  container: {
    maxWidth: '800px',
    margin: '20px auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  inputContainer: {
    display: 'flex',
    marginBottom: '20px',
  },
  input: {
    flex: 1,
    padding: '10px',
    fontSize: '16px',
    border: '1px solid #ccc',
    borderRadius: '4px 0 0 4px',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '0 4px 4px 0',
    cursor: 'pointer',
  },
  buttonDisabled: {
    backgroundColor: '#ccc',
    cursor: 'not-allowed',
  },
  responseContainer: {
    marginTop: '20px',
    padding: '15px',
    backgroundColor: '#f8f9fa',
    borderRadius: '4px',
    border: '1px solid #dee2e6',
  },
  sources: {
    marginTop: '15px',
    fontSize: '14px',
  },
  sourceItem: {
    marginBottom: '8px',
    padding: '8px',
    backgroundColor: 'white',
    borderRadius: '3px',
    border: '1px solid #e9ecef',
  },
  loading: {
    color: '#6c757d',
    fontStyle: 'italic',
  },
  error: {
    color: '#dc3545',
    backgroundColor: '#f8d7da',
    borderColor: '#f5c6cb',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid',
    marginTop: '10px'
  },
  apiError: {
    color: '#856404',
    backgroundColor: '#fff3cd',
    borderColor: '#ffeaa7',
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid',
    marginTop: '10px'
  }
};

const RagChatbot = () => {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!query.trim()) return;

    setIsLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Call the API service to query the RAG system
      const result = await ragAPIService.queryRAG(query.trim());
      setResponse(result);
    } catch (err) {
      // Provide more specific error messages based on the error type
      if (err.message && err.message.includes('NetworkError')) {
        setError('Network error: Unable to connect to the RAG system. Please check your connection and try again.');
      } else if (err.message && err.message.includes('400')) {
        setError('Invalid request: Please check your query and try again.');
      } else if (err.message && err.message.includes('500')) {
        setError('Server error: The RAG system encountered an error. Please check the server configuration.');
      } else {
        setError('Failed to get response from RAG system. Please check that the backend is running and environment variables are configured.');
      }
      console.error('Error querying RAG system:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div style={styles.container}>
      <h3>Ask about the Documentation</h3>
      <form style={styles.inputContainer} onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the documentation..."
          style={styles.input}
          disabled={isLoading}
        />
        <button
          type="submit"
          style={{
            ...styles.button,
            ...(isLoading ? styles.buttonDisabled : {})
          }}
          disabled={isLoading}
        >
          {isLoading ? 'Asking...' : 'Ask'}
        </button>
      </form>

      {isLoading && (
        <div style={styles.loading}>Processing your query...</div>
      )}

      {error && (
        <div style={styles.error}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {response && !isLoading && (
        <div style={styles.responseContainer}>
          <h4>Response:</h4>
          <div>{response.answer}</div>

          {response.sources && response.sources.length > 0 && (
            <div style={styles.sources}>
              <h5>Sources:</h5>
              {response.sources.map((source, index) => (
                <div key={index} style={styles.sourceItem}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div style={{ flex: 1 }}>
                      <strong>{source.title || 'Untitled Source'}</strong>
                      {source.url && (
                        <div>
                          <a href={source.url} target="_blank" rel="noopener noreferrer" style={{ color: '#007bff', textDecoration: 'none' }}>
                            {source.url}
                          </a>
                        </div>
                      )}
                      {source.snippet && (
                        <div style={{ marginTop: '8px', fontStyle: 'italic', fontSize: '14px', color: '#555' }}>
                          "{source.snippet}"
                        </div>
                      )}
                    </div>
                    {source.page_number && (
                      <div style={{
                        marginLeft: '10px',
                        fontSize: '12px',
                        backgroundColor: '#e9ecef',
                        padding: '4px 8px',
                        borderRadius: '3px',
                        alignSelf: 'flex-start'
                      }}>
                        Page: {source.page_number}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
          {response.sources && response.sources.length === 0 && (
            <div style={{ fontSize: '14px', color: '#6c757d', fontStyle: 'italic' }}>
              No specific sources referenced in this response.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default RagChatbot;