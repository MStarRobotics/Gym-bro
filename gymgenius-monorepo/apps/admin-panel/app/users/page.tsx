'use client';


/**
 * User Management Dashboard
 * 
 * **Features:**
 * - View all registered users (clients, trainers, nutritionists)
 * - Filter by role, subscription status, join date
 * - User details modal with full profile
 * - Activate/deactivate accounts
 * - Manual subscription management
 * - Export user data (CSV, Excel)
 * - User activity analytics
 * 
 * NOTE: API integration pending - using mock data
 * NOTE: Role-based filtering will be added in next iteration
 * NOTE: Search functionality requires backend endpoint
 * NOTE: User detail modal requires user profile API
 */
export default function UsersPage() {
  // Mock data for demonstration
  const mockUsers = [
    { id: 1, name: 'John Doe', role: 'Client', status: 'Active', joinDate: '2024-01-15' },
    { id: 2, name: 'Jane Smith', role: 'Trainer', status: 'Active', joinDate: '2024-02-20' },
    { id: 3, name: 'Mike Johnson', role: 'Nutritionist', status: 'Active', joinDate: '2024-03-10' },
  ];

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">User Management</h1>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search users..."
            className="w-full px-4 py-2 rounded border dark:bg-gray-700 dark:border-gray-600"
          />
        </div>
        <table className="w-full">
          <thead>
            <tr className="border-b dark:border-gray-700">
              <th className="text-left py-2">Name</th>
              <th className="text-left py-2">Role</th>
              <th className="text-left py-2">Status</th>
              <th className="text-left py-2">Join Date</th>
              <th className="text-left py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {mockUsers.map((user) => (
              <tr key={user.id} className="border-b dark:border-gray-700">
                <td className="py-2">{user.name}</td>
                <td className="py-2">
                  <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900 rounded text-sm">
                    {user.role}
                  </span>
                </td>
                <td className="py-2">
                  <span className="px-2 py-1 bg-green-100 dark:bg-green-900 rounded text-sm">
                    {user.status}
                  </span>
                </td>
                <td className="py-2">{user.joinDate}</td>
                <td className="py-2">
                  <button className="text-blue-600 hover:text-blue-800 mr-2">View</button>
                  <button className="text-green-600 hover:text-green-800 mr-2">Edit</button>
                  <button className="text-red-600 hover:text-red-800">Suspend</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
