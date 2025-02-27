import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Header from "../components/Header";
import { vi, describe, it, expect } from "vitest";

// Mock AuthContext
vi.mock("../context/AuthContext", () => ({
  useAuth: () => ({
    user: { first_name: "Test User" },
    signOut: vi.fn(),
  }),
}));

describe("Header", () => {
  it("renders Header with correct title", () => {
    render(
      <MemoryRouter>
        <Header />
      </MemoryRouter>,
    );

    const headerElement = screen.getByText(/ThesisGenius/i);
    expect(headerElement).toBeInTheDocument();
  });
});
