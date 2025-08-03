<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Cloud Migration Tool - AI-Powered Migration Planning

## Project Overview
This is a Gen-AI powered cloud migration planning tool that assists with pre-sales planning, data migration strategy advisory, and server migration strategy planning.

## Technology Stack
- **Frontend**: ReactJS with TypeScript, Ant Design UI components
- **Backend**: Python Flask with SQLAlchemy ORM
- **Database**: SQLite for local development
- **AI Integration**: AWS Bedrock for intelligent recommendations
- **Charts**: Ant Design Plots for data visualization

## Architecture
- Full-stack application with separate frontend and backend
- RESTful API design
- Modular component structure for frontend
- Service-based architecture for backend business logic

## Key Features
1. **Pre-sales Planning**: Cost estimation, resource planning, timeline generation
2. **Data Migration Strategy**: AI-powered recommendations for databases and file shares
3. **Server Migration Strategy**: Rehost vs Replatform recommendations with cloud service mappings
4. **Export Functionality**: Excel, PDF, and Word report generation

## Development Guidelines
- Use TypeScript for type safety in frontend components
- Follow Ant Design design patterns for UI consistency
- Implement proper error handling and loading states
- Use async/await for API calls
- Maintain separation of concerns between components and services

## Backend Services
- `CostCalculator`: Handles cost estimation for cloud services and migration
- `MigrationAdvisor`: AI-powered migration strategy recommendations
- `TimelineGenerator`: Creates detailed migration timelines with dependencies
- `ExportService`: Generates reports in multiple formats

## Database Models
- Server, Database, FileShare: Inventory management
- CloudPreference, BusinessConstraint: Configuration
- ResourceRate, MigrationPlan: Planning and results

## API Endpoints
All endpoints are prefixed with `/api/` and support CRUD operations for inventory management, configuration, and analysis.
