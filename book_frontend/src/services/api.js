// Frontend API service for communicating with the RAG backend
class RAGAPIService {
  constructor(baseURL = 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  // Method to query the RAG system
  async queryRAG(query, userId = null, context = {}) {
    try {
      const response = await fetch(`${this.baseURL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          user_id: userId,
          context,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error querying RAG system:', error);
      // Re-throw with more context
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('NetworkError: Unable to connect to the RAG API. Please ensure the backend server is running on http://localhost:8000');
      }
      throw error;
    }
  }

  // Method to test API connectivity
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseURL}/`);
      return response.ok;
    } catch (error) {
      console.error('API health check failed:', error);
      return false;
    }
  }
}

// Export a singleton instance
const ragAPIService = new RAGAPIService();
export default ragAPIService;

// For CommonJS compatibility (if needed)
// module.exports = ragAPIService;