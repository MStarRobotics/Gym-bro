import React, { useState } from 'react';
import Dashboard from './components/Dashboard';
import FactChecker from './components/FactChecker';
import FloatingChatbot from './components/FloatingChatbot';
import LocationFinder from './components/LocationFinder';
import MealAnalyzer from './components/MealAnalyzer';
import PlanGenerator from './components/PlanGenerator';
import Sidebar from './components/Sidebar';
import type { View } from './types';

const MenuIcon = (): React.ReactElement => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className="h-6 w-6"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M4 6h16M4 12h16m-7 6h7"
    />
  </svg>
);

const App: React.FC = (): React.ReactElement => {
  const [currentView, setCurrentView] = useState<View>('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const toggleChat = (): void => setIsChatOpen((prev) => !prev);

  const renderView = (): React.ReactElement => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />;
      case 'meal-analyzer':
        return <MealAnalyzer />;
      case 'plan-generator':
        return <PlanGenerator />;
      case 'location-finder':
        return <LocationFinder />;
      case 'fact-checker':
        return <FactChecker />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen text-gray-100 font-sans">
      <Sidebar
        currentView={currentView}
        setCurrentView={setCurrentView}
        isSidebarOpen={isSidebarOpen}
        setIsSidebarOpen={setIsSidebarOpen}
        toggleChat={toggleChat}
      />
      <main className="flex-1 flex flex-col overflow-hidden">
        <div className="flex items-center justify-between p-4 bg-gray-800/70 backdrop-blur-sm shadow-md lg:hidden">
          <h1 className="text-xl font-bold text-teal-400">FitAI</h1>
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            aria-label="Toggle navigation"
            className="text-gray-200 hover:text-white"
          >
            <MenuIcon />
          </button>
        </div>
        <div className="flex-1 p-4 md:p-6 lg:p-8 overflow-y-auto">
          {renderView()}
        </div>
      </main>
      <FloatingChatbot
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
      />
    </div>
  );
};

export default App;
