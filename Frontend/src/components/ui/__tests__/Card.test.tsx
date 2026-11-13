import { render, screen, fireEvent } from "@testing-library/react";
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "../Card";

describe("Card Components", () => {
  describe("Card", () => {
    it("renders children correctly", () => {
      render(<Card>Card Content</Card>);
      expect(screen.getByText("Card Content")).toBeInTheDocument();
    });

    it("applies different padding sizes correctly", () => {
      const { rerender } = render(<Card padding="small">Content</Card>);
      expect(screen.getByText("Content")).toHaveClass("p-3");

      rerender(<Card padding="large">Content</Card>);
      expect(screen.getByText("Content")).toHaveClass("p-6");
    });

    it("applies hoverable styles when hoverable prop is true", () => {
      render(<Card hoverable>Content</Card>);
      expect(screen.getByText("Content")).toHaveClass(
        "transition-shadow",
        "hover:shadow-md",
        "cursor-pointer"
      );
    });

    it("handles click events", () => {
      const handleClick = jest.fn();
      render(<Card onClick={handleClick}>Clickable Card</Card>);

      fireEvent.click(screen.getByText("Clickable Card"));
      expect(handleClick).toHaveBeenCalledTimes(1);
    });
  });

  describe("CardHeader", () => {
    it("renders with correct styles", () => {
      render(<CardHeader>Header Content</CardHeader>);
      expect(screen.getByText("Header Content")).toHaveClass(
        "border-b",
        "border-gray-200",
        "pb-4",
        "mb-4"
      );
    });
  });

  describe("CardTitle", () => {
    it("renders with correct styles", () => {
      render(<CardTitle>Card Title</CardTitle>);
      expect(screen.getByText("Card Title")).toHaveClass(
        "text-lg",
        "font-semibold",
        "text-gray-900"
      );
    });
  });

  describe("CardContent", () => {
    it("renders children correctly", () => {
      render(<CardContent>Content Area</CardContent>);
      expect(screen.getByText("Content Area")).toBeInTheDocument();
    });
  });

  describe("CardFooter", () => {
    it("renders with correct styles", () => {
      render(<CardFooter>Footer Content</CardFooter>);
      expect(screen.getByText("Footer Content")).toHaveClass(
        "border-t",
        "border-gray-200",
        "pt-4",
        "mt-4"
      );
    });
  });
});
