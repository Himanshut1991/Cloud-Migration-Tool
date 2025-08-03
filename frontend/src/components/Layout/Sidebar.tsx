import React, { useState } from 'react';
import { Layout, Menu } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  DatabaseOutlined,
  DesktopOutlined,
  FolderOpenOutlined,
  SettingOutlined,
  BarChartOutlined,
  FileTextOutlined,
  CloudOutlined,
  CalendarOutlined,
  DollarOutlined,
  TeamOutlined,
  ExportOutlined,
  ScheduleOutlined,
  RocketOutlined,
} from '@ant-design/icons';

const { Sider } = Layout;

const Sidebar: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const location = useLocation();

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: <Link to="/dashboard">Dashboard</Link>,
    },
    {
      key: 'inventory',
      icon: <DatabaseOutlined />,
      label: 'Inventory Management',
      children: [
        {
          key: '/inventory/servers',
          icon: <DesktopOutlined />,
          label: <Link to="/inventory/servers">Servers</Link>,
        },
        {
          key: '/inventory/databases',
          icon: <DatabaseOutlined />,
          label: <Link to="/inventory/databases">Databases</Link>,
        },
        {
          key: '/inventory/file-shares',
          icon: <FolderOpenOutlined />,
          label: <Link to="/inventory/file-shares">File Shares</Link>,
        },
      ],
    },
    {
      key: 'configuration',
      icon: <SettingOutlined />,
      label: 'Configuration',
      children: [
        {
          key: '/configuration/cloud-preferences',
          icon: <CloudOutlined />,
          label: <Link to="/configuration/cloud-preferences">Cloud Preferences</Link>,
        },
        {
          key: '/configuration/business-constraints',
          icon: <CalendarOutlined />,
          label: <Link to="/configuration/business-constraints">Business Constraints</Link>,
        },
        {
          key: '/configuration/resource-rates',
          icon: <TeamOutlined />,
          label: <Link to="/configuration/resource-rates">Resource Rates</Link>,
        },
      ],
    },
    {
      key: 'analysis',
      icon: <BarChartOutlined />,
      label: 'Analysis & Planning',
      children: [
        {
          key: '/analysis/cost-estimation',
          icon: <DollarOutlined />,
          label: <Link to="/analysis/cost-estimation">Cost Estimation</Link>,
        },
        {
          key: '/analysis/migration-strategy',
          icon: <RocketOutlined />,
          label: <Link to="/analysis/migration-strategy">Migration Strategy</Link>,
        },
        {
          key: '/analysis/timeline',
          icon: <ScheduleOutlined />,
          label: <Link to="/analysis/timeline">Timeline</Link>,
        },
      ],
    },
    {
      key: 'reports',
      icon: <FileTextOutlined />,
      label: 'Reports',
      children: [
        {
          key: '/reports/export',
          icon: <ExportOutlined />,
          label: <Link to="/reports/export">Export Reports</Link>,
        },
      ],
    },
  ];

  return (
    <Sider
      collapsible
      collapsed={collapsed}
      onCollapse={(value) => setCollapsed(value)}
      theme="dark"
      width={260}
    >
      <div style={{ 
        height: 32, 
        margin: 16, 
        background: 'rgba(255, 255, 255, 0.3)',
        borderRadius: 6,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'white',
        fontWeight: 'bold',
        fontSize: collapsed ? '12px' : '14px'
      }}>
        {collapsed ? 'CMT' : 'Cloud Migration Tool'}
      </div>
      <Menu
        theme="dark"
        selectedKeys={[location.pathname]}
        mode="inline"
        items={menuItems}
        style={{ borderRight: 0 }}
      />
    </Sider>
  );
};

export default Sidebar;
