import React, { useState } from 'react';
import axios from 'axios';

export default function UploadForm({ setData }) {
  const [file, setFile] = useState(null);
  const [topics, setTopics] = useState("");

  const upload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("topics", topics);
    const res = await axios.post("http://localhost:8000/upload/", formData);
    setData(res.data);
  };

  return (
    <div>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <input type="text" placeholder="e.g., AI, Biology" onChange={e => setTopics(e.target.value)} />
      <button onClick={upload}>Upload & Process</button>
    </div>
  );
}
