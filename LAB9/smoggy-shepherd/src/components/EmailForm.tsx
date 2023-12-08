import React, {FC, FormEvent, useCallback} from 'react';

export const EmailForm: FC = () => {
    const handleOnSubmit = useCallback(async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        const formData = new FormData(event.target);
        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }

        try {
            const response = await fetch('api/sendEmail', {
                method: 'POST',
                body: formData,
            });
            console.info(response);
            alert('Email Sent!');

        } catch (e) {
            console.error(e);
        }
    }, []);

    return (
        <form onSubmit={handleOnSubmit} encType="multipart/form-data">
            <div className="mb-3">
                <label htmlFor="destinationEmail" className="form-label" style={{color: '#0077b6'}}>Destination
                    Email</label>
                <input type="email" className="form-control" id="destinationEmail" name="destinationEmail" required/>
            </div>
            <div className="mb-3">
                <label htmlFor="subject" className="form-label" style={{color: '#0077b6'}}>Subject</label>
                <input type="text" className="form-control" id="subject" name="subject" required/>
            </div>
            <div className="mb-3">
                <label htmlFor="fileUpload" className="form-label" style={{color: '#0077b6'}}>File Upload</label>
                <input type="file" className="form-control" id="fileBinaries" name="fileBinaries"/>
            </div>
            <div style={{textAlign: 'center'}}>
                <button
                    type="submit"
                    className="btn"
                    style={{backgroundColor: '#2a9d8f', border: 'none', color: 'white'}}
                >
                    Send Email
                </button>
            </div>
        </form>
    );
};
