import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Typography, 
  Row, 
  Col, 
  Statistic, 
  Button, 
  Spin, 
  Alert,
  Tag,
  Divider,
  Space
} from 'antd';
import {
  DollarOutlined,
  CloudOutlined,
  DatabaseOutlined,
  HddOutlined,
  ReloadOutlined,
  RobotOutlined,
  DesktopOutlined
} from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;

interface SimpleCostEstimationData {
  total_monthly_cost: number;
  total_migration_cost: number;
  cost_breakdown: {
    compute: number;
    storage: number;
    database: number;
  };
  resource_details: {
    servers: number;
    databases: number;
    file_shares: number;
  };
  ai_insights: {
    confidence_level: number;
    recommendations: string[];
    fallback_used: boolean;
    ai_available: boolean;
    ai_status?: string;
    cost_optimization_tips?: string[];
  };
}

const CostEstimationSimple: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<SimpleCostEstimationData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [aiStatus, setAiStatus] = useState<any>(null);

  const fetchCostEstimation = async () => {
    console.log('Fetching cost estimation...');
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/api/cost-estimation');
      console.log('Cost estimation response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch cost estimation: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('Cost estimation data:', result);
      setData(result);
    } catch (err) {
      console.error('Cost estimation error:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const fetchAiStatus = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/ai-status');
      if (response.ok) {
        const status = await response.json();
        setAiStatus(status);
      }
    } catch (err) {
      console.warn('Failed to fetch AI status:', err);
    }
  };

  useEffect(() => {
    fetchCostEstimation();
    fetchAiStatus();
  }, []);

  const formatCurrency = (amount: number) => 
    `$${amount.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;

  if (error) {
    return (
      <Card>
        <Alert
          message="Error Loading Cost Estimation"
          description={error}
          type="error"
          action={
            <Button size="small" onClick={fetchCostEstimation}>
              Retry
            </Button>
          }
        />
      </Card>
    );
  }

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col span={24}>
          <Card>
            <Row justify="space-between" align="middle">
              <Col>
                <Title level={2} style={{ margin: 0 }}>
                  <DollarOutlined style={{ marginRight: 8 }} />
                  Cost Estimation Analysis
                </Title>
                {aiStatus && (
                  <div style={{ marginTop: 8 }}>
                    <Tag color={aiStatus.ai_available ? 'green' : 'orange'}>
                      {aiStatus.ai_available ? '🤖 AI-Powered' : '📋 Rule-Based'} Analysis
                    </Tag>
                    <Text type="secondary" style={{ marginLeft: 8, fontSize: '12px' }}>
                      Provider: {aiStatus.provider || 'Rule-based fallback'}
                    </Text>
                  </div>
                )}
              </Col>
              <Col>
                <Button 
                  type="primary" 
                  icon={<ReloadOutlined />} 
                  onClick={() => {
                    fetchCostEstimation();
                    fetchAiStatus();
                  }}
                  loading={loading}
                >
                  Refresh
                </Button>
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>

      {loading ? (
        <Card>
          <div style={{ textAlign: 'center', padding: '50px 0' }}>
            <Spin size="large" />
            <Paragraph style={{ marginTop: 16 }}>Calculating cost estimation...</Paragraph>
          </div>
        </Card>
      ) : data ? (
        <>
          {/* Executive Summary */}
          <Card title="Executive Summary" style={{ marginBottom: 24 }}>
            <Row gutter={[24, 16]}>
              <Col xs={24} sm={12} lg={8}>
                <Statistic
                  title="Monthly Cloud Cost"
                  value={data.total_monthly_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<CloudOutlined />}
                />
              </Col>
              <Col xs={24} sm={12} lg={8}>
                <Statistic
                  title="Migration Cost (One-time)"
                  value={data.total_migration_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<RobotOutlined />}
                />
              </Col>
              <Col xs={24} sm={12} lg={8}>
                <Statistic
                  title="Annual Cloud Cost"
                  value={data.total_monthly_cost * 12}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<DollarOutlined />}
                />
              </Col>
            </Row>
          </Card>

          {/* Cost Breakdown */}
          <Card title="Cost Breakdown" style={{ marginBottom: 24 }}>
            <Row gutter={[24, 16]}>
              <Col xs={24} sm={8}>
                <Statistic
                  title="Compute Services"
                  value={data.cost_breakdown.compute}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<DesktopOutlined />}
                />
                <Text type="secondary">Monthly cost for server hosting</Text>
              </Col>
              <Col xs={24} sm={8}>
                <Statistic
                  title="Database Services"
                  value={data.cost_breakdown.database}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<DatabaseOutlined />}
                />
                <Text type="secondary">Monthly cost for database services</Text>
              </Col>
              <Col xs={24} sm={8}>
                <Statistic
                  title="Storage Services"
                  value={data.cost_breakdown.storage}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<HddOutlined />}
                />
                <Text type="secondary">Monthly cost for file storage</Text>
              </Col>
            </Row>
          </Card>

          {/* Resource Details */}
          <Card title="Resource Inventory" style={{ marginBottom: 24 }}>
            <Row gutter={[24, 16]}>
              <Col xs={24} sm={8}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', color: '#1890ff' }}>
                    <DesktopOutlined />
                  </div>
                  <Statistic
                    title="Servers"
                    value={data.resource_details.servers}
                    suffix="servers"
                  />
                </div>
              </Col>
              <Col xs={24} sm={8}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', color: '#52c41a' }}>
                    <DatabaseOutlined />
                  </div>
                  <Statistic
                    title="Databases"
                    value={data.resource_details.databases}
                    suffix="databases"
                  />
                </div>
              </Col>
              <Col xs={24} sm={8}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', color: '#faad14' }}>
                    <HddOutlined />
                  </div>
                  <Statistic
                    title="File Shares"
                    value={data.resource_details.file_shares}
                    suffix="shares"
                  />
                </div>
              </Col>
            </Row>
          </Card>

          {/* AI Insights */}
          <Card 
            title={
              <Space>
                <RobotOutlined />
                AI Cost Analysis
                <Tag color={data.ai_insights.ai_available ? 'green' : 'orange'}>
                  {data.ai_insights.confidence_level}% Confidence
                </Tag>
                {data.ai_insights.fallback_used && (
                  <Tag color="blue">Rule-based</Tag>
                )}
              </Space>
            } 
            style={{ marginBottom: 24 }}
          >
            {data.ai_insights.fallback_used && (
              <Alert 
                message="Intelligent Rule-based Analysis Active" 
                description={data.ai_insights.ai_status || "Using advanced rule-based cost optimization recommendations"}
                type="info" 
                style={{ marginBottom: 16 }}
              />
            )}
            
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={12}>
                <Title level={4}>💡 Cost Optimization Recommendations:</Title>
                {data.ai_insights.recommendations.map((recommendation, index) => (
                  <div key={index} style={{ marginBottom: 12, padding: '8px', backgroundColor: '#f6f8ff', borderRadius: '4px' }}>
                    <Text strong style={{ color: '#1890ff' }}>#{index + 1}</Text>
                    <Text style={{ marginLeft: 8 }}>{recommendation}</Text>
                  </div>
                ))}
              </Col>
              
              <Col xs={24} lg={12}>
                {data.ai_insights.cost_optimization_tips && (
                  <>
                    <Title level={4}>🎯 Quick Savings Tips:</Title>
                    {data.ai_insights.cost_optimization_tips.map((tip, index) => (
                      <div key={index} style={{ marginBottom: 12, padding: '8px', backgroundColor: '#f6ffed', borderRadius: '4px' }}>
                        <Tag color="green" style={{ marginRight: 8 }}>TIP</Tag>
                        <Text>{tip}</Text>
                      </div>
                    ))}
                  </>
                )}
              </Col>
            </Row>
          </Card>
        </>
      ) : (
        <Card>
          <div style={{ textAlign: 'center', padding: '50px 0' }}>
            <Paragraph>No cost estimation data available. Click refresh to load data.</Paragraph>
          </div>
        </Card>
      )}
    </div>
  );
};

export default CostEstimationSimple;
