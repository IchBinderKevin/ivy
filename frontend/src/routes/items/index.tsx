import { Button } from "@/components/ui/button";
import { AccordionDataTable } from "@/features/items/components/AccordionDataTable";
import CreateItemModal from "@/features/items/components/CreateItemModal";
import { itemTableColumns } from "@/features/items/components/DataTableColumns";
import ItemCard from "@/features/items/components/ItemCard";
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
    <div className="w-full h-full flex justify-start items-center p-10 gap-5 flex-col">
      <ItemWidgetRow />

      <div className="flex w-full flex-col gap-3 px-20">
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
          <div className="w-full h-full flex flex-row flex-wrap gap-5">
            {itemData?.map((item) => (
              <ItemCard key={item.id} item={item} />
            ))}
          </div>
        )}
        {displayMode === "list" && itemData && (
          <AccordionDataTable columns={itemTableColumns} data={itemData} />
        )}
      </div>
    </div>
  );
}
