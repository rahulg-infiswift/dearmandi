"use client";

import { useEffect, useState } from 'react';

const MyComponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('http://localhost:8000/api/income_statement/1');
      const jsonData = await response.json();
      console.log(jsonData)
      setData(jsonData);
    };

    fetchData();
  }, []);

  return (
    <div>
      {data ? (
        <div>{data}</div>
      ) : (
        <div>Loading...</div>
      )}
    </div>
  );
};

export default MyComponent;
