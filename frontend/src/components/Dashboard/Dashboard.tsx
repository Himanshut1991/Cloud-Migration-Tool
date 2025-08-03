import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Progress, Typography, Space, Button, Alert } from 'antd';
import {
  DesktopOutlined,
  DatabaseOutlined,
  FolderOpenOutlined,
  CloudOutlined,
  DollarCircleOutlined,
  ClockCircleOutlined,
  RocketOutlined,
  BarChartOutlined,
} from '@ant-design/icons';
import { Line, Column, Pie } from '@ant-design/plots';

const { Title, Paragraph } = Typography;

interface DashboardData {
  servers_count: number;
  databases_count: number;
  file_shares_count: number;
  total_data_size_gb: number;
  last_updated: string;
}

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/dashboard');
      const data = await response.json();
      setDashboardData(data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Sample data for charts
  const migrationProgressData = [
    { phase: 'Assessment', completed: 100, total: 100 },
    { phase: 'Planning', completed: 75, total: 100 },
    { phase: 'Data Migration', completed: 30, total: 100 },
    { phase: 'Server Migration', completed: 10, total: 100 },
    { phase: 'Testing', completed: 0, total: 100 },
  ];

  const costBreakdownData = [
    { category: 'Server Migration', value: 45000, color: '#1890ff' },
    { category: 'Database Migration', value: 32000, color: '#52c41a' },
    { category: 'Storage Migration', value: 18000, color: '#fa8c16' },
    { category: 'Professional Services', value: 75000, color: '#eb2f96' },
  ];

  const timelineData = [
    { month: 'Jan', planning: 20, execution: 0 },
    { month: 'Feb', planning: 40, execution: 10 },
    { month: 'Mar', planning: 20, execution: 30 },
    { month: 'Apr', planning: 10, execution: 50 },
    { month: 'May', planning: 5, execution: 40 },
    { month: 'Jun', planning: 0, execution: 20 },
  ];

  const pieConfig = {
    data: costBreakdownData,
    angleField: 'value',
    colorField: 'category',
    radius: 0.8,
    label: {
      type: 'spider',
      labelHeight: 28,
      content: '{name}\n{percentage}',
    },
    interactions: [{ type: 'element-selected' }, { type: 'element-active' }],
  };

  const columnConfig = {
    data: migrationProgressData,
    xField: 'phase',
    yField: 'completed',
    color: '#1890ff',
    columnWidthRatio: 0.8,
    meta: {
      phase: { alias: 'Migration Phase' },
      completed: { alias: 'Progress (%)' },
    },
  };

  const lineConfig = {
    data: timelineData.flatMap(item => [
      { month: item.month, value: item.planning, type: 'Planning' },
      { month: item.month, value: item.execution, type: 'Execution' },
    ]),
    xField: 'month',
    yField: 'value',
    seriesField: 'type',
    color: ['#1890ff', '#52c41a'],
  };

  return (
    <div>
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Title level={2}>Migration Dashboard</Title>
          <Paragraph>
            Overview of your cloud migration project status, inventory, and progress.
          </Paragraph>
        </Col>
      </Row>

      {/* Key Metrics */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Servers"
              value={dashboardData?.servers_count || 0}
              prefix={<DesktopOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Databases"
              value={dashboardData?.databases_count || 0}
              prefix={<DatabaseOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="File Shares"
              value={dashboardData?.file_shares_count || 0}
              prefix={<FolderOpenOutlined />}
              valueStyle={{ color: '#fa8c16' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Data (GB)"
              value={dashboardData?.total_data_size_gb || 0}
              prefix={<CloudOutlined />}
              valueStyle={{ color: '#eb2f96' }}
              precision={0}
            />
          </Card>
        </Col>
      </Row>

      {/* Migration Progress */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={16}>
          <Card 
            title="Migration Progress by Phase" 
            extra={<Button type="primary" icon={<BarChartOutlined />}>View Details</Button>}
          >
            <Column {...columnConfig} height={300} />
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="Overall Progress">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Progress
                type="circle"
                percent={28}
                format={() => '28% Complete'}
                size={120}
              />
              <div style={{ textAlign: 'center', marginTop: 16 }}>
                <Statistic
                  title="Estimated Completion"
                  value="12 weeks"
                  prefix={<ClockCircleOutlined />}
                />
              </div>
            </Space>
          </Card>
        </Col>
      </Row>

      {/* Cost Analysis and Timeline */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} lg={12}>
          <Card 
            title="Cost Breakdown" 
            extra={<Button type="link" icon={<DollarCircleOutlined />}>View Details</Button>}
          >
            <Pie {...pieConfig} height={250} />
            <div style={{ textAlign: 'center', marginTop: 16 }}>
              <Statistic
                title="Total Estimated Cost"
                value={170000}
                prefix="$"
                precision={0}
                valueStyle={{ color: '#1890ff' }}
              />
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card 
            title="Migration Timeline" 
            extra={<Button type="link" icon={<RocketOutlined />}>View Timeline</Button>}
          >
            <Line {...lineConfig} height={250} />
          </Card>
        </Col>
      </Row>

      {/* Recent Activity and Recommendations */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card title="Recent Activity">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Alert
                message="Server Inventory Updated"
                description="Added 5 new servers to migration scope"
                type="info"
                showIcon
              />
              <Alert
                message="Cost Analysis Complete"
                description="Migration cost estimation has been updated"
                type="success"
                showIcon
              />
              <Alert
                message="Timeline Adjustment Needed"
                description="Database migration may require additional time"
                type="warning"
                showIcon
              />
            </Space>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="AI Recommendations">
            <Space direction="vertical" style={{ width: '100%' }}>
              <Alert
                message="Optimize Database Migration"
                description="Consider using AWS DMS for 3 large databases to reduce downtime"
                type="info"
                showIcon
              />
              <Alert
                message="Cost Optimization"
                description="Right-sizing servers could save 15% on cloud costs"
                type="success"
                showIcon
              />
              <Alert
                message="Risk Mitigation"
                description="Plan additional buffer time for critical systems migration"
                type="warning"
                showIcon
              />
            </Space>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
