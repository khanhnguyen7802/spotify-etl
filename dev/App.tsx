import React from 'react';
import { useStore } from './store/useStore';
import { AppRoute } from './types';
import Login from './components/Login';
import Layout from './components/Layout';
import Overview from './components/Overview';
import Pipelines from './components/Pipelines';
import Analysis from './components/Analysis';
import Share from './components/Share';
import About from './components/About';

const App: React.FC = () => {
  const { isAuthenticated, currentRoute } = useStore();

  if (!isAuthenticated) {
    return <Login />;
  }

  const renderContent = () => {
    switch (currentRoute) {
      case AppRoute.OVERVIEW: return <Overview />;
      case AppRoute.PIPELINES: return <Pipelines />;
      case AppRoute.ANALYSIS: return <Analysis />;
      case AppRoute.SHARE: return <Share />;
      case AppRoute.ABOUT: return <About />;
      default: return <Overview />;
    }
  };

  return (
    <Layout>
      {renderContent()}
    </Layout>
  );
};

export default App;