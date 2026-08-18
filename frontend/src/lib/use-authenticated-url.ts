import { useEffect, useState } from "react";

import { authenticatedFetch } from "./api-client";

export function useAuthenticatedUrl(sourceUrl: string | null | undefined): string | undefined {
  const initialUrl =
    typeof sourceUrl === "string" &&
    (sourceUrl.startsWith("blob:") || sourceUrl.startsWith("data:"))
      ? sourceUrl
      : undefined;
  const [resolvedUrl, setResolvedUrl] = useState<string | undefined>(initialUrl);

  useEffect(() => {
    if (!sourceUrl) {
      setResolvedUrl(undefined);
      return;
    }
    if (sourceUrl.startsWith("blob:") || sourceUrl.startsWith("data:")) {
      setResolvedUrl(sourceUrl);
      return;
    }

    const controller = new AbortController();
    let objectUrl: string | undefined;
    setResolvedUrl(undefined);

    void authenticatedFetch(sourceUrl, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`Failed to load resource: ${response.status}`);
        return response.blob();
      })
      .then((blob) => {
        if (controller.signal.aborted) return;
        objectUrl = URL.createObjectURL(blob);
        setResolvedUrl(objectUrl);
      })
      .catch((error: unknown) => {
        if (!(error instanceof DOMException && error.name === "AbortError")) {
          setResolvedUrl(undefined);
        }
      });

    return () => {
      controller.abort();
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [sourceUrl]);

  return resolvedUrl;
}
