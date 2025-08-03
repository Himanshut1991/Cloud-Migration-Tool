import React from 'react';
import { Card, Typography } from 'antd';

const { Title, Paragraph } = Typography;

const Timeline: React.FC = () => {
  return (
    <Card>
      <Title level={2}>Migration Timeline</Title>
      <Paragraph>
        Migration timeline visualization and planning will be implemented here.
        This will include phase-wise timelines, milestones, and dependencies.
      </Paragraph>
    </Card>
  );
};

export default Timeline;
