import React, { useState } from 'react';
import UploadForm from './UploadForm';
import FileList from './FileList';

function App() {
    const [refresh, setRefresh] = useState(false);
    const [directory, setDirectory] = useState('');

    return (
        <div>
            <h1>Mann Cloud Storage</h1>
            <UploadForm onUpload={() => setRefresh(!refresh)} />
            <input
                type="text"
                placeholder="Filter by directory"
                onChange={(e) => setDirectory(e.target.value)}
            />
            <FileList directory={directory} key={refresh} />
        </div>
    );
}

export default App;
