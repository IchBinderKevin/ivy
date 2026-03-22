import { createFileRoute } from "@tanstack/react-router";
import { useEffect } from "react";

export const Route = createFileRoute("/")({
  component: RouteComponent,
});

function RouteComponent() {
  useEffect(() => {
    document.title = "Dashboard | ivy";
  }, []);

  return (
    <div className="w-full h-full flex justify-center items-center">
      <img src="/wip.png" width={700} />
    </div>
  );
}
