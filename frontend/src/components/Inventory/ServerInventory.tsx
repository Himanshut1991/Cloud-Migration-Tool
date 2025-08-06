import React, { useState, useEffect } from 'react';
import {
  Table,
  Button,
  Space,
  Modal,
  Form,
  Input,
  Select,
  InputNumber,
  message,
  Popconfirm,
  Typography,
  Card,
  Tag,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, DesktopOutlined } from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

interface Server {
  id: number;
  server_id: string;
  os_type: string;
  vcpu: number;
  ram: number;
  disk_size: number;
  disk_type: string;
  uptime_pattern: string;
  current_hosting: string;
  technology: string;
  technology_version: string;
  created_at: string;
  updated_at?: string;
}

const ServerInventory: React.FC = () => {
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingServer, setEditingServer] = useState<Server | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchServers();
  }, []);

  const fetchServers = async () => {
    console.log('🔄 ServerInventory: Starting to fetch servers...');
    try {
      // Try multiple URLs to see which one works
      const urls = [
        'http://127.0.0.1:5000/api/servers',
        'http://localhost:5000/api/servers',
        `${window.location.protocol}//${window.location.hostname}:5000/api/servers`
      ];
      
      let response: Response | null = null;
      let data: any = null;
      
      for (const url of urls) {
        try {
          console.log(`🌐 ServerInventory: Trying URL: ${url}`);
          const currentResponse = await fetch(url);
          console.log(`📡 ServerInventory: Response status for ${url}: ${currentResponse.status}`);
          
          if (currentResponse.ok) {
            response = currentResponse;
            data = await currentResponse.json();
            console.log(`✅ ServerInventory: Success with ${url}:`, data);
            break;
          }
        } catch (urlError) {
          console.log(`❌ ServerInventory: Failed with ${url}:`, (urlError as Error).message);
          continue;
        }
      }
      
      if (!response || !response.ok || !data) {
        throw new Error('All URLs failed');
      }
      
      // Backend returns {servers: [...]} or possibly just [...]
      let servers: Server[] = [];
      if (data && typeof data === 'object' && data.servers && Array.isArray(data.servers)) {
        servers = data.servers;
        console.log(`✅ ServerInventory: Found servers array with ${servers.length} items`);
      } else if (Array.isArray(data)) {
        servers = data;
        console.log(`✅ ServerInventory: Data is direct array with ${servers.length} items`);
      } else {
        console.warn('⚠️ ServerInventory: Unexpected data format:', data);
        console.warn('⚠️ ServerInventory: Data type:', typeof data);
        if (data && typeof data === 'object') {
          console.warn('⚠️ ServerInventory: Data keys:', Object.keys(data));
        }
        servers = [];
      }
      
      console.log(`🎯 ServerInventory: Setting ${servers.length} servers to state`);
      setServers(servers);
      
    } catch (error) {
      console.error('❌ ServerInventory: Error:', error);
      message.error(`Failed to fetch servers: ${error.message}`);
      setServers([]);
    } finally {
      setLoading(false);
      console.log('🏁 ServerInventory: Fetch completed');
    }
  };

  const handleSubmit = async (values: any) => {
    console.log('🔄 ServerInventory: Form submission started');
    console.log('📝 ServerInventory: Form values:', values);
    console.log('✏️ ServerInventory: Editing server:', editingServer);
    
    try {
      const url = editingServer 
        ? `http://127.0.0.1:5000/api/servers/${editingServer.id}`
        : 'http://127.0.0.1:5000/api/servers';
      
      const method = editingServer ? 'PUT' : 'POST';
      
      console.log(`🌐 ServerInventory: Sending ${method} request to ${url}`);
      console.log('📦 ServerInventory: Request body:', JSON.stringify(values));
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });

      console.log(`📡 ServerInventory: Response status: ${response.status}`);
      console.log(`📡 ServerInventory: Response headers:`, response.headers);
      
      const responseText = await response.text();
      console.log(`📄 ServerInventory: Response text: ${responseText}`);

      if (response.ok) {
        console.log('✅ ServerInventory: Request successful');
        message.success(`Server ${editingServer ? 'updated' : 'added'} successfully`);
        setModalVisible(false);
        setEditingServer(null);
        form.resetFields();
        await fetchServers();
      } else {
        console.log('❌ ServerInventory: Request failed');
        message.error(`Failed to save server: ${response.status} - ${responseText}`);
      }
    } catch (error) {
      console.error('❌ ServerInventory: Error in handleSubmit:', error);
      message.error(`Failed to save server: ${(error as Error).message}`);
    }
  };

  const handleEdit = (server: Server) => {
    setEditingServer(server);
    form.setFieldsValue(server);
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/servers/${id}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        message.success('Server deleted successfully');
        fetchServers();
      } else {
        message.error('Failed to delete server');
      }
    } catch (error) {
      message.error('Failed to delete server');
    }
  };

  const columns = [
    {
      title: 'Server ID',
      dataIndex: 'server_id',
      key: 'server_id',
      render: (text: string) => (
        <Space>
          <DesktopOutlined />
          <strong>{text}</strong>
        </Space>
      ),
    },
    {
      title: 'OS Type',
      dataIndex: 'os_type',
      key: 'os_type',
      render: (text: string) => (
        <Tag color={text.toLowerCase().includes('windows') ? 'blue' : 'green'}>
          {text}
        </Tag>
      ),
    },
    {
      title: 'vCPU',
      dataIndex: 'vcpu',
      key: 'vcpu',
      sorter: (a: Server, b: Server) => a.vcpu - b.vcpu,
    },
    {
      title: 'RAM (GB)',
      dataIndex: 'ram',
      key: 'ram',
      sorter: (a: Server, b: Server) => a.ram - b.ram,
    },
    {
      title: 'Disk Size (GB)',
      dataIndex: 'disk_size',
      key: 'disk_size',
      sorter: (a: Server, b: Server) => a.disk_size - b.disk_size,
    },
    {
      title: 'Disk Type',
      dataIndex: 'disk_type',
      key: 'disk_type',
      render: (text: string) => (
        <Tag color={text === 'SSD' ? 'green' : 'blue'}>
          {text}
        </Tag>
      ),
    },
    {
      title: 'Current Hosting',
      dataIndex: 'current_hosting',
      key: 'current_hosting',
    },
    {
      title: 'Technology',
      dataIndex: 'technology',
      key: 'technology',
      render: (text: string, record: Server) => (
        <span>{text} {record.technology_version}</span>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Server) => (
        <Space>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure to delete this server?"
            onConfirm={() => handleDelete(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              Delete
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={2}>Server Inventory</Title>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingServer(null);
              form.resetFields();
              setModalVisible(true);
            }}
          >
            Add Server
          </Button>
        </div>

        <Table
          dataSource={servers}
          columns={columns}
          rowKey="id"
          loading={loading}
          scroll={{ x: 1200 }}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} servers`,
          }}
        />
      </Card>

      <Modal
        title={editingServer ? 'Edit Server' : 'Add Server'}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          setEditingServer(null);
          form.resetFields();
        }}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Form.Item
            name="server_id"
            label="Server ID"
            rules={[{ required: true, message: 'Please input server ID!' }]}
          >
            <Input placeholder="e.g., SRV-001, APP-SVR-01" />
          </Form.Item>

          <Form.Item
            name="os_type"
            label="Operating System"
            rules={[{ required: true, message: 'Please select OS!' }]}
          >
            <Select placeholder="Select OS">
              <Option value="Windows Server 2019">Windows Server 2019</Option>
              <Option value="Windows Server 2016">Windows Server 2016</Option>
              <Option value="Windows Server 2012 R2">Windows Server 2012 R2</Option>
              <Option value="Ubuntu 20.04">Ubuntu 20.04</Option>
              <Option value="Ubuntu 18.04">Ubuntu 18.04</Option>
              <Option value="CentOS 7">CentOS 7</Option>
              <Option value="CentOS 8">CentOS 8</Option>
              <Option value="RHEL 7">RHEL 7</Option>
              <Option value="RHEL 8">RHEL 8</Option>
            </Select>
          </Form.Item>

          <div style={{ display: 'flex', gap: 16 }}>
            <Form.Item
              name="vcpu"
              label="vCPU"
              rules={[{ required: true, message: 'Please input vCPU!' }]}
              style={{ flex: 1 }}
            >
              <InputNumber min={1} max={64} placeholder="4" style={{ width: '100%' }} />
            </Form.Item>

            <Form.Item
              name="ram"
              label="RAM (GB)"
              rules={[{ required: true, message: 'Please input RAM!' }]}
              style={{ flex: 1 }}
            >
              <InputNumber min={1} max={1024} placeholder="16" style={{ width: '100%' }} />
            </Form.Item>
          </div>

          <div style={{ display: 'flex', gap: 16 }}>
            <Form.Item
              name="disk_size"
              label="Disk Size (GB)"
              rules={[{ required: true, message: 'Please input disk size!' }]}
              style={{ flex: 1 }}
            >
              <InputNumber min={1} max={10000} placeholder="500" style={{ width: '100%' }} />
            </Form.Item>

            <Form.Item
              name="disk_type"
              label="Disk Type"
              rules={[{ required: true, message: 'Please select disk type!' }]}
              style={{ flex: 1 }}
            >
              <Select placeholder="Select disk type">
                <Option value="SSD">SSD</Option>
                <Option value="HDD">HDD</Option>
                <Option value="NVMe">NVMe</Option>
              </Select>
            </Form.Item>
          </div>

          <Form.Item
            name="uptime_pattern"
            label="Uptime Pattern"
            rules={[{ required: true, message: 'Please input uptime pattern!' }]}
          >
            <Select placeholder="Select uptime pattern">
              <Option value="24x7">24x7</Option>
              <Option value="Business Hours">Business Hours</Option>
              <Option value="Variable">Variable</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="current_hosting"
            label="Current Hosting"
            rules={[{ required: true, message: 'Please input current hosting!' }]}
          >
            <Select placeholder="Select hosting">
              <Option value="On-Premise">On-Premise</Option>
              <Option value="Colocation">Colocation</Option>
              <Option value="Hybrid Cloud">Hybrid Cloud</Option>
              <Option value="Public Cloud">Public Cloud</Option>
            </Select>
          </Form.Item>

          <div style={{ display: 'flex', gap: 16 }}>
            <Form.Item
              name="technology"
              label="Technology"
              rules={[{ required: true, message: 'Please input technology!' }]}
              style={{ flex: 1 }}
            >
              <Input placeholder="e.g., Web Server, Database, Application" />
            </Form.Item>

            <Form.Item
              name="technology_version"
              label="Technology Version"
              rules={[{ required: true, message: 'Please input version!' }]}
              style={{ flex: 1 }}
            >
              <Input placeholder="e.g., 1.0, 2.1" />
            </Form.Item>
          </div>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit">
                {editingServer ? 'Update' : 'Add'} Server
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ServerInventory;
