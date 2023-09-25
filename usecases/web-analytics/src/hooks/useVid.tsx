import { customAlphabet, urlAlphabet } from 'nanoid';
import { createContext, useContext } from "react";

const nanoid = customAlphabet(urlAlphabet.replace(/-/, '').replace(/_/, ''), 8);

const VidContext = createContext<string>(nanoid());

export function useVid() {
  const vid = useContext(VidContext);
  return vid;
}
