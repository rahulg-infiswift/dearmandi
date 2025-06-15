"use client";
import { useState, useEffect } from "react";
import fetchSelfCustomers from "./fetchSelfCustomers";

const CashSale = () => {
  const [formData, setFormData] = useState({
    customerName: "",
    cropName: "",
    quantity: "",
    amount: "",
  });
  const [customers, setCustomers] = useState<
    Array<{ id: string; name: string }>
  >([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token"); // Retrieve the token from local storage
    console.log(token);
    if (!token) {
      console.log("No token found");
      return;
    }

    const loadData = async () => {
      try {
        const data = await fetchSelfCustomers(token);
        console.log(data);
        setCustomers(data);
        setIsLoading(false);
      } catch (err) {
        setError("Failed to fetch data.");
        setIsLoading(false);
        console.error(err);
      }
    };

    loadData();
  }, []);
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formData);
    // Create transaction and Line Item for the form data
    await fetch("/api/create_cash_sale", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customer_name: formData.customerName,
        crop_name: formData.cropName,
        quantity: formData.quantity,
        amount: formData.amount,
      }),
    });

    // Reset form after submission
    setFormData({
      customerName: "",
      cropName: "",
      quantity: "",
      amount: "",
    });
  };

  return (
    <>
      <div className="flex flex-col md:flex-row min-h-screen">
        {/* Content area */}
        <div className="flex-1 p-4">
          {/* Center the form container on medium and larger screens */}
          <div className="max-w-4xl mx-auto">
            <h1 className="text-center text-2xl font-semibold mb-6">
              Sales Tracking
            </h1>
            <p className="text-center mb-8">
              Monitor sales trends, analyze performance, and identify
              opportunities for growth. Track sales by product, region, or
              salesperson.
            </p>
            <form
              onSubmit={handleSubmit}
              className="flex flex-col space-y-4 items-center"
            >
              <div className="w-full max-w-md">
                <label
                  htmlFor="customerName"
                  className="block font-bold text-xl mb-2"
                >
                  Customer Name
                </label>
                <select
                  name="customerName"
                  value={formData.customerName}
                  onChange={handleChange}
                  className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  // className="mt-1 w-full px-4 py-2 border rounded-md"
                  required
                >
                  <option value="">Select customer name</option>
                  {customers
                    .filter((customer) => customer) // Filter out empty or undefined values
                    .map((customer) => (
                      <option key={customer.id} value={customer.name}>
                        {customer.name}
                      </option>
                    ))}
                </select>
              </div>

              <div className="w-full max-w-md">
                <label
                  htmlFor="cropName"
                  className="block font-bold text-xl mb-2"
                >
                  Crop Name
                </label>
                <input
                  type="text"
                  id="cropName"
                  name="cropName"
                  value={formData.cropName}
                  onChange={handleChange}
                  className="mt-1 w-full px-4 py-2 border rounded-md"
                  required
                />
              </div>

              <div className="w-full max-w-md">
                <label
                  htmlFor="quantity"
                  className="block font-bold text-xl mb-2"
                >
                  Quantity (No of Bags)
                </label>
                <input
                  type="number"
                  id="quantity"
                  name="quantity"
                  value={formData.quantity}
                  onChange={handleChange}
                  className="mt-1 w-full px-4 py-2 border rounded-md"
                  required
                />
              </div>

              <div className="w-full max-w-md">
                <label
                  htmlFor="amount"
                  className="block font-bold text-xl mb-2"
                >
                  Amount
                </label>
                <input
                  type="number"
                  id="amount"
                  name="amount"
                  value={formData.amount}
                  onChange={handleChange}
                  className="mt-1 w-full px-4 py-2 border rounded-md"
                  required
                />
              </div>

              <button
                type="submit"
                className="mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              >
                Submit
              </button>
            </form>
          </div>
        </div>
      </div>
    </>
  );
};

export default CashSale;
