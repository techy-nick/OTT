const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getVideos() {
  const res = await fetch(`${API_URL}/videos`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch videos");
  }

  return res.json();
}
