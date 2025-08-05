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
  strategy_overview: {
    recommended_approach: string;
    timeline_weeks: number;
    confidence_level: number;
    complexity_score: number;
  };
  migration_phases: Array<{
    phase: number;
    name: string;
    duration_weeks: number;
    activities: string[];
  }>;
  recommendations: Array<{
    type: string;
    title: string;
    description: string;
    priority: string;
  }>;
  risk_assessment: Array<{
    risk: string;
    probability: string;
    impact: string;
    mitigation: string;
  }>;
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
                      {data.strategy_overview.recommended_approach}
                    </Tag>
                  </div>
                  <div>
                    <Text strong>Timeline: </Text>
                    <Text>{data.strategy_overview.timeline_weeks} weeks</Text>
                  </div>
                  <div>
                    <Text strong>Complexity Score: </Text>
                    <Progress 
                      percent={data.strategy_overview.complexity_score * 10} 
                      steps={10}
                      size="small"
                      status={data.strategy_overview.complexity_score > 7 ? 'exception' : 
                             data.strategy_overview.complexity_score > 4 ? 'active' : 'success'}
                    />
                  </div>
                </Space>
              </Col>
              <Col xs={24} lg={8}>
                <div style={{ textAlign: 'center' }}>
                  <RobotOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
                  <div style={{ marginTop: 16 }}>
                    <Text strong>AI Confidence</Text>
                    <div style={{ fontSize: '24px', color: '#52c41a' }}>
                      {data.strategy_overview.confidence_level}%
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
                      <Tag color="green">{phase.duration_weeks} weeks</Tag>
                    </Space>
                    <List
                      size="small"
                      dataSource={phase.activities}
                      renderItem={(activity, idx) => (
                        <List.Item key={idx}>
                          <Space>
                            <Badge status="processing" />
                            {activity}
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
            <List
              dataSource={data.recommendations}
              renderItem={(rec) => (
                <List.Item>
                  <List.Item.Meta
                    avatar={<InfoCircleOutlined style={{ color: '#1890ff' }} />}
                    title={
                      <Space>
                        {rec.title}
                        <Tag color={getPriorityColor(rec.priority)}>
                          {rec.priority} Priority
                        </Tag>
                        <Tag color="blue">{rec.type}</Tag>
                      </Space>
                    }
                    description={rec.description}
                  />
                </List.Item>
              )}
            />
          </Card>

          {/* Risk Assessment */}
          <Card title="Risk Assessment" style={{ marginBottom: 24 }}>
            <List
              dataSource={data.risk_assessment}
              renderItem={(risk) => (
                <List.Item>
                  <List.Item.Meta
                    avatar={<ExclamationCircleOutlined style={{ color: '#faad14' }} />}
                    title={
                      <Space>
                        {risk.risk}
                        <Tag color={getRiskColor(risk.probability)}>
                          {risk.probability} Probability
                        </Tag>
                        <Tag color={getRiskColor(risk.impact)}>
                          {risk.impact} Impact
                        </Tag>
                      </Space>
                    }
                    description={
                      <div>
                        <Text strong>Mitigation: </Text>
                        {risk.mitigation}
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
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
