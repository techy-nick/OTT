"use client";

import { useState } from "react";

export default function UploadPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] =
    useState("");
  const [file, setFile] = useState<File | null>(
    null
  );

  const handleUpload = async () => {
    if (!file) {
      alert("Select a file");
      return;
    }

    const token =
      localStorage.getItem("token");

    const formData = new FormData();

    formData.append("title", title);
    formData.append(
      "description",
      description
    );
    formData.append("file", file);

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/videos/upload`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      }
    );

    if (response.ok) {
      alert("Upload Successful");
      setTitle("");
      setDescription("");
    } else {
      const error =
        await response.text();

      alert(error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Upload Video</h1>

      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) =>
          setTitle(e.target.value)
        }
      />

      <br />
      <br />

      <textarea
        placeholder="Description"
        value={description}
        onChange={(e) =>
          setDescription(e.target.value)
        }
      />

      <br />
      <br />

      <input
        type="file"
        accept="video/*"
        onChange={(e) =>
          setFile(
            e.target.files?.[0] || null
          )
        }
      />

      <br />
      <br />

      <button onClick={handleUpload}>
        Upload
      </button>
    </div>
  );
}
