import nodemailer from 'nodemailer';
import type { APIContext } from "astro";

import { upload } from "./utils/file.ts";
import * as fs from "fs";

export async function POST({request}: APIContext) {
    try {
        const transporter = nodemailer.createTransport({
            host: 'smtp.gmail.com',
            port: 587,
            secure: false,
            auth: {
                user: 'cocostarcandrei84@gmail.com',
                pass: 'wxxo mbqa nims qbqo'
            }
        })

        const data = await request.formData();

        const destinationEmail = data.get('destinationEmail');
        const subject = data.get('subject');
        const file = data.get('fileBinaries');

        if (!(file instanceof File)) {
            throw new Error('Not file type');
        }

        const filePath = `uploads/${file.name}`;

        const arrayBuffer = await file.arrayBuffer();
        const buffer = Buffer.from(arrayBuffer);

        if (!fs.existsSync('uploads')){
            fs.mkdirSync('uploads');
        }

        fs.writeFileSync(filePath, buffer);

        await upload(filePath, file.name);

        fs.unlink(filePath, (err) => {
            if (err) console.error('Error deleting file:', err);
        });

        const downloadLink = `http://localhost:4321/file/${file.name}`;

        const mailOptions = {
            from: 'cocostarcandrei84@gmail.com',
            to: destinationEmail,
            subject,
            html: `<a href="${downloadLink}" download="${file.name}">Download ${file.name}</a>`,
            attachments: [
                {
                    filename: file.name,
                    content: buffer
                }

            ]
        }

        transporter.sendMail(mailOptions, (error, info) => {
            if (error) {
                console.error(error);
            }
            return new Response({
                status: 204,
                headers: {
                    "Content-Type": "application/json"
                }
            })
        })

        return new Response(JSON.stringify({}), {
            status: 200,
            headers: {
                "Content-Type": "application/json"
            }
        });
    } catch (e) {
        console.error(e)
    }
}
