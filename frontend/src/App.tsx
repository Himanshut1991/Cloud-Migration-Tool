import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, ConfigProvider } from 'antd';
import 'antd/dist/reset.css';
import './App.css';

// Components
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';
import Dashboard from './components/Dashboard/Dashboard';
import ServerInventory from './components/Inventory/ServerInventory';
import DatabaseInventory from './components/Inventory/DatabaseInventory';
import FileShareInventory from './components/Inventory/FileShareInventory';
import CloudPreferences from './components/Configuration/CloudPreferences';
import BusinessConstraints from './components/Configuration/BusinessConstraints';
import ResourceRates from './components/Configuration/ResourceRates';
import CostEstimationSimple from './components/Analysis/CostEstimationSimple';
import MigrationStrategySimple from './components/Analysis/MigrationStrategySimple';
import TimelineSimple from './components/Analysis/TimelineSimple';
import ExportReports from './components/Reports/ExportReports';
import ApiTester from './components/Debug/ApiTester';

const { Content } = Layout;

const App: React.FC = () => {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 6,
        },
      }}
    >
      <div className="app">
        <Router>
          <Layout hasSider style={{ minHeight: '100vh' }}>
            <Sidebar />
            <Layout style={{ marginLeft: 260 }}>
              <Header />
              <Content style={{ 
                padding: '24px', 
                background: '#f5f5f5',
                overflow: 'initial',
                minHeight: 'calc(100vh - 64px)'
              }}>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  
                  {/* Debug */}
                  <Route path="/debug/api-test" element={<ApiTester />} />
                  
                  {/* Inventory Management */}
                  <Route path="/inventory/servers" element={<ServerInventory />} />
                  <Route path="/inventory/databases" element={<DatabaseInventory />} />
                  <Route path="/inventory/file-shares" element={<FileShareInventory />} />
                  
                  {/* Configuration */}
                  <Route path="/configuration/cloud-preferences" element={<CloudPreferences />} />
                  <Route path="/configuration/business-constraints" element={<BusinessConstraints />} />
                  <Route path="/configuration/resource-rates" element={<ResourceRates />} />
                  
                  {/* Analysis */}
                  <Route path="/analysis/cost-estimation" element={<CostEstimationSimple />} />
                  <Route path="/analysis/migration-strategy" element={<MigrationStrategySimple />} />
                  <Route path="/analysis/timeline" element={<TimelineSimple />} />
                  
                  {/* Reports */}
                  <Route path="/reports/export" element={<ExportReports />} />
                </Routes>
              </Content>
            </Layout>
          </Layout>
        </Router>
      </div>
    </ConfigProvider>
  );
};

export default App;
