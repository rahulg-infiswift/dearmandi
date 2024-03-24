// EntityForm.tsx
import React, { useState } from "react";

function CreateCustomer() {
  const [customerName, setCustomerName] = useState("");
  const [customerEmail, setCustomerEmail] = useState("");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token"); // Retrieve the token from local storage
      if (!token) {
        console.error("No token found");
        return;
      }
      // fetch request to create a new customer here
      const response = await fetch("/api/customers/create_customer", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: customerName,
          email: customerEmail,
        }),
      });
      if (response.ok) {
        const responseData = await response.json();
        console.log("Customer Created:", responseData);
        // Fetch the customer ID from the response
        const customerId = responseData.id;
      } else {
        // Handle server errors for create_customer
        const errorData = await response.json();
        console.error("Error creating customer:", errorData);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
    setCustomerName(""); // Reset the form
    setCustomerEmail(""); // Reset the form
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-sm mx-auto mt-10">
      <label
        htmlFor="customerName"
        className="block mb-2 text-sm font-medium text-gray-900"
      >
        Customer Name:
        <input
          type="text"
          id="customerName"
          name="customerName"
          value={customerName}
          onChange={(e) => setCustomerName(e.target.value)}
          className="block w-full p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter Customer Name"
          required
        />
      </label>
      <label
        htmlFor="customerEmail"
        className="block mb-2 text-sm font-medium text-gray-900"
      >
        Email address:
        <input
          type="text"
          id="customerEmail"
          name="customerEmail"
          value={customerEmail}
          onChange={(e) => setCustomerEmail(e.target.value)}
          className="block w-full p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter email address"
          required
        />
      </label>
      <button
        type="submit"
        className="text-white bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
      >
        Create New Customer
      </button>
    </form>
  );
}

export default CreateCustomer;
