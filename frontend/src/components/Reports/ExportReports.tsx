import React, { useState } from 'react';
import {
  Card,
  Typography,
  Button,
  Space,
  Row,
  Col,
  Alert,
  Spin,
  message,
  Descriptions,
  Tag,
  Divider,
  Steps,
  Progress,
  List,
  Modal
} from 'antd';
import {
  FileExcelOutlined,
  FilePdfOutlined,
  FileWordOutlined,
  DownloadOutlined,
  CheckCircleOutlined,
  InfoCircleOutlined,
  ClockCircleOutlined,
  FileTextOutlined,
  CloudDownloadOutlined
} from '@ant-design/icons';

const { Title, Paragraph, Text } = Typography;
const { Step } = Steps;

interface ExportResult {
  message: string;
  format: string;
  filename: string;
  filepath: string;
  file_size: number;
  timestamp: string;
}

const ExportReports: React.FC = () => {
  const [loading, setLoading] = useState<string | null>(null);
  const [exports, setExports] = useState<ExportResult[]>([]);
  const [previewVisible, setPreviewVisible] = useState(false);
  const [selectedExport, setSelectedExport] = useState<ExportResult | null>(null);
  const [selectedTypes, setSelectedTypes] = useState<string[]>(['cost_estimation', 'migration_strategy', 'timeline']);

  const exportFormats = [
    {
      key: 'excel',
      title: 'Excel Workbook',
      description: 'Comprehensive report with multiple sheets including inventory, cost analysis, and timeline',
      icon: <FileExcelOutlined style={{ fontSize: '48px', color: '#52c41a' }} />,
      features: ['Multiple worksheets', 'Inventory details', 'Cost breakdown', 'Timeline phases', 'Resource planning'],
      color: '#52c41a'
    },
    {
      key: 'pdf',
      title: 'PDF Report',
      description: 'Executive-friendly PDF document with charts and summary tables',
      icon: <FilePdfOutlined style={{ fontSize: '48px', color: '#f5222d' }} />,
      features: ['Executive summary', 'Cost analysis', 'Timeline overview', 'Professional formatting', 'Print-ready'],
      color: '#f5222d'
    },
    {
      key: 'word',
      title: 'Word Document',
      description: 'Editable document for customization and collaboration',
      icon: <FileWordOutlined style={{ fontSize: '48px', color: '#1890ff' }} />,
      features: ['Editable format', 'Inventory tables', 'Cost summary', 'Timeline details', 'Easy collaboration'],
      color: '#1890ff'
    }
  ];

  const reportTypes = [
    {
      key: 'cost_estimation',
      title: 'Cost Estimation',
      description: 'Detailed cost analysis and optimization recommendations'
    },
    {
      key: 'migration_strategy',
      title: 'Migration Strategy',
      description: 'Migration approach, phases, and component strategies'
    },
    {
      key: 'timeline',
      title: 'Timeline & Phases',
      description: 'Project timeline with milestones and dependencies'
    }
  ];

  const handleExport = async (format: string) => {
    setLoading(format);
    try {
      const response = await fetch('http://localhost:5000/api/export', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          format,
          types: selectedTypes 
        }),
      });

      if (!response.ok) {
        throw new Error('Export failed');
      }

      const result: ExportResult = await response.json();
      setExports(prev => [result, ...prev]);
      
      message.success({
        content: `${format.toUpperCase()} export completed successfully!`,
        duration: 5,
        icon: <CheckCircleOutlined style={{ color: '#52c41a' }} />
      });

    } catch (error) {
      console.error('Export error:', error);
      message.error({
        content: `Failed to export ${format.toUpperCase()} report. Please try again.`,
        duration: 5,
      });
    } finally {
      setLoading(null);
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  const handleDownload = async (exportResult: ExportResult) => {
    try {
      const response = await fetch(`http://localhost:5000/api/download/${exportResult.filename}`);
      
      if (!response.ok) {
        throw new Error('Download failed');
      }

      // Create blob and download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = exportResult.filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      message.success(`Downloaded ${exportResult.filename} successfully!`);
    } catch (error) {
      console.error('Download error:', error);
      message.error('Failed to download file. Please try again.');
    }
  };

  const showPreview = (exportResult: ExportResult) => {
    setSelectedExport(exportResult);
    setPreviewVisible(true);
  };

  const getReportSections = () => {
    return [
      {
        title: 'Executive Summary',
        description: 'High-level overview of migration scope and objectives',
        icon: <InfoCircleOutlined />
      },
      {
        title: 'Inventory Analysis',
        description: 'Detailed listing of servers, databases, and file shares',
        icon: <FileTextOutlined />
      },
      {
        title: 'Cost Estimation',
        description: 'Comprehensive cost breakdown and financial analysis',
        icon: <ClockCircleOutlined />
      },
      {
        title: 'Migration Timeline',
        description: 'Phase-by-phase timeline with milestones and dependencies',
        icon: <CheckCircleOutlined />
      },
      {
        title: 'Risk Assessment',
        description: 'Identified risks and recommended mitigation strategies',
        icon: <InfoCircleOutlined />
      }
    ];
  };

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>Export Migration Reports</Title>
      <Paragraph>
        Generate comprehensive migration reports in multiple formats for stakeholders, 
        executives, and technical teams. Each report includes detailed analysis, cost estimates, 
        and implementation timelines based on your current inventory and configuration.
      </Paragraph>

      {/* Report Content Overview */}
      <Card title="Report Contents" style={{ marginBottom: '24px' }}>
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Title level={4}>What's Included</Title>
            <List
              dataSource={getReportSections()}
              renderItem={item => (
                <List.Item>
                  <List.Item.Meta
                    avatar={item.icon}
                    title={item.title}
                    description={item.description}
                  />
                </List.Item>
              )}
            />
          </Col>
          <Col span={12}>
            <Title level={4}>Export Process</Title>
            <Steps direction="vertical" size="small">
              <Step 
                title="Select Format" 
                description="Choose from Excel, PDF, or Word formats"
                status="process"
              />
              <Step 
                title="Generate Report" 
                description="System compiles data and creates document"
              />
              <Step 
                title="Download" 
                description="Access your completed migration report"
              />
            </Steps>
          </Col>
        </Row>
      </Card>

      {/* Report Type Selection */}
      <Card title="Select Report Contents" style={{ marginBottom: '24px' }}>
        <Paragraph>
          Choose which analysis types to include in your report. You can select multiple types 
          to create a comprehensive migration document.
        </Paragraph>
        <Row gutter={[16, 16]}>
          {reportTypes.map((type) => (
            <Col xs={24} md={8} key={type.key}>
              <Card 
                size="small" 
                style={{ 
                  border: selectedTypes.includes(type.key) ? '2px solid #1890ff' : '1px solid #d9d9d9',
                  backgroundColor: selectedTypes.includes(type.key) ? '#f6ffed' : 'white'
                }}
              >
                <div 
                  style={{ cursor: 'pointer' }}
                  onClick={() => {
                    if (selectedTypes.includes(type.key)) {
                      setSelectedTypes(prev => prev.filter(t => t !== type.key));
                    } else {
                      setSelectedTypes(prev => [...prev, type.key]);
                    }
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
                    <input 
                      type="checkbox" 
                      checked={selectedTypes.includes(type.key)}
                      onChange={() => {}} 
                      style={{ marginRight: 8 }}
                    />
                    <Text strong>{type.title}</Text>
                  </div>
                  <Text type="secondary" style={{ fontSize: '12px' }}>
                    {type.description}
                  </Text>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
        <div style={{ marginTop: 16 }}>
          <Tag color="blue">{selectedTypes.length} of {reportTypes.length} types selected</Tag>
          <Button 
            type="link" 
            size="small"
            onClick={() => setSelectedTypes(reportTypes.map(t => t.key))}
            style={{ marginLeft: 8 }}
          >
            Select All
          </Button>
          <Button 
            type="link" 
            size="small"
            onClick={() => setSelectedTypes([])}
          >
            Clear All
          </Button>
        </div>
      </Card>

      {/* Export Format Cards */}
      <Title level={3}>Choose Export Format</Title>
      <Row gutter={[24, 24]} style={{ marginBottom: '32px' }}>
        {exportFormats.map((format) => (
          <Col xs={24} md={8} key={format.key}>
            <Card
              hoverable
              style={{ height: '100%' }}
              actions={[
                <Button
                  type="primary"
                  icon={<DownloadOutlined />}
                  loading={loading === format.key}
                  disabled={selectedTypes.length === 0}
                  onClick={() => handleExport(format.key)}
                  style={{ backgroundColor: format.color, borderColor: format.color }}
                >
                  {loading === format.key ? 'Generating...' : `Export ${format.title}`}
                </Button>
              ]}
            >
              <div style={{ textAlign: 'center', marginBottom: '16px' }}>
                {format.icon}
              </div>
              <Card.Meta
                title={format.title}
                description={format.description}
              />
              <Divider />
              <div>
                <Text strong>Features:</Text>
                <div style={{ marginTop: '8px' }}>
                  {format.features.map((feature, index) => (
                    <Tag key={index} style={{ marginBottom: '4px' }}>
                      {feature}
                    </Tag>
                  ))}
                </div>
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      {/* Export History */}
      {exports.length > 0 && (
        <Card title="Recent Exports" style={{ marginTop: '24px' }}>
          <List
            dataSource={exports}
            renderItem={(item) => {
              const formatConfig = exportFormats.find(f => f.key === item.format);
              return (
                <List.Item
                  actions={[
                    <Button
                      type="link"
                      icon={<InfoCircleOutlined />}
                      onClick={() => showPreview(item)}
                    >
                      Details
                    </Button>,
                    <Button
                      type="primary"
                      icon={<CloudDownloadOutlined />}
                      size="small"
                      onClick={() => handleDownload(item)}
                    >
                      Download
                    </Button>
                  ]}
                >
                  <List.Item.Meta
                    avatar={formatConfig?.icon}
                    title={
                      <Space>
                        {item.filename}
                        <Tag color={formatConfig?.color}>{item.format.toUpperCase()}</Tag>
                      </Space>
                    }
                    description={
                      <Space split={<Divider type="vertical" />}>
                        <Text type="secondary">
                          Generated: {formatTimestamp(item.timestamp)}
                        </Text>
                        <Text type="secondary">
                          Size: {formatFileSize(item.file_size)}
                        </Text>
                      </Space>
                    }
                  />
                </List.Item>
              );
            }}
          />
        </Card>
      )}

      {/* Loading State */}
      {loading && (
        <Card style={{ marginTop: '24px' }}>
          <div style={{ textAlign: 'center', padding: '40px' }}>
            <Spin size="large" />
            <div style={{ marginTop: '16px' }}>
              <Title level={4}>Generating Your Report</Title>
              <Paragraph>
                Please wait while we compile your migration data and generate the {loading.toUpperCase()} report...
              </Paragraph>
              <Progress percent={Math.random() * 100} status="active" />
            </div>
          </div>
        </Card>
      )}

      {/* Export Details Modal */}
      <Modal
        title="Export Details"
        open={previewVisible}
        onCancel={() => setPreviewVisible(false)}
        footer={[
          <Button key="close" onClick={() => setPreviewVisible(false)}>
            Close
          </Button>,
          <Button key="download" type="primary" icon={<DownloadOutlined />}>
            Download File
          </Button>
        ]}
      >
        {selectedExport && (
          <Descriptions bordered column={1}>
            <Descriptions.Item label="Format">
              <Tag color={exportFormats.find(f => f.key === selectedExport.format)?.color}>
                {selectedExport.format.toUpperCase()}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="Filename">
              {selectedExport.filename}
            </Descriptions.Item>
            <Descriptions.Item label="File Size">
              {formatFileSize(selectedExport.file_size)}
            </Descriptions.Item>
            <Descriptions.Item label="Generated">
              {formatTimestamp(selectedExport.timestamp)}
            </Descriptions.Item>
            <Descriptions.Item label="Status">
              <Tag color="success" icon={<CheckCircleOutlined />}>
                Ready for Download
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="File Path">
              <Text code>{selectedExport.filepath}</Text>
            </Descriptions.Item>
          </Descriptions>
        )}
      </Modal>

      {/* Help Information */}
      <Alert
        message="Export Information"
        description={
          <div>
            <p>Each export format serves different purposes:</p>
            <ul>
              <li><strong>Excel:</strong> Best for detailed analysis and data manipulation</li>
              <li><strong>PDF:</strong> Ideal for presentations and executive reviews</li>
              <li><strong>Word:</strong> Perfect for collaborative editing and customization</li>
            </ul>
            <p>All reports include the same core information but are formatted appropriately for their intended use.</p>
          </div>
        }
        type="info"
        showIcon
        style={{ marginTop: '24px' }}
      />
    </div>
  );
};

export default ExportReports;
