import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Typography, 
  Row, 
  Col, 
  Button, 
  Spin, 
  Alert,
  Tabs,
  Tag,
  Table,
  Divider,
  Progress,
  Timeline,
  Statistic
} from 'antd';
import {
  CloudOutlined,
  DatabaseOutlined,
  HddOutlined,
  ReloadOutlined,
  RocketOutlined,
  SafetyOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;
const { TabPane } = Tabs;

interface MigrationStrategyData {
  migration_approach: {
    overall_strategy: string;
    rationale: string;
    complexity_level: string;
    estimated_duration: string;
  };
  component_strategies: {
    servers: Array<{
      server_id: string;
      current_state: string;
      target_state: string;
      migration_type: string;
      rationale: string;
      complexity: string;
      estimated_effort: string;
    }>;
    databases: Array<{
      db_name: string;
      current_engine: string;
      target_engine: string;
      migration_type: string;
      approach: string;
      data_migration_strategy: string;
      downtime_estimate: string;
      complexity: string;
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
  migration_phases: Array<{
    phase: number;
    name: string;
    duration: string;
    components: string[];
    dependencies: string[];
    risks: string[];
    success_criteria: string[];
  }>;
  risk_assessment: {
    high_risks: string[];
    medium_risks: string[];
    low_risks: string[];
    mitigation_strategies: { [key: string]: string };
  };
  recommendations: {
    quick_wins: string[];
    modernization_opportunities: string[];
    cost_optimization: string[];
    performance_improvements: string[];
  };
}

const MigrationStrategy: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<MigrationStrategyData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchMigrationStrategy = async () => {
    console.log('🔧 MigrationStrategy: Starting fetch...');
    setLoading(true);
    setError(null);
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
      
      const requestData = { analysis_type: 'comprehensive' };
      console.log('🔧 MigrationStrategy: Request data:', requestData);
      console.log('🔧 MigrationStrategy: Making fetch request...');
      
      const response = await fetch('http://localhost:5000/api/migration-strategy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      console.log('🔧 MigrationStrategy: Response status:', response.status);
      console.log('🔧 MigrationStrategy: Response headers:', Object.fromEntries(response.headers));
      
      if (!response.ok) {
        throw new Error(`Failed to fetch migration strategy: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('🔧 MigrationStrategy: Data received:', result);
      console.log('🔧 MigrationStrategy: Setting data and clearing error...');
      setData(result);
      setError(null); // Explicitly clear any previous error
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error';
      console.error('🔧 MigrationStrategy: Error occurred:', err);
      console.error('🔧 MigrationStrategy: Error message:', errorMessage);
      setError(`Failed to fetch migration strategy: ${errorMessage}`);
    } finally {
      console.log('🔧 MigrationStrategy: Setting loading to false');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMigrationStrategy();
  }, []);

  const getComplexityColor = (complexity: string) => {
    switch (complexity?.toLowerCase()) {
      case 'low': return 'green';
      case 'medium': return 'orange';
      case 'high': return 'red';
      default: return 'blue';
    }
  };

  const getRiskColor = (risk: string) => {
    if (risk.includes('high')) return 'red';
    if (risk.includes('medium')) return 'orange';
    return 'green';
  };

  const serverColumns = [
    {
      title: 'Server ID',
      dataIndex: 'server_id',
      key: 'server_id',
    },
    {
      title: 'Current State',
      dataIndex: 'current_state',
      key: 'current_state',
    },
    {
      title: 'Target State',
      dataIndex: 'target_state',
      key: 'target_state',
      render: (value: string) => <Tag color="blue">{value}</Tag>,
    },
    {
      title: 'Migration Type',
      dataIndex: 'migration_type',
      key: 'migration_type',
      render: (value: string) => <Tag color="purple">{value}</Tag>,
    },
    {
      title: 'Complexity',
      dataIndex: 'complexity',
      key: 'complexity',
      render: (value: string) => <Tag color={getComplexityColor(value)}>{value}</Tag>,
    },
    {
      title: 'Estimated Effort',
      dataIndex: 'estimated_effort',
      key: 'estimated_effort',
    },
    {
      title: 'Rationale',
      dataIndex: 'rationale',
      key: 'rationale',
      render: (value: string) => <Text style={{ fontSize: '12px' }}>{value}</Text>,
    },
  ];

  const databaseColumns = [
    {
      title: 'Database',
      dataIndex: 'db_name',
      key: 'db_name',
    },
    {
      title: 'Current Engine',
      dataIndex: 'current_engine',
      key: 'current_engine',
      render: (value: string) => <Tag color="green">{value}</Tag>,
    },
    {
      title: 'Target Engine',
      dataIndex: 'target_engine',
      key: 'target_engine',
      render: (value: string) => <Tag color="blue">{value}</Tag>,
    },
    {
      title: 'Migration Type',
      dataIndex: 'migration_type',
      key: 'migration_type',
      render: (value: string) => <Tag color="purple">{value}</Tag>,
    },
    {
      title: 'Data Strategy',
      dataIndex: 'data_migration_strategy',
      key: 'data_migration_strategy',
    },
    {
      title: 'Downtime',
      dataIndex: 'downtime_estimate',
      key: 'downtime_estimate',
    },
    {
      title: 'Complexity',
      dataIndex: 'complexity',
      key: 'complexity',
      render: (value: string) => <Tag color={getComplexityColor(value)}>{value}</Tag>,
    },
  ];

  const storageColumns = [
    {
      title: 'Share Name',
      dataIndex: 'share_name',
      key: 'share_name',
    },
    {
      title: 'Current Type',
      dataIndex: 'current_type',
      key: 'current_type',
    },
    {
      title: 'Target Type',
      dataIndex: 'target_type',
      key: 'target_type',
      render: (value: string) => <Tag color="cyan">{value}</Tag>,
    },
    {
      title: 'Migration Method',
      dataIndex: 'migration_method',
      key: 'migration_method',
      render: (value: string) => <Tag color="orange">{value}</Tag>,
    },
    {
      title: 'Sync Strategy',
      dataIndex: 'sync_strategy',
      key: 'sync_strategy',
    },
    {
      title: 'Cutover Approach',
      dataIndex: 'cutover_approach',
      key: 'cutover_approach',
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
                  <RocketOutlined style={{ marginRight: 8 }} />
                  Migration Strategy & Planning
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
            <Paragraph style={{ marginTop: 16 }}>Generating migration strategy...</Paragraph>
          </div>
        </Card>
      ) : data ? (
        <>
          {/* Executive Summary */}
          <Card title="Migration Strategy Overview" style={{ marginBottom: 24 }}>
            <Row gutter={[24, 16]}>
              <Col xs={24} lg={12}>
                <Card size="small" title="Overall Approach">
                  <Tag color="blue" style={{ fontSize: '16px', padding: '8px 16px', marginBottom: 16 }}>
                    {data.migration_approach?.overall_strategy || 'Hybrid Migration'}
                  </Tag>
                  <Paragraph>{data.migration_approach?.rationale || 'Comprehensive migration strategy combining lift-and-shift with selective modernization.'}</Paragraph>
                </Card>
              </Col>
              <Col xs={24} lg={12}>
                <Row gutter={[16, 16]}>
                  <Col span={12}>
                    <Statistic
                      title="Complexity Level"
                      value={data.migration_approach?.complexity_level || 'Medium'}
                      prefix={<SafetyOutlined />}
                      valueStyle={{ color: getComplexityColor(data.migration_approach?.complexity_level || 'medium') }}
                    />
                  </Col>
                  <Col span={12}>
                    <Statistic
                      title="Estimated Duration"
                      value={data.migration_approach?.estimated_duration || '12-16 weeks'}
                      prefix={<ClockCircleOutlined />}
                    />
                  </Col>
                </Row>
              </Col>
            </Row>
          </Card>

          {/* Main Content Tabs */}
          <Card>
            <Tabs defaultActiveKey="components">
              <TabPane 
                tab={
                  <span>
                    <CloudOutlined />
                    Component Strategies
                  </span>
                } 
                key="components"
              >
                <Row gutter={[16, 16]}>
                  <Col span={24}>
                    <Card title="Server Migration Strategy" size="small" style={{ marginBottom: 16 }}>
                      <Table
                        dataSource={data.component_strategies?.servers || []}
                        columns={serverColumns}
                        pagination={false}
                        size="small"
                        rowKey="server_id"
                        scroll={{ x: true }}
                      />
                    </Card>
                  </Col>
                  
                  <Col span={24}>
                    <Card title="Database Migration Strategy" size="small" style={{ marginBottom: 16 }}>
                      <Table
                        dataSource={data.component_strategies?.databases || []}
                        columns={databaseColumns}
                        pagination={false}
                        size="small"
                        rowKey="db_name"
                        scroll={{ x: true }}
                      />
                    </Card>
                  </Col>
                  
                  <Col span={24}>
                    <Card title="Storage Migration Strategy" size="small">
                      <Table
                        dataSource={data.component_strategies?.storage || []}
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
                    <ClockCircleOutlined />
                    Migration Phases
                  </span>
                } 
                key="phases"
              >
                <Row gutter={[16, 16]}>
                  <Col span={24}>
                    <Timeline>
                      {(data.migration_phases || []).map((phase, index) => (
                        <Timeline.Item 
                          key={index}
                          dot={<CheckCircleOutlined style={{ fontSize: '16px' }} />}
                          color="blue"
                        >
                          <Card size="small" style={{ marginBottom: 16 }}>
                            <Row justify="space-between" align="middle">
                              <Col>
                                <Title level={4} style={{ margin: 0 }}>
                                  Phase {phase.phase}: {phase.name}
                                </Title>
                              </Col>
                              <Col>
                                <Tag color="blue">{phase.duration}</Tag>
                              </Col>
                            </Row>
                            
                            <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
                              <Col xs={24} md={12}>
                                <Text strong>Components:</Text>
                                <ul style={{ marginTop: 8 }}>
                                  {phase.components.map((component, idx) => (
                                    <li key={idx}>{component}</li>
                                  ))}
                                </ul>
                              </Col>
                              <Col xs={24} md={12}>
                                <Text strong>Success Criteria:</Text>
                                <ul style={{ marginTop: 8 }}>
                                  {phase.success_criteria.map((criteria, idx) => (
                                    <li key={idx}>{criteria}</li>
                                  ))}
                                </ul>
                              </Col>
                            </Row>
                            
                            {phase.risks.length > 0 && (
                              <div style={{ marginTop: 16 }}>
                                <Text strong>Key Risks:</Text>
                                <div style={{ marginTop: 8 }}>
                                  {phase.risks.map((risk, idx) => (
                                    <Tag key={idx} color="orange" style={{ marginBottom: 4 }}>
                                      ⚠️ {risk}
                                    </Tag>
                                  ))}
                                </div>
                              </div>
                            )}
                          </Card>
                        </Timeline.Item>
                      ))}
                    </Timeline>
                  </Col>
                </Row>
              </TabPane>

              <TabPane 
                tab={
                  <span>
                    <SafetyOutlined />
                    Risk Assessment
                  </span>
                } 
                key="risks"
              >
                <Row gutter={[16, 16]}>
                  <Col xs={24} lg={8}>
                    <Card title="High Risk Items" size="small" style={{ height: '100%' }}>
                      {(data.risk_assessment?.high_risks || []).map((risk, index) => (
                        <Tag key={index} color="red" style={{ width: '100%', marginBottom: 8, padding: '8px' }}>
                          🔴 {risk}
                        </Tag>
                      ))}
                    </Card>
                  </Col>
                  <Col xs={24} lg={8}>
                    <Card title="Medium Risk Items" size="small" style={{ height: '100%' }}>
                      {(data.risk_assessment?.medium_risks || []).map((risk, index) => (
                        <Tag key={index} color="orange" style={{ width: '100%', marginBottom: 8, padding: '8px' }}>
                          🟡 {risk}
                        </Tag>
                      ))}
                    </Card>
                  </Col>
                  <Col xs={24} lg={8}>
                    <Card title="Low Risk Items" size="small" style={{ height: '100%' }}>
                      {(data.risk_assessment?.low_risks || []).map((risk, index) => (
                        <Tag key={index} color="green" style={{ width: '100%', marginBottom: 8, padding: '8px' }}>
                          🟢 {risk}
                        </Tag>
                      ))}
                    </Card>
                  </Col>
                </Row>
              </TabPane>

              <TabPane 
                tab={
                  <span>
                    🎯 Recommendations
                  </span>
                } 
                key="recommendations"
              >
                <Row gutter={[16, 16]}>
                  <Col xs={24} lg={12}>
                    <Card title="Quick Wins" size="small" style={{ marginBottom: 16 }}>
                      {(data.recommendations?.quick_wins || []).map((win, index) => (
                        <Tag key={index} color="green" style={{ width: '100%', marginBottom: 8, padding: '8px' }}>
                          ⚡ {win}
                        </Tag>
                      ))}
                    </Card>
                    
                    <Card title="Cost Optimization" size="small">
                      {(data.recommendations?.cost_optimization || []).map((opt, index) => (
                        <Tag key={index} color="gold" style={{ width: '100%', marginBottom: 8, padding: '8px' }}>
                          💰 {opt}
                        </Tag>
                      ))}
                    </Card>
                  </Col>
                  <Col xs={24} lg={12}>
                    <Card title="Modernization Opportunities" size="small" style={{ marginBottom: 16 }}>
                      {(data.recommendations?.modernization_opportunities || []).map((mod, index) => (
                        <Tag key={index} color="purple" style={{ width: '100%', marginBottom: 8, padding: '8px' }}>
                          🚀 {mod}
                        </Tag>
                      ))}
                    </Card>
                    
                    <Card title="Performance Improvements" size="small">
                      {(data.recommendations?.performance_improvements || []).map((perf, index) => (
                        <Tag key={index} color="blue" style={{ width: '100%', marginBottom: 8, padding: '8px' }}>
                          ⚡ {perf}
                        </Tag>
                      ))}
                    </Card>
                  </Col>
                </Row>
              </TabPane>
            </Tabs>
          </Card>
        </>
      ) : (
        <Card>
          <Paragraph>No migration strategy data available. Click refresh to generate.</Paragraph>
        </Card>
      )}
    </div>
  );
};

export default MigrationStrategy;
