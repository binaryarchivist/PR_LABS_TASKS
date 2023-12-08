import React, { useState, useEffect } from 'react';

export const FileDownloader = ({ fileName }) => {
    const [isDownloading, setIsDownloading] = useState<boolean>(false);

    useEffect(() => {
        const fetchFile = async () => {
            try {
                const response = await fetch(`http://localhost:4321/api/files/${fileName}`, {
                    method: 'GET'
                });

                const base64Content = await response.text();
                setIsDownloading(true);

                const link = document.createElement('a');
                link.href = 'data:application/octet-stream;base64,' + base64Content;
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                setIsDownloading(false);
            } catch (error) {
                console.error(error);
            }
        };

        fetchFile();
    }, [fileName]);

    return (
        <div className="card" style={cardStyle}>
            <div className="card-body">
                <h1 className="card-title" style={titleStyle}>Downloading File: {fileName}</h1>
                {isDownloading &&
                    <p style={downloadingTextStyle}>Downloading file...</p>
                }
            </div>
        </div>
    );
};

const cardStyle = {
    maxWidth: '500px',
    width: '100%',
    margin: '20px',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#ffffff'
};

const titleStyle = {
    color: '#005f73',
    textAlign: 'center'
};

const downloadingTextStyle = {
    color: '#0077b6',
    textAlign: 'center'
};
