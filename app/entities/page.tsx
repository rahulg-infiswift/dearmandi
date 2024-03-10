"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

interface Entity {
  id: number;
  name: string;
  locale: string;
}

const EntitiesList = () => {
  const [entities, setEntities] = useState<Entity[]>([]);

  useEffect(() => {
    const fetchEntities = async () => {
      const response = await fetch("http://localhost:8000/api/entities");
      const data = await response.json();
      console.log(data);
      setEntities(data);
    };

    fetchEntities();
  }, []);

  const renderListData = (entity, idx) => {
    return (
      <div key={idx}>
        <Link href={`/entities/${entity.id}`}>{entity.name}</Link>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto my-10 p-5 rounded shadow-lg bg-white">
      <Link
        href="entities/create_entity/"
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        Create new entity
      </Link>
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Entities List</h2>
      <ul className="divide-y divide-gray-300">
        {entities.map(renderListData)}
      </ul>
    </div>
  );
};

export default EntitiesList;
