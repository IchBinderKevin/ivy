import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/settings/")({
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <div className="w-full h-full flex justify-center items-center">
      <img src="/wip.png" width={700} />
    </div>
  );
}
