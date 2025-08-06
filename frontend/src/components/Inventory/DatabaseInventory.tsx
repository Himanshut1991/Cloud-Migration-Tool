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
  Switch,
  Row,
  Col,
  Statistic,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, DatabaseOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title } = Typography;
const { Option } = Select;

interface Database {
  id?: number;
  db_name: string;
  db_type: string;
  size_gb: number;
  server_id: string;
  backup_frequency: string;
  ha_dr_required: number;
  licensing_model: string;
  write_frequency: string;
  downtime_tolerance: string;
  real_time_sync: number;
  created_at?: string;
  updated_at?: string;
}

const DatabaseInventory: React.FC = () => {
  const [databases, setDatabases] = useState<Database[]>([]);
  const [servers, setServers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingDatabase, setEditingDatabase] = useState<Database | null>(null);
  const [form] = Form.useForm();

  const API_BASE_URL = 'http://127.0.0.1:5000/api';

  useEffect(() => {
    fetchDatabases();
    fetchServers();
  }, []);

  const fetchServers = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/servers`);
      if (response.ok) {
        const data = await response.json();
        const servers = data.servers || data || [];
        setServers(servers);
        console.log('✅ DatabaseInventory: Fetched servers for dropdown:', servers.length);
      } else {
        console.warn('⚠️ DatabaseInventory: Failed to fetch servers for dropdown');
      }
    } catch (error) {
      console.error('❌ DatabaseInventory: Error fetching servers:', error);
    }
  };

  const fetchDatabases = async () => {
    console.log('🔄 DatabaseInventory: Starting to fetch databases...');
    try {
      const urls = [
        'http://127.0.0.1:5000/api/databases',
        'http://localhost:5000/api/databases',
        `${window.location.protocol}//${window.location.hostname}:5000/api/databases`
      ];
      
      let response: Response | null = null;
      let data: any = null;
      
      for (const url of urls) {
        try {
          console.log(`🌐 DatabaseInventory: Trying URL: ${url}`);
          const currentResponse = await fetch(url);
          console.log(`📡 DatabaseInventory: Response status for ${url}: ${currentResponse.status}`);
          
          if (currentResponse.ok) {
            response = currentResponse;
            data = await currentResponse.json();
            console.log(`✅ DatabaseInventory: Success with ${url}:`, data);
            break;
          }
        } catch (urlError) {
          console.log(`❌ DatabaseInventory: Failed with ${url}:`, (urlError as Error).message);
          continue;
        }
      }
      
      if (!response || !response.ok || !data) {
        throw new Error('All URLs failed');
      }
      
      let databases: Database[] = [];
      if (data && typeof data === 'object' && data.databases && Array.isArray(data.databases)) {
        databases = data.databases;
        console.log(`✅ DatabaseInventory: Found databases array with ${databases.length} items`);
      } else if (Array.isArray(data)) {
        databases = data;
        console.log(`✅ DatabaseInventory: Data is direct array with ${databases.length} items`);
      } else {
        console.warn('⚠️ DatabaseInventory: Unexpected data format:', data);
        console.warn('⚠️ DatabaseInventory: Data type:', typeof data);
        if (data && typeof data === 'object') {
          console.warn('⚠️ DatabaseInventory: Data keys:', Object.keys(data));
        }
        databases = [];
      }
      
      console.log(`🎯 DatabaseInventory: Setting ${databases.length} databases to state`);
      setDatabases(databases);
      
    } catch (error) {
      console.error('❌ DatabaseInventory: Error:', error);
      message.error(`Failed to fetch databases: ${(error as Error).message}`);
      setDatabases([]);
    } finally {
      setLoading(false);
      console.log('🏁 DatabaseInventory: Fetch completed');
    }
  };

  const handleSubmit = async (values: any) => {
    console.log('🔄 DatabaseInventory: Form submission started');
    console.log('📝 DatabaseInventory: Form values:', values);
    console.log('✏️ DatabaseInventory: Editing database:', editingDatabase);
    
    try {
      if (editingDatabase) {
        console.log(`🌐 DatabaseInventory: Updating database ${editingDatabase.id}`);
        const response = await axios.put(`${API_BASE_URL}/databases/${editingDatabase.id}`, values);
        console.log('✅ DatabaseInventory: Update successful:', response.data);
        message.success('Database updated successfully');
      } else {
        console.log('🌐 DatabaseInventory: Creating new database');
        const response = await axios.post(`${API_BASE_URL}/databases`, values);
        console.log('✅ DatabaseInventory: Creation successful:', response.data);
        message.success('Database created successfully');
      }
      setModalVisible(false);
      setEditingDatabase(null);
      form.resetFields();
      await fetchDatabases();
    } catch (error: any) {
      console.error('❌ DatabaseInventory: Error saving database:', error);
      console.error('❌ DatabaseInventory: Error response:', error.response?.data);
      console.error('❌ DatabaseInventory: Error status:', error.response?.status);
      message.error(`Failed to ${editingDatabase ? 'update' : 'create'} database: ${error.response?.data?.error || error.message}`);
    }
  };

  const handleEdit = (database: Database) => {
    setEditingDatabase(database);
    form.setFieldsValue(database);
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`${API_BASE_URL}/databases/${id}`);
      message.success('Database deleted successfully');
      fetchDatabases();
    } catch (error) {
      message.error('Failed to delete database');
      console.error('Error deleting database:', error);
    }
  };

  const columns = [
    {
      title: 'Database Name',
      dataIndex: 'db_name',
      key: 'db_name',
      render: (text: string) => (
        <Space>
          <DatabaseOutlined />
          <strong>{text}</strong>
        </Space>
      ),
    },
    {
      title: 'Type',
      dataIndex: 'db_type',
      key: 'db_type',
    },
    {
      title: 'Size (GB)',
      dataIndex: 'size_gb',
      key: 'size_gb',
      sorter: (a: Database, b: Database) => a.size_gb - b.size_gb,
      render: (size: number) => `${size} GB`,
    },
    {
      title: 'Server',
      dataIndex: 'server_id',
      key: 'server_id',
    },
    {
      title: 'Backup Frequency',
      dataIndex: 'backup_frequency',
      key: 'backup_frequency',
    },
    {
      title: 'HA/DR Required',
      dataIndex: 'ha_dr_required',
      key: 'ha_dr_required',
      render: (required: number) => required ? '✅' : '❌',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Database) => (
        <Space>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure to delete this database?"
            onConfirm={() => handleDelete(record.id!)}
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

  const getDatabaseStats = () => {
    const totalDatabases = databases.length;
    const totalSize = databases.reduce((sum, db) => sum + db.size_gb, 0);
    const hadrEnabled = databases.filter(db => db.ha_dr_required).length;
    const realTimeSyncEnabled = databases.filter(db => db.real_time_sync).length;
    
    return { totalDatabases, totalSize, hadrEnabled, realTimeSyncEnabled };
  };

  const stats = getDatabaseStats();

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={2}>Database Inventory</Title>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingDatabase(null);
              form.resetFields();
              setModalVisible(true);
            }}
          >
            Add Database
          </Button>
        </div>

        <Row gutter={16} style={{ marginBottom: 16 }}>
          <Col span={6}>
            <Statistic title="Total Databases" value={stats.totalDatabases} />
          </Col>
          <Col span={6}>
            <Statistic title="Total Size (GB)" value={stats.totalSize} />
          </Col>
          <Col span={6}>
            <Statistic title="HA/DR Enabled" value={`${stats.hadrEnabled}/${stats.totalDatabases}`} />
          </Col>
          <Col span={6}>
            <Statistic title="Real-time Sync" value={`${stats.realTimeSyncEnabled}/${stats.totalDatabases}`} />
          </Col>
        </Row>

        <Table
          dataSource={databases}
          columns={columns}
          rowKey="id"
          loading={loading}
          scroll={{ x: 1200 }}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} databases`,
          }}
        />
      </Card>

      <Modal
        title={editingDatabase ? 'Edit Database' : 'Add Database'}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          setEditingDatabase(null);
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
            name="db_name"
            label="Database Name"
            rules={[{ required: true, message: 'Please input database name!' }]}
          >
            <Input placeholder="e.g., AppDB, CustomerDB, FinanceDB" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="db_type"
                label="Database Type"
                rules={[{ required: true, message: 'Please select database type!' }]}
              >
                <Select placeholder="Select database type">
                  <Option value="MySQL">MySQL</Option>
                  <Option value="PostgreSQL">PostgreSQL</Option>
                  <Option value="SQL Server">SQL Server</Option>
                  <Option value="Oracle">Oracle</Option>
                  <Option value="MongoDB">MongoDB</Option>
                  <Option value="Redis">Redis</Option>
                  <Option value="Other">Other</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="size_gb"
                label="Size (GB)"
                rules={[{ required: true, message: 'Please input size!' }]}
              >
                <InputNumber min={1} max={100000} placeholder="100" style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="server_id"
                label="Server"
                rules={[{ required: true, message: 'Please select a server!' }]}
              >
                <Select placeholder="Select server">
                  {servers.map(server => (
                    <Option key={server.server_id} value={server.server_id}>
                      {server.server_id} ({server.os_type})
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="backup_frequency"
                label="Backup Frequency"
                rules={[{ required: true, message: 'Please select backup frequency!' }]}
              >
                <Select placeholder="Select backup frequency">
                  <Option value="Hourly">Hourly</Option>
                  <Option value="Daily">Daily</Option>
                  <Option value="Weekly">Weekly</Option>
                  <Option value="Monthly">Monthly</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="licensing_model"
                label="Licensing Model"
              >
                <Select placeholder="Select licensing model">
                  <Option value="Open Source">Open Source</Option>
                  <Option value="Commercial">Commercial</Option>
                  <Option value="Enterprise">Enterprise</Option>
                  <Option value="Per Core">Per Core</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="write_frequency"
                label="Write Frequency"
              >
                <Select placeholder="Select write frequency">
                  <Option value="High">High</Option>
                  <Option value="Medium">Medium</Option>
                  <Option value="Low">Low</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="downtime_tolerance"
                label="Downtime Tolerance"
              >
                <Select placeholder="Select tolerance">
                  <Option value="High">High</Option>
                  <Option value="Medium">Medium</Option>
                  <Option value="Low">Low</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="ha_dr_required"
                label="HA/DR Required"
                valuePropName="checked"
              >
                <Switch />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="real_time_sync"
                label="Real-time Sync Required"
                valuePropName="checked"
              >
                <Switch />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit">
                {editingDatabase ? 'Update' : 'Add'} Database
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DatabaseInventory;
