import React, { useState, useEffect } from 'react';
import {
  Card, Table, Button, Modal, Form, Input, Select, InputNumber, Switch,
  Space, Popconfirm, message, Typography, Row, Col, Statistic
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
  snapshot_required: boolean;
  retention_days: number;
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

const FileShareInventory: React.FC = () => {
  const [fileShares, setFileShares] = useState<FileShare[]>([]);
  const [servers, setServers] = useState<Server[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingFileShare, setEditingFileShare] = useState<FileShare | null>(null);
  const [form] = Form.useForm();

  const API_BASE_URL = 'http://127.0.0.1:5000/api';

  // Fetch file shares
  const fetchFileShares = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/file-shares`);
      setFileShares(response.data);
    } catch (error) {
      message.error('Failed to fetch file shares');
      console.error('Error fetching file shares:', error);
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
    fetchFileShares();
    fetchServers();
  }, []);

  // Handle create/update file share
  const handleSubmit = async (values: FileShare) => {
    try {
      console.log('Submitting file share values:', values);
      if (editingFileShare) {
        await axios.put(`${API_BASE_URL}/file-shares/${editingFileShare.id}`, values);
        message.success('File share updated successfully');
      } else {
        await axios.post(`${API_BASE_URL}/file-shares`, values);
        message.success('File share created successfully');
      }
      setModalVisible(false);
      setEditingFileShare(null);
      form.resetFields();
      fetchFileShares();
    } catch (error) {
      message.error(`Failed to ${editingFileShare ? 'update' : 'create'} file share`);
      console.error('Error saving file share:', error);
    }
  };

  // Handle delete file share
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

  // Handle edit file share
  const handleEdit = (fileShare: FileShare) => {
    setEditingFileShare(fileShare);
    form.setFieldsValue(fileShare);
    setModalVisible(true);
  };

  // Handle add new file share
  const handleAdd = () => {
    setEditingFileShare(null);
    form.resetFields();
    setModalVisible(true);
  };

  const columns = [
    {
      title: 'Share Name',
      dataIndex: 'share_name',
      key: 'share_name',
      sorter: (a: FileShare, b: FileShare) => a.share_name.localeCompare(b.share_name),
    },
    {
      title: 'Size (GB)',
      dataIndex: 'total_size_gb',
      key: 'total_size_gb',
      sorter: (a: FileShare, b: FileShare) => a.total_size_gb - b.total_size_gb,
      render: (size: number) => `${size.toLocaleString()} GB`,
    },
    {
      title: 'Access Pattern',
      dataIndex: 'access_pattern',
      key: 'access_pattern',
      filters: [
        { text: 'Hot', value: 'Hot' },
        { text: 'Warm', value: 'Warm' },
        { text: 'Cold', value: 'Cold' },
      ],
      onFilter: (value: any, record: FileShare) => record.access_pattern === value,
    },
    {
      title: 'Write Frequency',
      dataIndex: 'write_frequency',
      key: 'write_frequency',
      filters: [
        { text: 'High', value: 'High' },
        { text: 'Medium', value: 'Medium' },
        { text: 'Low', value: 'Low' },
      ],
      onFilter: (value: any, record: FileShare) => record.write_frequency === value,
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
      title: 'Snapshot Required',
      dataIndex: 'snapshot_required',
      key: 'snapshot_required',
      render: (snapshot: boolean) => snapshot ? 'Yes' : 'No',
      filters: [
        { text: 'Yes', value: true },
        { text: 'No', value: false },
      ],
      onFilter: (value: any, record: FileShare) => record.snapshot_required === value,
    },
    {
      title: 'Retention (Days)',
      dataIndex: 'retention_days',
      key: 'retention_days',
      sorter: (a: FileShare, b: FileShare) => a.retention_days - b.retention_days,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: FileShare) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure you want to delete this file share?"
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
  const totalShares = fileShares.length;
  const totalSize = fileShares.reduce((sum, share) => sum + share.total_size_gb, 0);
  const snapshotCount = fileShares.filter(share => share.snapshot_required).length;
  const rtSyncCount = fileShares.filter(share => share.real_time_sync).length;
  const hotAccessCount = fileShares.filter(share => share.access_pattern === 'Hot').length;

  return (
    <div>
      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total File Shares"
              value={totalShares}
              prefix={<FolderOutlined />}
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
              title="Snapshots Required"
              value={snapshotCount}
              suffix={`/ ${totalShares}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Hot Access Pattern"
              value={hotAccessCount}
              suffix={`/ ${totalShares}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Main Table */}
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={2} style={{ margin: 0 }}>File Share Inventory</Title>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            Add File Share
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={fileShares}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} file shares`,
          }}
        />
      </Card>

      {/* Add/Edit Modal */}
      <Modal
        title={`${editingFileShare ? 'Edit' : 'Add'} File Share`}
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
          initialValues={{
            snapshot_required: false,
            real_time_sync: false,
            write_frequency: 'Medium',
            access_pattern: 'Warm',
            retention_days: 30,
            downtime_tolerance: 'Low',
          }}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="share_name"
                label="Share Name"
                rules={[{ required: true, message: 'Please enter share name' }]}
              >
                <Input placeholder="Enter share name" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="total_size_gb"
                label="Total Size (GB)"
                rules={[{ required: true, message: 'Please enter size' }]}
              >
                <InputNumber
                  min={1}
                  placeholder="Enter size in GB"
                  style={{ width: '100%' }}
                />
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
                  <Option value="High">High</Option>
                  <Option value="Medium">Medium</Option>
                  <Option value="Low">Low</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="access_pattern"
                label="Access Pattern"
                rules={[{ required: true, message: 'Please select access pattern' }]}
              >
                <Select>
                  <Option value="Hot">Hot</Option>
                  <Option value="Warm">Warm</Option>
                  <Option value="Cold">Cold</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="server_id"
                label="Server"
                rules={[{ required: true, message: 'Please select server' }]}
              >
                <Select placeholder="Select server">
                  {servers.map(server => (
                    <Option key={server.server_id} value={server.server_id}>
                      {server.server_id}
                    </Option>
                  ))}
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
                name="retention_days"
                label="Retention Days"
                rules={[{ required: true, message: 'Please enter retention days' }]}
              >
                <InputNumber
                  min={1}
                  placeholder="Enter retention days"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="snapshot_required"
                label="Snapshot Required"
                rules={[{ required: true, message: 'Please select snapshot requirement' }]}
              >
                <Select placeholder="Select snapshot requirement">
                  <Option value={true}>Yes</Option>
                  <Option value={false}>No</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="real_time_sync"
                label="Real-time Sync Required"
                rules={[{ required: true, message: 'Please select sync requirement' }]}
              >
                <Select placeholder="Select sync requirement">
                  <Option value={true}>Yes</Option>
                  <Option value={false}>No</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit">
                {editingFileShare ? 'Update' : 'Create'} File Share
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default FileShareInventory;
