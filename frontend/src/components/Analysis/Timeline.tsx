import React, { useState, useEffect } from 'react';
import dayjs, { Dayjs } from 'dayjs';
import {
  Card,
  Typography,
  Row,
  Col,
  Timeline as AntTimeline,
  Button,
  Spin,
  Alert,
  Tabs,
  Progress,
  Tag,
  Statistic,
  Descriptions,
  Table,
  Space,
  Divider,
  DatePicker,
  message
} from 'antd';
import {
  ClockCircleOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  ReloadOutlined,
  CalendarOutlined,
  ProjectOutlined,
  TeamOutlined,
  WarningOutlined,
  RocketOutlined
} from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;

interface TimelinePhase {
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
  status: 'pending' | 'in-progress' | 'completed' | 'delayed';
}

interface TimelineData {
  project_overview: {
    total_duration_weeks: number;
    total_duration_months: number;
    estimated_start_date: string;
    estimated_end_date: string;
    confidence_level: string;
    complexity_score: number;
  };
  phases: TimelinePhase[];
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
  ai_insights?: {
    optimization_suggestions: string[];
    timeline_risks: string[];
    resource_recommendations: string[];
  };
}

const Timeline: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isRealData, setIsRealData] = useState(false);
  const [customStartDate, setCustomStartDate] = useState<Dayjs | null>(null);
  const [calculatedEndDate, setCalculatedEndDate] = useState<string | null>(null);

  // Mock data for development/fallback
  const mockTimelineData: TimelineData = {
    project_overview: {
      total_duration_weeks: 16,
      total_duration_months: 4,
      estimated_start_date: "2024-01-01",
      estimated_end_date: "2024-04-15",
      confidence_level: "85%",
      complexity_score: 7.5
    },
    phases: [
      {
        phase: 1,
        title: "Assessment & Planning",
        description: "Initial assessment and detailed migration planning",
        duration_weeks: 4,
        start_week: 1,
        end_week: 4,
        dependencies: [],
        milestones: ["Infrastructure Assessment Complete", "Migration Plan Approved"],
        components: ["Server Assessment", "Database Analysis", "Network Planning"],
        risks: ["Incomplete inventory", "Resource availability"],
        resources_required: ["Cloud Architect", "Database Expert", "Network Engineer"],
        status: "pending"
      },
      {
        phase: 2,
        title: "Environment Setup",
        description: "Set up cloud infrastructure and prepare migration tools",
        duration_weeks: 3,
        start_week: 5,
        end_week: 7,
        dependencies: ["Phase 1"],
        milestones: ["Cloud Environment Ready", "Migration Tools Configured"],
        components: ["VPC Setup", "Security Groups", "Database Setup"],
        risks: ["Cloud service limitations", "Security compliance"],
        resources_required: ["DevOps Engineer", "Security Specialist"],
        status: "pending"
      },
      {
        phase: 3,
        title: "Data Migration",
        description: "Migrate databases and file shares to cloud",
        duration_weeks: 6,
        start_week: 8,
        end_week: 13,
        dependencies: ["Phase 2"],
        milestones: ["Database Migration Complete", "File Share Migration Complete"],
        components: ["Database Replication", "File Transfer", "Data Validation"],
        risks: ["Data corruption", "Extended downtime"],
        resources_required: ["Database Administrator", "Storage Specialist"],
        status: "pending"
      },
      {
        phase: 4,
        title: "Server Migration & Cutover",
        description: "Migrate applications and perform final cutover",
        duration_weeks: 3,
        start_week: 14,
        end_week: 16,
        dependencies: ["Phase 3"],
        milestones: ["Application Migration Complete", "Production Cutover"],
        components: ["Application Deployment", "DNS Cutover", "Monitoring Setup"],
        risks: ["Application compatibility", "User acceptance"],
        resources_required: ["Application Developer", "System Administrator"],
        status: "pending"
      }
    ],
    critical_path: ["Phase 1", "Phase 2", "Phase 3", "Phase 4"],
    resource_allocation: [
      {
        role: "Cloud Architect",
        weeks_allocated: 4,
        overlap_phases: [1],
        peak_utilization_week: 2
      },
      {
        role: "Database Expert",
        weeks_allocated: 8,
        overlap_phases: [1, 3],
        peak_utilization_week: 10
      },
      {
        role: "DevOps Engineer",
        weeks_allocated: 6,
        overlap_phases: [2, 4],
        peak_utilization_week: 6
      }
    ],
    risk_mitigation: [
      {
        risk: "Data corruption during migration",
        probability: "Medium",
        impact: "High",
        mitigation_strategy: "Implement comprehensive backup strategy",
        timeline_buffer_weeks: 2
      },
      {
        risk: "Extended downtime during cutover",
        probability: "High",
        impact: "High",
        mitigation_strategy: "Plan for rollback procedures and conduct thorough testing",
        timeline_buffer_weeks: 1
      }
    ],
    success_criteria: [
      "All servers migrated successfully",
      "Zero data loss during migration",
      "Application performance maintained",
      "Downtime within acceptable limits"
    ],
    ai_insights: {
      optimization_suggestions: [
        "Consider parallel database migrations to reduce timeline",
        "Implement blue-green deployment for zero-downtime cutover"
      ],
      timeline_risks: [
        "Database migration may take longer than estimated",
        "User acceptance testing might reveal compatibility issues"
      ],
      resource_recommendations: [
        "Add additional database specialist for large databases",
        "Consider 24/7 support during cutover weekend"
      ]
    }
  };

  // Initialize with mock data
  const [data, setData] = useState<TimelineData>(mockTimelineData);

  // Function to calculate end date based on start date and duration
  const calculateEndDate = (startDate: Dayjs, durationWeeks: number): string => {
    return startDate.add(durationWeeks, 'week').format('YYYY-MM-DD');
  };

  // Function to update timeline data with custom start date
  const updateTimelineWithCustomDate = (baseData: TimelineData, newStartDate: Dayjs): TimelineData => {
    const newEndDate = calculateEndDate(newStartDate, baseData.project_overview.total_duration_weeks);
    
    return {
      ...baseData,
      project_overview: {
        ...baseData.project_overview,
        estimated_start_date: newStartDate.format('YYYY-MM-DD'),
        estimated_end_date: newEndDate
      }
    };
  };

  // Handle start date change
  const handleStartDateChange = (date: Dayjs | null) => {
    setCustomStartDate(date);
    
    if (date) {
      const newEndDate = calculateEndDate(date, data.project_overview.total_duration_weeks);
      setCalculatedEndDate(newEndDate);
      
      // Update the timeline data with new dates
      const updatedData = updateTimelineWithCustomDate(data, date);
      setData(updatedData);
      
      message.success(`Timeline updated: Start date set to ${date.format('YYYY-MM-DD')}, End date: ${newEndDate}`);
    } else {
      setCalculatedEndDate(null);
    }
  };

  const fetchTimeline = async () => {
    setLoading(true);
    setError(null);
    try {
      // Add timeout to prevent hanging
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout
      
      // Include custom start date if provided
      const requestBody = customStartDate ? {
        start_date: customStartDate.format('YYYY-MM-DD')
      } : {};
      
      const response = await fetch('http://localhost:5000/api/timeline', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        throw new Error('Failed to fetch timeline data');
      }
      let timelineData = await response.json();
      
      // If we have a custom start date, update the received data
      if (customStartDate) {
        timelineData = updateTimelineWithCustomDate(timelineData, customStartDate);
      }
      
      setData(timelineData);
      setError(null); // Clear error if API succeeds
      setIsRealData(true); // Mark as real data
    } catch (err) {
      console.warn('API not available, using mock data:', err);
      setError('Backend not available - showing sample data');
      let fallbackData = mockTimelineData;
      
      // Apply custom start date to mock data if provided
      if (customStartDate) {
        fallbackData = updateTimelineWithCustomDate(mockTimelineData, customStartDate);
      }
      
      setData(fallbackData); // Always fall back to mock data
      setIsRealData(false); // Mark as mock data
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    console.log('Timeline component mounted - showing mock data by default');
    // Don't auto-fetch to prevent blank page, let user click refresh for real data
  }, []);

  // Debug logging
  console.log('Timeline render - loading:', loading, 'error:', error, 'data available:', !!data);

  const getPhaseColor = (status: string) => {
    switch (status) {
      case 'completed': return 'green';
      case 'in-progress': return 'blue';
      case 'delayed': return 'red';
      default: return 'gray';
    }
  };

  const getPhaseIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircleOutlined />;
      case 'in-progress': return <ClockCircleOutlined />;
      case 'delayed': return <ExclamationCircleOutlined />;
      default: return <ClockCircleOutlined />;
    }
  };

  // Remove loading state that hides content - show data with loading button instead
  // if (loading) {
  //   return (
  //     <div style={{ textAlign: 'center', padding: '50px' }}>
  //       <Spin size="large" />
  //       <div style={{ marginTop: 16 }}>
  //         <Text>Generating migration timeline...</Text>
  //       </div>
  //     </div>
  //   );
  // }

  if (error && !data) {
    return (
      <Card>
        <Alert
          message="Error Loading Timeline"
          description={error}
          type="error"
          action={
            <Button size="small" danger onClick={fetchTimeline}>
              <ReloadOutlined /> Retry
            </Button>
          }
        />
      </Card>
    );
  }

  if (!data) {
    // This should never happen since we initialize with mock data
    return <div>No data available</div>;
  }

  const tabItems = [
    {
      key: 'overview',
      label: 'Project Overview',
      children: (
        <Row gutter={[24, 24]}>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Total Duration"
                value={data.project_overview.total_duration_months}
                suffix="months"
                prefix={<CalendarOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Total Weeks"
                value={data.project_overview.total_duration_weeks}
                suffix="weeks"
                prefix={<ClockCircleOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Confidence Level"
                value={data.project_overview.confidence_level}
                prefix={<CheckCircleOutlined />}
              />
            </Card>
          </Col>
          <Col xs={24} sm={12} md={6}>
            <Card>
              <Statistic
                title="Complexity Score"
                value={data.project_overview.complexity_score}
                precision={1}
                suffix="/10"
                prefix={<WarningOutlined />}
              />
            </Card>
          </Col>
          <Col span={24}>
            <Card title="Project Timeline">
              <Row gutter={[16, 16]}>
                <Col xs={24} sm={12}>
                  <div style={{ marginBottom: 16 }}>
                    <label style={{ display: 'block', marginBottom: 8, fontWeight: 'bold' }}>
                      Project Start Date:
                    </label>
                    <DatePicker
                      value={customStartDate}
                      onChange={handleStartDateChange}
                      placeholder="Select start date"
                      style={{ width: '100%' }}
                      format="YYYY-MM-DD"
                    />
                    {!customStartDate && (
                      <div style={{ marginTop: 4, fontSize: '12px', color: '#666' }}>
                        Using default date: {data.project_overview.estimated_start_date}
                      </div>
                    )}
                  </div>
                </Col>
                <Col xs={24} sm={12}>
                  <Descriptions bordered size="small">
                    <Descriptions.Item label="Start Date" span={3}>
                      <Text strong>
                        {customStartDate ? customStartDate.format('YYYY-MM-DD') : data.project_overview.estimated_start_date}
                      </Text>
                    </Descriptions.Item>
                    <Descriptions.Item label="End Date" span={3}>
                      <Text strong style={{ color: '#52c41a' }}>
                        {calculatedEndDate || data.project_overview.estimated_end_date}
                      </Text>
                    </Descriptions.Item>
                    <Descriptions.Item label="Total Phases" span={3}>
                      {data.phases.length}
                    </Descriptions.Item>
                  </Descriptions>
                </Col>
              </Row>
            </Card>
          </Col>
        </Row>
      )
    },
    {
      key: 'phases',
      label: 'Migration Phases',
      children: (
        <Row gutter={[24, 24]}>
          <Col span={24}>
            <Card title="Phase Timeline">
              <AntTimeline>
                {data.phases.map((phase) => (
                  <AntTimeline.Item
                    key={phase.phase}
                    color={getPhaseColor(phase.status)}
                    dot={getPhaseIcon(phase.status)}
                  >
                    <div>
                      <Title level={4} style={{ margin: 0 }}>
                        Phase {phase.phase}: {phase.title}
                      </Title>
                      <Paragraph type="secondary" style={{ margin: '8px 0' }}>
                        {phase.description}
                      </Paragraph>
                      <Space wrap>
                        <Tag>Week {phase.start_week} - {phase.end_week}</Tag>
                        <Tag>{phase.duration_weeks} weeks</Tag>
                        <Tag color={getPhaseColor(phase.status)}>{phase.status}</Tag>
                      </Space>
                      <div style={{ marginTop: '12px' }}>
                        <Text strong>Components: </Text>
                        <Space wrap>
                          {phase.components.map((comp, idx) => (
                            <Tag key={idx}>{comp}</Tag>
                          ))}
                        </Space>
                      </div>
                      <div style={{ marginTop: '8px' }}>
                        <Text strong>Milestones: </Text>
                        <ul style={{ marginLeft: '20px' }}>
                          {phase.milestones.map((milestone, idx) => (
                            <li key={idx}>{milestone}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </AntTimeline.Item>
                ))}
              </AntTimeline>
            </Card>
          </Col>
        </Row>
      )
    },
    {
      key: 'resources',
      label: 'Resource Allocation',
      children: (
        <Card title="Resource Planning">
          <Table
            dataSource={data.resource_allocation}
            rowKey="role"
            columns={[
              {
                title: 'Role',
                dataIndex: 'role',
                key: 'role',
                render: (role: string) => <Text strong>{role}</Text>
              },
              {
                title: 'Weeks Allocated',
                dataIndex: 'weeks_allocated',
                key: 'weeks_allocated',
                render: (weeks: number) => `${weeks} weeks`
              },
              {
                title: 'Phases Involved',
                dataIndex: 'overlap_phases',
                key: 'overlap_phases',
                render: (phases: number[]) => (
                  <Space wrap>
                    {phases.map(phase => (
                      <Tag key={phase}>Phase {phase}</Tag>
                    ))}
                  </Space>
                )
              },
              {
                title: 'Peak Week',
                dataIndex: 'peak_utilization_week',
                key: 'peak_utilization_week',
                render: (week: number) => `Week ${week}`
              }
            ]}
          />
        </Card>
      )
    },
    {
      key: 'risks',
      label: 'Risk Management',
      children: (
        <Card title="Risk Analysis & Mitigation">
          <Table
            dataSource={data.risk_mitigation}
            rowKey="risk"
            columns={[
              {
                title: 'Risk',
                dataIndex: 'risk',
                key: 'risk',
                render: (risk: string) => <Text strong>{risk}</Text>
              },
              {
                title: 'Probability',
                dataIndex: 'probability',
                key: 'probability',
                render: (prob: string) => (
                  <Tag color={prob === 'High' ? 'red' : prob === 'Medium' ? 'orange' : 'green'}>
                    {prob}
                  </Tag>
                )
              },
              {
                title: 'Impact',
                dataIndex: 'impact',
                key: 'impact',
                render: (impact: string) => (
                  <Tag color={impact === 'High' ? 'red' : impact === 'Medium' ? 'orange' : 'green'}>
                    {impact}
                  </Tag>
                )
              },
              {
                title: 'Mitigation Strategy',
                dataIndex: 'mitigation_strategy',
                key: 'mitigation_strategy'
              },
              {
                title: 'Buffer Weeks',
                dataIndex: 'timeline_buffer_weeks',
                key: 'timeline_buffer_weeks',
                render: (weeks: number) => `${weeks} weeks`
              }
            ]}
          />
        </Card>
      )
    }
  ];

  if (data.ai_insights) {
    tabItems.push({
      key: 'insights',
      label: 'AI Insights',
      children: (
        <Row gutter={[24, 24]}>
          <Col xs={24} md={8}>
            <Card title="Optimization Suggestions" size="small">
              <ul>
                {data.ai_insights.optimization_suggestions.map((suggestion, idx) => (
                  <li key={idx}>{suggestion}</li>
                ))}
              </ul>
            </Card>
          </Col>
          <Col xs={24} md={8}>
            <Card title="Timeline Risks" size="small">
              <ul>
                {data.ai_insights.timeline_risks.map((risk, idx) => (
                  <li key={idx}>{risk}</li>
                ))}
              </ul>
            </Card>
          </Col>
          <Col xs={24} md={8}>
            <Card title="Resource Recommendations" size="small">
              <ul>
                {data.ai_insights.resource_recommendations.map((rec, idx) => (
                  <li key={idx}>{rec}</li>
                ))}
              </ul>
            </Card>
          </Col>
        </Row>
      )
    });
  }

  if (data.success_criteria && data.success_criteria.length > 0) {
    tabItems.push({
      key: 'success',
      label: 'Success Criteria',
      children: (
        <Card title="Project Success Criteria">
          <ul>
            {data.success_criteria.map((criteria, idx) => (
              <li key={idx}>{criteria}</li>
            ))}
          </ul>
        </Card>
      )
    });
  }

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <Title level={2}>
              <ProjectOutlined /> Migration Timeline
            </Title>
            <Paragraph>
              Timeline generated from your inventory and configuration settings.
            </Paragraph>
          </div>
          <Space>
            <div>
              <label style={{ marginRight: 8 }}>Project Start Date:</label>
              <DatePicker
                value={customStartDate}
                onChange={(date) => {
                  setCustomStartDate(date);
                  if (date) {
                    // Calculate new end date and update timeline
                    const newEndDate = date.add(16, 'weeks').format('YYYY-MM-DD');
                    setCalculatedEndDate(newEndDate);
                    
                    // Trigger refetch with new start date
                    fetchTimeline();
                    
                    message.success(`Timeline updated: Start date set to ${date.format('YYYY-MM-DD')}, End date: ${newEndDate}`);
                  }
                }}
                placeholder="Select start date"
              />
            </div>
            <Button 
              type="primary" 
              icon={<ReloadOutlined />} 
              onClick={fetchTimeline}
              loading={loading}
            >
              Regenerate Timeline
            </Button>
          </Space>
        </div>
        {!isRealData && (
          <Alert
            message="Sample Timeline Data"
            description="This timeline is generated from sample data. Click 'Regenerate Timeline' to create a timeline based on your actual inventory and configuration."
            type="info"
            showIcon
            style={{ marginBottom: 16 }}
          />
        )}
        {isRealData && (
          <Alert
            message="Dynamic Timeline Generated"
            description="This timeline is generated from your actual inventory, configuration, and business constraints."
            type="success"
            showIcon
            style={{ marginBottom: 16 }}
          />
        )}
        {error && (
          <Alert
            message="Using Sample Data"
            description={error}
            type="warning"
            showIcon
            closable
            style={{ marginBottom: 16 }}
          />
        )}
      </div>

      <div style={{ position: 'relative' }}>
        {loading && (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(255, 255, 255, 0.8)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            minHeight: '300px'
          }}>
            <div style={{ textAlign: 'center' }}>
              <Spin size="large" />
              <div style={{ marginTop: 16 }}>
                <Text>Regenerating timeline from your inventory...</Text>
              </div>
            </div>
          </div>
        )}
        <Tabs defaultActiveKey="overview" items={tabItems} />
      </div>
    </div>
  );
};

export default Timeline;
