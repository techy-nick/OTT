"use client";

import Hls from "hls.js";
import {
  useEffect,
  useRef,
} from "react";

export default function VideoPlayer({
  url,
}: {
  url: string;
}) {
  const videoRef =
    useRef<HTMLVideoElement>(null);

  useEffect(() => {
    const video = videoRef.current;

    if (!video) return;

    if (
      Hls.isSupported() &&
      url.endsWith(".m3u8")
    ) {
      const hls = new Hls();

      hls.loadSource(url);
      hls.attachMedia(video);

      return () => {
        hls.destroy();
      };
    }

    video.src = url;
  }, [url]);

  return (
    <video
      ref={videoRef}
      controls
      width="100%"
    />
  );
}
