import React, { useCallback, useState } from 'react';
import { analyzeMealImage, suggestMealPrompt } from '../services/geminiService';
import Button from './common/Button';
import Card from './common/Card';
import LoadingSpinner from './common/LoadingSpinner';
import MarkdownRenderer from './common/MarkdownRenderer';

interface NutritionalFacts {
  calories: string | null;
  protein: string | null;
  carbs: string | null;
  fat: string | null;
}

const FileUploadIcon = (): React.ReactElement => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    className="h-12 w-12 text-gray-500"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M7 16a4 4 0 01-4-4V6a4 4 0 014-4h1.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V16a4 4 0 01-4 4H7z"
    />
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      strokeWidth={2}
      d="M11 12.586l-2.293-2.293a1 1 0 00-1.414 1.414L10.586 15H5"
    />
  </svg>
);

const MealAnalyzer: React.FC = (): React.ReactElement => {
  const [image, setImage] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [prompt, setPrompt] = useState<string>(
    'Estimate the calories and macronutrients for this meal, and provide a general health analysis.'
  );
  const [result, setResult] = useState<string>('');
  const [nutritionalFacts, setNutritionalFacts] =
    useState<NutritionalFacts | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSuggesting, setIsSuggesting] = useState(false);
  const [error, setError] = useState<string>('');

  const examplePrompts = [
    {
      label: 'Is this healthy?',
      value: 'Is this meal healthy? Why or why not?',
    },
    {
      label: 'Suggest recipe',
      value: 'Can you suggest a recipe based on this image?',
    },
    {
      label: 'Guess ingredients',
      value: 'What ingredients are likely in this dish?',
    },
    {
      label: 'Make it healthier',
      value: 'How could I make this meal healthier?',
    },
  ];

  const parseNutritionalFacts = (text: string): NutritionalFacts => {
    const findFact = (pattern: RegExp): string | null => {
      const match = pattern.exec(text);
      return match?.[1]?.trim() ?? null;
    };

    return {
      calories: findFact(
        /(?:calories|energy|kcal)[:\s]*([\d\s.,~-]+(?:kcal|calories)?)/i
      ),
      protein: findFact(/protein[:\s]*([\d\s.,~-]+g)/i),
      carbs: findFact(/(?:carbohydrates|carbs)[:\s]*([\d\s.,~-]+g)/i),
      fat: findFact(/fat[:\s]*([\d\s.,~-]+g)/i),
    };
  };

  const handleImageChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ): void => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 4 * 1024 * 1024) {
        // 4MB limit for inline data
        setError('That image is a bit too large. Please choose one under 4MB.');
        return;
      }
      setError('');
      setResult(''); // Clear previous result on new image
      setNutritionalFacts(null);
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = (): void => {
        setImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const toBase64 = (file: File): Promise<string> =>
    new Promise<string>((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = (): void =>
        resolve((reader.result as string).split(',')[1]);
      reader.onerror = (): void => reject(new Error('Failed to read file'));
    });

  const getMimeType = (file: File): string | null => {
    const supportedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (file.type && supportedTypes.includes(file.type)) return file.type;
    const extension = file.name.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'jpg':
      case 'jpeg':
        return 'image/jpeg';
      case 'png':
        return 'image/png';
      case 'webp':
        return 'image/webp';
      default:
        return null;
    }
  };

  const analyzeImage = useCallback(async (): Promise<void> => {
    if (!imageFile) {
      setError('Please upload an image first.');
      return;
    }
    if (!prompt) {
      setError('Please provide a prompt so I know what to look for!');
      return;
    }
    setIsLoading(true);
    setResult('');
    setNutritionalFacts(null);
    setError('');
    try {
      const mimeType = getMimeType(imageFile);
      if (!mimeType) {
        throw new Error(
          "That file format isn't supported. Please use a PNG, JPG, or WEBP image."
        );
      }
      const base64Image = await toBase64(imageFile);
      const analysisResult = await analyzeMealImage(
        base64Image,
        mimeType,
        prompt
      );
      setResult(analysisResult);
      const facts = parseNutritionalFacts(analysisResult);
      setNutritionalFacts(facts);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to analyze meal');
    } finally {
      setIsLoading(false);
    }
  }, [imageFile, prompt]);

  const handleSuggestPrompt = useCallback(async (): Promise<void> => {
    if (!imageFile) return;
    setIsSuggesting(true);
    setError('');
    try {
      const mimeType = getMimeType(imageFile);
      if (!mimeType) {
        throw new Error(
          "That file format isn't supported. Please use a PNG, JPG, or WEBP image."
        );
      }
      const base64Image = await toBase64(imageFile);
      const suggested = await suggestMealPrompt(base64Image, mimeType);
      setPrompt(suggested);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to suggest prompt');
    } finally {
      setIsSuggesting(false);
    }
  }, [imageFile]);

  const hasFacts =
    nutritionalFacts && Object.values(nutritionalFacts).some((v) => v !== null);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-4">Meal Analyzer</h1>
      <p className="text-gray-400 mb-6">
        Upload a photo of your meal and ask anything! Get a nutritional
        estimate, check if it&apos;s healthy, or even ask for a recipe.
      </p>

      <Card>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex flex-col items-center justify-center">
            <label htmlFor="image-upload" className="w-full cursor-pointer">
              {image ? (
                <img
                  src={image}
                  alt="Meal preview"
                  className="rounded-lg object-cover w-full h-64 shadow-md"
                />
              ) : (
                <div className="w-full h-64 border-2 border-dashed border-gray-600 rounded-lg flex flex-col justify-center items-center text-gray-400 hover:bg-gray-700 hover:border-gray-500 transition-colors">
                  <FileUploadIcon />
                  <p className="mt-2">Click to upload an image</p>
                  <p className="text-xs text-gray-500">
                    PNG, JPG, WEBP (Max 4MB)
                  </p>
                </div>
              )}
            </label>
            <input
              id="image-upload"
              type="file"
              accept="image/png, image/jpeg, image/webp"
              className="hidden"
              onChange={handleImageChange}
            />
          </div>
          <div className="flex flex-col">
            <label
              htmlFor="prompt"
              className="block text-sm font-medium text-gray-300 mb-2"
            >
              What should I look for?
            </label>
            <textarea
              id="prompt"
              rows={3}
              className="w-full bg-gray-700 text-white p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 mb-2"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ask anything about this meal..."
            />
            <div className="flex flex-wrap gap-2 mb-4">
              <p className="text-xs text-gray-400 w-full mb-1">
                Or try an example:
              </p>
              {examplePrompts.map((p) => (
                <button
                  key={p.label}
                  onClick={() => setPrompt(p.value)}
                  className="px-3 py-1 bg-gray-600/80 text-gray-200 rounded-full text-xs hover:bg-gray-500/80 transition-colors focus:outline-none focus:ring-2 focus:ring-teal-500"
                >
                  {p.label}
                </button>
              ))}
            </div>
            {image && (
              <Button
                onClick={handleSuggestPrompt}
                disabled={!image || isLoading || isSuggesting}
                variant="secondary"
                className="text-xs py-1 px-3 w-full mb-4"
              >
                {isSuggesting ? (
                  <>
                    <LoadingSpinner /> Thinking...
                  </>
                ) : (
                  <span className="flex items-center gap-2">
                    ✨ Suggest a Prompt
                  </span>
                )}
              </Button>
            )}
            <Button
              onClick={analyzeImage}
              disabled={isLoading || !image}
              className="mt-auto"
            >
              {isLoading ? (
                <>
                  <LoadingSpinner /> Analyzing your meal...
                </>
              ) : (
                'Analyze Meal'
              )}
            </Button>
            {error && (
              <p className="text-red-400 mt-2 text-sm text-center">{error}</p>
            )}
          </div>
        </div>

        {result && !isLoading && (
          <div className="mt-6 pt-6 border-t border-gray-700">
            {hasFacts && (
              <div className="mb-6">
                <h3 className="text-xl font-semibold text-white mb-3">
                  Nutritional Summary
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                  <div className="bg-gray-700/50 p-3 rounded-lg">
                    <p className="text-sm text-gray-400">Calories</p>
                    <p className="text-2xl font-bold text-teal-400">
                      {nutritionalFacts.calories || 'N/A'}
                    </p>
                  </div>
                  <div className="bg-gray-700/50 p-3 rounded-lg">
                    <p className="text-sm text-gray-400">Protein</p>
                    <p className="text-2xl font-bold text-teal-400">
                      {nutritionalFacts.protein || 'N/A'}
                    </p>
                  </div>
                  <div className="bg-gray-700/50 p-3 rounded-lg">
                    <p className="text-sm text-gray-400">Carbs</p>
                    <p className="text-2xl font-bold text-teal-400">
                      {nutritionalFacts.carbs || 'N/A'}
                    </p>
                  </div>
                  <div className="bg-gray-700/50 p-3 rounded-lg">
                    <p className="text-sm text-gray-400">Fat</p>
                    <p className="text-2xl font-bold text-teal-400">
                      {nutritionalFacts.fat || 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
            )}
            <h2 className="text-xl font-semibold text-white mb-2">
              Detailed Analysis
            </h2>
            <div className="bg-gray-900 p-4 rounded-md">
              <MarkdownRenderer content={result} />
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default MealAnalyzer;
