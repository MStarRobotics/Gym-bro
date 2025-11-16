'use client';


/**
 * Meal Plan Builder
 * 
 * **Features:**
 * - Drag-and-drop meal planner
 * - Food database integration
 * - Macro calculator
 * - Meal timing optimizer
 * - Recipe library
 * - Portion size recommendations
 * - Dietary restriction filters
 * - Export plans as PDF
 * 
 * NOTE: Meal builder UI requires drag-and-drop library (react-dnd)
 * NOTE: Nutrition API integration uses USDA FoodData Central
 * NOTE: Template system will use JSON schema with validation
 */
export default function MealPlansPage() {
  // Mock meal plan templates for demonstration
  const mockTemplates = [
    { id: 'T001', name: 'Weight Loss - 1500 Cal', calories: 1500, protein: 120, carbs: 150, fat: 50 },
    { id: 'T002', name: 'Muscle Gain - 2500 Cal', calories: 2500, protein: 200, carbs: 300, fat: 80 },
    { id: 'T003', name: 'Balanced - 2000 Cal', calories: 2000, protein: 150, carbs: 225, fat: 65 },
  ];

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Meal Plans</h1>
      <div className="mb-6">
        <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          + Create New Plan
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {mockTemplates.map((template) => (
          <div key={template.id} className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 className="text-xl font-bold mb-4">{template.name}</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Calories</span>
                <span className="font-semibold">{template.calories} kcal</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Protein</span>
                <span className="font-semibold">{template.protein}g</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Carbs</span>
                <span className="font-semibold">{template.carbs}g</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Fat</span>
                <span className="font-semibold">{template.fat}g</span>
              </div>
            </div>
            <div className="mt-4 flex gap-2">
              <button className="flex-1 px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700">
                Use Template
              </button>
              <button className="flex-1 px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700">
                Edit
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
