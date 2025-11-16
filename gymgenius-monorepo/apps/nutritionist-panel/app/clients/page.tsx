'use client';


/**
 * Client Nutrition Plans Dashboard
 * 
 * **Features:**
 * - View all assigned clients
 * - Active meal plans overview
 * - Client adherence tracking
 * - Upcoming meal plan renewals
 * - Quick access to create new plans
 * - Client progress summaries
 * - Chat with clients
 * 
 * NOTE: Client list API requires backend endpoint
 * NOTE: Meal plan templates will use JSON schema format
 * NOTE: Plan assignment workflow requires state management
 */
export default function ClientsPage() {
  // Mock client data for demonstration
  const mockClients = [
    { id: 'C001', name: 'Anita Desai', plan: 'Weight Loss', adherence: 85, nextReview: '2024-11-20' },
    { id: 'C002', name: 'Karthik Reddy', plan: 'Muscle Gain', adherence: 92, nextReview: '2024-11-22' },
    { id: 'C003', name: 'Meera Shah', plan: 'Balanced Diet', adherence: 78, nextReview: '2024-11-25' },
  ];

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">My Clients</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {mockClients.map((client) => (
          <div key={client.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 className="text-xl font-bold mb-2">{client.name}</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-3">{client.plan}</p>
            <div className="mb-3">
              <div className="flex justify-between mb-1">
                <span className="text-sm">Adherence</span>
                <span className="text-sm font-semibold">{client.adherence}%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className={`bg-green-600 h-2 rounded-full`}
                  {...{ style: { width: `${client.adherence}%` } }}
                ></div>
              </div>
            </div>
            <p className="text-sm text-gray-500 mb-3">Next Review: {client.nextReview}</p>
            <div className="flex gap-2">
              <button className="flex-1 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700">
                View Plan
              </button>
              <button className="flex-1 px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700">
                Chat
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
