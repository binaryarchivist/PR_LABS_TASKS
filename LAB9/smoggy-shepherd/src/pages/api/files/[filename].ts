import {download} from "../utils/file.ts";

export async function GET({params}) {
    const {filename} = params;

    try {
        const file = await download(filename);
        return new Response(file, {
            status: 200,
            headers: {
                'Content-Type': 'application/octet-stream',
                'Content-Disposition': `attachment; filename="${filename}"`,
            },
        });

    } catch (e) {
        return new Response(JSON.stringify({ message: "File not found or an error occurred." }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }
}
