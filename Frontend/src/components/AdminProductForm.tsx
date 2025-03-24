import { useState } from "react";
import adminApi from "../services/adminApi";

interface FormError {
  message: string;
  field?: string;
}

export default function AdminProductForm() {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<FormError | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError(null);
    setSuccess(false);
    setLoading(true);

    try {
      // Validate file
      if (!file) {
        setError({ message: "Please select an image file", field: "image" });
        return;
      }

      const form = e.currentTarget as HTMLFormElement;
      const formData = new FormData();

      // Get form values
      const nameInput = form.elements.namedItem("name") as HTMLInputElement;
      const priceInput = form.elements.namedItem("price") as HTMLInputElement;
      const descriptionInput = form.elements.namedItem(
        "description"
      ) as HTMLTextAreaElement;

      const name = nameInput.value.trim();
      const price = parseFloat(priceInput.value);
      const description = descriptionInput.value.trim();

      // Validate inputs
      if (!name) {
        setError({ message: "Product name is required", field: "name" });
        return;
      }
      if (isNaN(price) || price <= 0) {
        setError({ message: "Please enter a valid price", field: "price" });
        return;
      }
      if (!description) {
        setError({
          message: "Product description is required",
          field: "description",
        });
        return;
      }

      // Append data to FormData
      formData.append("image", file);
      formData.append("name", name);
      formData.append("price", price.toString());
      formData.append("description", description);

      const response = await adminApi.addProduct(formData);
      console.log("Product added:", response);
      setSuccess(true);

      // Reset form
      form.reset();
      setFile(null);
    } catch (error) {
      console.error("Error adding product:", error);
      setError({
        message:
          error instanceof Error
            ? error.message
            : "Failed to add product. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6">Add New Product</h2>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error.message}
        </div>
      )}

      {success && (
        <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-md">
          Product added successfully!
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="name"
            className="block text-sm font-medium text-gray-700"
          >
            Product Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            className={`mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${
              error?.field === "name" ? "border-red-500" : ""
            }`}
            placeholder="Product Name"
            required
          />
        </div>

        <div>
          <label
            htmlFor="price"
            className="block text-sm font-medium text-gray-700"
          >
            Price
          </label>
          <input
            type="number"
            id="price"
            name="price"
            step="0.01"
            min="0"
            className={`mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${
              error?.field === "price" ? "border-red-500" : ""
            }`}
            placeholder="0.00"
            required
          />
        </div>

        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700"
          >
            Description
          </label>
          <textarea
            id="description"
            name="description"
            rows={3}
            className={`mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 ${
              error?.field === "description" ? "border-red-500" : ""
            }`}
            placeholder="Product description"
            required
          />
        </div>

        <div>
          <label
            htmlFor="image"
            className="block text-sm font-medium text-gray-700"
          >
            Product Image
          </label>
          <input
            type="file"
            id="image"
            accept="image/*"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className={`mt-1 block w-full ${
              error?.field === "image" ? "border-red-500" : ""
            }`}
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 ${
            loading ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          {loading ? "Adding Product..." : "Add Product"}
        </button>
      </form>
    </div>
  );
}
