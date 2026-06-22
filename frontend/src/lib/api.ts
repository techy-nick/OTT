const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getVideos() {
  const response = await fetch(
    `${API_URL}/videos`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to load videos");
  }

  return response.json();
}

export async function getVideo(id: number) {
  const response = await fetch(
    `${API_URL}/videos/${id}`,
    {
      cache: "no-store",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to load video");
  }

  return response.json();
}
