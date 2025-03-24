import React, { useState, useEffect } from "react";
import adminApi from "../../services/adminApi";

interface SalesData {
  daily: {
    date: string;
    total: number;
    orders: number;
  }[];
  monthly: {
    month: string;
    total: number;
    orders: number;
  }[];
  topProducts: {
    _id: string;
    name: string;
    total_sales: number;
    quantity_sold: number;
  }[];
}

export default function SalesAnalytics() {
  const [salesData, setSalesData] = useState<SalesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeframe, setTimeframe] = useState<"daily" | "monthly">("daily");

  useEffect(() => {
    fetchSalesData();
  }, []);

  const fetchSalesData = async () => {
    try {
      const response = await adminApi.getSalesAnalytics();
      setSalesData(response);
    } catch (err) {
      setError("Failed to load sales data");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!salesData) return null;

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Sales Analytics</h2>
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value as "daily" | "monthly")}
          className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        >
          <option value="daily">Daily</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded-md mb-4">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="bg-indigo-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-indigo-900 mb-2">
            Total Sales
          </h3>
          <p className="text-3xl font-bold text-indigo-600">
            $
            {salesData[timeframe]
              .reduce((acc, curr) => acc + curr.total, 0)
              .toFixed(2)}
          </p>
        </div>
        <div className="bg-green-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-green-900 mb-2">
            Total Orders
          </h3>
          <p className="text-3xl font-bold text-green-600">
            {salesData[timeframe].reduce((acc, curr) => acc + curr.orders, 0)}
          </p>
        </div>
        <div className="bg-purple-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-purple-900 mb-2">
            Average Order Value
          </h3>
          <p className="text-3xl font-bold text-purple-600">
            $
            {(
              salesData[timeframe].reduce((acc, curr) => acc + curr.total, 0) /
              salesData[timeframe].reduce((acc, curr) => acc + curr.orders, 0)
            ).toFixed(2)}
          </p>
        </div>
      </div>

      <div className="mb-8">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">
          Top Selling Products
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {salesData.topProducts.map((product) => (
            <div key={product._id} className="bg-white border rounded-lg p-4">
              <h4 className="font-medium text-gray-900">{product.name}</h4>
              <p className="text-sm text-gray-500">
                Sold: {product.quantity_sold} units
              </p>
              <p className="text-sm font-medium text-indigo-600">
                Revenue: ${product.total_sales.toFixed(2)}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-xl font-semibold text-gray-800 mb-4">
          {timeframe === "daily" ? "Daily" : "Monthly"} Sales Trend
        </h3>
        <div className="h-64 bg-gray-50 rounded-lg p-4">
          {/* Add chart component here */}
        </div>
      </div>
    </div>
  );
}
