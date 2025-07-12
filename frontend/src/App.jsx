import React, { useState } from 'react';
import FileManager from './FileManager';

function App() {
    const [currentPath, setCurrentPath] = useState('');

    return (
        <div>
            <h1>📂 Azure Video Drive</h1>
            <FileManager currentPath={currentPath} setPath={setCurrentPath} />
        </div>
    );
}

export default App;
