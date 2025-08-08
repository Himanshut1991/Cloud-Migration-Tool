import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Typography, 
  Row, 
  Col, 
  Button, 
  Spin, 
  Alert,
  Tag,
  Timeline,
  Progress,
  List,
  Space,
  Badge
} from 'antd';
import {
  CloudOutlined,
  ReloadOutlined,
  RobotOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  InfoCircleOutlined
} from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;

interface MigrationStrategyData {
  migration_approach: {
    overall_strategy: string;
    estimated_duration: string;
    complexity_level: string;
    rationale: string;
  };
  migration_phases: Array<{
    phase: number;
    name: string;
    duration: string;
    components: string[];
    dependencies: string[];
    risks: string[];
    success_criteria: string[];
  }>;
  recommendations: {
    quick_wins: string[];
    cost_optimization: string[];
    performance_improvements: string[];
    modernization_opportunities: string[];
  };
  risk_assessment: {
    high_risks: string[];
    medium_risks: string[];
    low_risks: string[];
    mitigation_strategies: Record<string, string>;
  };
  component_strategies: {
    servers: Array<{
      server_id: string;
      migration_type: string;
      current_state: string;
      target_state: string;
      complexity: string;
      estimated_effort: string;
      rationale: string;
    }>;
    databases: Array<{
      db_name: string;
      current_engine: string;
      target_engine: string;
      migration_type: string;
      approach: string;
      complexity: string;
      data_migration_strategy: string;
      downtime_estimate: string;
    }>;
    storage: Array<{
      share_name: string;
      current_type: string;
      target_type: string;
      migration_method: string;
      sync_strategy: string;
      cutover_approach: string;
    }>;
  };
  ai_insights?: {
    confidence_level: number;
    ai_model_used: string;
    fallback_used: boolean;
    strategic_recommendations: string[];
  };
}

const MigrationStrategySimple: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<MigrationStrategyData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchMigrationStrategy = async () => {
    console.log('Fetching migration strategy...');
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:5000/api/migration-strategy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      });
      console.log('Migration strategy response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch migration strategy: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('Migration strategy data:', result);
      setData(result);
    } catch (err) {
      console.error('Migration strategy error:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMigrationStrategy();
  }, []);

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high': return 'red';
      case 'medium': return 'orange';
      case 'low': return 'green';
      default: return 'blue';
    }
  };

  const getRiskColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'high': return 'red';
      case 'medium': return 'orange';
      case 'low': return 'green';
      default: return 'blue';
    }
  };

  if (error) {
    return (
      <Card>
        <Alert
          message="Error Loading Migration Strategy"
          description={error}
          type="error"
          action={
            <Button size="small" onClick={fetchMigrationStrategy}>
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
                  <CloudOutlined style={{ marginRight: 8 }} />
                  Migration Strategy Analysis
                </Title>
              </Col>
              <Col>
                <Button 
                  type="primary" 
                  icon={<ReloadOutlined />} 
                  onClick={fetchMigrationStrategy}
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
            <Paragraph style={{ marginTop: 16 }}>Analyzing migration strategy...</Paragraph>
          </div>
        </Card>
      ) : data ? (
        <>
          {/* Strategy Overview */}
          <Card title="Strategy Overview" style={{ marginBottom: 24 }}>
            <Row gutter={[24, 16]}>
              <Col xs={24} lg={16}>
                <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                  <div>
                    <Text strong>Recommended Approach: </Text>
                    <Tag color="blue" style={{ fontSize: '14px' }}>
                      {data.migration_approach.overall_strategy}
                    </Tag>
                  </div>
                  <div>
                    <Text strong>Timeline: </Text>
                    <Text>{data.migration_approach.estimated_duration}</Text>
                  </div>
                  <div>
                    <Text strong>Complexity Level: </Text>
                    <Tag color={data.migration_approach.complexity_level.toLowerCase() === 'high' ? 'red' : 
                                data.migration_approach.complexity_level.toLowerCase() === 'medium' ? 'orange' : 'green'}>
                      {data.migration_approach.complexity_level}
                    </Tag>
                  </div>
                </Space>
              </Col>
              <Col xs={24} lg={8}>
                <div style={{ textAlign: 'center' }}>
                  <RobotOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
                  <div style={{ marginTop: 16 }}>
                    <Text strong>Rationale</Text>
                    <div style={{ fontSize: '14px', color: '#666', marginTop: 8 }}>
                      {data.migration_approach.rationale}
                    </div>
                  </div>
                </div>
              </Col>
            </Row>
          </Card>

          {/* Migration Phases */}
          <Card title="Migration Phases" style={{ marginBottom: 24 }}>
            <Timeline>
              {data.migration_phases.map((phase, index) => (
                <Timeline.Item
                  key={phase.phase}
                  dot={<CheckCircleOutlined style={{ fontSize: '16px' }} />}
                  color="blue"
                >
                  <div style={{ marginBottom: 16 }}>
                    <Space align="baseline">
                      <Title level={4} style={{ margin: 0 }}>
                        Phase {phase.phase}: {phase.name}
                      </Title>
                      <Tag color="green">{phase.duration}</Tag>
                    </Space>
                    <List
                      size="small"
                      dataSource={phase.components}
                      renderItem={(component: string, idx) => (
                        <List.Item key={idx}>
                          <Space>
                            <Badge status="processing" />
                            {component}
                          </Space>
                        </List.Item>
                      )}
                    />
                  </div>
                </Timeline.Item>
              ))}
            </Timeline>
          </Card>

          {/* Recommendations */}
          <Card title="Strategic Recommendations" style={{ marginBottom: 24 }}>
            <Row gutter={[16, 16]}>
              <Col xs={24} md={12}>
                <Card size="small" title="Quick Wins" style={{ height: '100%' }}>
                  <List
                    size="small"
                    dataSource={data.recommendations.quick_wins}
                    renderItem={(item: string) => (
                      <List.Item>
                        <Space>
                          <CheckCircleOutlined style={{ color: '#52c41a' }} />
                          {item}
                        </Space>
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>
              <Col xs={24} md={12}>
                <Card size="small" title="Cost Optimization" style={{ height: '100%' }}>
                  <List
                    size="small"
                    dataSource={data.recommendations.cost_optimization}
                    renderItem={(item: string) => (
                      <List.Item>
                        <Space>
                          <InfoCircleOutlined style={{ color: '#1890ff' }} />
                          {item}
                        </Space>
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>
              <Col xs={24} md={12}>
                <Card size="small" title="Performance Improvements" style={{ height: '100%' }}>
                  <List
                    size="small"
                    dataSource={data.recommendations.performance_improvements}
                    renderItem={(item: string) => (
                      <List.Item>
                        <Space>
                          <InfoCircleOutlined style={{ color: '#faad14' }} />
                          {item}
                        </Space>
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>
              <Col xs={24} md={12}>
                <Card size="small" title="Modernization Opportunities" style={{ height: '100%' }}>
                  <List
                    size="small"
                    dataSource={data.recommendations.modernization_opportunities}
                    renderItem={(item: string) => (
                      <List.Item>
                        <Space>
                          <RobotOutlined style={{ color: '#722ed1' }} />
                          {item}
                        </Space>
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>
            </Row>
          </Card>

          {/* Risk Assessment */}
          <Card title="Risk Assessment" style={{ marginBottom: 24 }}>
            <Row gutter={[16, 16]}>
              <Col xs={24} md={8}>
                <Card size="small" title="High Risks" style={{ height: '100%' }}>
                  <List
                    size="small"
                    dataSource={data.risk_assessment.high_risks}
                    renderItem={(risk: string) => (
                      <List.Item>
                        <Space>
                          <ExclamationCircleOutlined style={{ color: '#ff4d4f' }} />
                          <Text>{risk}</Text>
                        </Space>
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>
              <Col xs={24} md={8}>
                <Card size="small" title="Medium Risks" style={{ height: '100%' }}>
                  <List
                    size="small"
                    dataSource={data.risk_assessment.medium_risks}
                    renderItem={(risk: string) => (
                      <List.Item>
                        <Space>
                          <ExclamationCircleOutlined style={{ color: '#faad14' }} />
                          <Text>{risk}</Text>
                        </Space>
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>
              <Col xs={24} md={8}>
                <Card size="small" title="Low Risks" style={{ height: '100%' }}>
                  <List
                    size="small"
                    dataSource={data.risk_assessment.low_risks}
                    renderItem={(risk: string) => (
                      <List.Item>
                        <Space>
                          <CheckCircleOutlined style={{ color: '#52c41a' }} />
                          <Text>{risk}</Text>
                        </Space>
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>
            </Row>
            {data.risk_assessment.mitigation_strategies && Object.keys(data.risk_assessment.mitigation_strategies).length > 0 && (
              <Card size="small" title="Mitigation Strategies" style={{ marginTop: 16 }}>
                <List
                  size="small"
                  dataSource={Object.entries(data.risk_assessment.mitigation_strategies)}
                  renderItem={([risk, mitigation]: [string, string]) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={<InfoCircleOutlined style={{ color: '#1890ff' }} />}
                        title={<Text strong>{risk}</Text>}
                        description={mitigation}
                      />
                    </List.Item>
                  )}
                />
              </Card>
            )}
          </Card>

          {/* AI Insights */}
          {data.ai_insights && (
            <Card 
              title={
                <Space>
                  <RobotOutlined />
                  AI Strategy Analysis
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
                  description="AI services are temporarily unavailable. Using intelligent rule-based migration strategy recommendations."
                  type="info" 
                  style={{ marginBottom: 16 }}
                />
              )}
              
              {!data.ai_insights.fallback_used && (
                <Alert 
                  message="AI-Powered Migration Strategy Active" 
                  description={`Strategy analysis powered by ${data.ai_insights.ai_model_used} with ${Math.round(data.ai_insights.confidence_level * 100)}% confidence level.`}
                  type="success" 
                  style={{ marginBottom: 16 }}
                />
              )}
              
              <Card size="small" title="🎯 Strategic AI Recommendations">
                {data.ai_insights.strategic_recommendations?.map((recommendation, index) => (
                  <div key={index} style={{ marginBottom: 12, padding: '8px', backgroundColor: '#f6f8ff', borderRadius: '4px' }}>
                    <Text strong style={{ color: '#1890ff' }}>#{index + 1}</Text>
                    <Text style={{ marginLeft: 8 }}>{recommendation}</Text>
                  </div>
                ))}
              </Card>
            </Card>
          )}
        </>
      ) : (
        <Card>
          <div style={{ textAlign: 'center', padding: '50px 0' }}>
            <Paragraph>No migration strategy data available. Click refresh to load data.</Paragraph>
          </div>
        </Card>
      )}
    </div>
  );
};

export default MigrationStrategySimple;
