import React, { useCallback, useState } from 'react';
import useGeolocation from '../hooks/useGeolocation';
import { findNearbyPlaces } from '../services/geminiService';
import type { GroundingChunk } from '../types';
import Button from './common/Button';
import Card from './common/Card';
import { ExternalLinkIcon } from './common/Icons';
import LoadingSpinner from './common/LoadingSpinner';
import MarkdownRenderer from './common/MarkdownRenderer';

const LocationFinder: React.FC = () => {
  const [prompt, setPrompt] = useState('Find top-rated gyms near me');
  const [result, setResult] = useState<{
    text: string;
    sources: GroundingChunk[];
  } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const location = useGeolocation();

  const findPlaces = useCallback(async () => {
    if (!location.data) {
      setError(
        "I can't seem to find your location. Please ensure location services are enabled in your browser and for this site."
      );
      return;
    }
    setIsLoading(true);
    setResult(null);
    setError('');
    try {
      const searchResult = await findNearbyPlaces(prompt, {
        latitude: location.data.latitude,
        longitude: location.data.longitude,
      });
      if (
        searchResult.sources.length === 0 &&
        searchResult.text.toLowerCase().includes('sorry')
      ) {
        setError(searchResult.text);
      } else {
        setResult(searchResult);
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : 'Failed to find locations');
    } finally {
      setIsLoading(false);
    }
  }, [prompt, location.data]);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-4">Find Nearby</h1>
      <p className="text-gray-400 mb-6">
        Discover local gyms, parks, or healthy restaurants using real-time
        Google Maps data.
      </p>

      <Card>
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., 'Find parks with running trails'"
            className="flex-1 bg-gray-700 text-white p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            disabled={isLoading || location.loading}
          />
          <Button
            onClick={findPlaces}
            disabled={isLoading || location.loading || !location.data}
          >
            {isLoading ? <LoadingSpinner /> : 'Search'}
            {location.loading && (
              <span className="ml-2">Finding your location...</span>
            )}
          </Button>
        </div>
        {location.error && (
          <p className="text-red-400 mt-2 text-sm">
            {
              "I can't seem to find your location. Please ensure location services are enabled in your browser and for this site."
            }
          </p>
        )}
        {error && <p className="text-red-400 mt-2 text-sm">{error}</p>}
      </Card>

      {result && (
        <div className="mt-6">
          <Card>
            <h2 className="text-xl font-semibold text-white mb-4">
              Here&apos;s what I found
            </h2>
            <div className="bg-gray-900 p-4 rounded-md mb-4">
              <MarkdownRenderer content={result.text} />
            </div>
            {result.sources && result.sources.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-teal-400 mb-3">
                  Sources from Google Maps
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {result.sources.map(
                    (source) =>
                      source.maps && (
                        <a
                          key={source.maps.uri}
                          href={source.maps.uri}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block"
                        >
                          <Card className="h-full !p-4">
                            <div className="flex justify-between items-start">
                              <p className="font-semibold text-teal-300 pr-2">
                                {source.maps.title}
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

export default LocationFinder;
