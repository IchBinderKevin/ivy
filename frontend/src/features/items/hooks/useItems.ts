import {
  createItem,
  deleteItem,
  fetchItems,
} from "@/features/items/requests/items";
import type { Item } from "@/features/items/types/Item";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function useListItems() {
  return useQuery<Item[]>({
    queryKey: ["items"],
    queryFn: fetchItems,
  });
}

export function useCreateItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["items"] });
    },
  });
}

export function useDeleteItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteItem,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["items"] });
    },
  });
}
