import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Typography, 
  Row, 
  Col, 
  Statistic, 
  Table, 
  Button, 
  Spin, 
  Alert,
  Tabs,
  Progress,
  Tag,
  Divider
} from 'antd';
import {
  DollarOutlined,
  CloudOutlined,
  DatabaseOutlined,
  HddOutlined,
  TeamOutlined,
  ReloadOutlined
} from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;
const { TabPane } = Tabs;

interface CostEstimationData {
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
        size_gb: number;
        recommended_instance: string;
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
        access_pattern: string;
        recommended_storage: string;
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
      duration_weeks: number;
      hours_per_week: number;
      rate_per_hour: number;
      total_hours: number;
      total_cost: number;
    }>;
  };
  grand_total: {
    one_time_migration_cost: number;
    annual_cloud_cost: number;
    total_first_year_cost: number;
  };
  ai_insights?: {
    analysis?: string;
    migration_strategy?: string;
    key_recommendations?: string[];
    cost_optimization?: string[];
    modernization_opportunities?: string[];
    timeline_estimate?: string;
    risk_assessment?: {
      high?: string[];
      medium?: string[];
      low?: string[];
    };
    priority_phases?: Array<{
      phase: number;
      components: string[];
      rationale: string;
    }>;
    success_metrics?: string[];
  };
}

const CostEstimation: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<CostEstimationData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [aiStatus, setAiStatus] = useState<any>(null);

  const fetchCostEstimation = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/api/cost-estimation');
      if (!response.ok) {
        throw new Error('Failed to fetch cost estimation');
      }
      const result = await response.json();
      setData(result);
    } catch (err) {
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

  const formatCurrency = (amount: number) => `$${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

  const serverColumns = [
    {
      title: 'Server ID',
      dataIndex: 'server_id',
      key: 'server_id',
    },
    {
      title: 'Current Specifications',
      dataIndex: 'current_specs',
      key: 'current_specs',
    },
    {
      title: 'Recommended Instance',
      dataIndex: 'recommended_instance',
      key: 'recommended_instance',
      render: (value: string, record: any) => (
        <div>
          <Tag color="blue">{value}</Tag>
          {record.confidence_level && (
            <Tag color={record.confidence_level === 'high' ? 'green' : record.confidence_level === 'medium' ? 'orange' : 'red'}>
              {record.confidence_level} confidence
            </Tag>
          )}
        </div>
      ),
    },
    {
      title: 'Monthly Cost',
      dataIndex: 'monthly_cost',
      key: 'monthly_cost',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'Annual Cost',
      dataIndex: 'annual_cost',
      key: 'annual_cost',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'AI Insights',
      key: 'insights',
      render: (record: any) => (
        <div>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {record.ai_reasoning}
          </Text>
          {record.cost_optimization_tips && record.cost_optimization_tips.length > 0 && (
            <div style={{ marginTop: 4 }}>
              {record.cost_optimization_tips.map((tip: string, index: number) => (
                <Tag key={index} color="green" style={{ fontSize: '10px', marginTop: 2 }}>
                  💡 {tip}
                </Tag>
              ))}
            </div>
          )}
        </div>
      ),
    },
  ];

  const databaseColumns = [
    {
      title: 'Database Name',
      dataIndex: 'db_name',
      key: 'db_name',
    },
    {
      title: 'Type',
      dataIndex: 'db_type',
      key: 'db_type',
      render: (value: string) => <Tag color="green">{value}</Tag>,
    },
    {
      title: 'Size (GB)',
      dataIndex: 'size_gb',
      key: 'size_gb',
    },
    {
      title: 'Recommended Instance',
      dataIndex: 'recommended_instance',
      key: 'recommended_instance',
      render: (value: string, record: any) => (
        <div>
          <Tag color="purple">{value}</Tag>
          {record.migration_complexity && (
            <Tag color={record.migration_complexity === 'low' ? 'green' : record.migration_complexity === 'medium' ? 'orange' : 'red'}>
              {record.migration_complexity} complexity
            </Tag>
          )}
        </div>
      ),
    },
    {
      title: 'Monthly Cost',
      dataIndex: 'monthly_cost',
      key: 'monthly_cost',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'Annual Cost',
      dataIndex: 'annual_cost',
      key: 'annual_cost',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'AI Insights',
      key: 'insights',
      render: (record: any) => (
        <div>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {record.ai_reasoning}
          </Text>
          {record.engine_recommendation && record.engine_recommendation !== record.db_type && (
            <div style={{ marginTop: 4 }}>
              <Tag color="blue" style={{ fontSize: '10px' }}>
                🔄 Consider {record.engine_recommendation}
              </Tag>
            </div>
          )}
          {record.performance_insights && (
            <div style={{ marginTop: 4 }}>
              <Text type="secondary" style={{ fontSize: '10px' }}>
                ⚡ {record.performance_insights}
              </Text>
            </div>
          )}
        </div>
      ),
    },
  ];

  const storageColumns = [
    {
      title: 'Share Name',
      dataIndex: 'share_name',
      key: 'share_name',
    },
    {
      title: 'Size (GB)',
      dataIndex: 'size_gb',
      key: 'size_gb',
    },
    {
      title: 'Access Pattern',
      dataIndex: 'access_pattern',
      key: 'access_pattern',
      render: (value: string) => <Tag color={value === 'Hot' ? 'red' : value === 'Warm' ? 'orange' : 'blue'}>{value}</Tag>,
    },
    {
      title: 'Recommended Storage',
      dataIndex: 'recommended_storage',
      key: 'recommended_storage',
      render: (value: string, record: any) => (
        <div>
          <Tag color="cyan">{value}</Tag>
          {record.confidence_level && (
            <Tag color={record.confidence_level === 'high' ? 'green' : record.confidence_level === 'medium' ? 'orange' : 'red'}>
              {record.confidence_level} confidence
            </Tag>
          )}
        </div>
      ),
    },
    {
      title: 'Monthly Cost',
      dataIndex: 'monthly_cost',
      key: 'monthly_cost',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'Annual Cost',
      dataIndex: 'annual_cost',
      key: 'annual_cost',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'AI Insights',
      key: 'insights',
      render: (record: any) => (
        <div>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {record.ai_reasoning}
          </Text>
          {record.lifecycle_policy && (
            <div style={{ marginTop: 4 }}>
              <Tag color="green" style={{ fontSize: '10px' }}>
                📅 {record.lifecycle_policy}
              </Tag>
            </div>
          )}
          {record.cost_optimization_tips && record.cost_optimization_tips.length > 0 && (
            <div style={{ marginTop: 4 }}>
              {record.cost_optimization_tips.map((tip: string, index: number) => (
                <Tag key={index} color="gold" style={{ fontSize: '10px', marginTop: 2 }}>
                  💰 {tip}
                </Tag>
              ))}
            </div>
          )}
          {record.performance_considerations && (
            <div style={{ marginTop: 4 }}>
              <Text type="secondary" style={{ fontSize: '10px' }}>
                ⚡ {record.performance_considerations}
              </Text>
            </div>
          )}
        </div>
      ),
    },
  ];

  const serviceColumns = [
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
    },
    {
      title: 'Duration (Weeks)',
      dataIndex: 'duration_weeks',
      key: 'duration_weeks',
    },
    {
      title: 'Hours/Week',
      dataIndex: 'hours_per_week',
      key: 'hours_per_week',
    },
    {
      title: 'Rate/Hour',
      dataIndex: 'rate_per_hour',
      key: 'rate_per_hour',
      render: (value: number) => formatCurrency(value),
    },
    {
      title: 'Total Hours',
      dataIndex: 'total_hours',
      key: 'total_hours',
    },
    {
      title: 'Total Cost',
      dataIndex: 'total_cost',
      key: 'total_cost',
      render: (value: number) => formatCurrency(value),
    },
  ];

  if (error) {
    return (
      <Card>
        <Alert
          message="Error"
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
                    <Tag color={aiStatus.ai_enabled ? 'green' : 'orange'}>
                      {aiStatus.ai_enabled ? '🤖 AI-Powered' : '📋 Rule-Based'} Recommendations
                    </Tag>
                    <Text type="secondary" style={{ marginLeft: 8, fontSize: '12px' }}>
                      {aiStatus.message}
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
              <Col xs={24} sm={12} lg={6}>
                <Statistic
                  title="One-Time Migration Cost"
                  value={data.grand_total.one_time_migration_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<TeamOutlined />}
                />
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <Statistic
                  title="Annual Cloud Cost"
                  value={data.grand_total.annual_cloud_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<CloudOutlined />}
                />
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <Statistic
                  title="Total First Year Cost"
                  value={data.grand_total.total_first_year_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<DollarOutlined />}
                />
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <Statistic
                  title="Monthly Cloud Operations"
                  value={data.cloud_infrastructure.total_monthly_cost}
                  formatter={(value) => formatCurrency(Number(value))}
                  prefix={<CloudOutlined />}
                />
              </Col>
            </Row>
            
            <Divider />
            
            <Row gutter={[24, 16]}>
              <Col span={24}>
                <Title level={4}>Cost Breakdown Distribution</Title>
                <Row gutter={16}>
                  <Col span={8}>
                    <Card size="small">
                      <Statistic
                        title="Migration Services"
                        value={(data.grand_total.one_time_migration_cost / data.grand_total.total_first_year_cost * 100)}
                        suffix="%"
                        precision={1}
                      />
                    </Card>
                  </Col>
                  <Col span={8}>
                    <Card size="small">
                      <Statistic
                        title="Cloud Infrastructure"
                        value={(data.grand_total.annual_cloud_cost / data.grand_total.total_first_year_cost * 100)}
                        suffix="%"
                        precision={1}
                      />
                    </Card>
                  </Col>
                  <Col span={8}>
                    <Card size="small">
                      <Statistic
                        title="ROI Timeline"
                        value="12-18"
                        suffix="months"
                      />
                    </Card>
                  </Col>
                </Row>
              </Col>
            </Row>
          </Card>

          {/* Detailed Breakdown */}
          <Card>
            <Tabs defaultActiveKey="infrastructure">
              <TabPane 
                tab={
                  <span>
                    <CloudOutlined />
                    Cloud Infrastructure
                  </span>
                } 
                key="infrastructure"
              >
                <Row gutter={[16, 16]}>
                  <Col span={24}>
                    <Card title="Servers" size="small" style={{ marginBottom: 16 }}>
                      <Statistic
                        title="Total Annual Cost"
                        value={data.cloud_infrastructure.servers.total_annual_cost}
                        formatter={(value) => formatCurrency(Number(value))}
                        style={{ marginBottom: 16 }}
                      />
                      <Table
                        dataSource={data.cloud_infrastructure.servers.server_recommendations}
                        columns={serverColumns}
                        pagination={false}
                        size="small"
                        rowKey="server_id"
                        scroll={{ x: true }}
                      />
                    </Card>
                  </Col>
                  
                  <Col span={24}>
                    <Card title="Databases" size="small" style={{ marginBottom: 16 }}>
                      <Statistic
                        title="Total Annual Cost"
                        value={data.cloud_infrastructure.databases.total_annual_cost}
                        formatter={(value) => formatCurrency(Number(value))}
                        style={{ marginBottom: 16 }}
                      />
                      <Table
                        dataSource={data.cloud_infrastructure.databases.database_recommendations}
                        columns={databaseColumns}
                        pagination={false}
                        size="small"
                        rowKey="db_name"
                        scroll={{ x: true }}
                      />
                    </Card>
                  </Col>
                  
                  <Col span={24}>
                    <Card title="Storage" size="small">
                      <Statistic
                        title="Total Annual Cost"
                        value={data.cloud_infrastructure.storage.total_annual_cost}
                        formatter={(value) => formatCurrency(Number(value))}
                        style={{ marginBottom: 16 }}
                      />
                      <Table
                        dataSource={data.cloud_infrastructure.storage.storage_recommendations}
                        columns={storageColumns}
                        pagination={false}
                        size="small"
                        rowKey="share_name"
                        scroll={{ x: true }}
                      />
                    </Card>
                  </Col>
                </Row>
              </TabPane>

              <TabPane 
                tab={
                  <span>
                    <TeamOutlined />
                    Professional Services
                  </span>
                } 
                key="services"
              >
                <Row gutter={[16, 16]}>
                  <Col span={24}>
                    <Statistic
                      title="Total Professional Services Cost"
                      value={data.migration_services.total_professional_services_cost}
                      formatter={(value) => formatCurrency(Number(value))}
                      style={{ marginBottom: 24 }}
                    />
                    <Table
                      dataSource={data.migration_services.resource_breakdown}
                      columns={serviceColumns}
                      pagination={false}
                      rowKey="role"
                    />
                  </Col>
                </Row>
              </TabPane>

              <TabPane 
                tab={
                  <span>
                    🤖 AI Insights
                  </span>
                } 
                key="ai-insights"
              >
                <Row gutter={[16, 16]}>
                  <Col span={24}>
                    {data.ai_insights ? (
                      <div>
                        {data.ai_insights.analysis && (
                          <Card title="Migration Strategy Analysis" style={{ marginBottom: 16 }}>
                            <Paragraph>{data.ai_insights.analysis}</Paragraph>
                          </Card>
                        )}
                        
                        {data.ai_insights.migration_strategy && (
                          <Card title="Recommended Migration Approach" style={{ marginBottom: 16 }}>
                            <Tag color="blue" style={{ fontSize: '14px', padding: '8px 16px' }}>
                              {data.ai_insights.migration_strategy}
                            </Tag>
                          </Card>
                        )}
                        
                        {data.ai_insights.key_recommendations && data.ai_insights.key_recommendations.length > 0 && (
                          <Card title="Key Recommendations" style={{ marginBottom: 16 }}>
                            <ul>
                              {data.ai_insights.key_recommendations.map((rec: string, index: number) => (
                                <li key={index} style={{ marginBottom: 8 }}>
                                  <Text>{rec}</Text>
                                </li>
                              ))}
                            </ul>
                          </Card>
                        )}
                        
                        {data.ai_insights.cost_optimization && data.ai_insights.cost_optimization.length > 0 && (
                          <Card title="Cost Optimization Opportunities" style={{ marginBottom: 16 }}>
                            <Row gutter={[8, 8]}>
                              {data.ai_insights.cost_optimization.map((opp: string, index: number) => (
                                <Col key={index} span={24}>
                                  <Tag color="green" style={{ width: '100%', padding: '8px', marginBottom: 8 }}>
                                    💰 {opp}
                                  </Tag>
                                </Col>
                              ))}
                            </Row>
                          </Card>
                        )}
                        
                        {data.ai_insights.modernization_opportunities && data.ai_insights.modernization_opportunities.length > 0 && (
                          <Card title="Modernization Opportunities" style={{ marginBottom: 16 }}>
                            <Row gutter={[8, 8]}>
                              {data.ai_insights.modernization_opportunities.map((mod: string, index: number) => (
                                <Col key={index} span={24}>
                                  <Tag color="purple" style={{ width: '100%', padding: '8px', marginBottom: 8 }}>
                                    🚀 {mod}
                                  </Tag>
                                </Col>
                              ))}
                            </Row>
                          </Card>
                        )}
                        
                        {data.ai_insights.timeline_estimate && (
                          <Card title="Timeline Estimate">
                            <Statistic
                              title="Estimated Migration Duration"
                              value={data.ai_insights.timeline_estimate}
                              prefix="⏱️"
                            />
                          </Card>
                        )}
                      </div>
                    ) : (
                      <Card>
                        <Alert
                          message="AI Insights Setup Required"
                          description={
                            <div>
                              <Paragraph>
                                AI-powered insights are currently not available. To enable AI recommendations:
                              </Paragraph>
                              <ol style={{ paddingLeft: 20 }}>
                                <li>Set up AWS account with Bedrock access</li>
                                <li>Request access to Claude 3 Sonnet model</li>
                                <li>Configure AWS credentials in backend/.env file</li>
                                <li>Restart the backend server</li>
                              </ol>
                              <Paragraph>
                                <Text strong>Current Status:</Text> {aiStatus?.message || 'Using rule-based recommendations'}
                              </Paragraph>
                              <Paragraph>
                                <Text type="secondary">
                                  See BEDROCK_SETUP_GUIDE.md for detailed setup instructions.
                                </Text>
                              </Paragraph>
                            </div>
                          }
                          type="info"
                          showIcon
                        />
                      </Card>
                    )}
                  </Col>
                </Row>
              </TabPane>
            </Tabs>
          </Card>
        </>
      ) : (
        <Card>
          <Paragraph>No cost estimation data available. Click refresh to calculate.</Paragraph>
        </Card>
      )}
    </div>
  );
};

export default CostEstimation;
