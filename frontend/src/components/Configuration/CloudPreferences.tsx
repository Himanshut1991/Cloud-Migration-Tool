import React, { useState, useEffect } from 'react';
import {
  Card, Form, Select, Input, Button, message, Typography, Row, Col,
  Space, Divider, Tag, Switch
} from 'antd';
import { CloudOutlined, SaveOutlined, ReloadOutlined } from '@ant-design/icons';
import axios from 'axios';

const { Title, Text } = Typography;
const { Option } = Select;
const { TextArea } = Input;

interface CloudPreference {
  id?: number;
  cloud_provider: string;
  region: string;
  preferred_services: string;
  network_config: string;
  created_at?: string;
  updated_at?: string;
}

const CloudPreferences: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [cloudPreference, setCloudPreference] = useState<CloudPreference | null>(null);

  const API_BASE_URL = 'http://localhost:5000/api';

  // Cloud provider configurations
  const cloudProviders = {
    AWS: {
      regions: [
        'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2',
        'eu-west-1', 'eu-west-2', 'eu-west-3', 'eu-central-1',
        'ap-southeast-1', 'ap-southeast-2', 'ap-northeast-1', 'ap-south-1'
      ],
      services: [
        'EC2', 'RDS', 'S3', 'Lambda', 'ECS', 'EKS', 'ElastiCache',
        'DynamoDB', 'CloudFront', 'Route53', 'VPC', 'ELB'
      ]
    },
    Azure: {
      regions: [
        'East US', 'East US 2', 'West US', 'West US 2', 'Central US',
        'West Europe', 'North Europe', 'UK South', 'UK West',
        'Southeast Asia', 'East Asia', 'Australia East', 'Japan East'
      ],
      services: [
        'Virtual Machines', 'SQL Database', 'Blob Storage', 'Functions',
        'Container Instances', 'AKS', 'Redis Cache', 'Cosmos DB',
        'CDN', 'DNS', 'Virtual Network', 'Load Balancer'
      ]
    },
    GCP: {
      regions: [
        'us-central1', 'us-east1', 'us-west1', 'us-west2',
        'europe-west1', 'europe-west2', 'europe-west3', 'europe-west4',
        'asia-southeast1', 'asia-northeast1', 'asia-south1', 'australia-southeast1'
      ],
      services: [
        'Compute Engine', 'Cloud SQL', 'Cloud Storage', 'Cloud Functions',
        'Cloud Run', 'GKE', 'Memorystore', 'Firestore',
        'Cloud CDN', 'Cloud DNS', 'VPC', 'Cloud Load Balancing'
      ]
    }
  };

  const networkConfigs = [
    'Public Cloud',
    'Virtual Private Cloud (VPC)',
    'Hybrid Cloud',
    'Private Cloud',
    'Multi-Cloud'
  ];

  // Fetch existing cloud preferences
  const fetchCloudPreferences = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE_URL}/cloud_preferences`);
      if (response.data && response.data.length > 0) {
        const preference = response.data[0]; // Assuming single configuration
        setCloudPreference(preference);
        
        // Parse preferred services if it's a JSON string
        let services = [];
        try {
          services = JSON.parse(preference.preferred_services || '[]');
        } catch {
          services = [];
        }
        
        form.setFieldsValue({
          ...preference,
          preferred_services: services
        });
      }
    } catch (error) {
      console.error('Error fetching cloud preferences:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCloudPreferences();
  }, []);

  // Handle form submission
  const handleSubmit = async (values: any) => {
    setSaving(true);
    try {
      const payload = {
        ...values,
        preferred_services: JSON.stringify(values.preferred_services || [])
      };

      if (cloudPreference?.id) {
        await axios.put(`${API_BASE_URL}/cloud_preferences/${cloudPreference.id}`, payload);
        message.success('Cloud preferences updated successfully');
      } else {
        await axios.post(`${API_BASE_URL}/cloud_preferences`, payload);
        message.success('Cloud preferences saved successfully');
      }
      fetchCloudPreferences();
    } catch (error) {
      message.error('Failed to save cloud preferences');
      console.error('Error saving cloud preferences:', error);
    } finally {
      setSaving(false);
    }
  };

  // Reset form
  const handleReset = () => {
    form.resetFields();
    fetchCloudPreferences();
  };

  const selectedProvider = Form.useWatch('cloud_provider', form);

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 24 }}>
          <CloudOutlined style={{ fontSize: '24px', marginRight: '12px', color: '#1890ff' }} />
          <Title level={2} style={{ margin: 0 }}>Cloud Preferences</Title>
        </div>

        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{
            cloud_provider: 'AWS',
            network_config: 'Public Cloud',
            preferred_services: []
          }}
        >
          <Row gutter={24}>
            <Col span={12}>
              <Form.Item
                name="cloud_provider"
                label="Cloud Provider"
                rules={[{ required: true, message: 'Please select a cloud provider' }]}
              >
                <Select
                  placeholder="Select cloud provider"
                  onChange={() => {
                    // Reset region and services when provider changes
                    form.setFieldsValue({
                      region: undefined,
                      preferred_services: []
                    });
                  }}
                >
                  <Option value="AWS">Amazon Web Services (AWS)</Option>
                  <Option value="Azure">Microsoft Azure</Option>
                  <Option value="GCP">Google Cloud Platform (GCP)</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="region"
                label="Primary Region"
                rules={[{ required: true, message: 'Please select a region' }]}
              >
                <Select placeholder="Select primary region">
                  {selectedProvider && cloudProviders[selectedProvider as keyof typeof cloudProviders]?.regions.map(region => (
                    <Option key={region} value={region}>{region}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Form.Item
                name="network_config"
                label="Network Configuration"
                rules={[{ required: true, message: 'Please select network configuration' }]}
              >
                <Select placeholder="Select network configuration">
                  {networkConfigs.map(config => (
                    <Option key={config} value={config}>{config}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Form.Item
                name="preferred_services"
                label="Preferred Cloud Services"
                extra="Select the cloud services you prefer to use for migration"
              >
                <Select
                  mode="multiple"
                  placeholder="Select preferred services"
                  maxTagCount="responsive"
                >
                  {selectedProvider && cloudProviders[selectedProvider as keyof typeof cloudProviders]?.services.map(service => (
                    <Option key={service} value={service}>{service}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Divider />

          {/* Service Recommendations */}
          {selectedProvider && (
            <Card
              size="small"
              title={`${selectedProvider} Service Recommendations`}
              style={{ marginBottom: 24 }}
            >
              <Row gutter={16}>
                <Col span={8}>
                  <Text strong>Compute:</Text>
                  <div style={{ marginTop: 8 }}>
                    {selectedProvider === 'AWS' && <Tag color="orange">EC2</Tag>}
                    {selectedProvider === 'Azure' && <Tag color="blue">Virtual Machines</Tag>}
                    {selectedProvider === 'GCP' && <Tag color="green">Compute Engine</Tag>}
                  </div>
                </Col>
                <Col span={8}>
                  <Text strong>Database:</Text>
                  <div style={{ marginTop: 8 }}>
                    {selectedProvider === 'AWS' && <Tag color="orange">RDS</Tag>}
                    {selectedProvider === 'Azure' && <Tag color="blue">SQL Database</Tag>}
                    {selectedProvider === 'GCP' && <Tag color="green">Cloud SQL</Tag>}
                  </div>
                </Col>
                <Col span={8}>
                  <Text strong>Storage:</Text>
                  <div style={{ marginTop: 8 }}>
                    {selectedProvider === 'AWS' && <Tag color="orange">S3</Tag>}
                    {selectedProvider === 'Azure' && <Tag color="blue">Blob Storage</Tag>}
                    {selectedProvider === 'GCP' && <Tag color="green">Cloud Storage</Tag>}
                  </div>
                </Col>
              </Row>
            </Card>
          )}

          <Form.Item style={{ marginBottom: 0 }}>
            <Space>
              <Button 
                type="primary" 
                htmlType="submit" 
                icon={<SaveOutlined />}
                loading={saving}
              >
                Save Preferences
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
      {cloudPreference && (
        <Card 
          title="Current Configuration Summary" 
          style={{ marginTop: 24 }}
          size="small"
        >
          <Row gutter={16}>
            <Col span={6}>
              <Text strong>Provider:</Text>
              <div>{cloudPreference.cloud_provider}</div>
            </Col>
            <Col span={6}>
              <Text strong>Region:</Text>
              <div>{cloudPreference.region}</div>
            </Col>
            <Col span={6}>
              <Text strong>Network:</Text>
              <div>{cloudPreference.network_config}</div>
            </Col>
            <Col span={6}>
              <Text strong>Services:</Text>
              <div>
                {(() => {
                  try {
                    const services = JSON.parse(cloudPreference.preferred_services || '[]');
                    return services.length > 0 ? `${services.length} selected` : 'None';
                  } catch {
                    return 'None';
                  }
                })()}
              </div>
            </Col>
          </Row>
        </Card>
      )}
    </div>
  );
};

export default CloudPreferences;
