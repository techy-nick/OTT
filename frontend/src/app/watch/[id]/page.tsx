import VideoPlayer from "./player";

async function getVideo(id: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/videos/${id}`,
    {
      cache: "no-store",
    }
  );

  return res.json();
}

export default async function WatchPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const video = await getVideo(id);

  return (
    <div className="p-8">
      <h1 className="text-2xl mb-4">
        {video.title}
      </h1>

      <VideoPlayer url={video.hls_url} />
    </div>
  );
}
