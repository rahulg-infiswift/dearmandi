"use client";
import React, { useState, useEffect } from "react";
import fetchSelfAccounts from "./fetchSelfAccounts";

// React component to display the accounts list
const GetSelfAccounts: React.FC = () => {
  const [accounts, setAccounts] = useState<Array<{ id: string; name: string }>>(
    []
  );
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Placeholder for the bearer token. Ensure you replace this with secure token handling logic.
  useEffect(() => {
    const token = localStorage.getItem("token"); // Retrieve the token from local storage
    if (!token) {
      setError("No token found");
      setIsLoading(false);
      return;
    }

    const loadData = async () => {
      try {
        const data = await fetchSelfAccounts(token);
        console.log(data);
        setAccounts(data);
        setIsLoading(false);
      } catch (err) {
        setError("Failed to fetch data.");
        setIsLoading(false);
        console.error(err);
      }
    };

    loadData();
  }, []); // Empty dependency array to run only once on component mount

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  console.log(accounts);
  return (
    <div>
      <h2>Accounts List</h2>
      <ul>
        {accounts.map((account) => (
          <li key={account.id}>{account.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default GetSelfAccounts;
