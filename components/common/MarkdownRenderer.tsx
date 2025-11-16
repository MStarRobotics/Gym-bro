import React from 'react';

interface MarkdownRendererProps {
  content: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({
  content,
}): React.ReactElement => {
  const elements: React.ReactNode[] = [];
  let listItems: React.ReactNode[] = [];

  const flushList = (): void => {
    if (listItems.length > 0) {
      elements.push(
        <ul
          key={`ul-${elements.length}`}
          className="list-disc pl-6 space-y-1 my-3"
        >
          {listItems.map((item, i) => (
            <li key={`li-${elements.length}-${i}`}>{item}</li>
          ))}
        </ul>
      );
      listItems = [];
    }
  };

  const parseLine = (line: string): React.ReactNode => {
    // This is not a full markdown parser, just a simple one for the app's needs.
    const boldRegex = /\*\*(.*?)\*\*/g;
    const parts = line.split(boldRegex);
    return (
      <>
        {parts.map((part, i) =>
          i % 2 === 1 ? (
            <strong key={`strong-${i}-${part}`}>{part}</strong>
          ) : (
            part
          )
        )}
      </>
    );
  };

  for (const line of content.split('\n')) {
    const isListItem =
      line.trim().startsWith('* ') || line.trim().startsWith('- ');

    if (isListItem) {
      // If a list item is found, push previous non-list content.
      if (elements.length > 0 && listItems.length === 0) flushList();
      listItems.push(parseLine(line.trim().substring(2)));
    } else {
      flushList();
      if (line.startsWith('### ')) {
        elements.push(
          <h3
            key={`h3-${line.substring(4)}`}
            className="text-lg font-semibold mt-4 mb-2 text-teal-300"
          >
            {parseLine(line.substring(4))}
          </h3>
        );
      } else if (line.startsWith('## ')) {
        elements.push(
          <h2
            key={`h2-${line.substring(3)}`}
            className="text-xl font-bold mt-5 mb-3 text-teal-400"
          >
            {parseLine(line.substring(3))}
          </h2>
        );
      } else if (line.startsWith('# ')) {
        elements.push(
          <h1
            key={`h1-${line.substring(2)}`}
            className="text-2xl font-bold mt-6 mb-4 text-teal-400"
          >
            {parseLine(line.substring(2))}
          </h1>
        );
      } else if (line.trim() !== '') {
        elements.push(
          <p
            key={`p-${line}-${elements.length}`}
            className="my-2 text-gray-300"
          >
            {parseLine(line)}
          </p>
        );
      }
    }
  }

  flushList(); // Flush any remaining list items at the end

  return <div>{elements}</div>;
};

export default MarkdownRenderer;
