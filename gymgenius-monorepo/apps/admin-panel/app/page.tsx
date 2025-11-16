export default function AdminDashboard() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">GymGenius Admin Panel</h1>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-sm text-gray-400 mb-2">Total Users</h3>
            <p className="text-3xl font-bold text-primary">1,247</p>
            <p className="text-xs text-green-400 mt-2">↑ 12% from last month</p>
          </div>

          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-sm text-gray-400 mb-2">Active Subscriptions</h3>
            <p className="text-3xl font-bold text-secondary">892</p>
            <p className="text-xs text-green-400 mt-2">↑ 8% from last month</p>
          </div>

          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-sm text-gray-400 mb-2">Revenue (MTD)</h3>
            <p className="text-3xl font-bold text-accent">₹2.4L</p>
            <p className="text-xs text-green-400 mt-2">↑ 15% from last month</p>
          </div>

          <div className="bg-gray-800 rounded-lg p-6">
            <h3 className="text-sm text-gray-400 mb-2">Support Tickets</h3>
            <p className="text-3xl font-bold text-yellow-400">23</p>
            <p className="text-xs text-gray-400 mt-2">5 urgent</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">User Management</h2>
            <div className="space-y-3">
              <button className="w-full bg-primary text-black py-3 rounded-lg hover:opacity-80">
                View All Users
              </button>
              <button className="w-full bg-secondary text-black py-3 rounded-lg hover:opacity-80">
                Manage Trainers
              </button>
              <button className="w-full bg-accent text-white py-3 rounded-lg hover:opacity-80">
                Manage Nutritionists
              </button>
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">System Health</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">API Status</span>
                <span className="text-green-400 font-semibold">● Healthy</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Database</span>
                <span className="text-green-400 font-semibold">● Healthy</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Socket.io Server</span>
                <span className="text-green-400 font-semibold">● Healthy</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400">Redis Cache</span>
                <span className="text-green-400 font-semibold">● Healthy</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
