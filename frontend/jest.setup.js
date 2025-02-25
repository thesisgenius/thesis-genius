import "@testing-library/jest-dom";

import { TextEncoder, TextDecoder } from "util";
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

global.import = {
  meta: {
    env: {
      VITE_API_BASE_URL: "http://127.0.0.1:8557/api",
    },
  },
};
