import React, { useState } from 'react';
import axios from 'axios';

function UploadDialog({ path, onComplete }) {
    const [show, setShow] = useState(false);
    const [mode, setMode] = useState('upload');
    const [file, setFile] = useState(null);
    const [folderName, setFolderName] = useState('');

    const toggle = () => setShow(!show);

    const createFolder = async () => {
        if (!folderName) return;
        await axios.post('/api/create-folder', { path: `${path}/${folderName}` });
        toggle();
        onComplete();
    };

    const uploadFile = async () => {
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        formData.append('path', path);
        await axios.post('/api/upload', formData);
        toggle();
        onComplete();
    };

    return (
        <div>
            <button onClick={toggle}>➕</button>
            {show && (
                <div style={{ border: '1px solid black', padding: 10, marginTop: 10 }}>
                    <div>
                        <button onClick={() => setMode('upload')}>Upload File</button>
                        <button onClick={() => setMode('folder')}>Create Folder</button>
                    </div>
                    {mode === 'upload' ? (
                        <div>
                            <input type="file" onChange={e => setFile(e.target.files[0])} />
                            <button onClick={uploadFile}>Upload</button>
                        </div>
                    ) : (
                        <div>
                            <input type="text" placeholder="Folder name" onChange={e => setFolderName(e.target.value)} />
                            <button onClick={createFolder}>Create</button>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default UploadDialog;
