import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "../button";

describe("Button Component", () => {
  it("renders children correctly", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText("Click me")).toBeInTheDocument();
  });

  it("applies different variants correctly", () => {
    const { rerender } = render(<Button variant="primary">Button</Button>);
    expect(screen.getByText("Button")).toHaveClass("bg-[var(--color-accent)]");

    rerender(<Button variant="secondary">Button</Button>);
    expect(screen.getByText("Button")).toHaveClass("bg-[var(--color-ink)]");

    rerender(<Button variant="outline">Button</Button>);
    expect(screen.getByText("Button")).toHaveClass("border-[var(--color-rule)]");
  });

  it("applies different sizes correctly", () => {
    const { rerender } = render(<Button size="sm">Button</Button>);
    expect(screen.getByText("Button")).toHaveClass("px-3 py-1.5 text-sm");

    rerender(<Button size="lg">Button</Button>);
    expect(screen.getByText("Button")).toHaveClass("px-5 py-2.5 text-base");
  });

  it("handles click events", () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByText("Click me"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it("displays loading state correctly", () => {
    render(<Button loading>Submit</Button>);

    expect(screen.getByText("Working…")).toBeInTheDocument();
    expect(screen.queryByText("Submit")).not.toBeInTheDocument();
    expect(screen.getByRole("button")).toBeDisabled();
  });

  it("applies fullWidth class when fullWidth prop is true", () => {
    render(<Button fullWidth>Full Width Button</Button>);
    expect(screen.getByText("Full Width Button")).toHaveClass("w-full");
  });

  it("is disabled when disabled prop is true", () => {
    render(<Button disabled>Disabled Button</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});
