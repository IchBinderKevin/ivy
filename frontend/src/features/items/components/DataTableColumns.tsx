import { Badge } from "@/components/ui/badge";
import type { Item } from "@/features/items/types/Item";
import { getTextColorForHex } from "@/lib/utils";
import type { ColumnDef } from "@tanstack/react-table";

export const itemTableColumns: ColumnDef<Item>[] = [
  {
    accessorKey: "name",
    header: "Name",
  },
  {
    accessorKey: "location",
    header: "Location",
    cell: ({ row }) => {
      return (
        <span>
          {row.original.location ? row.original.location.name : "Unknown"}
        </span>
      );
    },
  },
  {
    accessorKey: "tags",
    header: "Tags",
    cell: ({ row }) => {
      return (
        <div className="flex flex-row flex-wrap w-full gap-2">
          {row.original.tags.map((tag) => (
            <Badge
              style={{ backgroundColor: tag.color }}
              className={`font-mono ${getTextColorForHex(tag.color)}`}
            >
              {tag.name}
            </Badge>
          ))}
        </div>
      );
    },
  },
];
