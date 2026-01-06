# Quickstart: RAG System Frontend Integration

## Prerequisites
- Python 3.11+
- Node.js 16+
- Docusaurus project set up in `book_frontend/`
- Existing RAG agent in `agent.py`

## Setup Instructions

### 1. Backend Setup
1. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

2. Create the FastAPI server in `api.py`:
   ```python
   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   import agent  # Import existing RAG agent

   app = FastAPI()

   class QueryRequest(BaseModel):
       query: str
       user_id: str = None
       context: dict = None

   @app.post("/query")
   async def query_endpoint(request: QueryRequest):
       try:
           # Call the RAG agent with the query
           response = agent.process_query(request.query, request.context)
           return response
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
   ```

3. Run the backend server:
   ```bash
   uvicorn api:app --reload --port 8000
   ```

### 2. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd book_frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Create a new chatbot component in `src/components/RagChatbot/RagChatbot.js`:
   ```javascript
   import React, { useState } from 'react';
   import './RagChatbot.css';

   const RagChatbot = () => {
     const [query, setQuery] = useState('');
     const [response, setResponse] = useState('');
     const [isLoading, setIsLoading] = useState(false);

     const handleSubmit = async (e) => {
       e.preventDefault();
       setIsLoading(true);

       try {
         const result = await fetch('http://localhost:8000/query', {
           method: 'POST',
           headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ query })
         });

         const data = await result.json();
         setResponse(data.answer);
       } catch (error) {
         setResponse('Error: Could not process query');
       } finally {
         setIsLoading(false);
       }
     };

     return (
       <div className="rag-chatbot">
         <form onSubmit={handleSubmit}>
           <input
             type="text"
             value={query}
             onChange={(e) => setQuery(e.target.value)}
             placeholder="Ask a question about the documentation..."
           />
           <button type="submit" disabled={isLoading}>
             {isLoading ? 'Loading...' : 'Ask'}
           </button>
         </form>
         {response && <div className="response">{response}</div>}
       </div>
     );
   };

   export default RagChatbot;
   ```

### 3. Integration
1. Add the chatbot component to your Docusaurus pages
2. Configure CORS settings in FastAPI if needed
3. Test the integration by submitting queries through the frontend

## Testing
Run the backend tests:
```bash
pytest tests/
```

Run the frontend tests:
```bash
cd book_frontend && npm test
```

## Next Steps
- Implement proper error handling
- Add rate limiting
- Set up logging
- Deploy to production