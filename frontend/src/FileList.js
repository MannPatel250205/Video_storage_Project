import React, { useEffect, useState } from 'react';
import axios from 'axios';

function FileList({ directory }) {
    const [files, setFiles] = useState([]);

    useEffect(() => {
        axios.get(`/api/list-files?directory=${directory || ''}`).then(res => {
            setFiles(res.data);
        });
    }, [directory]);

    return (
        <div>
            <h3>Files</h3>
            <ul>
                {files.map(f => (
                    <li key={f.name}>
                        {f.name}
                        {' '}
                        <a href={f.url} target="_blank" rel="noreferrer">View</a>
                        {' '}
                        <a href={f.url} download>Download</a>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default FileList;
