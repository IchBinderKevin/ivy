import IvySidebar from "@/components/IvySidebar";
import TopBar from "@/components/TopBar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { createRootRoute, Outlet } from "@tanstack/react-router";

export const Route = createRootRoute({
  component: () => (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <IvySidebar />
        <main className="flex-1 min-w-0 flex flex-col">
          <TopBar />
          <div className="flex-1 overflow-y-hidden">
            <TooltipProvider>
              <Outlet />
            </TooltipProvider>
          </div>
        </main>
      </div>
      <Toaster />
    </SidebarProvider>
  ),
});
