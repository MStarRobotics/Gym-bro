import React, { useCallback, useState } from 'react';
import { generatePlan, generateSpeech } from '../services/geminiService';
import { decode, decodeAudioData } from '../utils/audioUtils';
import Button from './common/Button';
import Card from './common/Card';
import { SoundIcon } from './common/Icons';
import LoadingSpinner from './common/LoadingSpinner';
import MarkdownRenderer from './common/MarkdownRenderer';

const PlanGenerator: React.FC = (): React.ReactElement => {
  const [goal, setGoal] = useState('lose weight');
  const [level, setLevel] = useState('beginner');
  const [days, setDays] = useState('3');
  const [plan, setPlan] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [isGeneratingQuick, setIsGeneratingQuick] = useState(false);
  const [isGeneratingDetailed, setIsGeneratingDetailed] = useState(false);
  const [error, setError] = useState<string>('');
  const [isSpeaking, setIsSpeaking] = useState(false);

  const generate = useCallback(
    async (isDetailed: boolean): Promise<void> => {
      if (isDetailed) {
        setIsGeneratingDetailed(true);
      } else {
        setIsGeneratingQuick(true);
      }
      setIsLoading(true);
      setPlan('');
      setError('');
      try {
        const prompt = `Create a ${isDetailed ? 'highly detailed and comprehensive' : 'quick and simple'} fitness and nutrition plan for a ${level} individual whose goal is to ${goal}. The plan should be for ${days} days a week. Provide specific exercises, sets, reps, and meal suggestions. Format the response nicely using markdown.`;
        const result = await generatePlan(prompt, isDetailed);
        setPlan(result);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : 'Failed to generate plan');
      } finally {
        setIsLoading(false);
        setIsGeneratingQuick(false);
        setIsGeneratingDetailed(false);
      }
    },
    [goal, level, days]
  );

  const playAudio = useCallback(async (): Promise<void> => {
    if (!plan || isSpeaking) return;
    setIsSpeaking(true);
    const audioContent = await generateSpeech(plan);
    if (audioContent) {
      try {
        const outputAudioContext = new (window.AudioContext ||
          (window as unknown as { webkitAudioContext: typeof AudioContext })
            .webkitAudioContext)({ sampleRate: 24000 });
        const audioBuffer = await decodeAudioData(
          decode(audioContent),
          outputAudioContext,
          24000,
          1
        );
        const source = outputAudioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(outputAudioContext.destination);
        source.start();
        source.onended = (): void => setIsSpeaking(false);
      } catch {
        setError(
          "Sorry, I couldn't play the audio summary. Your browser might not be supported."
        );
        setIsSpeaking(false);
      }
    } else {
      setError("Sorry, I couldn't generate an audio summary for this plan.");
      setIsSpeaking(false);
    }
  }, [plan, isSpeaking]);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-white mb-4">Plan Generator</h1>
      <p className="text-gray-400 mb-6">
        Describe your fitness goals, and we&apos;ll generate a personalized
        workout and nutrition plan for you.
      </p>

      <Card className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label
              htmlFor="goal"
              className="block text-sm font-medium text-gray-300 mb-1"
            >
              My Primary Goal
            </label>
            <select
              id="goal"
              value={goal}
              onChange={(e) => setGoal(e.target.value)}
              className="w-full bg-gray-700 text-white p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="lose weight">Lose Weight</option>
              <option value="build muscle">Build Muscle</option>
              <option value="improve endurance">Improve Endurance</option>
              <option value="general fitness">General Fitness</option>
            </select>
          </div>
          <div>
            <label
              htmlFor="level"
              className="block text-sm font-medium text-gray-300 mb-1"
            >
              My Fitness Level
            </label>
            <select
              id="level"
              value={level}
              onChange={(e) => setLevel(e.target.value)}
              className="w-full bg-gray-700 text-white p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
          <div>
            <label
              htmlFor="days"
              className="block text-sm font-medium text-gray-300 mb-1"
            >
              Workout Days per Week
            </label>
            <select
              id="days"
              value={days}
              onChange={(e) => setDays(e.target.value)}
              className="w-full bg-gray-700 text-white p-2 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            >
              <option value="2">2 days</option>
              <option value="3">3 days</option>
              <option value="4">4 days</option>
              <option value="5">5 days</option>
            </select>
          </div>
        </div>
        <div className="flex flex-col sm:flex-row gap-4 mt-4">
          <Button
            onClick={() => generate(false)}
            disabled={isLoading}
            className="w-full"
          >
            {isGeneratingQuick ? (
              <>
                <LoadingSpinner /> Getting your plan...
              </>
            ) : (
              'Generate Quick Plan'
            )}
          </Button>
          <Button
            onClick={() => generate(true)}
            disabled={isLoading}
            variant="secondary"
            className="w-full"
          >
            {isGeneratingDetailed ? (
              <>
                <LoadingSpinner /> Building your blueprint...
              </>
            ) : (
              'Generate Detailed Plan'
            )}
          </Button>
        </div>
        {error && (
          <p className="text-red-400 mt-2 text-sm text-center">{error}</p>
        )}
      </Card>

      {plan && !isLoading && (
        <Card>
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-xl font-semibold text-white">
              Your Personal Plan
            </h2>
            <Button
              onClick={playAudio}
              disabled={isSpeaking}
              variant="secondary"
            >
              <SoundIcon className="h-5 w-5 mr-1" />
              {isSpeaking ? 'Speaking...' : 'Read Aloud'}
            </Button>
          </div>
          <div className="bg-gray-900 p-4 rounded-md">
            <MarkdownRenderer content={plan} />
          </div>
        </Card>
      )}
    </div>
  );
};

export default PlanGenerator;
