import { createFileRoute } from "@tanstack/react-router";
import { useEffect } from "react";

export const Route = createFileRoute("/settings/")({
  component: RouteComponent,
});

function RouteComponent() {
  useEffect(() => {
    document.title = "Settings | ivy";
  }, []);

  return (
    <div className="w-full h-full flex justify-center items-center">
      <img src="/wip.png" width={700} />
    </div>
  );
}
