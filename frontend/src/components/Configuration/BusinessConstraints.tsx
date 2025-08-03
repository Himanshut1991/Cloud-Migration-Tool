import React, { useState, useEffect } from 'react';
import {
  Card, Form, Select, Input, Button, message, Typography, Row, Col,
  Space, DatePicker, InputNumber, Alert, Divider
} from 'antd';
import { ScheduleOutlined, SaveOutlined, ReloadOutlined, WarningOutlined } from '@ant-design/icons';
import axios from 'axios';
import dayjs, { Dayjs } from 'dayjs';

const { Title, Text } = Typography;
const { Option } = Select;

interface BusinessConstraint {
  id?: number;
  migration_window: string;
  cutover_date: string;
  downtime_tolerance: string;
  budget_cap?: number;
  created_at?: string;
  updated_at?: string;
}

const BusinessConstraints: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [businessConstraint, setBusinessConstraint] = useState<BusinessConstraint | null>(null);

  const API_BASE_URL = 'http://localhost:5000/api';

  // Migration window options
  const migrationWindows = [
    { value: 'Weekends Only', label: 'Weekends Only (Sat-Sun)' },
    { value: 'Evenings (6PM-6AM)', label: 'Evenings (6PM-6AM)' },
    { value: 'Maintenance Windows', label: 'Scheduled Maintenance Windows' },
    { value: 'Business Hours', label: 'Business Hours (9AM-5PM)' },
    { value: 'Extended Hours', label: 'Extended Hours (6AM-10PM)' },
    { value: '24/7 Available', label: '24/7 Available' }
  ];

  // Downtime tolerance options
  const downtimeTolerances = [
    { value: 'None', label: 'None (0 minutes)', description: 'Zero downtime migration required' },
    { value: 'Very Low', label: 'Very Low (< 5 minutes)', description: 'Critical systems' },
    { value: 'Low', label: 'Low (< 15 minutes)', description: 'Important business systems' },
    { value: 'Medium', label: 'Medium (< 1 hour)', description: 'Standard business systems' },
    { value: 'High', label: 'High (< 4 hours)', description: 'Non-critical systems' },
    { value: 'Very High', label: 'Very High (< 8 hours)', description: 'Development/test systems' }
  ];

  // Fetch existing business constraints
  const fetchBusinessConstraints = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/business_constraints`);
      if (response.data && response.data.length > 0) {
        const constraint = response.data[0]; // Assuming single configuration
        setBusinessConstraint(constraint);
        
        // Convert date string to dayjs object for DatePicker
        const formValues = {
          ...constraint,
          cutover_date: constraint.cutover_date ? dayjs(constraint.cutover_date) : null
        };
        
        form.setFieldsValue(formValues);
      }
    } catch (error) {
      console.error('Error fetching business constraints:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBusinessConstraints();
  }, []);

  // Handle form submission
  const handleSubmit = async (values: any) => {
    setSaving(true);
    try {
      const payload = {
        ...values,
        cutover_date: values.cutover_date ? values.cutover_date.format('YYYY-MM-DD') : null
      };

      if (businessConstraint?.id) {
        await axios.put(`${API_BASE_URL}/business_constraints/${businessConstraint.id}`, payload);
        message.success('Business constraints updated successfully');
      } else {
        await axios.post(`${API_BASE_URL}/business_constraints`, payload);
        message.success('Business constraints saved successfully');
      }
      fetchBusinessConstraints();
    } catch (error) {
      message.error('Failed to save business constraints');
      console.error('Error saving business constraints:', error);
    } finally {
      setSaving(false);
    }
  };

  // Reset form
  const handleReset = () => {
    form.resetFields();
    fetchBusinessConstraints();
  };

  // Get migration window recommendation
  const getMigrationWindowRecommendation = (downtime: string) => {
    if (downtime === 'None' || downtime === 'Very Low') {
      return 'Recommend: 24/7 Available with blue-green deployment';
    } else if (downtime === 'Low') {
      return 'Recommend: Maintenance Windows or Evenings';
    } else if (downtime === 'Medium') {
      return 'Recommend: Weekends Only';
    } else {
      return 'Recommend: Business Hours acceptable';
    }
  };

  const selectedDowntime = Form.useWatch('downtime_tolerance', form);
  const selectedCutoverDate = Form.useWatch('cutover_date', form);

  // Calculate days until cutover
  const daysUntilCutover = selectedCutoverDate ? 
    selectedCutoverDate.diff(dayjs(), 'day') : null;

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 24 }}>
          <ScheduleOutlined style={{ fontSize: '24px', marginRight: '12px', color: '#1890ff' }} />
          <Title level={2} style={{ margin: 0 }}>Business Constraints</Title>
        </div>

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            migration_window: 'Weekends Only',
            downtime_tolerance: 'Low'
          }}
        >
          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                name="migration_window"
                label="Migration Window"
                rules={[{ required: true, message: 'Please select a migration window' }]}
                extra="When can migration activities be performed?"
              >
                <Select placeholder="Select migration window">
                  {migrationWindows.map(window => (
                    <Option key={window.value} value={window.value}>
                      {window.label}
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="cutover_date"
                label="Target Cutover Date"
                rules={[{ required: true, message: 'Please select a cutover date' }]}
                extra="When should the migration be completed?"
              >
                <DatePicker 
                  style={{ width: '100%' }}
                  disabledDate={(current) => current && current < dayjs().startOf('day')}
                  placeholder="Select cutover date"
                />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                name="downtime_tolerance"
                label="Downtime Tolerance"
                rules={[{ required: true, message: 'Please select downtime tolerance' }]}
                extra="Maximum acceptable downtime per system"
              >
                <Select placeholder="Select downtime tolerance">
                  {downtimeTolerances.map(tolerance => (
                    <Option key={tolerance.value} value={tolerance.value}>
                      <div>
                        <div>{tolerance.label}</div>
                        <Text type="secondary" style={{ fontSize: '12px' }}>
                          {tolerance.description}
                        </Text>
                      </div>
                    </Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="budget_cap"
                label="Budget Cap (USD)"
                extra="Maximum budget for migration project (optional)"
              >
                <InputNumber
                  style={{ width: '100%' }}
                  placeholder="Enter budget limit"
                  min={0}
                  step={1000}
                  formatter={(value) => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={(value) => value!.replace(/\$\s?|(,*)/g, '') as any}
                />
              </Form.Item>
            </Col>
          </Row>

          <Divider />

          {/* Recommendations and Warnings */}
          {selectedDowntime && (
            <Alert
              message="Migration Window Recommendation"
              description={getMigrationWindowRecommendation(selectedDowntime)}
              type="info"
              showIcon
              style={{ marginBottom: 16 }}
            />
          )}

          {daysUntilCutover !== null && (
            <Alert
              message={`Timeline Alert`}
              description={
                daysUntilCutover < 30 
                  ? `⚠️ Only ${daysUntilCutover} days until cutover date. Consider extending timeline for thorough planning and testing.`
                  : daysUntilCutover < 90
                    ? `📅 ${daysUntilCutover} days until cutover date. Adequate time for most migrations.`
                    : `✅ ${daysUntilCutover} days until cutover date. Plenty of time for comprehensive planning.`
              }
              type={daysUntilCutover < 30 ? 'warning' : daysUntilCutover < 90 ? 'info' : 'success'}
              showIcon
              style={{ marginBottom: 16 }}
            />
          )}

          <Form.Item style={{ marginBottom: 0 }}>
            <Space>
              <Button 
                type="primary" 
                htmlType="submit" 
                icon={<SaveOutlined />}
                loading={saving}
              >
                Save Constraints
              </Button>
              <Button 
                icon={<ReloadOutlined />}
                onClick={handleReset}
                loading={loading}
              >
                Reset
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>

      {/* Current Configuration Summary */}
      {businessConstraint && (
        <Card 
          title="Current Constraints Summary" 
          style={{ marginTop: 24 }}
          size="small"
        >
          <Row gutter={16}>
            <Col span={6}>
              <Text strong>Migration Window:</Text>
              <div>{businessConstraint.migration_window}</div>
            </Col>
            <Col span={6}>
              <Text strong>Cutover Date:</Text>
              <div>{dayjs(businessConstraint.cutover_date).format('MMM DD, YYYY')}</div>
            </Col>
            <Col span={6}>
              <Text strong>Downtime Tolerance:</Text>
              <div>{businessConstraint.downtime_tolerance}</div>
            </Col>
            <Col span={6}>
              <Text strong>Budget Cap:</Text>
              <div>
                {businessConstraint.budget_cap 
                  ? `$${businessConstraint.budget_cap.toLocaleString()}` 
                  : 'Not specified'
                }
              </div>
            </Col>
          </Row>
        </Card>
      )}

      {/* Planning Guidelines */}
      <Card 
        title="Migration Planning Guidelines" 
        style={{ marginTop: 24 }}
        size="small"
      >
        <Row gutter={16}>
          <Col span={8}>
            <Text strong>📋 Pre-Migration (30%)</Text>
            <ul style={{ marginTop: 8, fontSize: '12px' }}>
              <li>Assessment & Planning</li>
              <li>Architecture Design</li>
              <li>Tool Selection</li>
              <li>Resource Allocation</li>
            </ul>
          </Col>
          <Col span={8}>
            <Text strong>🔄 Migration (50%)</Text>
            <ul style={{ marginTop: 8, fontSize: '12px' }}>
              <li>Data Migration</li>
              <li>Application Migration</li>
              <li>Testing & Validation</li>
              <li>Performance Tuning</li>
            </ul>
          </Col>
          <Col span={8}>
            <Text strong>✅ Post-Migration (20%)</Text>
            <ul style={{ marginTop: 8, fontSize: '12px' }}>
              <li>Monitoring Setup</li>
              <li>Optimization</li>
              <li>Documentation</li>
              <li>Knowledge Transfer</li>
            </ul>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default BusinessConstraints;
