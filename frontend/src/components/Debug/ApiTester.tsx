import React, { useState, useEffect } from 'react';
import { Card, Button, Alert, Typography, Space, Table, Tag } from 'antd';
import { ReloadOutlined, BugOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

interface EndpointTest {
  name: string;
  url: string;
  method: string;
  status: 'loading' | 'success' | 'error';
  data?: any;
  error?: string;
  duration?: number;
}

const ApiTester: React.FC = () => {
  const [tests, setTests] = useState<EndpointTest[]>([]);
  const [testing, setTesting] = useState(false);

  const endpoints = [
    { name: 'Health Check', url: 'http://localhost:5000/api/health', method: 'GET' },
    { name: 'Dashboard', url: 'http://localhost:5000/api/dashboard', method: 'GET' },
    { name: 'Servers', url: 'http://localhost:5000/api/servers', method: 'GET' },
    { name: 'Databases', url: 'http://localhost:5000/api/databases', method: 'GET' },
    { name: 'File Shares', url: 'http://localhost:5000/api/file-shares', method: 'GET' },
    { name: 'Cost Estimation', url: 'http://localhost:5000/api/cost-estimation', method: 'GET' },
    { name: 'Migration Strategy', url: 'http://localhost:5000/api/migration-strategy', method: 'GET' },
    { name: 'AI Status', url: 'http://localhost:5000/api/ai-status', method: 'GET' },
  ];

  const testEndpoint = async (endpoint: { name: string; url: string; method: string }): Promise<EndpointTest> => {
    const startTime = Date.now();
    try {
      console.log(`Testing ${endpoint.name}: ${endpoint.method} ${endpoint.url}`);
      
      let response;
      if (endpoint.method === 'POST') {
        response = await fetch(endpoint.url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({})
        });
      } else {
        response = await fetch(endpoint.url);
      }
      
      const duration = Date.now() - startTime;
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      return {
        ...endpoint,
        status: 'success',
        data,
        duration,
      };
    } catch (error) {
      const duration = Date.now() - startTime;
      return {
        ...endpoint,
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
        duration,
      };
    }
  };

  const runAllTests = async () => {
    setTesting(true);
    setTests(endpoints.map(ep => ({ ...ep, status: 'loading' as const })));

    for (let i = 0; i < endpoints.length; i++) {
      const result = await testEndpoint(endpoints[i]);
      setTests(prev => prev.map((test, index) => index === i ? result : test));
    }
    
    setTesting(false);
  };

  useEffect(() => {
    runAllTests();
  }, []);

  const columns = [
    {
      title: 'Endpoint',
      dataIndex: 'name',
      key: 'name',
      render: (text: string, record: EndpointTest) => (
        <Space>
          <BugOutlined />
          <strong>{text}</strong>
          <Tag color="blue">{record.method}</Tag>
        </Space>
      ),
    },
    {
      title: 'Status',
      key: 'status',
      render: (test: EndpointTest) => {
        const { status } = test;
        if (status === 'loading') return <Tag color="processing">Loading...</Tag>;
        if (status === 'success') return <Tag color="success">✅ Success</Tag>;
        return <Tag color="error">❌ Failed</Tag>;
      },
    },
    {
      title: 'Duration',
      key: 'duration',
      render: (test: EndpointTest) => test.duration ? `${test.duration}ms` : '-',
    },
    {
      title: 'Result',
      key: 'result',
      render: (test: EndpointTest) => {
        if (test.status === 'loading') return <Text type="secondary">Testing...</Text>;
        if (test.status === 'error') return <Text type="danger">{test.error}</Text>;
        
        const dataType = Array.isArray(test.data) ? `Array[${test.data.length}]` : 'Object';
        const keys = Array.isArray(test.data) ? [] : Object.keys(test.data || {});
        
        return (
          <Space direction="vertical" size="small">
            <Text>{dataType}</Text>
            {keys.length > 0 && (
              <Text type="secondary" style={{ fontSize: '12px' }}>
                Keys: {keys.slice(0, 3).join(', ')}{keys.length > 3 ? '...' : ''}
              </Text>
            )}
          </Space>
        );
      },
    },
  ];

  const successCount = tests.filter(t => t.status === 'success').length;
  const errorCount = tests.filter(t => t.status === 'error').length;

  return (
    <div>
      <Title level={2}>
        <BugOutlined style={{ marginRight: '8px' }} />
        API Connection Test
      </Title>
      
      <Space direction="vertical" style={{ width: '100%' }} size="large">
        <Alert
          message="Backend API Connectivity Test"
          description="Testing connection to all backend API endpoints to diagnose data loading issues."
          type="info"
          showIcon
        />

        <Card 
          title="Test Results"
          extra={
            <Button 
              icon={<ReloadOutlined />} 
              onClick={runAllTests}
              loading={testing}
              type="primary"
            >
              Run Tests Again
            </Button>
          }
        >
          <Table
            columns={columns}
            dataSource={tests}
            rowKey="name"
            size="small"
            pagination={false}
            loading={testing}
          />
        </Card>

        {!testing && (
          <Space>
            {successCount > 0 && (
              <Alert
                message={`✅ ${successCount} endpoints working`}
                type="success"
                showIcon
              />
            )}
            
            {errorCount > 0 && (
              <Alert
                message={`❌ ${errorCount} endpoints failed`}
                type="error"
                showIcon
              />
            )}
          </Space>
        )}
      </Space>
    </div>
  );
};

export default ApiTester;
