import Link from "next/link";

async function getVideos() {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/videos`,
    {
      cache: "no-store",
    }
  );

  return response.json();
}

export default async function Home() {
  const videos = await getVideos();

  return (
    <main style={{ padding: "20px" }}>
      <h1>OTT Platform</h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fill,minmax(250px,1fr))",
          gap: "20px",
        }}
      >
        {videos.map((video: any) => (
          <div
            key={video.id}
            style={{
              border: "1px solid #ddd",
              padding: "15px",
            }}
          >
            <h3>{video.title}</h3>

            <p>{video.description}</p>

            <Link
              href={`/watch/${video.id}`}
            >
              Watch Now
            </Link>
          </div>
        ))}
      </div>
    </main>
  );
}
