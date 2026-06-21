import Link from "next/link";

async function getVideos() {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/videos`,
    {
      cache: "no-store",
    }
  );

  if (!res.ok) {
    return [];
  }

  return res.json();
}

export default async function Home() {
  const videos = await getVideos();

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold mb-6">
        OTT Platform
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {videos.map((video: any) => (
          <div
            key={video.id}
            className="border rounded-lg p-4"
          >
            <h2 className="font-semibold">
              {video.title}
            </h2>

            <p className="text-sm text-gray-500">
              {video.description}
            </p>

            <Link
              href={`/watch/${video.id}`}
              className="text-blue-500"
            >
              Watch
            </Link>
          </div>
        ))}
      </div>
    </main>
  );
}
