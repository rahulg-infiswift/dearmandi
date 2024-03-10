"use client";

import { useState, FormEvent } from "react";

export default function CreateEntity() {
  const [entityName, setEntityName] = useState<string>("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/api/create_entity", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: entityName }),
      });
      const data = await response.json();
      console.log(data);
      setEntityName("");
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-sm mx-auto mt-10">
      <div className="mb-6">
        <label
          htmlFor="entityName"
          className="block mb-2 text-sm font-medium text-gray-900"
        >
          Kisan Name
        </label>
        <input
          type="text"
          id="entityName"
          name="entityName"
          value={entityName}
          onChange={(e) => setEntityName(e.target.value)}
          className="block w-full p-2.5 text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Enter Kisan Name"
          required
        />
      </div>
      <button
        type="submit"
        className="text-white bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
      >
        Submit
      </button>
    </form>
  );
}
