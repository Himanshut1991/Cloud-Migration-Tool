import React, { useState, useEffect } from 'react';
import {
  Card, Table, Button, Modal, Form, Input, Select, InputNumber,
  Space, Popconfirm, message, Typography, Row, Col, Statistic, Divider
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, DollarOutlined, TeamOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { Option } = Select;

interface ResourceRate {
  id?: number;
  role: string;
  duration_weeks: number;
  hours_per_week: number;
  rate_per_hour: number;
  created_at?: string;
  updated_at?: string;
}

const ResourceRates: React.FC = () => {
  const [resourceRates, setResourceRates] = useState<ResourceRate[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingRate, setEditingRate] = useState<ResourceRate | null>(null);
  const [form] = Form.useForm();
  const [previewCost, setPreviewCost] = useState<number>(0);

  const API_BASE_URL = 'http://127.0.0.1:5000/api';

  // Predefined roles with typical rates
  const predefinedRoles = [
    { role: 'Cloud Architect', defaultRate: 175, description: 'Senior level cloud architecture and strategy' },
    { role: 'Migration Engineer', defaultRate: 145, description: 'Technical migration execution and troubleshooting' },
    { role: 'DevOps Engineer', defaultRate: 135, description: 'CI/CD, automation, and infrastructure setup' },
    { role: 'Database Specialist', defaultRate: 155, description: 'Database migration and optimization' },
    { role: 'Security Engineer', defaultRate: 165, description: 'Security assessment and implementation' },
    { role: 'Project Manager', defaultRate: 125, description: 'Project coordination and stakeholder management' },
    { role: 'Cloud Consultant', defaultRate: 185, description: 'Strategic consulting and best practices' },
    { role: 'Application Developer', defaultRate: 115, description: 'Application modification and testing' },
    { role: 'Infrastructure Engineer', defaultRate: 125, description: 'Network and infrastructure configuration' },
    { role: 'QA Engineer', defaultRate: 95, description: 'Testing and quality assurance' }
  ];

  // Fetch resource rates
  const fetchResourceRates = async () => {
    console.log('🔄 ResourceRates: Starting to fetch resource rates...');
    setLoading(true);
    try {
      // Try multiple URLs to see which one works
      const urls = [
        'http://127.0.0.1:5000/api/resource-rates',
        'http://localhost:5000/api/resource-rates',
        `${window.location.protocol}//${window.location.hostname}:5000/api/resource-rates`
      ];
      
      let response: Response | null = null;
      let data: any = null;
      
      for (const url of urls) {
        try {
          console.log(`🌐 ResourceRates: Trying URL: ${url}`);
          const res = await fetch(url);
          console.log(`📡 ResourceRates: Response status for ${url}: ${res.status}`);
          
          if (res.ok) {
            data = await res.json();
            console.log(`✅ ResourceRates: Success with ${url}:`, data);
            response = res;
            break;
          }
        } catch (urlError) {
          console.log(`❌ ResourceRates: Failed with ${url}:`, (urlError as Error).message);
          continue;
        }
      }
      
      if (!response || !response.ok || !data) {
        throw new Error('All URLs failed');
      }
      
      // Backend returns {resource_rates: [...]} or possibly just [...]
      let resourceRates: ResourceRate[] = [];
      if (data.resource_rates && Array.isArray(data.resource_rates)) {
        resourceRates = data.resource_rates;
        console.log(`✅ ResourceRates: Found resource_rates array with ${resourceRates.length} items`);
      } else if (Array.isArray(data)) {
        resourceRates = data;
        console.log(`✅ ResourceRates: Data is direct array with ${resourceRates.length} items`);
      } else {
        console.warn('⚠️ ResourceRates: Unexpected data format:', data);
        console.warn('⚠️ ResourceRates: Data type:', typeof data);
        console.warn('⚠️ ResourceRates: Data keys:', Object.keys(data));
        resourceRates = [];
      }
      
      console.log(`🎯 ResourceRates: Setting ${resourceRates.length} resource rates to state`);
      setResourceRates(resourceRates);
      
    } catch (error) {
      console.error('❌ ResourceRates: Error:', error);
      message.error(`Failed to fetch resource rates: ${(error as Error).message}`);
      setResourceRates([]);
    } finally {
      setLoading(false);
      console.log('🏁 ResourceRates: Fetch completed');
    }
  };

  useEffect(() => {
    fetchResourceRates();
  }, []);

  // Calculate preview cost
  const updatePreviewCost = (changedFields?: any, allFields?: any) => {
    const values = form.getFieldsValue();
    const duration = values.duration_weeks || 0;
    const hours = values.hours_per_week || 0;
    const rate = values.rate_per_hour || 0;
    const total = duration * hours * rate;
    setPreviewCost(total);
  };

  // Update preview when form values change
  useEffect(() => {
    updatePreviewCost();
  }, [form]);

  // Handle create/update resource rate
  const handleSubmit = async (values: ResourceRate) => {
    console.log('🔄 ResourceRates: Form submission started');
    console.log('📝 ResourceRates: Form values:', values);
    console.log('✏️ ResourceRates: Editing rate:', editingRate);
    
    try {
      if (editingRate?.id) {
        console.log(`🌐 ResourceRates: Updating resource rate ${editingRate.id}`);
        const response = await axios.put(`${API_BASE_URL}/resource-rates/${editingRate.id}`, values);
        console.log('✅ ResourceRates: Update successful:', response.data);
        message.success('Resource rate updated successfully');
      } else {
        console.log('🌐 ResourceRates: Creating new resource rate');
        const response = await axios.post(`${API_BASE_URL}/resource-rates`, values);
        console.log('✅ ResourceRates: Creation successful:', response.data);
        message.success('Resource rate created successfully');
      }
      setModalVisible(false);
      setEditingRate(null);
      form.resetFields();
      await fetchResourceRates(); // Ensure data refreshes
    } catch (error: any) {
      console.error('❌ ResourceRates: Error saving resource rate:', error);
      console.error('❌ ResourceRates: Error response:', error.response?.data);
      console.error('❌ ResourceRates: Error status:', error.response?.status);
      message.error(`Failed to ${editingRate?.id ? 'update' : 'create'} resource rate: ${error.response?.data?.error || error.message}`);
    }
  };

  // Handle delete resource rate
  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`${API_BASE_URL}/resource-rates/${id}`);
      message.success('Resource rate deleted successfully');
      fetchResourceRates();
    } catch (error) {
      message.error('Failed to delete resource rate');
      console.error('Error deleting resource rate:', error);
    }
  };

  // Handle modal close/cancel
  const handleModalCancel = () => {
    setModalVisible(false);
    setEditingRate(null);
    setPreviewCost(0);
    form.resetFields();
  };

  // Handle edit resource rate
  const handleEdit = (rate: ResourceRate) => {
    setEditingRate(rate);
    form.setFieldsValue(rate);
    setPreviewCost((rate.duration_weeks || 0) * (rate.hours_per_week || 0) * (rate.rate_per_hour || 0));
    setModalVisible(true);
  };

  // Handle add new resource rate
  const handleAdd = () => {
    setEditingRate(null);
    form.resetFields();
    // Set initial values when adding
    form.setFieldsValue({
      role: '',
      duration_weeks: 12,
      hours_per_week: 40,
      rate_per_hour: 125
    });
    setPreviewCost(12 * 40 * 125); // Calculate initial preview
    setModalVisible(true);
  };

  // Handle role selection change
  const handleRoleChange = (role: string) => {
    const predefinedRole = predefinedRoles.find(r => r.role === role);
    if (predefinedRole) {
      form.setFieldsValue({
        rate_per_hour: predefinedRole.defaultRate
      });
    }
  };

  const columns = [
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
      sorter: (a: ResourceRate, b: ResourceRate) => a.role.localeCompare(b.role),
    },
    {
      title: 'Duration (Weeks)',
      dataIndex: 'duration_weeks',
      key: 'duration_weeks',
      sorter: (a: ResourceRate, b: ResourceRate) => a.duration_weeks - b.duration_weeks,
    },
    {
      title: 'Hours/Week',
      dataIndex: 'hours_per_week',
      key: 'hours_per_week',
      sorter: (a: ResourceRate, b: ResourceRate) => a.hours_per_week - b.hours_per_week,
    },
    {
      title: 'Rate/Hour ($)',
      dataIndex: 'rate_per_hour',
      key: 'rate_per_hour',
      sorter: (a: ResourceRate, b: ResourceRate) => a.rate_per_hour - b.rate_per_hour,
      render: (rate: number) => `$${rate.toFixed(2)}`,
    },
    {
      title: 'Total Cost ($)',
      key: 'total_cost',
      render: (record: ResourceRate) => {
        const total = record.duration_weeks * record.hours_per_week * record.rate_per_hour;
        return `$${total.toLocaleString()}`;
      },
      sorter: (a: ResourceRate, b: ResourceRate) => {
        const totalA = a.duration_weeks * a.hours_per_week * a.rate_per_hour;
        const totalB = b.duration_weeks * b.hours_per_week * b.rate_per_hour;
        return totalA - totalB;
      },
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: ResourceRate) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure you want to delete this resource rate?"
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
  const totalRoles = resourceRates.length;
  const avgRate = resourceRates.length > 0 ? 
    resourceRates.reduce((sum, rate) => sum + rate.rate_per_hour, 0) / resourceRates.length : 0;
  const maxRate = resourceRates.length > 0 ? 
    Math.max(...resourceRates.map(rate => rate.rate_per_hour)) : 0;
  const totalProjectCost = resourceRates.reduce((sum, rate) => 
    sum + (rate.duration_weeks * rate.hours_per_week * rate.rate_per_hour), 0);

  return (
    <div>
      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Roles"
              value={totalRoles}
              prefix={<TeamOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Average Rate"
              value={avgRate}
              prefix={<DollarOutlined />}
              formatter={(value) => `$${Number(value).toFixed(2)}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Max Rate"
              value={maxRate}
              prefix={<DollarOutlined />}
              formatter={(value) => `$${Number(value).toFixed(2)}`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Project Cost"
              value={totalProjectCost}
              prefix={<DollarOutlined />}
              formatter={(value) => `$${Number(value).toLocaleString()}`}
            />
          </Card>
        </Col>
      </Row>

      {/* Main Table */}
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <Title level={2} style={{ margin: 0 }}>Resource Rates & Billing</Title>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            Add Resource Rate
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={resourceRates}
          rowKey="id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `${range[0]}-${range[1]} of ${total} resource rates`,
          }}
        />
      </Card>

      {/* Add/Edit Modal */}
      <Modal
        title={`${editingRate ? 'Edit' : 'Add'} Resource Rate`}
        open={modalVisible}
        onCancel={handleModalCancel}
        footer={null}
        width={600}
        destroyOnClose={true}
        maskClosable={false}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          onValuesChange={updatePreviewCost}
          preserve={false}
        >
          <Form.Item
            name="role"
            label="Role"
            rules={[{ required: true, message: 'Please select or enter a role' }]}
          >
            <Select
              placeholder="Select a role or type custom role"
              showSearch
              allowClear
              optionFilterProp="children"
              onChange={handleRoleChange}
              dropdownRender={(menu) => (
                <div>
                  {menu}
                  <Divider style={{ margin: '8px 0' }} />
                  <Text type="secondary" style={{ padding: '0 12px', fontSize: '12px' }}>
                    Select from dropdown or type custom role name
                  </Text>
                </div>
              )}
            >
              {predefinedRoles.map(role => (
                <Option key={role.role} value={role.role}>
                  <div>
                    <div>{role.role}</div>
                    <Text type="secondary" style={{ fontSize: '12px' }}>
                      ${role.defaultRate}/hr - {role.description}
                    </Text>
                  </div>
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="duration_weeks"
                label="Duration (Weeks)"
                rules={[{ required: true, message: 'Please enter duration' }]}
              >
                <InputNumber
                  min={1}
                  max={52}
                  placeholder="Enter weeks"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="hours_per_week"
                label="Hours per Week"
                rules={[{ required: true, message: 'Please enter hours per week' }]}
              >
                <InputNumber
                  min={1}
                  max={80}
                  placeholder="Enter hours"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="rate_per_hour"
            label="Rate per Hour (USD)"
            rules={[{ required: true, message: 'Please enter hourly rate' }]}
          >
            <InputNumber
              min={1}
              placeholder="Enter hourly rate"
              style={{ width: '100%' }}
              formatter={(value) => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={(value) => value!.replace(/\$\s?|(,*)/g, '') as any}
            />
          </Form.Item>

          {/* Cost Preview */}
          {previewCost > 0 && (
            <Card size="small" style={{ marginBottom: 16, backgroundColor: '#f6f8fa' }}>
              <Text strong>Cost Preview:</Text>
              <div style={{ marginTop: 8 }}>
                <Text>
                  {form.getFieldValue('duration_weeks') || 0} weeks × {' '}
                  {form.getFieldValue('hours_per_week') || 0} hours/week × {' '}
                  ${form.getFieldValue('rate_per_hour') || 0}/hour = {' '}
                  <Text strong style={{ color: '#52c41a' }}>
                    ${previewCost.toLocaleString()}
                  </Text>
                </Text>
              </div>
            </Card>
          )}

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={handleModalCancel}>
                Cancel
              </Button>
              <Button type="primary" htmlType="submit">
                {editingRate ? 'Update' : 'Create'} Rate
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* Billing Guidelines */}
      <Card 
        title="Resource Billing Guidelines" 
        style={{ marginTop: 24 }}
        size="small"
      >
        <Row gutter={16}>
          <Col span={8}>
            <Text strong>💰 Rate Categories</Text>
            <ul style={{ marginTop: 8, fontSize: '12px' }}>
              <li>Senior Consultants: $150-200/hr</li>
              <li>Technical Specialists: $120-180/hr</li>
              <li>Engineers: $100-150/hr</li>
              <li>Project Managers: $100-140/hr</li>
            </ul>
          </Col>
          <Col span={8}>
            <Text strong>📅 Typical Durations</Text>
            <ul style={{ marginTop: 8, fontSize: '12px' }}>
              <li>Assessment: 2-4 weeks</li>
              <li>Planning: 4-8 weeks</li>
              <li>Migration: 8-24 weeks</li>
              <li>Post-Migration: 2-6 weeks</li>
            </ul>
          </Col>
          <Col span={8}>
            <Text strong>⏰ Effort Allocation</Text>
            <ul style={{ marginTop: 8, fontSize: '12px' }}>
              <li>Full-time: 40 hrs/week</li>
              <li>Part-time: 20 hrs/week</li>
              <li>Consultant: 8-16 hrs/week</li>
              <li>Advisory: 4-8 hrs/week</li>
            </ul>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default ResourceRates;
