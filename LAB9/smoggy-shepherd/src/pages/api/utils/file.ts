import * as ftp from 'basic-ftp';
import { Writable } from 'stream';

export const upload = async(filePath, fileName) => {
    const client = new ftp.Client();
    client.ftp.verbose = true;
    try {
        await client.access({
            host: "138.68.98.108",
            user: "yourusername",
            password: "yourusername",
        })
        await client.uploadFrom(filePath, fileName);

    } catch (e) {
        console.error("FTP Error:", e);
    } finally {
        client.close();
    }
}

export const download = async(fileName) => {
    const client = new ftp.Client();
    client.ftp.verbose = true;

    try {
        await client.access({
            host: "138.68.98.108",
            user: "yourusername",
            password: "yourusername",
        });

        const chunks = [];
        const writableStream = new Writable({
            write(chunk, encoding, callback) {
                chunks.push(chunk);
                callback();
            }
        });

        await client.downloadTo(writableStream, fileName);

        const buffer = Buffer.concat(chunks);
        console.log(buffer.toString('base64'));
        return buffer.toString('base64');

    } catch (error) {
        console.error("FTP operation failed: ", error);
        throw error;
    } finally {
        client.close();
    }
}
