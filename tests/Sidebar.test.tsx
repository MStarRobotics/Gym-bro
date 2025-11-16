import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { axe } from 'vitest-axe';
// combined import
import Sidebar from '../components/Sidebar';
import type { View } from '../types';

// using axe directly and asserting no violations

describe('Sidebar', () => {
  it('renders and is accessible', async () => {
    const setCurrentView = (_v: View): void => {
      return;
    };
    const setIsSidebarOpen = (_b: boolean): void => {
      return;
    };
    const toggleChat = (): void => {
      return;
    };
    const props = {
      currentView: 'dashboard' as View,
      setCurrentView,
      isSidebarOpen: true,
      setIsSidebarOpen,
      toggleChat,
    };
    const { container } = render(<Sidebar {...props} />);
    expect(screen.getByText('FitAI')).toBeInTheDocument();
    // Run a11y checks
    const results = await axe(container as unknown as HTMLElement);
    expect(results.violations.length).toBe(0);
  });
});
