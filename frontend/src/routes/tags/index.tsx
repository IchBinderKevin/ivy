import { DataTable } from "@/components/DataTable";
import { Button } from "@/components/ui/button";
import CreateTagModal from "@/features/tags/components/CreateTagModal";
import { tagTableColumns } from "@/features/tags/components/DataTableColumns";
import TagWidgetRow from "@/features/tags/components/TagWidgetRow";
import { useListTags } from "@/features/tags/hooks/useTags";
import { createFileRoute } from "@tanstack/react-router";
import { PlusIcon } from "lucide-react";
export const Route = createFileRoute("/tags/")({
  component: RouteComponent,
});

function RouteComponent() {
  const { data: tagData } = useListTags();

  return (
    <div className="w-full h-full flex justify-start items-center p-10 gap-5 flex-col">
      <TagWidgetRow />
      <div className="flex w-full flex-col gap-3 px-20">
        <div className="w-full flex flex-row justify-end items-center">
          <CreateTagModal
            trigger={
              <Button className="px-5 bg-green-500 text-white hover:bg-green-400">
                <PlusIcon />
                New Tag
              </Button>
            }
          />
        </div>

        {tagData && <DataTable columns={tagTableColumns} data={tagData} />}
      </div>
    </div>
  );
}
