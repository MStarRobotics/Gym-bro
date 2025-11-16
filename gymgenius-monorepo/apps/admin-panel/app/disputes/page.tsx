'use client';


/**
 * Dispute Management System
 * 
 * **Features:**
 * - View all customer disputes/complaints
 * - Filter by status (open, in-progress, resolved, closed)
 * - Assign disputes to support staff
 * - Internal notes and communication log
 * - Attach refund processing
 * - Escalation workflow
 * - Response time SLA tracking
 * - Customer satisfaction after resolution
 * 
 * NOTE: Dispute API integration requires backend endpoint
 * NOTE: Detail view modal will be implemented with state management
 * NOTE: Status workflow requires role-based permissions
 * NOTE: Refund processing integrates with Razorpay API
 */
export default function DisputesPage() {
  // Mock dispute data for demonstration
  const mockDisputes = [
    { id: 'D001', customer: 'Ravi Kumar', issue: 'Payment not reflected', status: 'Open', priority: 'High', sla: '2h remaining' },
    { id: 'D002', customer: 'Sneha Reddy', issue: 'Trainer cancelled session', status: 'In Progress', priority: 'Medium', sla: '5h remaining' },
    { id: 'D003', customer: 'Arjun Patel', issue: 'Subscription not activated', status: 'Open', priority: 'High', sla: '1h remaining' },
  ];

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200';
      case 'Medium': return 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200';
      case 'Low': return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
      default: return 'bg-gray-100 dark:bg-gray-700';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Open': return 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200';
      case 'In Progress': return 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200';
      case 'Resolved': return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200';
      default: return 'bg-gray-100 dark:bg-gray-700';
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Dispute Management</h1>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <table className="w-full">
          <thead>
            <tr className="border-b dark:border-gray-700">
              <th className="text-left py-2">ID</th>
              <th className="text-left py-2">Customer</th>
              <th className="text-left py-2">Issue</th>
              <th className="text-left py-2">Status</th>
              <th className="text-left py-2">Priority</th>
              <th className="text-left py-2">SLA</th>
              <th className="text-left py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {mockDisputes.map((dispute) => (
              <tr key={dispute.id} className="border-b dark:border-gray-700">
                <td className="py-2 font-mono">{dispute.id}</td>
                <td className="py-2">{dispute.customer}</td>
                <td className="py-2">{dispute.issue}</td>
                <td className="py-2">
                  <span className={`px-2 py-1 rounded text-sm ${getStatusColor(dispute.status)}`}>
                    {dispute.status}
                  </span>
                </td>
                <td className="py-2">
                  <span className={`px-2 py-1 rounded text-sm ${getPriorityColor(dispute.priority)}`}>
                    {dispute.priority}
                  </span>
                </td>
                <td className="py-2 text-sm">{dispute.sla}</td>
                <td className="py-2">
                  <button className="text-blue-600 hover:text-blue-800 mr-2">Assign</button>
                  <button className="text-green-600 hover:text-green-800 mr-2">Resolve</button>
                  <button className="text-orange-600 hover:text-orange-800">Escalate</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
