import React, { useState, useEffect } from 'react';
import axios from 'axios';
import FileItem from './FileItem';
import UploadDialog from './UploadDialog';

function FileManager({ currentPath, setPath }) {
    const [items, setItems] = useState([]);
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        axios.get(`/api/list?path=${currentPath}`,).then(res => {
            setItems(res.data);
        });
    }, [currentPath, refresh]);

    const goBack = () => {
        const parts = currentPath.split('/');
        parts.pop();
        setPath(parts.join('/'));
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <button onClick={goBack} disabled={!currentPath}>⬅ Back</button>
                <UploadDialog path={currentPath} onComplete={() => setRefresh(!refresh)} />
            </div>
            <div>
                {items.map(item => (
                    <FileItem
                        key={item.name}
                        item={item}
                        onOpenFolder={() => setPath(`${currentPath}/${item.name}`.replace(/^\/+/, ''))}
                    />
                ))}
            </div>
        </div>
    );
}

export default FileManager;
