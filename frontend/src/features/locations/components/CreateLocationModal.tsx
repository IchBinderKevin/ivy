import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateLocation } from "@/features/locations/hooks/useLocations";

import { useState } from "react";
import { toast } from "sonner";

interface CreateLocationModalProps {
  trigger: React.ReactNode;
  onClose?: () => void;
}

function CreateLocationModal({ trigger, onClose }: CreateLocationModalProps) {
  const [name, setName] = useState("");
  const [open, setOpen] = useState(false);
  const createLocation = useCreateLocation();

  const handleOpenChange = (newOpen: boolean) => {
    setOpen(newOpen);
    if (!newOpen) {
      onClose?.();
    }
  };

  function createLocationButtonFunc() {
    createLocation.reset();
    createLocation.mutate(name, {
      onSuccess: () => {
        toast.success("Location created!");
      },
      onError: () => {
        toast.error("Could not create location!");
      },
    });
    onClose?.();
    setOpen(false);
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create new Location</DialogTitle>
          <DialogDescription>
            Creates a new Location for grouping items.
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-col w-full h-full justify-start items-start gap-2">
          <Label className="text-md">Name</Label>
          <Input value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button className="bg-red-500 text-white hover:bg-red-400 hover:text-white cursor-pointer">
              Cancel
            </Button>
          </DialogClose>
          <Button
            className="text-white bg-green-500 hover:bg-green-400 hover:text-white cursor-pointer"
            variant={"outline"}
            onClick={createLocationButtonFunc}
          >
            Create
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

export default CreateLocationModal;
