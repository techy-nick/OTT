import VideoPlayer from "./player";

async function getVideo(id: string) {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/videos/${id}`,
    {
      cache: "no-store",
    }
  );

  return response.json();
}

export default async function WatchPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const video = await getVideo(id);

  return (
    <div style={{ padding: "20px" }}>
      <h1>{video.title}</h1>

      <p>{video.description}</p>

      <VideoPlayer
        url={video.hls_url}
      />
    </div>
  );
}
