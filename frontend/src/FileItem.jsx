import React from 'react';
import axios from 'axios';

function FileItem({ item, onOpenFolder, onDelete }) {
    const handleDelete = async () => {
        if (window.confirm(`Delete ${item.name}?`)) {
            try {
                await axios.post('/api/delete', { blob_name: item.fullPath });
                onDelete(); // trigger refresh
            } catch (err) {
                alert('Delete failed');
            }
        }
    };

    if (item.type === 'folder') {
        return (
            <div style={{ cursor: 'pointer', marginBottom: 8 }} onClick={onOpenFolder}>
                📁 <strong>{item.name}</strong>
            </div>
        );
    }

    return (
        <div style={{ marginBottom: 8 }}>
            📹 {item.name}{' '}
            <a href={item.url} target="_blank" rel="noreferrer">View</a>{' '}
            <a href={item.url} download>Download</a>{' '}
            <button onClick={handleDelete}>🗑️ Delete</button>
        </div>
    );
}

export default FileItem;
