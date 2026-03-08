import { AttachmentPicker } from "@/components/AttachmentPicker";
import { ImagePicker } from "@/components/ImagePicker";
import { Button } from "@/components/ui/button";
import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from "@/components/ui/combobox";
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

import { Field, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { useCreateItem } from "@/features/items/hooks/useItems";
import { itemToFormData } from "@/features/items/lib/utils";
import type { ItemCreationData } from "@/features/items/types/Item";
import { useListLocations } from "@/features/locations/hooks/useLocations";
import { TagCombobox } from "@/features/tags/components/TagCombobox";
import { useListTags } from "@/features/tags/hooks/useTags";
import { useState } from "react";
import { toast } from "sonner";

interface CreateItemModelProps {
  trigger: React.ReactNode;
  onClose?: () => void;
}

export default function CreateItemModal({
  trigger,
  onClose,
}: CreateItemModelProps) {
  const { data: locations } = useListLocations();
  const { data: tags } = useListTags();
  const createItem = useCreateItem();

  const [open, setOpen] = useState(false);
  const [itemToBeCreated, setItemToBeCreated] = useState<ItemCreationData>({
    name: "",
    description: "",
    image: null,
    location: null,
    quantity: 1,
    tags: [],
    attachments: [],
    dateOfPurchase: null,
    buyPrice: null,
    boughtFrom: null,
    serialNumber: null,
    modelNumber: null,
    isbn: null,
    notes: null,
  });

  const handleOpenChange = (newOpen: boolean) => {
    setOpen(newOpen);
    if (!newOpen) {
      onClose?.();
    }
  };

  function createItemButtonFunc() {
    const formData = itemToFormData(itemToBeCreated);
    createItem.reset();
    createItem.mutate(formData, {
      onSuccess: () => {
        toast.success("Item created!");
      },
      onError: () => {
        toast.error("Could not create item!");
      },
    });

    setOpen(false);
  }
  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>
      <DialogContent className="min-w-5/6">
        <DialogHeader>
          <DialogTitle>Create new Item</DialogTitle>
          <DialogDescription>
            Creates a new Item with associated tags and metadata.
          </DialogDescription>
        </DialogHeader>

        <div
          className={`h-full min-h-full w-full grid auto-rows-fr gap-2 p-2 overflow-y-auto grid-cols-2`}
        >
          <div className="flex flex-col gap-3">
            <div className="w-full h-12 bg-slate-100 rounded-md flex justify-start items-center text-lg font-medium px-3">
              <span>Basic Information</span>
            </div>
            <div className="w-full flex flex-col px-3 gap-3 items-center">
              <div className="w-full flex flex-row items-center justify-start gap-5">
                <ImagePicker
                  value={itemToBeCreated.image}
                  onChange={(file) =>
                    setItemToBeCreated({
                      ...itemToBeCreated,
                      image: file,
                    })
                  }
                />
                <div className="flex flex-col gap-2 w-full">
                  <Field className="gap-1.5">
                    <FieldLabel htmlFor="input-field-username">Name</FieldLabel>
                    <Input
                      id="name"
                      placeholder="Item Name"
                      value={itemToBeCreated.name}
                      onChange={(e) =>
                        setItemToBeCreated({
                          ...itemToBeCreated,
                          name: e.target.value,
                        })
                      }
                    />
                  </Field>
                  <Field className="gap-1.5">
                    <FieldLabel htmlFor="input-field-description">
                      Description
                    </FieldLabel>
                    <Textarea
                      id="description"
                      placeholder="Item Description"
                      className="resize-none"
                      value={itemToBeCreated.description}
                      onChange={(e) =>
                        setItemToBeCreated({
                          ...itemToBeCreated,
                          description: e.target.value,
                        })
                      }
                    />
                  </Field>
                </div>
              </div>
              <div className="w-full flex flex-row items-center justify-start gap-5">
                <Field className="gap-1.5 w-3/4">
                  <FieldLabel htmlFor="input-field-location">
                    Location
                  </FieldLabel>
                  <Combobox
                    items={locations}
                    value={itemToBeCreated.location?.name ?? ""}
                    onValueChange={(locationId) => {
                      const location =
                        locations?.find(
                          (loc) => loc.id.toString() === locationId,
                        ) ?? null;

                      setItemToBeCreated({
                        ...itemToBeCreated,
                        location,
                      });
                    }}
                  >
                    <ComboboxInput placeholder="Select a location..." />
                    <ComboboxContent>
                      <ComboboxEmpty>Select location...</ComboboxEmpty>
                      {/* Pointer events auto was needed here to make the items clickable in a dialog */}
                      <ComboboxList className="pointer-events-auto">
                        {(item) => (
                          <ComboboxItem
                            key={item.name}
                            value={item.id.toString()}
                          >
                            {item.name}
                          </ComboboxItem>
                        )}
                      </ComboboxList>
                    </ComboboxContent>
                  </Combobox>
                </Field>
                <Field className="gap-1.5 w-1/4">
                  <FieldLabel htmlFor="input-field-quantity">
                    Quantity
                  </FieldLabel>
                  <Input
                    id="quantity"
                    type="number"
                    placeholder="Item Quantity"
                    min={1}
                    step={1}
                    value={itemToBeCreated.quantity}
                    onChange={(e) =>
                      setItemToBeCreated({
                        ...itemToBeCreated,
                        quantity: e.target.valueAsNumber,
                      })
                    }
                  />
                </Field>
              </div>
              <Field className="gap-1.5">
                <FieldLabel htmlFor="input-field-tags">Tags</FieldLabel>
                <TagCombobox
                  tags={tags || []}
                  selectedValues={itemToBeCreated.tags}
                  onChange={(selectedTagIds) => {
                    const selectedTags =
                      tags?.filter((tag) =>
                        selectedTagIds.includes(tag.id.toString()),
                      ) ?? [];

                    setItemToBeCreated({
                      ...itemToBeCreated,
                      tags: selectedTags,
                    });
                  }}
                  placeholder="Select tags..."
                />
              </Field>
              <Field className="ga-1.5">
                <FieldLabel htmlFor="input-field-attachments">
                  Attachments
                </FieldLabel>
                <AttachmentPicker
                  value={itemToBeCreated.attachments}
                  onChange={(files) =>
                    setItemToBeCreated({
                      ...itemToBeCreated,
                      attachments: files ?? [],
                    })
                  }
                />
              </Field>
            </div>
          </div>
          <div className="flex flex-col gap-5 mb-0">
            <div className="flex flex-col gap-3">
              <div className="w-full h-12 bg-slate-100 rounded-md flex justify-start items-center text-lg font-medium px-3">
                <span>Purchase Detail (optional)</span>
              </div>
              <div className="w-full flex flex-col px-3 gap-3 items-start justify-start">
                <div className="w-full flex flex-row gap-3 items-center justify-start">
                  <Field className="gap-1.5 w-3/4">
                    <FieldLabel htmlFor="input-field-date-of-purchase">
                      Date of Purchase
                    </FieldLabel>
                    {/* TODO: Replace Input with calendar from shadcn for better crosbrowser support. type=date behaves weirdly on e.g. safari*/}
                    <Input
                      id="date-of-purchase"
                      placeholder="Date of Purchase"
                      type="date"
                      value={
                        itemToBeCreated.dateOfPurchase
                          ?.toISOString()
                          .split("T")[0] ?? ""
                      }
                      onChange={(e) =>
                        setItemToBeCreated({
                          ...itemToBeCreated,
                          dateOfPurchase: e.target.value
                            ? new Date(e.target.value)
                            : null,
                        })
                      }
                    />
                  </Field>
                  <Field className="gap-1.5 w-1/4">
                    <FieldLabel htmlFor="input-field-buy-price">
                      Buy Price
                    </FieldLabel>

                    <Input
                      className="bg-white"
                      placeholder="0.00"
                      min={0}
                      step={0.01}
                      type="number"
                      value={itemToBeCreated.buyPrice ?? ""}
                      onChange={(e) =>
                        setItemToBeCreated({
                          ...itemToBeCreated,
                          buyPrice: e.target.value
                            ? parseFloat(e.target.value)
                            : null,
                        })
                      }
                    />
                  </Field>
                </div>
                <Field className="gap-1.5">
                  <FieldLabel htmlFor="input-field-buy-price">
                    Bought from
                  </FieldLabel>
                  <Input
                    type="text"
                    placeholder="Bought from..."
                    value={itemToBeCreated.boughtFrom ?? ""}
                    onChange={(e) =>
                      setItemToBeCreated({
                        ...itemToBeCreated,
                        boughtFrom: e.target.value,
                      })
                    }
                  />
                </Field>
              </div>
            </div>
            <div className="flex flex-col gap-3">
              <div className="w-full h-12 bg-slate-100 rounded-md flex justify-start items-center text-lg font-medium px-3">
                <span>Item Metadata (optional)</span>
              </div>
              <div className="w-full flex flex-col px-3 gap-3 items-start justify-start">
                <div className="w-full flex flex-row gap-5">
                  <Field className="gap-1.5">
                    <FieldLabel htmlFor="input-field-serial-number">
                      Serial Number
                    </FieldLabel>
                    <Input
                      id="serial-number"
                      placeholder="Serial Number"
                      type="text"
                      value={itemToBeCreated.serialNumber ?? ""}
                      onChange={(e) =>
                        setItemToBeCreated({
                          ...itemToBeCreated,
                          serialNumber: e.target.value,
                        })
                      }
                    />
                  </Field>
                  <Field className="gap-1.5">
                    <FieldLabel htmlFor="input-field-model-number">
                      Model Number
                    </FieldLabel>
                    <Input
                      id="model-number"
                      placeholder="Model Number"
                      type="text"
                      value={itemToBeCreated.modelNumber ?? ""}
                      onChange={(e) =>
                        setItemToBeCreated({
                          ...itemToBeCreated,
                          modelNumber: e.target.value,
                        })
                      }
                    />
                  </Field>
                </div>

                <Field className="gap-1.5">
                  <FieldLabel htmlFor="input-field-isbn">ISBN</FieldLabel>
                  <Input id="isbn" placeholder="ISBN" type="text" />
                </Field>
                <Field className="gap-1.5">
                  <FieldLabel htmlFor="input-field-notes">Notes</FieldLabel>
                  <Textarea
                    id="notes"
                    placeholder="Additional notes about the item..."
                    className="resize-none h-18"
                    value={itemToBeCreated.notes ?? ""}
                    onChange={(e) =>
                      setItemToBeCreated({
                        ...itemToBeCreated,
                        notes: e.target.value,
                      })
                    }
                  />
                </Field>
              </div>
            </div>
          </div>
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
            onClick={createItemButtonFunc}
          >
            Create
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
