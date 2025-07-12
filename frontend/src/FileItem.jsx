import React from 'react';

function FileItem({ item, onOpenFolder }) {
    if (item.type === 'folder') {
        return (
            <div style={{ cursor: 'pointer' }} onClick={onOpenFolder}>
                📁 {item.name}
            </div>
        );
    }
    return (
        <div>
            📹 {item.name}
            {' '}
            <a href={item.url} target="_blank" rel="noreferrer">View</a>
            {' '}
            <a href={item.url} download>Download</a>
        </div>
    );
}

export default FileItem;
