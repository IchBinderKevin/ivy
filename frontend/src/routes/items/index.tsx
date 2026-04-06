import { Button } from "@/components/ui/button";
import { AccordionDataTable } from "@/features/items/components/AccordionDataTable";
import CreateItemModal from "@/features/items/components/CreateItemModal";
import CustomItemCard from "@/features/items/components/CustomItemCard";
import { itemTableColumns } from "@/features/items/components/DataTableColumns";
import ItemWidgetRow from "@/features/items/components/ItemWidgetRow";
import { useListItems } from "@/features/items/hooks/useItems";
import { createFileRoute } from "@tanstack/react-router";
import { Columns3Icon, ListIcon, PlusIcon } from "lucide-react";
import { useEffect, useState } from "react";

export const Route = createFileRoute("/items/")({
  component: RouteComponent,
});

function RouteComponent() {
  const { data: itemData } = useListItems();
  useEffect(() => {
    document.title = "Items | ivy";
  }, []);

  const [displayMode, setDisplayMode] = useState<"list" | "grid">("grid");

  return (
    <div className="w-full h-full flex flex-col pt-10 px-10 gap-5">
      <ItemWidgetRow />

      <div className="w-full flex flex-col gap-3 px-20 min-h-0 flex-1">
        <div className="w-full flex flex-row justify-between items-center">
          <span className="text-2xl font-bold">Items</span>
          <div className="flex flex-row gap-2">
            <Button
              variant={"ghost"}
              className="bg-blue-50"
              onClick={() => setDisplayMode("grid")}
              disabled={displayMode === "grid"}
            >
              <Columns3Icon className="text-black" />
            </Button>
            <Button
              variant={"ghost"}
              className="bg-blue-50"
              onClick={() => setDisplayMode("list")}
              disabled={displayMode === "list"}
            >
              <ListIcon className="text-black" />
            </Button>
            <CreateItemModal
              trigger={
                <Button className="px-5 bg-green-500 text-white hover:bg-green-400">
                  <PlusIcon />
                  New Item
                </Button>
              }
            />
          </div>
        </div>

        {displayMode === "grid" && (
          <div className="w-full flex-1 min-h-0 overflow-y-auto grid grid-cols-2 md:grid-cols-3 2xl:grid-cols-3 gap-5 mb-2 content-start [scrollbar-gutter:stable]">
            {itemData?.map((item) => (
              <CustomItemCard key={item.id} item={item} />
            ))}
          </div>
        )}

        {displayMode === "list" && itemData && (
          <div className="w-full flex-1 min-h-0 overflow-y-auto gap-5 mb-2 content-start [scrollbar-gutter:stable]">
            <AccordionDataTable columns={itemTableColumns} data={itemData} />
          </div>
        )}
      </div>
    </div>
  );
}
