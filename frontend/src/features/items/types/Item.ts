import type { Location } from "@/features/locations/types/location";
import type { Tag } from "@/features/tags/types/tag";

export type Item = {
  id: number;
  name: string;
  description: string;
  image: string | null;
  location: Location;
  buy_date: string;
  tags: Tag[];
  attachments?: string[];
  date_of_purchase?: Date;
  buy_price?: number;
  bought_from?: string;
  isbn?: string;
  model_number?: string;
  notes?: string;
  quantity: number;
  serial_number?: string;
};

export type ItemCreationData = {
  name: string;
  description: string;
  image: null | File;
  location: Location | null;
  quantity: number;
  tags: Tag[];
  attachments: File[];
  dateOfPurchase: Date | null;
  buyPrice: number | null;
  boughtFrom: string | null;
  serialNumber: string | null;
  modelNumber: string | null;
  isbn: string | null;
  notes: string | null;
};
