import { Logo } from "@/components/Logo";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import CreateItemModal from "@/features/items/components/CreateItemModal";
import CreateLocationModal from "@/features/locations/components/CreateLocationModal";
import CreateTagModal from "@/features/tags/components/CreateTagModal";
import { Link } from "@tanstack/react-router";
import {
  Box,
  HomeIcon,
  MapPin,
  Plus,
  Search,
  Settings,
  Tag,
} from "lucide-react";
import { useEffect, useState } from "react";

let versionPromise: Promise<string> | null = null;

export function getVersion(): Promise<string> {
  if (!versionPromise) {
    versionPromise = fetch("/api/version")
      .then((res) => res.json())
      .then((data) => data.version);
  }

  return versionPromise;
}

function IvySidebar() {
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const [version, setVersion] = useState<string | null>(null);

  useEffect(() => {
    getVersion().then(setVersion);
  }, []);

  return (
    <div className="h-full w-20 bg-[#f5f3f0] text-black flex flex-col items-center justify-start gap-3 py-4">
      <div className="flex justify-center items-center">
        <Logo />
      </div>
      {/* Sidebar Content */}
      <div className="flex flex-col justify-start items-center h-full w-full gap-8 py-5 px-2">
        <IvySidebarItem
          icon={<HomeIcon className="w-8 h-8" />}
          label="Home"
          to="/"
        />
        <IvySidebarItem
          icon={<Box className="w-8 h-8" />}
          label="Items"
          to="/items"
        />
        <IvySidebarItem
          icon={<MapPin className="w-8 h-8" />}
          label="Locations"
          to="/locations"
        />
        <IvySidebarItem
          icon={<Tag className="w-8 h-8" />}
          label="Tags"
          to="/tags"
        />
        <IvySidebarItem
          icon={<Search className="w-8 h-8" />}
          label="Search"
          to="/search"
        />
        <IvySidebarItem
          icon={<Settings className="w-8 h-8" />}
          label="Settings"
          to="/settings"
        />
        <DropdownMenu open={dropdownOpen} onOpenChange={setDropdownOpen}>
          <DropdownMenuTrigger asChild>
            <Button className="bg-green-400 w-12 h-12 hover:bg-green-300 rounded-xl">
              <Plus className="text-white text-3xl" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="bg-neutral-100  text-gray-600"
            align="start"
          >
            <CreateItemModal
              trigger={
                <DropdownMenuItem
                  className="text-lg"
                  onSelect={(e) => e.preventDefault()}
                >
                  New Item
                </DropdownMenuItem>
              }
              onClose={() => {
                setDropdownOpen(false);
              }}
            />
            <CreateLocationModal
              trigger={
                <DropdownMenuItem
                  className="text-lg"
                  onSelect={(e) => e.preventDefault()}
                >
                  New Location
                </DropdownMenuItem>
              }
              onClose={() => {
                setDropdownOpen(false);
              }}
            />
            <CreateTagModal
              trigger={
                <DropdownMenuItem
                  className="text-lg"
                  onSelect={(e) => e.preventDefault()}
                >
                  New Tag
                </DropdownMenuItem>
              }
              onClose={() => {
                setDropdownOpen(false);
              }}
            />
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      {/* Sidebar Footer for future elements */}
      <div className="flex flex-col h-1/5 items-center justify-end font-mono text-sm text-gray-500">
        <span className="text-xs">
          {/* checks if version is a semantic version to prefix accordingly othervise just shows the versio from the backend*/}
          {version && /^\d+\.\d+\.\d+/.test(version) ? `v${version}` : version}
        </span>
      </div>
    </div>
  );
}

export default IvySidebar;

interface IvySidebarItemProps {
  icon: React.ReactNode;
  label: string;
  to: string;
}

function IvySidebarItem({ icon, label, to }: IvySidebarItemProps) {
  return (
    <Link className="flex flex-col items-center justify-center gap-1" to={to}>
      {/* Icon */}
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="text-gray-600 w-8 h-8 flex items-center justify-center">
            {icon}
          </div>
        </TooltipTrigger>
        <TooltipContent
          side="right"
          className="bg-neutral-200 fill-neutral-200 text-gray-600"
        >
          <span className="text-lg">{label}</span>
        </TooltipContent>
      </Tooltip>
    </Link>
  );
}
