import {
  GoogleGenAI,
  GenerateContentResponse,
  Chat,
  Modality,
} from '@google/genai';
import type { GroundingChunk } from '../types';

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  throw new Error('API_KEY environment variable not set');
}

const ai = new GoogleGenAI({ apiKey: API_KEY });
let chat: Chat | null = null;

// Centralized, human-centric error handler implementing Pillar 1 of the Cortex Protocol
const handleApiError = (error: unknown, context: string): string => {
  // Rich, contextual logging for developers
  // Error logged internally for debugging

  if (error instanceof Error) {
    // Translate specific technical issues into reassuring, human-readable messages
    if (error.message.includes('API key not valid')) {
      return "There seems to be an issue with our system's configuration. Our team has been notified and is working on a fix.";
    }
    if (error.message.includes('content restrictions')) {
      return "I'm sorry, I can't provide a response for that request due to my safety guidelines. Could you please try a different topic?";
    }
    if (error.message.includes('timed out')) {
      // Provide an actionable next step
      return `The request is taking longer than expected. Please check your connection or try simplifying your request.`;
    }
  }
  // Generic, reassuring fallback with an escape hatch
  return `Oops! We had a little trouble ${context}. Please check your connection and try again in a moment. If the problem continues, please contact our support team.`;
};

export const analyzeMealImage = async (
  base64Image: string,
  mimeType: string,
  prompt: string
): Promise<string> => {
  try {
    const imagePart = { inlineData: { mimeType, data: base64Image } };
    const textPart = { text: prompt };
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: { parts: [imagePart, textPart] },
    });

    if (!response.text) {
      throw new Error(
        'The model returned an empty response. This might be due to my safety guidelines. Could you try a different image or prompt?'
      );
    }
    return response.text;
  } catch (error) {
    throw new Error(handleApiError(error, 'analyzing your meal'));
  }
};

export const suggestMealPrompt = async (
  base64Image: string,
  mimeType: string
): Promise<string> => {
  try {
    const imagePart = { inlineData: { mimeType, data: base64Image } };
    const metaPrompt =
      "Analyze this image of a meal. Based on what you see, suggest one creative and specific question a user could ask about it. For example, instead of 'Is this healthy?', suggest something like 'What specific vitamins am I getting from the greens in this dish?' or 'Could this meal be adapted for a vegan diet?'. Return only the suggested question as a single line of plain text, without any preamble or quotation marks.";
    const textPart = { text: metaPrompt };

    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash-lite',
      contents: { parts: [imagePart, textPart] },
    });

    if (!response.text) {
      throw new Error(
        'The model could not generate a suggestion for this image.'
      );
    }
    return response.text.trim();
  } catch (error) {
    throw new Error(handleApiError(error, 'suggesting a prompt'));
  }
};

export const generatePlan = async (
  prompt: string,
  isDetailed: boolean
): Promise<string> => {
  try {
    const modelName = isDetailed ? 'gemini-2.5-pro' : 'gemini-2.5-flash-lite';
    const config = isDetailed
      ? { thinkingConfig: { thinkingBudget: 32768 } }
      : {};

    const response = await ai.models.generateContent({
      model: modelName,
      contents: prompt,
      config: config,
    });
    return response.text || '';
  } catch (error) {
    throw new Error(handleApiError(error, 'generating your plan'));
  }
};

// AI Personality Guide implementing Pillars 2 & 3 of the Cortex Protocol
const geniusConciergeInstruction = `You are "Genius Concierge," a world-class AI fitness and wellness assistant for the FitAI app. Your personality is Encouraging, Professional, and Clear.

**Your Core Mandate (The Cortex Protocol):**
1.  **Be Empathetic & Encouraging:** Acknowledge the user's goals and feelings. Use a warm, supportive, and motivating tone. Your goal is to be a trusted coach.
2.  **Be Professional & Clear:** Provide concise, easy-to-understand information. Avoid jargon.
3.  **Be Proactive & Resilient (Conversational Fallbacks):**
    *   **Ambiguity Resolution:** If a user's query is vague (e.g., "show me my plan"), YOU MUST ask for clarification ("Of course! Are you looking for your Workout Plan or your Nutrition Plan?").
    *   **Typo Correction:** If you suspect a misspelling, suggest the correction politely (e.g., User: "I want to book a phisiotherapist." You: "I can help with that! Did you mean to 'book a physiotherapist'?").
    *   **Graceful No:** If you cannot fulfill a request, explain why in simple terms and suggest a viable alternative. Never just say "I can't do that."
4.  **Vary Your Responses:** Do not use the same greeting or acknowledgment every time. Use a natural mix of phrases like "Got it," "On it," "Let's take a look," "Perfect," "You got it," "I can certainly help with that."

**Safety First (Non-Negotiable):**
ALWAYS include a gentle reminder for users to consult with a healthcare professional or certified trainer for personalized medical advice, especially before starting a new, strenuous fitness program. YOU MUST NOT provide medical diagnoses or advice that could be interpreted as such.

**Example Interaction:**
User: "I wnat to lose some wight"
You: "That's a great goal, and I'm here to help you on that journey! Did you mean you want to 'lose some weight'?"

Begin the conversation now.`;

export const getChatbotResponse = async (message: string): Promise<string> => {
  try {
    if (!chat) {
      chat = ai.chats.create({
        model: 'gemini-2.5-flash',
        config: { systemInstruction: geniusConciergeInstruction },
      });
    }
    const response: GenerateContentResponse = await chat.sendMessage({
      message,
    });
    return response.text || '';
  } catch (error) {
    return handleApiError(error, 'getting a response');
  }
};

export const findNearbyPlaces = async (
  prompt: string,
  location: { latitude: number; longitude: number }
): Promise<{ text: string; sources: GroundingChunk[] }> => {
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: {
        tools: [{ googleMaps: {} }],
        toolConfig: { retrievalConfig: { latLng: location } },
      },
    });
    const sources =
      response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
    const responseText = response.text || '';
    // Graceful Degradation: Even if we have text, if sources are empty and it's an apology, treat as an error for the UI.
    if (sources.length === 0 && responseText.toLowerCase().includes('sorry')) {
      return { text: responseText, sources: [] };
    }
    return { text: responseText, sources: sources as GroundingChunk[] };
  } catch (error) {
    const userMessage = handleApiError(error, 'finding nearby places');
    return { text: userMessage, sources: [] };
  }
};

export const getUpToDateAnswer = async (
  prompt: string
): Promise<{ text: string; sources: GroundingChunk[] }> => {
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash',
      contents: prompt,
      config: { tools: [{ googleSearch: {} }] },
    });
    const sources =
      response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
    const responseText = response.text || '';
    // Graceful Degradation check
    if (sources.length === 0 && responseText.toLowerCase().includes('sorry')) {
      return { text: responseText, sources: [] };
    }
    return { text: responseText, sources: sources as GroundingChunk[] };
  } catch (error) {
    const userMessage = handleApiError(error, 'finding an answer');
    return { text: userMessage, sources: [] };
  }
};

export const generateSpeech = async (text: string): Promise<string | null> => {
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-2.5-flash-preview-tts',
      contents: [
        { parts: [{ text: `Say with a clear and encouraging tone: ${text}` }] },
      ],
      config: {
        responseModalities: [Modality.AUDIO],
        speechConfig: {
          voiceConfig: { prebuiltVoiceConfig: { voiceName: 'Kore' } },
        },
      },
    });
    return (
      response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data || null
    );
  } catch {
    // Graceful failure for speech generation
    return null;
  }
};
