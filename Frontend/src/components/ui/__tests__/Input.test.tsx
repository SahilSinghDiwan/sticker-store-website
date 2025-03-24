import { render, screen, fireEvent } from "@testing-library/react";
import { Input } from "../Input";

describe("Input Component", () => {
  it("renders input element correctly", () => {
    render(<Input placeholder="Enter text" />);
    expect(screen.getByPlaceholderText("Enter text")).toBeInTheDocument();
  });

  it("renders label when provided", () => {
    render(<Input label="Username" id="username" />);
    expect(screen.getByText("Username")).toBeInTheDocument();
    expect(screen.getByLabelText("Username")).toBeInTheDocument();
  });

  it("handles value changes", () => {
    const handleChange = jest.fn();
    render(<Input onChange={handleChange} />);

    const input = screen.getByRole("textbox");
    fireEvent.change(input, { target: { value: "test" } });

    expect(handleChange).toHaveBeenCalled();
    expect(input).toHaveValue("test");
  });

  it("displays error state correctly", () => {
    render(
      <Input error={true} helperText="This field is required" label="Email" />
    );

    const input = screen.getByRole("textbox");
    const errorMessage = screen.getByText("This field is required");

    expect(input).toHaveClass("border-error-main");
    expect(errorMessage).toHaveClass("text-error-main");
  });

  it("applies fullWidth class when fullWidth prop is true", () => {
    render(<Input fullWidth />);
    const container = screen.getByRole("textbox").parentElement;
    expect(container).toHaveClass("w-full");
  });

  it("handles disabled state", () => {
    render(<Input disabled />);
    expect(screen.getByRole("textbox")).toBeDisabled();
  });

  it("forwards ref correctly", () => {
    const ref = jest.fn();
    render(<Input ref={ref} />);
    expect(ref).toHaveBeenCalled();
  });

  it("passes through additional HTML attributes", () => {
    render(<Input data-testid="custom-input" maxLength={10} required />);

    const input = screen.getByTestId("custom-input");
    expect(input).toHaveAttribute("maxLength", "10");
    expect(input).toBeRequired();
  });
});
