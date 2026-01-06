import React, { useState } from 'react';
import OriginalLayout from '@theme-original/Layout';
import RagChatbot from '@site/src/components/RagChatbot/RagChatbot';
import { useLocation } from '@docusaurus/router';

export default function Layout(props) {
  const { pathname } = useLocation();
  const isDocsPage = pathname.startsWith('/docs');
  const isBlogPage = pathname.startsWith('/blog');
  const isHomePage = pathname === '/';

  // Show chatbot on docs, blog, and other pages, but not on homepage
  const showChatbot = !isHomePage;

  const [isChatbotOpen, setIsChatbotOpen] = useState(false);

  return (
    <>
      <OriginalLayout {...props}>
        {props.children}
        {showChatbot && (
          <>
            <button
              onClick={() => setIsChatbotOpen(!isChatbotOpen)}
              style={{
                position: 'fixed',
                bottom: isChatbotOpen ? '520px' : '20px',
                right: '20px',
                zIndex: 1000,
                padding: '10px 15px',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '50px',
                cursor: 'pointer',
                fontSize: '16px',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
              }}
            >
              {isChatbotOpen ? '×' : '?'}
            </button>
            {isChatbotOpen && (
              <div style={{
                position: 'fixed',
                bottom: '20px',
                right: '20px',
                zIndex: 1000,
                width: '400px',
                maxHeight: '500px',
                backgroundColor: 'white',
                border: '1px solid #ddd',
                borderRadius: '8px',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
                overflow: 'hidden'
              }}>
                <div style={{
                  padding: '10px',
                  backgroundColor: '#f8f9fa',
                  borderBottom: '1px solid #ddd',
                  fontWeight: 'bold',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <span>RAG Chatbot</span>
                  <button
                    onClick={() => setIsChatbotOpen(false)}
                    style={{
                      background: 'none',
                      border: 'none',
                      fontSize: '18px',
                      cursor: 'pointer',
                      color: '#666'
                    }}
                  >
                    ×
                  </button>
                </div>
                <div style={{ padding: '10px', maxHeight: '400px', overflowY: 'auto' }}>
                  <RagChatbot />
                </div>
              </div>
            )}
          </>
        )}
      </OriginalLayout>
    </>
  );
}