import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Separator } from "@/components/ui/separator";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { useDeleteItem } from "@/features/items/hooks/useItems";
import type { Item } from "@/features/items/types/Item";
import { getTextColorForHex } from "@/lib/utils";
import {
  Edit2,
  EllipsisVertical,
  FileIcon,
  MapPin,
  Trash2,
} from "lucide-react";
import type { SyntheticEvent } from "react";

export default function CustomItemCard(props: { item: Item }) {
  const deleteItem = useDeleteItem();
  return (
    <div className="bg-[#efeeeb] flex flex-row h-60 w-125 rounded-lg gap-4 shadow-md">
      <img
        src={props.item.image?.substring(1) ?? "/placeholder.png"}
        className="rounded-l-xl h-full w-50 min-w-50"
        onError={(e: SyntheticEvent<HTMLImageElement>) => {
          e.currentTarget.src = "/placeholder.png";
        }}
      />
      <div className="flex flex-col gap-2 py-4 pr-4 w-75">
        <div className="flex flex-row justify-between items-center">
          <span className="w-61 text-2xl font-bold truncate">
            {props.item.name}
          </span>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <EllipsisVertical className="text-gray-600 w-6 h-6" />
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem>
                <Edit2 />
                Edit
              </DropdownMenuItem>
              <DropdownMenuItem
                variant="destructive"
                onSelect={() => deleteItem.mutate(props.item.id)}
              >
                <Trash2 />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <div className="h-full w-60">
          {props.item.description ? (
            <p className="text-lg/5 text-slate-600 line-clamp-4">
              {props.item.description}
            </p>
          ) : (
            <p className="text-lg/5 text-slate-400 line-clamp-4">
              No description provided for this item.
            </p>
          )}
        </div>
        <div className="flex flex-row flex-wrap w-full gap-1 items-end h-6 max-h-6 overflow-clip">
          {props.item.tags.slice(0, 3).map((tag) => (
            <Tooltip>
              <TooltipTrigger asChild>
                <Badge
                  style={{ backgroundColor: tag.color }}
                  className={`${getTextColorForHex(tag.color)} w-18 shadow-sm py-0.5 px-1`}
                >
                  <span className="block min-w-0 p-0 truncate">{tag.name}</span>
                </Badge>
              </TooltipTrigger>
              <TooltipContent className="bg-[#C8C6C3] fill-[#C8C6C3] text-slate-800">
                <span>{tag.name}</span>
              </TooltipContent>
            </Tooltip>
          ))}
          {props.item.tags.length > 2 && (
            <Tooltip>
              <TooltipTrigger asChild>
                <Badge className="w-8 bg-[#45263B] text-white shadow-sm py-0.5 px-1">
                  +{props.item.tags.length - 3}
                </Badge>
              </TooltipTrigger>
              <TooltipContent className="bg-[#C8C6C3] fill-[#C8C6C3] text-slate-800">
                <div className="flex flex-col gap-2 justify-center items-center">
                  {props.item.tags.slice(3).map((tag) => (
                    <span>{tag.name}</span>
                  ))}
                </div>
              </TooltipContent>
            </Tooltip>
          )}
        </div>
        <Separator />
        <div className="flex flex-row justify-between items-center">
          <div className="flex flex-row gap-1 justify-center items-center">
            <MapPin size={18} className="text-gray-600" />
            {props.item.location ? (
              <a
                className="w-32 text-sm text-gray-600 truncate"
                href={`/locations/${props.item.location.id}`}
              >
                {props.item.location.name}
              </a>
            ) : (
              <span className="w-32 text-sm text-gray-600 truncate">
                Unknown
              </span>
            )}
          </div>
          <div className="flex flex-row gap-1 justify-center items-center">
            {props.item.attachments && props.item.attachments.length > 0 && (
              <div className="flex flex-row bg-[#CEEACD] px-3 py-1 rounded-md justify-center items-center gap-1">
                <span className="text-sm text-gray-600">
                  {Math.min(props.item.attachments?.length, 999)}
                </span>
                <FileIcon className="text-gray-600 w-3 h-3" />
              </div>
            )}
            <div className="flex flex-row bg-[#ede3e7] px-3 py-1 rounded-md justify-center items-center gap-1">
              <span className="text-sm text-gray-600">
                x {Math.min(props.item.quantity, 999)}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
