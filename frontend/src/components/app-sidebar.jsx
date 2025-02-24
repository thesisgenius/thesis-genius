// app-sidebar.jsx
import { ChevronRight } from "lucide-react";
import { useThesis } from "@/context/thesisContext";
import Logo from "/owl.png";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar";
import { useLocation, Link } from "react-router-dom";

// For demonstration, we might import from context
// import { useMyThesisContext } from "../context/ThesisContext";

const data = {
  navMain: [
    {
      title: "Writing Your Thesis",
      items: [
        { title: "Table of Contents", url: "table-of-contents" },
        { title: "Title", url: "title" },
        { title: "Copyright", url: "copyright" },
        { title: "Signature", url: "signature" },
        { title: "Abstract", url: "abstract" },
        { title: "Dedication", url: "dedication" },
        { title: "Appendices", url: "appendices" },
        { title: "References", url: "references" },
        { title: "List of Figures", url: "list-of-figures" },
        { title: "List of Tables", url: "list-of-tables" },
        { title: "Other Info", url: "other-info" },
      ],
    },
    {
      title: "Thesis",
      items: [
        { title: "Body", url: "thesis-body" },
        { title: "Manage Theses", url: "manage-theses" },
      ],
    },
    {
      title: "Forum",
      items: [{ title: "Manage Forums", url: "manage-forums" }],
    },
  ],
};

export function AppSidebar({ ...props }) {
  const location = useLocation();
  const { activeThesisId } = useThesis(); // <--- retrieve the ID from context

  // If no thesisId is set, you might always link to manage-theses or show a note

  return (
    <Sidebar {...props}>
      <SidebarHeader className="inline-flex flex-row gap-2 items-center my-2">
        <Link to="/" className="inline-flex gap-2 items-center">
          <img className="h-12 w-auto" src={Logo} alt="logo" />
          <div>
            <h1 className="font-bold text-2xl text-sky-300">ThesisGenius</h1>
            <p className="italic text-white">write smart, write less</p>
          </div>
        </Link>
      </SidebarHeader>
      <SidebarContent className="gap-0">
        {data.navMain.map((group) => (
          <Collapsible key={group.title} title={group.title} defaultOpen>
            <SidebarGroup>
              <SidebarGroupLabel
                asChild
                className="group/label text-sm text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              >
                <CollapsibleTrigger>
                  {group.title}{" "}
                  <ChevronRight className="ml-auto transition-transform group-data-[state=open]/label:rotate-90" />
                </CollapsibleTrigger>
              </SidebarGroupLabel>
              <CollapsibleContent>
                <SidebarGroupContent>
                  <SidebarMenu>
                    {group.items.map((navItem) => {
                      // If the user clicked "Manage Theses," maybe that doesn't require thesisId
                      const needsThesisId =
                        navItem.url !== "manage-theses" &&
                        navItem.url !== "manage-forums";

                      // Build the path
                      const fullPath =
                        needsThesisId && activeThesisId
                          ? `/app/${activeThesisId}/${navItem.url}`
                          : `/app/${navItem.url}`;

                      return (
                        <SidebarMenuItem key={navItem.title}>
                          <SidebarMenuButton
                            asChild
                            isActive={location.pathname.includes(navItem.url)}
                          >
                            <Link to={fullPath}>{navItem.title}</Link>
                          </SidebarMenuButton>
                        </SidebarMenuItem>
                      );
                    })}
                  </SidebarMenu>
                </SidebarGroupContent>
              </CollapsibleContent>
            </SidebarGroup>
          </Collapsible>
        ))}
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  );
}
