import AppSidebar from "@src/components/Sidebar"
import { SidebarProvider } from "@src/components/ui/sidebar"

type HomeLayoutProps = {
  children: React.ReactNode
}

const HomeLayout = ({ children }: HomeLayoutProps) => {
  return (
    <SidebarProvider>
      <AppSidebar />
      <main className="flex justify-center w-full my-12 mx-52">
        {children}
      </main>
    </SidebarProvider>
  )
}

export default HomeLayout