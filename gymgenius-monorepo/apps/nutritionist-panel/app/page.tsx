export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2 gradient-primary bg-clip-text text-transparent">
            GymGenius Nutritionist Panel
          </h1>
          <p className="text-gray-400">
            Manage client nutrition and meal plans
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Clients Card */}
          <div className="bg-background-card rounded-lg p-6 glow-effect">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Active Clients</h2>
              <div className="text-3xl">👥</div>
            </div>
            <p className="text-3xl font-bold text-primary-glow">24</p>
            <p className="text-sm text-gray-400 mt-2">+3 this week</p>
          </div>

          {/* Meal Plans Card */}
          <div className="bg-background-card rounded-lg p-6 glow-effect">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Meal Plans</h2>
              <div className="text-3xl">🍽️</div>
            </div>
            <p className="text-3xl font-bold text-secondary-glow">48</p>
            <p className="text-sm text-gray-400 mt-2">12 created today</p>
          </div>

          {/* Messages Card */}
          <div className="bg-background-card rounded-lg p-6 glow-effect">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Messages</h2>
              <div className="text-3xl">💬</div>
            </div>
            <p className="text-3xl font-bold text-accent-glow">7</p>
            <p className="text-sm text-gray-400 mt-2">Unread messages</p>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-8 bg-background-card rounded-lg p-6">
          <h2 className="text-2xl font-bold mb-4">Recent Activity</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-gray-700 pb-4">
              <div>
                <p className="font-semibold">New client registered</p>
                <p className="text-sm text-gray-400">
                  John Doe - 5 minutes ago
                </p>
              </div>
              <button className="px-4 py-2 bg-primary-glow text-black rounded-lg hover:opacity-80 transition">
                View Profile
              </button>
            </div>
            <div className="flex items-center justify-between border-b border-gray-700 pb-4">
              <div>
                <p className="font-semibold">Meal plan completed</p>
                <p className="text-sm text-gray-400">
                  Sarah Smith - 1 hour ago
                </p>
              </div>
              <button className="px-4 py-2 bg-secondary-glow text-black rounded-lg hover:opacity-80 transition">
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
