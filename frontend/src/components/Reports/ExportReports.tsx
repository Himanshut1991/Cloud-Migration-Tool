import React from 'react';
import { Card, Typography } from 'antd';

const { Title, Paragraph } = Typography;

const ExportReports: React.FC = () => {
  return (
    <Card>
      <Title level={2}>Export Reports</Title>
      <Paragraph>
        Report export functionality will be implemented here.
        This will include Excel, PDF, and Word export options for migration plans.
      </Paragraph>
    </Card>
  );
};

export default ExportReports;
