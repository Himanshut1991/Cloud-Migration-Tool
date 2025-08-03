import React from 'react';
import { Card, Typography } from 'antd';

const { Title, Paragraph } = Typography;

const CostEstimation: React.FC = () => {
  return (
    <Card>
      <Title level={2}>Cost Estimation</Title>
      <Paragraph>
        Cost estimation analysis will be implemented here.
        This will include cloud service costs, migration costs, and resource planning costs.
      </Paragraph>
    </Card>
  );
};

export default CostEstimation;
