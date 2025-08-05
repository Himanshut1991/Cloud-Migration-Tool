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
  DatePicker,
  Space,
  Statistic,
  List,
  Badge
} from 'antd';
import {
  CalendarOutlined,
  ReloadOutlined,
  RobotOutlined,
  CheckCircleOutlined,
  TeamOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons';
import dayjs from 'dayjs';

const { Title, Paragraph, Text } = Typography;

interface TimelineData {
  project_overview: {
    total_duration_weeks: number;
    total_duration_months: number;
    estimated_start_date: string;
    estimated_end_date: string;
    confidence_level: string;
    complexity_score: number;
  };
  phases: Array<{
    phase: number;
    title: string;
    description: string;
    duration_weeks: number;
    start_week: number;
    end_week: number;
    dependencies: string[];
    milestones: string[];
    components: string[];
    risks: string[];
    resources_required: string[];
    status: string;
  }>;
  critical_path: string[];
  resource_allocation: Array<{
    role: string;
    weeks_allocated: number;
    overlap_phases: number[];
    peak_utilization_week: number;
  }>;
  risk_mitigation: Array<{
    risk: string;
    probability: string;
    impact: string;
    mitigation_strategy: string;
    timeline_buffer_weeks: number;
  }>;
  success_criteria: string[];
  ai_insights: {
    optimization_suggestions: string[];
    timeline_risks: string[];
    resource_recommendations: string[];
  };
}

const TimelineSimple: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<TimelineData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [customStartDate, setCustomStartDate] = useState<dayjs.Dayjs | null>(null);

  const fetchTimeline = async (startDate?: string) => {
    console.log('Fetching timeline...');
    setLoading(true);
    setError(null);
    try {
      const payload = startDate ? { start_date: startDate } : {};
      const response = await fetch('http://localhost:5000/api/timeline', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });
      console.log('Timeline response status:', response.status);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch timeline: ${response.status}`);
      }
      
      const result = await response.json();
      console.log('Timeline data:', result);
      setData(result);
    } catch (err) {
      console.error('Timeline error:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTimeline();
  }, []);

  const handleDateChange = (date: dayjs.Dayjs | null) => {
    setCustomStartDate(date);
    if (date) {
      fetchTimeline(date.format('YYYY-MM-DD'));
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed': return 'green';
      case 'in-progress': return 'blue';
      case 'pending': return 'orange';
      case 'blocked': return 'red';
      default: return 'default';
    }
  };

  if (error) {
    return (
      <Card>
        <Alert
          message="Error Loading Timeline"
          description={error}
          type="error"
          action={
            <Button size="small" onClick={() => fetchTimeline()}>
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
                  <CalendarOutlined style={{ marginRight: 8 }} />
                  Migration Timeline
                </Title>
              </Col>
              <Col>
                <Space>
                  <DatePicker
                    placeholder="Select start date"
                    value={customStartDate}
                    onChange={handleDateChange}
                    style={{ marginRight: 8 }}
                  />
                  <Button 
                    type="primary" 
                    icon={<ReloadOutlined />} 
                    onClick={() => fetchTimeline()}
                    loading={loading}
                  >
                    Refresh
                  </Button>
                </Space>
              </Col>
            </Row>
          </Card>
        </Col>
      </Row>

      {loading ? (
        <Card>
          <div style={{ textAlign: 'center', padding: '50px 0' }}>
            <Spin size="large" />
            <Paragraph style={{ marginTop: 16 }}>Generating migration timeline...</Paragraph>
          </div>
        </Card>
      ) : data ? (
        <>
          {/* Project Overview */}
          <Card title="Project Overview" style={{ marginBottom: 24 }}>
            <Row gutter={[24, 16]}>
              <Col xs={24} sm={12} lg={6}>
                <Statistic
                  title="Total Duration"
                  value={data.project_overview.total_duration_weeks}
                  suffix="weeks"
                  prefix={<CalendarOutlined />}
                />
                <Text type="secondary">
                  ({data.project_overview.total_duration_months} months)
                </Text>
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <Statistic
                  title="Start Date"
                  value={dayjs(data.project_overview.estimated_start_date).format('MMM DD, YYYY')}
                />
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <Statistic
                  title="End Date"
                  value={dayjs(data.project_overview.estimated_end_date).format('MMM DD, YYYY')}
                />
              </Col>
              <Col xs={24} sm={12} lg={6}>
                <div style={{ textAlign: 'center' }}>
                  <RobotOutlined style={{ fontSize: '32px', color: '#1890ff' }} />
                  <div style={{ marginTop: 8 }}>
                    <Text strong>Confidence</Text>
                    <div style={{ fontSize: '18px', color: '#52c41a' }}>
                      {data.project_overview.confidence_level}
                    </div>
                  </div>
                </div>
              </Col>
            </Row>
          </Card>

          {/* Timeline Phases */}
          <Card title="Migration Phases" style={{ marginBottom: 24 }}>
            <Timeline>
              {data.phases.map((phase, index) => (
                <Timeline.Item
                  key={phase.phase}
                  dot={<CheckCircleOutlined style={{ fontSize: '16px' }} />}
                  color={getStatusColor(phase.status)}
                >
                  <div style={{ marginBottom: 16 }}>
                    <Space align="baseline" wrap>
                      <Title level={4} style={{ margin: 0 }}>
                        {phase.title}
                      </Title>
                      <Tag color="blue">{phase.duration_weeks} weeks</Tag>
                      <Tag color={getStatusColor(phase.status)}>
                        {phase.status}
                      </Tag>
                      <Text type="secondary">
                        Week {phase.start_week} - {phase.end_week}
                      </Text>
                    </Space>
                    
                    <Paragraph style={{ marginTop: 8, marginBottom: 12 }}>
                      {phase.description}
                    </Paragraph>

                    <Row gutter={[16, 8]}>
                      <Col xs={24} lg={12}>
                        <Text strong>Key Activities:</Text>
                        <List
                          size="small"
                          dataSource={phase.components}
                          renderItem={(component, idx) => (
                            <List.Item key={idx} style={{ padding: '4px 0' }}>
                              <Badge status="processing" />
                              {component}
                            </List.Item>
                          )}
                        />
                      </Col>
                      <Col xs={24} lg={12}>
                        <Text strong>Milestones:</Text>
                        <List
                          size="small"
                          dataSource={phase.milestones}
                          renderItem={(milestone, idx) => (
                            <List.Item key={idx} style={{ padding: '4px 0' }}>
                              <Badge status="success" />
                              {milestone}
                            </List.Item>
                          )}
                        />
                      </Col>
                    </Row>

                    {phase.resources_required.length > 0 && (
                      <div style={{ marginTop: 12 }}>
                        <Text strong>Resources Required: </Text>
                        {phase.resources_required.map((resource, idx) => (
                          <Tag key={idx} icon={<TeamOutlined />} color="geekblue">
                            {resource}
                          </Tag>
                        ))}
                      </div>
                    )}

                    {phase.risks.length > 0 && (
                      <div style={{ marginTop: 8 }}>
                        <Text strong>Risks: </Text>
                        {phase.risks.map((risk, idx) => (
                          <Tag key={idx} icon={<ExclamationCircleOutlined />} color="orange">
                            {risk}
                          </Tag>
                        ))}
                      </div>
                    )}
                  </div>
                </Timeline.Item>
              ))}
            </Timeline>
          </Card>

          {/* AI Insights */}
          <Card 
            title={
              <Space>
                <RobotOutlined />
                AI Timeline Insights
              </Space>
            } 
            style={{ marginBottom: 24 }}
          >
            <Row gutter={[16, 16]}>
              <Col xs={24} lg={8}>
                <Text strong>Optimization Suggestions:</Text>
                <List
                  size="small"
                  dataSource={data.ai_insights.optimization_suggestions}
                  renderItem={(suggestion, idx) => (
                    <List.Item key={idx}>
                      <Badge status="success" />
                      {suggestion}
                    </List.Item>
                  )}
                />
              </Col>
              <Col xs={24} lg={8}>
                <Text strong>Timeline Risks:</Text>
                <List
                  size="small"
                  dataSource={data.ai_insights.timeline_risks}
                  renderItem={(risk, idx) => (
                    <List.Item key={idx}>
                      <Badge status="warning" />
                      {risk}
                    </List.Item>
                  )}
                />
              </Col>
              <Col xs={24} lg={8}>
                <Text strong>Resource Recommendations:</Text>
                <List
                  size="small"
                  dataSource={data.ai_insights.resource_recommendations}
                  renderItem={(rec, idx) => (
                    <List.Item key={idx}>
                      <Badge status="processing" />
                      {rec}
                    </List.Item>
                  )}
                />
              </Col>
            </Row>
          </Card>

          {/* Success Criteria */}
          <Card title="Success Criteria" style={{ marginBottom: 24 }}>
            <List
              dataSource={data.success_criteria}
              renderItem={(criteria, idx) => (
                <List.Item key={idx}>
                  <List.Item.Meta
                    avatar={<CheckCircleOutlined style={{ color: '#52c41a' }} />}
                    title={criteria}
                  />
                </List.Item>
              )}
            />
          </Card>
        </>
      ) : (
        <Card>
          <div style={{ textAlign: 'center', padding: '50px 0' }}>
            <Paragraph>No timeline data available. Click refresh to load data.</Paragraph>
          </div>
        </Card>
      )}
    </div>
  );
};

export default TimelineSimple;
