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
  DesktopOutlined,
  UserOutlined,
  BarChartOutlined
} from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;

interface SimpleCostEstimationData {
  grand_total: {
    annual_cloud_cost: number;
    one_time_migration_cost: number;
    total_first_year_cost: number;
  };
  cloud_infrastructure: {
    servers: {
      total_monthly_cost: number;
      total_annual_cost: number;
      server_recommendations: Array<{
        server_id: string;
        current_specs: string;
        recommended_instance: string;
        monthly_cost: number;
        annual_cost: number;
      }>;
    };
    databases: {
      total_monthly_cost: number;
      total_annual_cost: number;
      database_recommendations: Array<{
        db_name: string;
        db_type: string;
        recommended_instance: string;
        size_gb: number;
        monthly_cost: number;
        annual_cost: number;
      }>;
    };
    storage: {
      total_monthly_cost: number;
      total_annual_cost: number;
      storage_recommendations: Array<{
        share_name: string;
        size_gb: number;
        recommended_storage: string;
        access_pattern: string;
        monthly_cost: number;
        annual_cost: number;
      }>;
    };
    total_monthly_cost: number;
    total_annual_cost: number;
  };
  migration_services: {
    total_professional_services_cost: number;
    resource_breakdown: Array<{
      role: string;
      rate_per_hour: number;
      hours_per_week: number;
      duration_weeks: number;
      total_hours: number;
      total_cost: number;
    }>;
  };
  ai_insights?: {
    confidence_level: number;
    cost_optimization_tips: string[];
    potential_savings: {
      percentage: number;
      annual_amount: number;
    };
    recommendations: string[];
    ai_model_used: string;
    fallback_used: boolean;
  };
}

const CostEstimationSimple: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<SimpleCostEstimationData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchCostEstimation = async () => {
    console.log('Fetching cost estimation...');
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/api/cost-estimation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cloud_provider: 'AWS',
          target_region: 'us-east-1',
          migration_type: 'lift_and_shift'
        })
      });
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

  useEffect(() => {
    fetchCostEstimation();
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
              </Col>
              <Col>
                <Button 
                  type="primary" 
                  icon={<ReloadOutlined />} 
                  onClick={() => {
                    fetchCostEstimation();
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
                  value={data.cloud_infrastructure.total_monthly_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<CloudOutlined />}
                />
              </Col>
              <Col xs={24} sm={12} lg={8}>
                <Statistic
                  title="Migration Cost (One-time)"
                  value={data.grand_total.one_time_migration_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<RobotOutlined />}
                />
              </Col>
              <Col xs={24} sm={12} lg={8}>
                <Statistic
                  title="Annual Cloud Cost"
                  value={data.cloud_infrastructure.total_annual_cost}
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
                  value={data.cloud_infrastructure.servers.total_monthly_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<DesktopOutlined />}
                />
                <Text type="secondary">Monthly cost for server hosting</Text>
              </Col>
              <Col xs={24} sm={8}>
                <Statistic
                  title="Database Services"
                  value={data.cloud_infrastructure.databases.total_monthly_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<DatabaseOutlined />}
                />
                <Text type="secondary">Monthly cost for database services</Text>
              </Col>
              <Col xs={24} sm={8}>
                <Statistic
                  title="Storage Services"
                  value={data.cloud_infrastructure.storage.total_monthly_cost}
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
                    value={data.cloud_infrastructure.servers.server_recommendations.length}
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
                    value={data.cloud_infrastructure.databases.database_recommendations.length}
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
                    value={data.cloud_infrastructure.storage.storage_recommendations.length}
                    suffix="shares"
                  />
                </div>
              </Col>
            </Row>
          </Card>

          {/* Migration Services */}
          <Card 
            title={
              <Space>
                <RobotOutlined />
                Migration Services Breakdown
                <Tag color="blue">
                  ${data.migration_services.total_professional_services_cost.toLocaleString()}
                </Tag>
              </Space>
            } 
            style={{ marginBottom: 24 }}
          >
            <Row gutter={[16, 16]}>
              {data.migration_services.resource_breakdown.map((resource, index) => (
                <Col xs={24} md={12} key={index}>
                  <Card size="small" style={{ height: '100%' }}>
                    <Statistic
                      title={resource.role}
                      value={resource.total_cost}
                      formatter={(value) => formatCurrency(Number(value))}
                      prefix={<UserOutlined />}
                    />
                    <div style={{ marginTop: 8 }}>
                      <Text type="secondary">
                        {resource.total_hours} hours over {resource.duration_weeks} weeks
                      </Text>
                      <br />
                      <Text type="secondary">
                        ${resource.rate_per_hour}/hour • {resource.hours_per_week} hrs/week
                      </Text>
                    </div>
                  </Card>
                </Col>
              ))}
            </Row>
          </Card>

          {/* AI Insights */}
          {data.ai_insights && (
            <Card 
              title={
                <Space>
                  <RobotOutlined />
                  AI Cost Analysis
                  <Tag color={data.ai_insights.fallback_used ? 'orange' : 'green'}>
                    {Math.round(data.ai_insights.confidence_level * 100)}% Confidence
                  </Tag>
                  {data.ai_insights.fallback_used && (
                    <Tag color="blue">Rule-based</Tag>
                  )}
                  {!data.ai_insights.fallback_used && (
                    <Tag color="purple">{data.ai_insights.ai_model_used}</Tag>
                  )}
                </Space>
              } 
              style={{ marginBottom: 24 }}
            >
              {data.ai_insights.fallback_used && (
                <Alert 
                  message="Using Advanced Rule-based Analysis" 
                  description="AI services are temporarily unavailable. Using intelligent rule-based cost optimization recommendations."
                  type="info" 
                  style={{ marginBottom: 16 }}
                />
              )}
              
              {!data.ai_insights.fallback_used && (
                <Alert 
                  message="AI-Powered Cost Analysis Active" 
                  description={`Analysis powered by ${data.ai_insights.ai_model_used} with ${Math.round(data.ai_insights.confidence_level * 100)}% confidence level.`}
                  type="success" 
                  style={{ marginBottom: 16 }}
                />
              )}
              
              <Row gutter={[16, 16]}>
                <Col xs={24} lg={12}>
                  <Card size="small" title="💡 Cost Optimization Tips" style={{ height: '100%' }}>
                    {data.ai_insights.cost_optimization_tips.map((tip, index) => (
                      <div key={index} style={{ marginBottom: 12, padding: '8px', backgroundColor: '#f6f8ff', borderRadius: '4px' }}>
                        <Text strong style={{ color: '#1890ff' }}>#{index + 1}</Text>
                        <Text style={{ marginLeft: 8 }}>{tip}</Text>
                      </div>
                    ))}
                  </Card>
                </Col>
                
                <Col xs={24} lg={12}>
                  <Card size="small" title="🎯 AI Recommendations" style={{ height: '100%' }}>
                    {data.ai_insights.recommendations.map((recommendation, index) => (
                      <div key={index} style={{ marginBottom: 12, padding: '8px', backgroundColor: '#f6ffed', borderRadius: '4px' }}>
                        <Tag color="green" style={{ marginRight: 8 }}>REC</Tag>
                        <Text>{recommendation}</Text>
                      </div>
                    ))}
                  </Card>
                </Col>
              </Row>
              
              {data.ai_insights.potential_savings && (
                <Card size="small" title="💰 Potential Savings" style={{ marginTop: 16 }}>
                  <Row gutter={16}>
                    <Col xs={24} sm={12}>
                      <Statistic
                        title="Potential Annual Savings"
                        value={data.ai_insights.potential_savings.annual_amount}
                        formatter={(value) => formatCurrency(Number(value))}
                        prefix={<DollarOutlined />}
                      />
                    </Col>
                    <Col xs={24} sm={12}>
                      <Statistic
                        title="Savings Percentage"
                        value={data.ai_insights.potential_savings.percentage}
                        suffix="%"
                        prefix={<BarChartOutlined />}
                      />
                    </Col>
                  </Row>
                </Card>
              )}
            </Card>
          )}
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
