export default async function handler(req, res) {
  const configured = String(process.env.MUSIC_VIDEO_WORKER_URL || "").trim();
  if (configured) {
    return res.status(200).json({
      ok: true,
      worker_url: configured.replace(/\/+$/, ""),
      source: "env",
    });
  }

  const controlUrl = String(
    process.env.MUSIC_VIDEO_CONTROL_URL ||
      "https://ai-music-video-studio-three.vercel.app/api/control/health"
  ).trim();

  const fallback =
    "https://freelance-michigan-losses-depending.trycloudflare.com";

  try {
    const response = await fetch(controlUrl, {
      headers: { accept: "application/json" },
      cache: "no-store",
    });
    if (!response.ok) {
      throw new Error(`control plane HTTP ${response.status}`);
    }
    const data = await response.json();
    const workerUrl = String(data.worker_url || "").trim();
    if (!workerUrl) {
      throw new Error("control plane did not return worker_url");
    }
    return res.status(200).json({
      ok: Boolean(data.online),
      worker_url: workerUrl.replace(/\/+$/, ""),
      source: "control-plane",
      worker: data.worker || null,
    });
  } catch (error) {
    return res.status(200).json({
      ok: false,
      worker_url: fallback,
      source: "fallback",
      error: error instanceof Error ? error.message : String(error),
    });
  }
}
