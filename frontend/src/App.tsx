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
import CostEstimation from './components/Analysis/CostEstimation';
import MigrationStrategy from './components/Analysis/MigrationStrategy';
import Timeline from './components/Analysis/Timeline';
import ExportReports from './components/Reports/ExportReports';

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
      <Router>
        <Layout className="app-layout">
          <Sidebar />
          <Layout style={{ marginLeft: 260 }}>
            <Header />
            <Content 
              className="app-content" 
              style={{ 
                margin: '0', 
                padding: '24px', 
                background: '#f5f5f5', 
                minHeight: 'calc(100vh - 64px)',
                overflow: 'auto'
              }}
            >
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/dashboard" element={<Dashboard />} />
                
                {/* Inventory Management */}
                <Route path="/inventory/servers" element={<ServerInventory />} />
                <Route path="/inventory/databases" element={<DatabaseInventory />} />
                <Route path="/inventory/file-shares" element={<FileShareInventory />} />
                
                {/* Configuration */}
                <Route path="/configuration/cloud-preferences" element={<CloudPreferences />} />
                <Route path="/configuration/business-constraints" element={<BusinessConstraints />} />
                <Route path="/configuration/resource-rates" element={<ResourceRates />} />
                
                {/* Analysis */}
                <Route path="/analysis/cost-estimation" element={<CostEstimation />} />
                <Route path="/analysis/migration-strategy" element={<MigrationStrategy />} />
                <Route path="/analysis/timeline" element={<Timeline />} />
                
                {/* Reports */}
                <Route path="/reports/export" element={<ExportReports />} />
              </Routes>
            </Content>
          </Layout>
        </Layout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
