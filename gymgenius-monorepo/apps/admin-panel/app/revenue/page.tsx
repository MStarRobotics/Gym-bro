'use client';


/**
 * Revenue Analytics Dashboard
 * 
 * **Features:**
 * - Real-time revenue metrics
 * - Subscription revenue breakdown
 * - Booking revenue vs subscription revenue
 * - Revenue trends (daily, monthly, yearly)
 * - Payment method distribution chart
 * - Top revenue-generating trainers
 * - Churn rate analysis
 * - MRR (Monthly Recurring Revenue) tracking
 * - Export financial reports
 * 
 * NOTE: Payment service API integration pending
 * NOTE: Chart visualizations require Recharts library
 * NOTE: Date range picker will use react-datepicker
 * NOTE: PDF reports require jsPDF library integration
 */
export default function RevenuePage() {
  // Mock revenue data for demonstration
  const mockRevenue = {
    total: 245680,
    mrr: 89500,
    subscriptions: 156,
    pending: 12,
    growth: 15.3,
  };

  const topTrainers = [
    { id: 'T001', name: 'Rahul Sharma', revenue: 45000, clients: 23 },
    { id: 'T002', name: 'Priya Patel', revenue: 38000, clients: 19 },
    { id: 'T003', name: 'Amit Kumar', revenue: 32000, clients: 16 },
  ];

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Revenue Analytics</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm font-medium">Total Revenue</h3>
          <p className="text-3xl font-bold mt-2">₹{mockRevenue.total.toLocaleString()}</p>
          <p className="text-green-600 text-sm mt-1">+{mockRevenue.growth}% from last month</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm font-medium">MRR</h3>
          <p className="text-3xl font-bold mt-2">₹{mockRevenue.mrr.toLocaleString()}</p>
          <p className="text-green-600 text-sm mt-1">+{mockRevenue.growth}% growth</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h3 className="text-gray-500 text-sm font-medium">Active Subscriptions</h3>
          <p className="text-3xl font-bold mt-2">{mockRevenue.subscriptions}</p>
          <p className="text-blue-600 text-sm mt-1">{mockRevenue.pending} pending</p>
        </div>
      </div>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Top Revenue Trainers</h2>
        <table className="w-full">
          <thead>
            <tr className="border-b dark:border-gray-700">
              <th className="text-left py-2">Trainer</th>
              <th className="text-left py-2">Revenue</th>
              <th className="text-left py-2">Clients</th>
            </tr>
          </thead>
          <tbody>
            {topTrainers.map((trainer) => (
              <tr key={trainer.id} className="border-b dark:border-gray-700">
                <td className="py-2">{trainer.name}</td>
                <td className="py-2">₹{trainer.revenue.toLocaleString()}</td>
                <td className="py-2">{trainer.clients}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
