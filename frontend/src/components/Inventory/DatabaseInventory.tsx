import React, { useState, useEffect } from 'react';
import {
  Card, Table, Button, Modal, Form, Input, Select, InputNumber, Switch,
  Space, Popconfirm, message, Typography, Row, Col, Statistic
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
  ha_dr_required: boolean;
  backup_frequency: string;
  licensing_model: string;
  server_id: string;
  write_frequency: string;
  downtime_tolerance: string;
  real_time_sync: boolean;
  created_at?: string;
  updated_at?: string;
}

interface Server {
  id: number;
  server_id: string;
  os_type: string;
}

const DatabaseInventory: React.FC = () => {
  const [databases, setDatabases] = useState<Database[]>([]);
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingDatabase, setEditingDatabase] = useState<Database | null>(null);
  const [form] = Form.useForm();

  const API_BASE_URL = 'http://127.0.0.1:5000/api';

  // Fetch databases
  const fetchDatabases = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/databases`);
      setDatabases(response.data);
    } catch (error) {
      message.error('Failed to fetch databases');
      console.error('Error fetching databases:', error);
    } finally {
      setLoading(false);
    }
  };

  // Fetch servers for the dropdown
  const fetchServers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/servers`);
      setServers(response.data);
    } catch (error) {
      console.error('Error fetching servers:', error);
    }
  };

  useEffect(() => {
    fetchDatabases();
    fetchServers();
  }, []);

  // Handle create/update database
  const handleSubmit = async (values: Database) => {
    try {
      if (editingDatabase) {
        await axios.put(`${API_BASE_URL}/databases/${editingDatabase.id}`, values);
        message.success('Database updated successfully');
      } else {
        await axios.post(`${API_BASE_URL}/databases`, values);
        message.success('Database created successfully');
      }
      setModalVisible(false);
      setEditingDatabase(null);
      form.resetFields();
      fetchDatabases();
    } catch (error) {
      message.error(`Failed to ${editingDatabase ? 'update' : 'create'} database`);
      console.error('Error saving database:', error);
    }
  };

  // Handle delete database
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

  // Handle edit database
  const handleEdit = (database: Database) => {
    setEditingDatabase(database);
    form.setFieldsValue(database);
    setModalVisible(true);
  };

  // Handle add new database
  const handleAdd = () => {
    setEditingDatabase(null);
    form.resetFields();
    setModalVisible(true);
  };

  const columns = [
    {
      title: 'Database Name',
      dataIndex: 'db_name',
      key: 'db_name',
      sorter: (a: Database, b: Database) => a.db_name.localeCompare(b.db_name),
    },
    {
      title: 'Type',
      dataIndex: 'db_type',
      key: 'db_type',
      filters: [
        { text: 'SQL Server', value: 'SQL Server' },
        { text: 'Oracle', value: 'Oracle' },
        { text: 'MySQL', value: 'MySQL' },
        { text: 'PostgreSQL', value: 'PostgreSQL' },
        { text: 'MongoDB', value: 'MongoDB' },
      ],
      onFilter: (value: any, record: Database) => record.db_type === value,
    },
    {
      title: 'Size (GB)',
      dataIndex: 'size_gb',
      key: 'size_gb',
      sorter: (a: Database, b: Database) => a.size_gb - b.size_gb,
      render: (size: number) => `${size.toLocaleString()} GB`,
    },
    {
      title: 'Server',
      dataIndex: 'server_id',
      key: 'server_id',
      render: (serverId: string) => {
        const server = servers.find(s => s.server_id === serverId);
        return server ? server.server_id : serverId;
      },
    },
    {
      title: 'Write Frequency',
      dataIndex: 'write_frequency',
      key: 'write_frequency',
      filters: [
        { text: 'Low', value: 'Low' },
        { text: 'Medium', value: 'Medium' },
        { text: 'High', value: 'High' },
      ],
      onFilter: (value: any, record: Database) => record.write_frequency === value,
    },
    {
      title: 'HA/DR',
      dataIndex: 'ha_dr_required',
      key: 'ha_dr_required',
      render: (hadr: boolean) => hadr ? 'Yes' : 'No',
      filters: [
        { text: 'Yes', value: true },
        { text: 'No', value: false },
      ],
      onFilter: (value: any, record: Database) => record.ha_dr_required === value,
    },
    {
      title: 'Backup Frequency',
      dataIndex: 'backup_frequency',
      key: 'backup_frequency',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Database) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure you want to delete this database?"
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

  // Calculate statistics
  const totalDatabases = databases.length;
  const totalSize = databases.reduce((sum, db) => sum + db.size_gb, 0);
  const hadrCount = databases.filter(db => db.ha_dr_required).length;
  const rtSyncCount = databases.filter(db => db.real_time_sync).length;

  return (
    <div>
      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Databases"
              value={totalDatabases}
              prefix={<DatabaseOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Size"
              value={totalSize}
              suffix="GB"
              formatter={(value) => `${Number(value).toLocaleString()}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="HA/DR Required"
              value={hadrCount}
              suffix={`/ ${totalDatabases}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Real-time Sync"
              value={rtSyncCount}
              suffix={`/ ${totalDatabases}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Main Table */}
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={2} style={{ margin: 0 }}>Database Inventory</Title>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            Add Database
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={databases}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} databases`,
          }}
        />
      </Card>

      {/* Add/Edit Modal */}
      <Modal
        title={`${editingDatabase ? 'Edit' : 'Add'} Database`}
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
          initialValues={{
            ha_dr_required: false,
            real_time_sync: false,
            write_frequency: 'Medium',
            backup_frequency: 'Daily',
            licensing_model: 'Standard',
            downtime_tolerance: 'Low',
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="db_name"
                label="Database Name"
                rules={[{ required: true, message: 'Please enter database name' }]}
              >
                <Input placeholder="Enter database name" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="db_type"
                label="Database Type"
                rules={[{ required: true, message: 'Please select database type' }]}
              >
                <Select placeholder="Select database type">
                  <Option value="SQL Server">SQL Server</Option>
                  <Option value="Oracle">Oracle</Option>
                  <Option value="MySQL">MySQL</Option>
                  <Option value="PostgreSQL">PostgreSQL</Option>
                  <Option value="MongoDB">MongoDB</Option>
                  <Option value="Redis">Redis</Option>
                  <Option value="Cassandra">Cassandra</Option>
                  <Option value="Other">Other</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="size_gb"
                label="Size (GB)"
                rules={[{ required: true, message: 'Please enter database size' }]}
              >
                <InputNumber
                  min={1}
                  placeholder="Enter size in GB"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="server_id"
                label="Server"
                rules={[{ required: true, message: 'Please select server' }]}
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
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="write_frequency"
                label="Write Frequency"
                rules={[{ required: true, message: 'Please select write frequency' }]}
              >
                <Select>
                  <Option value="Low">Low</Option>
                  <Option value="Medium">Medium</Option>
                  <Option value="High">High</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="backup_frequency"
                label="Backup Frequency"
                rules={[{ required: true, message: 'Please select backup frequency' }]}
              >
                <Select>
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
                rules={[{ required: true, message: 'Please select licensing model' }]}
              >
                <Select>
                  <Option value="Standard">Standard</Option>
                  <Option value="Enterprise">Enterprise</Option>
                  <Option value="Express">Express</Option>
                  <Option value="BYOL">BYOL (Bring Your Own License)</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="downtime_tolerance"
                label="Downtime Tolerance"
                rules={[{ required: true, message: 'Please select downtime tolerance' }]}
              >
                <Select>
                  <Option value="None">None (0 min)</Option>
                  <Option value="Low">Low (&lt; 15 min)</Option>
                  <Option value="Medium">Medium (&lt; 1 hour)</Option>
                  <Option value="High">High (&gt; 1 hour)</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="ha_dr_required" valuePropName="checked">
                <Switch /> HA/DR Required
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="real_time_sync" valuePropName="checked">
                <Switch /> Real-time Synchronization
              </Form.Item>
            </Col>
          </Row>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit">
                {editingDatabase ? 'Update' : 'Create'} Database
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DatabaseInventory;
