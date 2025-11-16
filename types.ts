export type View =
  | 'dashboard'
  | 'meal-analyzer'
  | 'plan-generator'
  | 'location-finder'
  | 'fact-checker';

export interface ChatMessage {
  sender: 'user' | 'bot';
  text: string;
  id?: string;
}

export interface GroundingChunk {
  web?: {
    uri: string;
    title: string;
  };
  maps?: {
    uri: string;
    title: string;
    placeAnswerSources?: {
      reviewSnippets: {
        text: string;
        author: string;
      }[];
    }[];
  };
}
