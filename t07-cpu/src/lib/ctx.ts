import { createContext, useContext } from "react";
import type { VideoInput } from "../schema";

export const InputCtx = createContext<VideoInput | null>(null);

export function useInput(): VideoInput {
  const v = useContext(InputCtx);
  if (!v) throw new Error("useInput must be used inside <InputCtx.Provider>");
  return v;
}
