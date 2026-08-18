import type { ImgHTMLAttributes } from "react";

import { useAuthenticatedUrl } from "@/lib/use-authenticated-url";

interface AuthenticatedImageProps extends Omit<ImgHTMLAttributes<HTMLImageElement>, "src"> {
  src: string;
}

export function AuthenticatedImage({ src, ...props }: AuthenticatedImageProps) {
  const resolvedUrl = useAuthenticatedUrl(src);
  if (!resolvedUrl) return null;
  return (
    <img
      {...props}
      src={resolvedUrl}
    />
  );
}
