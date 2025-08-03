import React from 'react';
import { Card, Typography } from 'antd';

const { Title, Paragraph } = Typography;

const MigrationStrategy: React.FC = () => {
  return (
    <Card>
      <Title level={2}>Migration Strategy</Title>
      <Paragraph>
        AI-powered migration strategy recommendations will be implemented here.
        This will include server migration strategies, data migration approaches, and tool recommendations.
      </Paragraph>
    </Card>
  );
};

export default MigrationStrategy;
