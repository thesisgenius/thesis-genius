// import * as React from 'react';
import { ChevronRight } from 'lucide-react';
import Logo from '/owl.png';

import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible';
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
} from '@/components/ui/sidebar';
import { useLocation, Link } from 'react-router-dom';

// This is sample data.
const data = {
  navMain: [
    {
      title: 'Writing Your Thesis',
      items: [
        {
          title: 'Table of Contents',
          url: 'table-of-contents',
        },
        {
          title: 'Title',
          url: 'title',
        },
        {
          title: 'Copyright',
          url: 'copyright',
        },
        {
          title: 'Signature',
          url: 'signature',
        },
        {
          title: 'Abstract',
          url: 'abstract',
        },
        {
          title: 'Dedication',
          url: 'dedication',
        },
        {
          title: 'Appendices',
          url: 'appendices',
        },
        {
          title: 'References',
          url: 'references',
        },
        {
          title: 'List of Figures',
          url: 'list-of-figures',
        },
        {
          title: 'List of Tables',
          url: 'list-of-tables',
        },
        {
          title: 'Other Info',
          url: 'other-info',
        },
      ],
    },
    {
      title: 'Thesis',
      items: [
        {
          title: 'Body',
          url: 'thesis-body',
        },
        {
          title: 'Manage Theses',
          url: 'manage-theses',
        },
      ],
    },
    {
      title: 'Forum',
      items: [
        {
          title: 'Manage Forums',
          url: 'manage-forums',
        },
        // {
        //   title: 'Manage Posts',
        //   url: '#',
        // },
      ],
    },
  ],
};

export function AppSidebar({ ...props }) {
  const location = useLocation();
  const pathname = location.pathname;

  return (
    <Sidebar {...props}>
      <SidebarHeader className='inline-flex flex-row gap-2 items-center my-2'>
        <img className='h-12 w-auto' src={Logo} alt='logo' />
        <div>
          <h1 className='font-bold text-2xl text-sky-500'>ThesisGenius</h1>
          <p className='italic'>write smart, write less</p>
        </div>
      </SidebarHeader>
      <SidebarContent className='gap-0'>
        {/* We create a collapsible SidebarGroup for each parent. */}
        {data.navMain.map((item) => (
          <Collapsible
            key={item.title}
            title={item.title}
            defaultOpen
            className='group/collapsible'
          >
            <SidebarGroup>
              <SidebarGroupLabel
                asChild
                className='group/label text-sm text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
              >
                <CollapsibleTrigger>
                  {item.title}{' '}
                  <ChevronRight className='ml-auto transition-transform group-data-[state=open]/collapsible:rotate-90' />
                </CollapsibleTrigger>
              </SidebarGroupLabel>
              <CollapsibleContent>
                <SidebarGroupContent>
                  <SidebarMenu>
                    {item.items.map((item) => (
                      <SidebarMenuItem key={item.title}>
                        <SidebarMenuButton
                          asChild
                          isActive={pathname.includes(item.url)}
                        >
                          <Link to={item.url}>{item.title}</Link>
                        </SidebarMenuButton>
                      </SidebarMenuItem>
                    ))}
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
