module.exports = {
  preset: "ts-jest",
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.ts"],
  moduleNameMapper: {
    "\\.(css|less|scss|sass)$": "identity-obj-proxy",
    "^@/(.*)$": "<rootDir>/src/$1",
    "^axios$": "<rootDir>/node_modules/axios/dist/node/axios.cjs",
  },
  testMatch: ["**/__tests__/**/*.test.(ts|tsx)"],
  transform: {
    "^.+\\.(ts|tsx)$": "ts-jest",
  },
  globals: {
    "ts-jest": {
      tsconfig: "tsconfig.app.json",
      diagnostics: { ignoreCodes: [1259] },
    },
  },
};
