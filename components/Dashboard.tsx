import React from 'react';
import Card from './common/Card';

const features = [
  {
    title: 'AI Coach Chat',
    description:
      'Get instant answers, motivation, and personalized advice from your AI coach.',
  },
  {
    title: 'Track Your Session',
    description:
      'Log your workouts and monitor your progress towards your goals.',
  },
  {
    title: 'View Nutrition Plan',
    description:
      'Access your personalized weekly meal plans and track your macros.',
  },
  {
    title: 'Book a Trainer',
    description:
      'Find and schedule sessions with certified personal trainers in your area.',
  },
  {
    title: 'Order Equipment',
    description:
      'Browse and order fitness equipment recommended for your plan.',
  },
];

const Dashboard: React.FC = () => {
  return (
    <div>
      <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
        Welcome to <span className="text-teal-400">FitAI</span>
      </h1>
      <p className="text-lg text-gray-300 mb-8">
        Your AI-powered personal fitness and nutrition coach. Select a feature
        from the sidebar to get started.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature) => (
          <Card
            key={feature.title}
            className="border-l-4 border-teal-400 opacity-0"
          >
            <h2 className="text-xl font-semibold text-white mb-2">
              {feature.title}
            </h2>
            <p className="text-gray-400">{feature.description}</p>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
