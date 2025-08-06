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
import { PlusOutlined, EditOutlined, DeleteOutlined, FolderOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title } = Typography;
const { Option } = Select;

interface FileShare {
  id?: number;
  share_name: string;
  total_size_gb: number;
  access_pattern: string;
  snapshot_required: number;
  retention_days: number;
  server_id: string;
  write_frequency: string;
  downtime_tolerance: string;
  real_time_sync: number;
  created_at?: string;
  updated_at?: string;
}

const FileShareInventory: React.FC = () => {
  const [fileShares, setFileShares] = useState<FileShare[]>([]);
  const [servers, setServers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingFileShare, setEditingFileShare] = useState<FileShare | null>(null);
  const [form] = Form.useForm();

  const API_BASE_URL = 'http://127.0.0.1:5000/api';

  useEffect(() => {
    fetchFileShares();
    fetchServers();
  }, []);

  const fetchServers = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/servers`);
      if (response.ok) {
        const data = await response.json();
        const servers = data.servers || data || [];
        setServers(servers);
        console.log('✅ FileShareInventory: Fetched servers for dropdown:', servers.length);
      } else {
        console.warn('⚠️ FileShareInventory: Failed to fetch servers for dropdown');
      }
    } catch (error) {
      console.error('❌ FileShareInventory: Error fetching servers:', error);
    }
  };

  const fetchFileShares = async () => {
    console.log('🔄 FileShareInventory: Starting to fetch file shares...');
    try {
      const urls = [
        'http://127.0.0.1:5000/api/file-shares',
        'http://localhost:5000/api/file-shares',
        `${window.location.protocol}//${window.location.hostname}:5000/api/file-shares`
      ];
      
      let response: Response | null = null;
      let data: any = null;
      
      for (const url of urls) {
        try {
          console.log(`🌐 FileShareInventory: Trying URL: ${url}`);
          const currentResponse = await fetch(url);
          console.log(`📡 FileShareInventory: Response status for ${url}: ${currentResponse.status}`);
          
          if (currentResponse.ok) {
            response = currentResponse;
            data = await currentResponse.json();
            console.log(`✅ FileShareInventory: Success with ${url}:`, data);
            break;
          }
        } catch (urlError) {
          console.log(`❌ FileShareInventory: Failed with ${url}:`, (urlError as Error).message);
          continue;
        }
      }
      
      if (!response || !response.ok || !data) {
        throw new Error('All URLs failed');
      }
      
      let fileShares: FileShare[] = [];
      if (data && typeof data === 'object' && data.file_shares && Array.isArray(data.file_shares)) {
        fileShares = data.file_shares;
        console.log(`✅ FileShareInventory: Found file_shares array with ${fileShares.length} items`);
      } else if (Array.isArray(data)) {
        fileShares = data;
        console.log(`✅ FileShareInventory: Data is direct array with ${fileShares.length} items`);
      } else {
        console.warn('⚠️ FileShareInventory: Unexpected data format:', data);
        console.warn('⚠️ FileShareInventory: Data type:', typeof data);
        if (data && typeof data === 'object') {
          console.warn('⚠️ FileShareInventory: Data keys:', Object.keys(data));
        }
        fileShares = [];
      }
      
      console.log(`🎯 FileShareInventory: Setting ${fileShares.length} file shares to state`);
      setFileShares(fileShares);
      
    } catch (error) {
      console.error('❌ FileShareInventory: Error:', error);
      message.error(`Failed to fetch file shares: ${(error as Error).message}`);
      setFileShares([]);
    } finally {
      setLoading(false);
      console.log('🏁 FileShareInventory: Fetch completed');
    }
  };

  const handleSubmit = async (values: any) => {
    console.log('🔄 FileShareInventory: Form submission started');
    console.log('📝 FileShareInventory: Form values:', values);
    console.log('✏️ FileShareInventory: Editing file share:', editingFileShare);
    
    try {
      if (editingFileShare) {
        console.log(`🌐 FileShareInventory: Updating file share ${editingFileShare.id}`);
        const response = await axios.put(`${API_BASE_URL}/file-shares/${editingFileShare.id}`, values);
        console.log('✅ FileShareInventory: Update successful:', response.data);
        message.success('File share updated successfully');
      } else {
        console.log('🌐 FileShareInventory: Creating new file share');
        const response = await axios.post(`${API_BASE_URL}/file-shares`, values);
        console.log('✅ FileShareInventory: Creation successful:', response.data);
        message.success('File share created successfully');
      }
      setModalVisible(false);
      setEditingFileShare(null);
      form.resetFields();
      await fetchFileShares();
    } catch (error: any) {
      console.error('❌ FileShareInventory: Error saving file share:', error);
      console.error('❌ FileShareInventory: Error response:', error.response?.data);
      console.error('❌ FileShareInventory: Error status:', error.response?.status);
      message.error(`Failed to ${editingFileShare ? 'update' : 'create'} file share: ${error.response?.data?.error || error.message}`);
    }
  };

  const handleEdit = (fileShare: FileShare) => {
    setEditingFileShare(fileShare);
    form.setFieldsValue(fileShare);
    setModalVisible(true);
  };

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`${API_BASE_URL}/file-shares/${id}`);
      message.success('File share deleted successfully');
      fetchFileShares();
    } catch (error) {
      message.error('Failed to delete file share');
      console.error('Error deleting file share:', error);
    }
  };

  const columns = [
    {
      title: 'Share Name',
      dataIndex: 'share_name',
      key: 'share_name',
      render: (text: string) => (
        <Space>
          <FolderOutlined />
          <strong>{text}</strong>
        </Space>
      ),
    },
    {
      title: 'Size (GB)',
      dataIndex: 'total_size_gb',
      key: 'total_size_gb',
      sorter: (a: FileShare, b: FileShare) => a.total_size_gb - b.total_size_gb,
      render: (size: number) => `${size} GB`,
    },
    {
      title: 'Server',
      dataIndex: 'server_id',
      key: 'server_id',
    },
    {
      title: 'Access Pattern',
      dataIndex: 'access_pattern',
      key: 'access_pattern',
    },
    {
      title: 'Retention (Days)',
      dataIndex: 'retention_days',
      key: 'retention_days',
      render: (days: number) => `${days} days`,
    },
    {
      title: 'Snapshot Required',
      dataIndex: 'snapshot_required',
      key: 'snapshot_required',
      render: (required: number) => required ? '✅' : '❌',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: FileShare) => (
        <Space>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure to delete this file share?"
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

  const getFileShareStats = () => {
    const totalShares = fileShares.length;
    const totalSize = fileShares.reduce((sum, fs) => sum + fs.total_size_gb, 0);
    const snapshotEnabled = fileShares.filter(fs => fs.snapshot_required).length;
    const realTimeSyncEnabled = fileShares.filter(fs => fs.real_time_sync).length;
    
    return { totalShares, totalSize, snapshotEnabled, realTimeSyncEnabled };
  };

  const stats = getFileShareStats();

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={2}>File Share Inventory</Title>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => {
              setEditingFileShare(null);
              form.resetFields();
              setModalVisible(true);
            }}
          >
            Add File Share
          </Button>
        </div>

        <Row gutter={16} style={{ marginBottom: 16 }}>
          <Col span={6}>
            <Statistic title="Total File Shares" value={stats.totalShares} />
          </Col>
          <Col span={6}>
            <Statistic title="Total Size (GB)" value={stats.totalSize} />
          </Col>
          <Col span={6}>
            <Statistic title="Snapshot Enabled" value={`${stats.snapshotEnabled}/${stats.totalShares}`} />
          </Col>
          <Col span={6}>
            <Statistic title="Real-time Sync" value={`${stats.realTimeSyncEnabled}/${stats.totalShares}`} />
          </Col>
        </Row>

        <Table
          dataSource={fileShares}
          columns={columns}
          rowKey="id"
          loading={loading}
          scroll={{ x: 1200 }}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} file shares`,
          }}
        />
      </Card>

      <Modal
        title={editingFileShare ? 'Edit File Share' : 'Add File Share'}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          setEditingFileShare(null);
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
            name="share_name"
            label="Share Name"
            rules={[{ required: true, message: 'Please input share name!' }]}
          >
            <Input placeholder="e.g., FileServer01, SharedDocs" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="total_size_gb"
                label="Total Size (GB)"
                rules={[{ required: true, message: 'Please input size!' }]}
              >
                <InputNumber min={1} max={10000} placeholder="500" style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="retention_days"
                label="Retention (Days)"
              >
                <InputNumber min={1} placeholder="30" style={{ width: '100%' }} />
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
                name="access_pattern"
                label="Access Pattern"
                rules={[{ required: true, message: 'Please select access pattern!' }]}
              >
                <Select placeholder="Select access pattern">
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
                name="snapshot_required"
                label="Snapshot Required"
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
                {editingFileShare ? 'Update' : 'Add'} File Share
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default FileShareInventory;
