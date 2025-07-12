import React, { useState } from 'react';
import axios from 'axios';

function UploadForm({ onUpload }) {
    const [file, setFile] = useState(null);
    const [directory, setDirectory] = useState('');

    const handleUpload = async () => {
        if (!file) return alert("Choose a file");

        const formData = new FormData();
        formData.append('file', file);
        formData.append('directory', directory);

        try {
            await axios.post('/api/upload', formData);
            onUpload();
        } catch (err) {
            alert("Upload failed");
        }
    };

    return (
        <div>
            <input type="text" placeholder="Directory (optional)" onChange={e => setDirectory(e.target.value)} />
            <input type="file" onChange={e => setFile(e.target.files[0])} />
            <button onClick={handleUpload}>Upload</button>
        </div>
    );
}

export default UploadForm;
