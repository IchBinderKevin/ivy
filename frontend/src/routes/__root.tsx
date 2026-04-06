import IvySidebar from "@/components/IvySidebar";
import TopBar from "@/components/TopBar";
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { createRootRoute, Outlet } from "@tanstack/react-router";

export const Route = createRootRoute({
  component: () => (
    <div className="flex h-screen w-full">
      <IvySidebar />
      <main className="flex-1 min-w-0 flex flex-col">
        <TopBar />
        <div className="flex-1 min-h-0 flex flex-col">
          <TooltipProvider>
            <Outlet />
          </TooltipProvider>
        </div>
      </main>
      <Toaster />
    </div>
  ),
});
