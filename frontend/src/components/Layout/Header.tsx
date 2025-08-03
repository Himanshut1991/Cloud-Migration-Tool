import React from 'react';
import { Layout, Typography, Space, Avatar, Dropdown, Button } from 'antd';
import { UserOutlined, BellOutlined, LogoutOutlined, SettingOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';

const { Header: AntHeader } = Layout;
const { Title } = Typography;

const Header: React.FC = () => {
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: 'Profile',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: 'Settings',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'Logout',
      danger: true,
    },
  ];

  const handleUserMenuClick: MenuProps['onClick'] = (e) => {
    console.log('User menu click', e);
    // Handle user menu actions
  };

  return (
    <AntHeader 
      style={{ 
        padding: '0 24px', 
        background: '#fff', 
        borderBottom: '1px solid #f0f0f0',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}
    >
      <Title level={4} style={{ margin: 0, color: '#1890ff' }}>
        Gen-AI Powered Cloud Migration Planning
      </Title>
      
      <Space size="middle">
        <Button 
          type="text" 
          icon={<BellOutlined />} 
          size="large"
        />
        
        <Dropdown
          menu={{
            items: userMenuItems,
            onClick: handleUserMenuClick,
          }}
          trigger={['click']}
          placement="bottomRight"
        >
          <Space style={{ cursor: 'pointer' }}>
            <Avatar icon={<UserOutlined />} />
            <span>Migration Architect</span>
          </Space>
        </Dropdown>
      </Space>
    </AntHeader>
  );
};

export default Header;
