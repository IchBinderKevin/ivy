import type { ItemCreationData } from "@/features/items/types/Item";

export function itemToFormData(item: ItemCreationData): FormData {
  const fd = new FormData();

  const json: any = {};

  Object.entries(item).forEach(([key, value]) => {
    if (value == null) return;

    if (value instanceof File) {
      fd.append(key, value);
    } else if (Array.isArray(value) && value.every((v) => v instanceof File)) {
      value.forEach((file) => fd.append(key, file));
    } else {
      json[key] = value;
    }
  });

  fd.append("item", JSON.stringify(json));

  return fd;
}
