// EntityForm.tsx
import React, { useState } from "react";

function CreateEntity() {
  const [entityName, setEntityName] = useState("");
  
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      // fetch request to create a new entity here
      const response = await fetch("/api/create-entity", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: entityName }),
      });
      if (response.ok) {
        const responseData = await response.json();
        console.log("Entity Created:", responseData);
        // Fetch the entity ID from the response
        const entityId = responseData.id;

        // Call the create-accounts endpoint with the entity ID
        await fetch("/api/create-accounts", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ entity_id: entityId }),
        });

        // Create tax accounts for the Kisan entity
        await fetch("/api/create-tax-accounts", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ entity_id: entityId }),
        });
      } else {
        // Handle server errors for create-entity
        const errorData = await response.json();
        console.error("Error creating entity:", errorData);
      }
    } catch (error) {
      console.error("Network error:", error);
    }
    setEntityName(""); // Reset the form
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-sm mx-auto mt-10">
      <label
        htmlFor="entityName"
        className="block mb-2 text-sm font-medium text-gray-900"
      >
        Kisan Name:
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
      </label>
      <button
        type="submit"
        className="text-white bg-blue-500 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center"
      >
        Create Entity
      </button>
    </form>
  );
}

export default CreateEntity;
