# Gen-AI Powered Cloud Migration Planning Tool

## Overview

This comprehensive cloud migration planning tool assists organizations in planning and executing cloud migrations with AI-powered recommendations. The tool addresses key challenges in pre-sales planning, data migration strategy, and server migration planning.

## Features

### 🎯 Pre-Sales Planning
- **Cloud Service Cost Estimation**: Automatic calculation of cloud infrastructure costs using source environment specs and target cloud provider SKUs
- **Migration Service Cost Estimation**: Professional service revenue computation based on project scope and complexity
- **Resource Planning**: Generate staffing plans with required skill sets, roles, estimated man-hours, and availability mapping
- **Migration Timeline**: Build milestone-based schedules with dependencies and estimated duration per task

### 🤖 AI-Powered Migration Strategy
- **Data Migration Advisor**: GenAI-powered solution for database and file share migration strategies
- **Server Migration Advisor**: Automated technology component analysis with cloud service recommendations
- **Migration Strategy Recommendations**: Determines whether to Rehost or Replatform each component

### 📊 Comprehensive Analysis
- **Cost Estimation**: Detailed breakdown of cloud infrastructure and migration service costs
- **Timeline Visualization**: Interactive timeline with milestones, dependencies, and critical path analysis
- **Risk Assessment**: Automated risk identification and mitigation strategies
- **Technology Mapping**: Maps on-premise technologies to optimal cloud-native services

### 📋 Export & Reporting
- **Multiple Formats**: Export migration plans to Excel, PDF, and Word formats
- **Executive Reports**: Executive-friendly dashboards and summaries
- **Detailed Documentation**: Complete migration runbooks with rollback plans

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | ReactJS with TypeScript |
| UI Library | Ant Design |
| Backend | Python Flask |
| Database | SQLite |
| AI Integration | AWS Bedrock |
| Data Processing | Pandas |
| Charts | Ant Design Plots |

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Services   │
│   (React)       │◄──►│   (Flask)       │◄──►│  (AWS Bedrock)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite)      │
                       └─────────────────┘
```

## Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- Git

### Backend Setup
```bash
cd backend
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your AWS credentials and other settings
# Start the Flask server
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Configuration
Create a `.env` file in the backend directory:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
```

## Usage

### 1. Inventory Management
- **Servers**: Add server specifications including vCPU, RAM, disk, OS, and technologies
- **Databases**: Configure database types, sizes, HA/DR requirements, and backup policies  
- **File Shares**: Define storage requirements, access patterns, and retention policies

### 2. Configuration
- **Cloud Preferences**: Select target cloud provider, region, and preferred services
- **Business Constraints**: Set migration windows, cutover dates, and downtime tolerance
- **Resource Rates**: Configure billing rates for different roles and time estimates

### 3. Analysis & Planning
- **Cost Estimation**: Generate comprehensive cost analysis for cloud services and migration
- **Migration Strategy**: Get AI-powered recommendations for migration approaches
- **Timeline Planning**: Create detailed project timelines with dependencies and milestones

### 4. Export Reports
- Generate executive summaries and detailed migration plans
- Export to Excel, PDF, or Word formats
- Include cost breakdowns, timelines, and risk assessments

## Sample Input Data

### Server Inventory
| Field | Example |
|-------|---------|
| Server ID | APP-SVR-01 |
| OS Type | Windows Server 2019 |
| vCPU | 4 |
| RAM | 16 GB |
| Disk Size | 500 GB |
| Technologies | JBoss, MySQL, Apache |

### Database Inventory
| Field | Example |
|-------|---------|
| DB Name | Finance_DB |
| DB Type | SQL Server |
| Size | 200 GB |
| HA/DR Required | Yes |
| Licensing | BYOL |

### File Share Inventory
| Field | Example |
|-------|---------|
| Share Name | SharedDocs |
| Size | 1 TB |
| Access Pattern | Warm |
| Retention | 90 days |

## System Outputs

- **Cloud Service Cost**: Based on source specs and cloud SKUs
- **Migration Service Cost**: Professional services revenue estimates
- **Resource Plan**: Detailed staffing and billing breakdown
- **Migration Timeline**: Milestone-based plan with dependencies
- **Data Migration Strategy**: Recommended tools and approaches
- **Server Migration Strategy**: Rehost vs Replatform recommendations
- **Technology Mapping**: Cloud service mappings for each component
- **Migration Runbook**: Complete task list with rollback plan
- **Risk Assessment**: Identified risks and mitigation strategies

## API Documentation

### Core Endpoints
- `GET|POST /api/servers` - Server inventory management
- `GET|POST /api/databases` - Database inventory management
- `GET|POST /api/file-shares` - File share inventory management
- `GET|POST /api/cloud-preferences` - Cloud target configuration
- `GET|POST /api/business-constraints` - Business requirements
- `POST /api/cost-estimation` - Generate cost analysis
- `POST /api/migration-strategy` - AI-powered strategy recommendations
- `POST /api/timeline` - Migration timeline generation
- `POST /api/export` - Report export functionality

## Target Users

- **Cloud Architects**: Infrastructure planning and optimization
- **Pre-Sales Teams**: Proposal preparation and cost estimation
- **Solutions Architects**: Technical migration planning
- **Program Managers**: Project planning and resource allocation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support and questions, please open an issue in the GitHub repository.
