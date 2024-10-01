import React, { useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import './App.css';

function App() {
  const [notes, setNotes] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(''); // Added error state

  const handleSubmit = () => {
    setLoading(true);
    fetch('http://127.0.0.1:8001/process/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/html',
      },
      body: JSON.stringify({ notes }),
    })
      .then((response) => response.text())
      .then((data) => {
        setResult(data); // data is the HTML string
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error:', error);
        setError('An error occurred while processing your notes.'); // Set error message
        setLoading(false);
      });
  };

  return (
    <div className="App">
      <h1>Notes Processor</h1>
      <textarea
        placeholder="Enter your notes here..."
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        style={{ width: '400px', height: '200px', padding: '10px', fontSize: '16px' }}
      />
      <br />
      <button onClick={handleSubmit} className="submit-button">
        Submit
      </button>

      <Dialog.Root open={loading}>
        <Dialog.Portal>
          <Dialog.Overlay className="DialogOverlay" />
          <Dialog.Content className="DialogContent">
            <Dialog.Title className="DialogTitle">Loading</Dialog.Title>
            <Dialog.Description className="DialogDescription">
              Please wait while we process your notes...
            </Dialog.Description>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      {result && (
        <div className="result" dangerouslySetInnerHTML={{ __html: result }} />
      )}

      {/* Error dialog */}
      <Dialog.Root open={!!error} onOpenChange={() => setError('')}>
        <Dialog.Portal>
          <Dialog.Overlay className="DialogOverlay" />
          <Dialog.Content className="DialogContent">
            <Dialog.Title className="DialogTitle">Error</Dialog.Title>
            <Dialog.Description className="DialogDescription">
              {error}
            </Dialog.Description>
            <button onClick={() => setError('')}>Close</button>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </div>
  );
}

export default App;
