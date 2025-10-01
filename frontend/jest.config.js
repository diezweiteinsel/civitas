module.exports = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.js"],
  moduleNameMapping: {
    "\\.(css|less|scss)$": "identity-obj-proxy",
  },
  transformIgnorePatterns: [
    "node_modules/(?!(react-router|react-router-dom)/)",
  ],
  testEnvironmentOptions: {
    url: "http://localhost",
  },
  // Add these lines
  coverageReporters: ["text", "cobertura"], // Add 'cobertura' for GitLab
  reporters: [
    "default",
    [
      "jest-junit",
      {
        outputDirectory: "reports",
        outputName: "junit.xml",
      },
    ],
  ],
};
