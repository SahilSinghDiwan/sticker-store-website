import { TextEncoder, TextDecoder } from "node:util";

// jsdom does not provide these; msw needs them before it loads.
Object.assign(globalThis, { TextEncoder, TextDecoder });

import "@testing-library/jest-dom";

if (typeof window !== "undefined") {
  // Mock IntersectionObserver
  class IntersectionObserver {
    observe = jest.fn();
    disconnect = jest.fn();
    unobserve = jest.fn();
  }

  Object.defineProperty(window, "IntersectionObserver", {
    writable: true,
    configurable: true,
    value: IntersectionObserver,
  });

  // Mock matchMedia
  Object.defineProperty(window, "matchMedia", {
    writable: true,
    value: jest.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    })),
  });
}
