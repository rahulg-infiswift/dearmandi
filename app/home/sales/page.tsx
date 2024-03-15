"use client";

import Link from "next/link";
import Layout from "../../layout";
import Navbar from "@/app/components/Navbar";
import { useState, useEffect } from "react";

interface Entity {
  id: number;
  name: string;
  locale: string;
}

const Sales = () => {
  const [formData, setFormData] = useState({
    entityName: "",
    cropName: "",
    quantity: "",
    amount: "",
  });
  const [entityNames, setEntityNames] = useState<Entity[]>([]);

  useEffect(() => {
    // Fetch entity names from the backend
    const fetchEntityNames = async () => {
      const response = await fetch("/api/entities");
      const data = await response.json();
      console.log(data);
      setEntityNames(data);
    };
    fetchEntityNames();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log(formData);
    // Create transaction and Line Item for the form data
    await fetch("/api/create-transaction-and-lineitem-cp", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        entity_name: formData.entityName,
        crop_name: formData.cropName,
        quantity: formData.quantity,
        amount: formData.amount,
      }),
    });

    // Reset form after submission
    // setFormData({
    //   entityName: "",
    //   cropName: "",
    //   quantity: "",
    //   amount: "",
    // });
  };

  return (
    <>
      {/* Wrap the navbar and content in a flex container */}
      <div className="flex flex-col md:flex-row min-h-screen">
        {/* Navbar with adjusted styles for mobile */}
        <div className="md:flex-1 md:max-w-xs">
          <Navbar />
        </div>
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
                  htmlFor="entityName"
                  className="block font-bold text-xl mb-2"
                >
                  Kisan Name
                </label>
                <select
                  name="entityName"
                  value={formData.entityName}
                  onChange={handleChange}
                  className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  // className="mt-1 w-full px-4 py-2 border rounded-md"
                  required
                >
                  <option value="">Select an entity</option>
                  {entityNames
                    .filter((entity) => entity) // Filter out empty or undefined values
                    .map((entity) => (
                      <option key={entity.id} value={entity.name}>
                        {entity.name}
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
                className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
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

export default Sales;
