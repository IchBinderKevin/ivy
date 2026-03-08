import { Button } from "@/components/ui/button";

import { DataTable } from "@/components/DataTable";
import CreateLocationModal from "@/features/locations/components/CreateLocationModal";
import { locationTableColumns } from "@/features/locations/components/DataTableColumns";
import LocationWidgetRow from "@/features/locations/components/LocationWidgetRow";
import { useListLocations } from "@/features/locations/hooks/useLocations";
import { createFileRoute } from "@tanstack/react-router";
import { PlusIcon } from "lucide-react";

export const Route = createFileRoute("/locations/")({
  component: LocationRouteComponent,
});

function LocationRouteComponent() {
  const { data: locationData } = useListLocations();

  return (
    <div className="w-full h-full flex justify-start items-center p-10 gap-5 flex-col">
      <LocationWidgetRow />
      <div className="flex w-full flex-col gap-3 px-20">
        <div className="w-full flex flex-row justify-end items-center">
          <CreateLocationModal
            trigger={
              <Button className="px-5 bg-green-500 text-white hover:bg-green-400">
                <PlusIcon />
                New Location
              </Button>
            }
          />
        </div>

        {locationData && (
          <DataTable columns={locationTableColumns} data={locationData} />
        )}
      </div>
    </div>
  );
}
