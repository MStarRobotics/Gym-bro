import React, { useCallback, useState } from 'react';
import { getUpToDateAnswer } from '../services/geminiService';
import type { GroundingChunk } from '../types';
import Button from './common/Button';
import Card from './common/Card';
import { ExternalLinkIcon } from './common/Icons';
import LoadingSpinner from './common/LoadingSpinner';
import MarkdownRenderer from './common/MarkdownRenderer';

const FactChecker: React.FC = (): React.ReactElement => {
  const [prompt, setPrompt] = useState(
    'What are the latest science-backed benefits of HIIT workouts?'
  );
  const [result, setResult] = useState<{
    text: string;
    sources: GroundingChunk[];
  } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const findAnswer = useCallback(async (): Promise<void> => {
    if (!prompt.trim()) {
      setError('Please enter a question to get an answer.');
      return;
    }
    setIsLoading(true);
    setResult(null);
    setError('');
    try {
      const searchResult = await getUpToDateAnswer(prompt);
      if (
        searchResult.sources.length === 0 &&
        searchResult.text.toLowerCase().includes('sorry')
      ) {
        setError(searchResult.text);
      } else {
        setResult(searchResult);
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to check facts');
    } finally {
      setIsLoading(false);
    }
  }, [prompt]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === 'Enter') {
      findAnswer();
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-4">
        Fitness Fact-Checker
      </h1>
      <p className="text-gray-400 mb-6">
        Ask any fitness or nutrition question and get up-to-date answers
        grounded in Google Search results.
      </p>

      <Card>
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a fitness question..."
            className="flex-1 bg-gray-700 text-white p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            disabled={isLoading}
          />
          <Button onClick={findAnswer} disabled={isLoading}>
            {isLoading ? (
              <>
                <LoadingSpinner /> Finding the facts...
              </>
            ) : (
              'Get Answer'
            )}
          </Button>
        </div>
        {error && <p className="text-red-400 mt-2 text-sm">{error}</p>}
      </Card>

      {result && (
        <div className="mt-6">
          <Card>
            <h2 className="text-xl font-semibold text-white mb-4">Answer</h2>
            <div className="bg-gray-900 p-4 rounded-md mb-4">
              <MarkdownRenderer content={result.text} />
            </div>
            {result.sources && result.sources.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-teal-400 mb-3">
                  Sources from Google Search
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {result.sources.map(
                    (source) =>
                      source.web && (
                        <a
                          key={source.web.uri}
                          href={source.web.uri}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block"
                        >
                          <Card className="h-full !p-4">
                            <div className="flex justify-between items-start">
                              <p
                                className="font-semibold text-teal-300 pr-2 truncate"
                                title={source.web.title}
                              >
                                {source.web.title}
                              </p>
                              <ExternalLinkIcon className="h-5 w-5 text-gray-400 flex-shrink-0" />
                            </div>
                          </Card>
                        </a>
                      )
                  )}
                </div>
              </div>
            )}
          </Card>
        </div>
      )}
    </div>
  );
};

export default FactChecker;
