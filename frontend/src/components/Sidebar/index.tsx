import { Sidebar, SidebarContent, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarMenu, SidebarMenuButton, SidebarMenuItem } from "@src/components/ui/sidebar";
import { Scale as DecisionSideIcon, ClipboardCheck as PoliciesIcon } from "lucide-react";
import { useLocation } from "react-router-dom";

type SidebarItem = {
  title: string
  url: string
  icon: JSX.Element
} 

const sidebarItems: SidebarItem[] = [
  {
    title: "Decision",
    url: "decision",
    icon: <DecisionSideIcon/>
  },
  {
    title: "Policies",
    url: "policies",
    icon: <PoliciesIcon/>
  }
]

export default function AppSidebar() {
  const location = useLocation()

  console.log(location)
  
  return (
    <Sidebar>
      <SidebarContent className="p-4 text-white bg-zinc-800">
        <SidebarGroup>
          <SidebarGroupLabel className="mb-4 text-xl font-semibold text-gray-300">
            Decision Engine
          </SidebarGroupLabel>
        </SidebarGroup>
        <SidebarGroupContent>
          <SidebarMenu className="space-y-2">
            {sidebarItems.map((item) => (
              <SidebarMenuItem key={item.title}>
                <SidebarMenuButton asChild>
                  <a
                    href={item.url}
                    className={`flex items-center gap-3 px-4 py-2 transition-colors rounded-md ${
                        location.pathname === `/${item.url}`
                        ? "bg-zinc-600 text-white"
                        : "hover:text-white hover:bg-zinc-700"
                    }`}
                  >
                    {item.icon}
                    <span className="text-lg">{item.title}</span>
                  </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
            ))}
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarContent>
    </Sidebar>
  )
}