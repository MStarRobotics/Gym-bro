import React from 'react';
import type { View } from '../types';
import {
  ChatIcon,
  DashboardIcon,
  FitAILogo,
  LocationIcon,
  MealIcon,
  PlanIcon,
  SearchIcon,
} from './common/Icons';

interface SidebarProps {
  currentView: View;
  setCurrentView: (view: View) => void;
  isSidebarOpen: boolean;
  setIsSidebarOpen: (isOpen: boolean) => void;
  toggleChat: () => void;
}

interface NavItemProps {
  onClick: () => void;
  isActive: boolean;
  icon: React.ReactNode;
  label: string;
  delayClass?: string;
}

const NavItem: React.FC<NavItemProps> = ({
  onClick,
  isActive,
  icon,
  label,
  delayClass,
}) => (
  <li className={`opacity-0 animate-slideInFromLeft ${delayClass ?? ''}`}>
    <button
      type="button"
      onClick={() => onClick()}
      className={`nav-item-retro flex items-center p-3 my-1 rounded-lg transition-colors duration-200 ${
        isActive
          ? 'bg-teal-500 text-white shadow-md'
          : 'text-gray-300 hover:bg-gray-700 hover:text-white'
      }`}
    >
      {icon}
      <span className="ml-4 font-medium">{label}</span>
    </button>
  </li>
);

const Sidebar: React.FC<SidebarProps> = ({
  currentView,
  setCurrentView,
  isSidebarOpen,
  setIsSidebarOpen,
  toggleChat,
}): React.ReactElement => {
  const navItems = [
    {
      id: 'dashboard',
      view: 'dashboard' as View,
      icon: <DashboardIcon className="h-6 w-6" />,
      label: 'Dashboard',
    },
    {
      id: 'chatbot',
      icon: <ChatIcon className="h-6 w-6" />,
      label: 'AI Coach Chat',
    },
    {
      id: 'meal-analyzer',
      view: 'meal-analyzer' as View,
      icon: <MealIcon className="h-6 w-6" />,
      label: 'Meal Analyzer',
    },
    {
      id: 'plan-generator',
      view: 'plan-generator' as View,
      icon: <PlanIcon className="h-6 w-6" />,
      label: 'Plan Generator',
    },
    {
      id: 'location-finder',
      view: 'location-finder' as View,
      icon: <LocationIcon className="h-6 w-6" />,
      label: 'Find Nearby',
    },
    {
      id: 'fact-checker',
      view: 'fact-checker' as View,
      icon: <SearchIcon className="h-6 w-6" />,
      label: 'Fitness Fact-Check',
    },
  ];

  const CloseIcon = (): React.ReactElement => (
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
        d="M6 18L18 6M6 6l12 12"
      />
    </svg>
  );

  return (
    <>
      <button
        className={`fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden transition-opacity ${isSidebarOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
        type="button"
        aria-label="Close navigation overlay"
        onClick={() => setIsSidebarOpen(false)}
      ></button>
      <aside
        className={`sidebar-retro absolute lg:relative flex flex-col w-64 bg-gray-800 h-full p-4 transition-transform duration-300 ease-in-out z-40 ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0`}
      >
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center text-2xl font-bold text-white">
            <FitAILogo className="h-8 w-8 text-teal-400 mr-2" />
            <span>FitAI</span>
          </div>
          <button
            onClick={() => setIsSidebarOpen(false)}
            aria-label="Close navigation"
            className="lg:hidden text-gray-300 hover:text-white"
          >
            <CloseIcon />
          </button>
        </div>
        <nav className="flex-1">
          <ul>
            {navItems.map((item, index) => (
              <NavItem
                key={item.id}
                isActive={currentView === item.view && item.id !== 'chatbot'}
                icon={item.icon}
                label={item.label}
                delayClass={
                  [
                    'delay-75',
                    'delay-100',
                    'delay-150',
                    'delay-200',
                    'delay-300',
                    'delay-500',
                  ][index] ?? ''
                }
                onClick={() => {
                  if (item.id === 'chatbot') {
                    toggleChat();
                  } else if (item.view) {
                    setCurrentView(item.view);
                  }
                  setIsSidebarOpen(false);
                }}
              />
            ))}
          </ul>
        </nav>
        <div className="mt-auto text-center text-xs text-gray-500">
          <p>&copy; {new Date().getFullYear()} FitAI. All rights reserved.</p>
          <p>Powered by Gemini</p>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
