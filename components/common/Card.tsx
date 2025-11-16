import React from 'react';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
}

const Card: React.FC<CardProps> = ({ children, className = '', ...props }) => {
  return (
    <div
      className={`bg-gray-800/70 backdrop-blur-sm p-6 rounded-lg shadow-lg border border-gray-700/80 transition-all duration-300 ease-in-out transform hover:-translate-y-2 hover:shadow-2xl hover:shadow-teal-500/20 hover:border-teal-400/60 ${className}`}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
