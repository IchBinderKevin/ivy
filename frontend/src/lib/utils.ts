import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function randomHexColor(): string {
  const hex = Math.floor(Math.random() * 0xffffff)
    .toString(16)
    .padStart(6, "0");
  return `#${hex}`;
}

function hexToLuminance(hex: string): number {
  const cleaned = hex.replace("#", "");

  const r = parseInt(cleaned.substring(0, 2), 16);
  const g = parseInt(cleaned.substring(2, 4), 16);
  const b = parseInt(cleaned.substring(4, 6), 16);

  return (r * 299 + g * 587 + b * 114) / 1000;
}

export function getTextColorForHex(hex: string): "text-black" | "text-white" {
  const luminance = hexToLuminance(hex);
  return luminance < 128 ? "text-white" : "text-black";
}
