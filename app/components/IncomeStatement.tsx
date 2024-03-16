"use client";

import React, { useEffect, useState } from "react";

interface IncomeStatementData {
  // Define the structure of your income statement data here
  income_statement: string;
}

interface Entity {
  id: number;
  name: string;
}

const IncomeStatement = () => {
  const [entities, setEntities] = useState<Entity[]>([]);
  const [selectedEntityId, setSelectedEntityId] = useState<number | null>(null);
  const [incomeStatement, setIncomeStatement] =
    useState<IncomeStatementData | null>(null);

  useEffect(() => {
    const fetchEntities = async () => {
      try {
        const response = await fetch("/api/entities");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data: Entity[] = await response.json();
        setEntities(data);
      } catch (error) {
        console.error("There was a problem with fetching entities:", error);
      }
    };

    fetchEntities();
  }, []);

  useEffect(() => {
    const fetchIncomeStatement = async () => {
      if (!selectedEntityId) return;

      try {
        const response = await fetch(
          `/api/income-statement/${selectedEntityId}`
        );
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data: IncomeStatementData = await response.json();
        setIncomeStatement(data);
      } catch (error) {
        console.error(
          "There was a problem with fetching income statement:",
          error
        );
      }
    };

    fetchIncomeStatement();
  }, [selectedEntityId]);

  //   const handleEntityChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
  //     setSelectedEntity(event.target.value);
  //     setIncomeStatement(null); // Reset income statement when changing entity
  //   };

  return (
    <div>
      <form className="mb-4">
        <label className="block mb-2 text-sm font-medium text-gray-700">
          Select Entity:
        </label>
        <select
          className="block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          value={selectedEntityId || ""}
          onChange={(e) =>
            setSelectedEntityId(e.target.value ? Number(e.target.value) : null)
          }
        >
          <option value="">Select an entity</option>
          {entities.map((entity) => (
            <option key={entity.id} value={entity.id}>
              {entity.name}
            </option>
          ))}
        </select>
      </form>

      {incomeStatement && (
        <div>
          <h2 className="text-lg font-semibold">
            Income Statement for{" "}
            {entities.find((entity) => entity.id === selectedEntityId)?.name}
          </h2>
          <p>Income Statement: </p>
          <div>{incomeStatement.income_statement}</div>
        </div>
      )}
    </div>
  );
};

export default IncomeStatement;
